#!/usr/bin/env python3
"""Uçtan uca v2 Reel üretimi: senaryo -> seslendirme -> görüntü -> ses miksajı.

Tek komutla content/storyboards.json'daki bir Reel'i yayına hazır MP4 yapar:

    python scripts/build_reel.py 13-kopek-kuyruk-yonu

Adımlar:
  1. Her beat için Türkçe neural seslendirme üretilir (scripts/voice.py).
  2. Gerçek ses süreleri okunur; altyazı kartlarının zaman çizelgesi bundan
     türetilir — yani altyazı ile ses arasında kayma imkânsız.
  3. Görüntü render edilir (scripts/reel_kit_v2.py).
  4. Müzik, seslendirmenin altına sidechain ducking ile karıştırılır.
  5. Dosya 20MB'ı (jsDelivr limiti) aşarsa otomatik yeniden kodlanır.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import imageio.v2 as imageio

sys.path.insert(0, str(Path(__file__).resolve().parent))

from footage import fetch_clip  # noqa: E402
from reel_kit_v2 import (  # noqa: E402
    FPS, H, W, Card, Shot, beat_chunks, build_cards, load_shot_base, render_timeline,
)
from voice import (  # noqa: E402
    DEFAULT_PITCH, DEFAULT_RATE, DEFAULT_VOICE, VoiceClip, audio_duration,
    concat_with_gaps, measure_chunks, shape_voice, synth_beats,
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
STORYBOARDS = PROJECT_ROOT / "content" / "storyboards.json"
MUSIC_LIBRARY = PROJECT_ROOT / "content" / "music_library.json"

LEAD_IN = 0.10          # kanca metni videonun ilk karesinde olsun
# Klipler artık konuşmaya kırpıldığı için beat'ler arasındaki nefesi bu değer
# belirliyor; önceden TTS'in kendi ~0,9 sn kuyruk sessizliği buna ekleniyordu
# ve ritim sürükleniyordu.
DEFAULT_GAP = 0.22
TAIL = 0.85             # son beat sonrası tutuş (loop kuyruğu buraya sığar)
JSDELIVR_LIMIT = 20 * 1024 * 1024


def load_storyboard(slug: str) -> dict:
    boards = json.loads(STORYBOARDS.read_text(encoding="utf-8"))
    for board in boards:
        if board["slug"] == slug:
            return board
    raise SystemExit(f"storyboards.json içinde '{slug}' yok. Mevcut: {[b['slug'] for b in boards]}")


def music_path(music_id: str) -> Path | None:
    if not music_id:
        return None
    library = json.loads(MUSIC_LIBRARY.read_text(encoding="utf-8"))
    for track in library["tracks"]:
        if track["id"] == music_id:
            return PROJECT_ROOT / track["file"]
    return None


VIDEO_EXT = {".mp4", ".mov", ".m4v", ".webm", ".mkv"}

# Kanal görünümünü çekimden çekime tutarlı kılan hafif renk düzeltmesi. Stok
# klipler farklı kameralardan geliyor; bu olmadan aynı Reel içinde belirgin
# ton farkı görünüyor.
CLIP_LOOK = "eq=contrast=1.05:saturation=1.07:gamma=0.99"


def prepare_clip(src: Path, dst: Path, duration: float, start_at: float = 0.0) -> None:
    """Klibi 1080x1920 / 30 fps'e ve tam çekim süresine hazırlar.

    Klip çekimden kısaysa `-stream_loop` ile döngüye alınır; uzunsa kesilir.
    Ken Burns uygulanmaz — hareket klibin kendisinden geliyor.
    """
    chain = (
        f"scale={W}:{H}:force_original_aspect_ratio=increase,"
        f"crop={W}:{H},fps={FPS},setsar=1,{CLIP_LOOK}"
    )
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error",
         "-stream_loop", "-1", "-ss", f"{max(start_at, 0):.2f}", "-i", str(src),
         "-t", f"{duration + 0.2:.3f}", "-vf", chain, "-an",
         "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p",
         str(dst)],
        check=True,
    )


def resolve_media(entry: dict, index: int, duration: float, used: set[str]) -> Path | None:
    """Çekimin kaynağını çözer: önce sabit dosya, yoksa stok arama."""
    if entry.get("media"):
        return PROJECT_ROOT / entry["media"]
    query = entry.get("query")
    if not query:
        raise SystemExit(f"Çekim {index}: 'media' de 'query' de yok.")
    print(f"      çekim {index}: '{query}' aranıyor")
    clip = fetch_clip(
        query, min_duration=max(duration, 3.0), exclude=used,
        must_include=entry.get("must_include"),
    )
    if clip is None:
        return None
    used.add(clip.path)
    return PROJECT_ROOT / clip.path


def build_shots(
    board: dict, beats: list[dict], starts: list[float], ends: list[float],
    total: float, work: Path, provenance: list[dict] | None = None,
) -> list[Shot]:
    """Beat'leri çekimlere gruplar; her çekim kendi kaynağını ve hareketini alır."""
    declared = board.get("shots") or [{"media": board["image"]}]
    shots: list[Shot] = []
    entries: list[dict] = []
    for index, entry in enumerate(declared):
        owned = [i for i, beat in enumerate(beats) if beat.get("shot", 0) == index]
        if not owned:
            continue
        shots.append(Shot(
            media=PROJECT_ROOT,  # aşağıda çözülüyor
            start=starts[owned[0]],
            end=ends[owned[-1]],
            motion=entry.get("motion", "push_in"),
            focus=tuple(entry.get("focus", (0.5, 0.42))),  # noqa: C408
            crop=tuple(entry["crop"]) if entry.get("crop") else None,
        ))
        entries.append(entry)
    if not shots:
        raise SystemExit("Hiçbir çekime beat atanmamış — storyboard'daki 'shot' indekslerini kontrol et.")

    # Çekim sınırları: ilki 0'dan başlar, sonuncusu sona kadar sürer, aradakiler
    # bir sonrakinin başlangıcında biter — böylece kesme tam beat sınırına düşer.
    shots[0].start = 0.0
    shots[-1].end = total + 0.1
    for previous, following in zip(shots, shots[1:]):
        previous.end = following.start

    used: set[str] = set()
    for index, (shot, entry) in enumerate(zip(shots, entries)):
        duration = shot.end - shot.start
        media = resolve_media(entry, index, duration, used)
        if media is None or not media.exists():
            fallback = entry.get("fallback_media")
            if not fallback:
                raise SystemExit(
                    f"Çekim {index} için kaynak bulunamadı ve 'fallback_media' tanımlı değil."
                )
            print(f"      çekim {index}: klip bulunamadı, fotoğrafa düşülüyor")
            media = PROJECT_ROOT / fallback
        shot.media = media

        if media.suffix.lower() in VIDEO_EXT:
            prepared = work / f"shot_{index:02d}.mp4"
            prepare_clip(media, prepared, duration, float(entry.get("start_at", 0.0)))
            shot.clip_path = prepared
        else:
            shot.base = load_shot_base(media, shot.focus, shot.crop)

        if provenance is not None:
            provenance.append({
                "shot": index,
                "query": entry.get("query", ""),
                "path": str(media.relative_to(PROJECT_ROOT)).replace("\\", "/"),
                "kind": "video" if shot.clip_path else "foto",
            })
    return shots


def mix_audio(vo_path: Path, music: Path | None, total: float, out_path: Path) -> None:
    """Seslendirmeyi öne alır, müziği altına ducking ile serer."""
    if music is None or not music.exists():
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-i", str(vo_path),
             "-af", f"apad,atrim=0:{total:.3f},volume=1.15",
             "-c:a", "aac", "-b:a", "160k", str(out_path)],
            check=True,
        )
        return

    fade_start = max(total - 1.2, 0.1)
    graph = (
        f"[0:a]apad,atrim=0:{total:.3f},asetpts=N/SR/TB,volume=1.30,"
        f"aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo[vo];"
        f"[1:a]atrim=0:{total:.3f},asetpts=N/SR/TB,volume=0.34,"
        f"afade=t=in:st=0:d=0.7,afade=t=out:st={fade_start:.3f}:d=1.2,"
        f"aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo[mus];"
        f"[vo]asplit=2[vo_main][vo_key];"
        f"[mus][vo_key]sidechaincompress=threshold=0.02:ratio=14:attack=12:release=320[duck];"
        f"[duck][vo_main]amix=inputs=2:duration=first:normalize=0,"
        # Sosyal platform hedefi ~-14 LUFS; her Reel'in aynı ses yüksekliğinde
        # çıkması kanalın "profesyonel" duyulmasının en ucuz yolu.
        f"loudnorm=I=-14:TP=-1.5:LRA=11,"
        f"alimiter=limit=0.94,aformat=sample_fmts=fltp[out]"
    )
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(vo_path), "-i", str(music),
         "-filter_complex", graph, "-map", "[out]",
         "-c:a", "aac", "-b:a", "160k", str(out_path)],
        check=True,
    )


def music_only_mix(music: Path | None, total: float, out_path: Path) -> None:
    """Seslendirme olmadan yalnızca müzik (veya tam sessizlik) — 'sessiz' önizleme için.

    Ducking yok (bastırılacak bir seslendirme yok), bu yüzden müzik normal
    dinleme seviyesinde çalar.
    """
    if music is None or not music.exists():
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi",
             "-i", f"anullsrc=r=48000:cl=stereo:d={total:.3f}",
             "-c:a", "aac", "-b:a", "160k", str(out_path)],
            check=True,
        )
        return
    fade_start = max(total - 1.2, 0.1)
    graph = (
        f"[0:a]atrim=0:{total:.3f},asetpts=N/SR/TB,volume=0.9,"
        f"afade=t=in:st=0:d=0.5,afade=t=out:st={fade_start:.3f}:d=1.2,"
        f"aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo[out]"
    )
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(music),
         "-filter_complex", graph, "-map", "[out]",
         "-c:a", "aac", "-b:a", "160k", str(out_path)],
        check=True,
    )


def shrink_if_needed(path: Path, duration: float) -> None:
    """20 MB (jsDelivr limiti) altına indirir — hedef bit hızıyla, CRF'le değil.

    Önceki hâli sabit CRF 20 ile yeniden kodluyordu; gerçek video kliplerinde
    bu limitin ALTINA inmeyi garanti etmiyor, hatta ölçüldü ki dosyayı
    büyütebiliyor (28,1 MB → 29,5 MB). Hedef bit hızı hesaplamak, süre ne
    olursa olsun sonucu limitin altına oturtuyor.
    """
    size = path.stat().st_size
    if size <= JSDELIVR_LIMIT:
        return
    audio_kbps = 160
    target_bytes = JSDELIVR_LIMIT * 0.92          # kap ek yükü için pay
    video_kbps = int((target_bytes * 8 / max(duration, 1)) / 1000) - audio_kbps
    video_kbps = max(video_kbps, 800)
    print(f"      {size / 1e6:.1f} MB > 20 MB — {video_kbps} kbps ile yeniden kodlanıyor")
    temp = path.with_suffix(".small.mp4")
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(path),
         "-c:v", "libx264", "-b:v", f"{video_kbps}k",
         "-maxrate", f"{int(video_kbps * 1.3)}k", "-bufsize", f"{video_kbps * 2}k",
         "-preset", "medium", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", f"{audio_kbps}k", str(temp)],
        check=True,
    )
    shutil.move(str(temp), str(path))


BUILD_LOG = PROJECT_ROOT / "content" / "build_log.json"


def write_manifest(slug: str, board: dict, total: float, clips: list, provenance: list[dict]) -> None:
    """Hangi Reel hangi klip ve hangi ses motoruyla üretildi — kaynak künyesi
    ve kalite kontrolü buradan okunuyor (make_captions_v2.py dahil)."""
    log = json.loads(BUILD_LOG.read_text(encoding="utf-8")) if BUILD_LOG.exists() else {}
    footage_index = {}
    index_path = PROJECT_ROOT / "footage" / "index.json"
    if index_path.exists():
        for entry in json.loads(index_path.read_text(encoding="utf-8")).values():
            footage_index[entry["path"]] = entry
    for item in provenance:
        found = footage_index.get(item["path"])
        if found:
            item["provider"] = found["provider"]
            item["source_page"] = found["source_page"]
    log[slug] = {
        "built_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "duration": round(total, 2),
        "voice_engine": sorted({clip.engine for clip in clips}),
        "aligned": all(clip.words for clip in clips),
        "music_id": board.get("music_id", ""),
        "shots": provenance,
    }
    BUILD_LOG.write_text(json.dumps(log, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build(slug: str, out_dir: Path, keep_work: bool = False,
          paid_voice: bool = False, silent: bool = False) -> Path:
    board = load_storyboard(slug)
    beats = board["beats"]
    work = Path(tempfile.mkdtemp(prefix=f"reel_{slug}_"))
    voice = board.get("voice", DEFAULT_VOICE)
    rate = board.get("rate", DEFAULT_RATE)
    pitch = board.get("pitch", DEFAULT_PITCH)

    recorded = sum(1 for beat in beats if beat.get("voice_file"))
    label = f"{recorded} kayıt + {len(beats) - recorded} sentez" if recorded else voice
    print(f"[1/6] Seslendirme üretiliyor ({len(beats)} beat, {label})")
    clips = synth_beats(
        [
            {
                "text": beat["vo"],
                "voice": beat.get("voice", voice),
                "rate": beat.get("rate", rate),
                "pitch": beat.get("pitch", pitch),
                "voice_file": beat.get("voice_file"),
            }
            for beat in beats
        ],
        work,
        voice=voice, rate=rate, pitch=pitch, prefer_eleven=paid_voice,
    )

    engines = {clip.engine for clip in clips}
    aligned = all(clip.words for clip in clips)
    print(f"      motor: {', '.join(sorted(engines))}"
          + ("  ·  kelime zamanlaması hizalamadan" if aligned else ""))

    # Hizalama varsa kart süreleri ölçümden gelir; ölçmeye gerek yok.
    card_weights: list[list[float]] | None = None
    if not aligned:
        print("[2/6] Altyazı kartlarının süreleri ölçülüyor (hizalama yok)")
        card_weights = []
        for index, beat in enumerate(beats):
            pieces = beat_chunks(beat)
            if len(pieces) == 1:
                card_weights.append([1.0])
                continue
            card_weights.append(measure_chunks(
                pieces, work / f"chunks_{index:02d}",
                voice=beat.get("voice", voice),
                rate=beat.get("rate", rate),
                pitch=beat.get("pitch", pitch),
            ))

    gaps = [float(beat.get("pause_after", DEFAULT_GAP)) for beat in beats]
    gaps[-1] = TAIL
    starts, ends = [], []
    cursor = LEAD_IN
    for clip, gap in zip(clips, gaps):
        starts.append(cursor)
        ends.append(cursor + clip.duration)
        cursor += clip.duration + gap
    total = round(cursor, 2)
    print(f"      toplam süre: {total:.2f} sn")
    if total > 42:
        print("      UYARI: 42 sn üstü Reels'te tamamlanma oranını düşürür, senaryoyu kısalt.")

    durations = [clip.duration for clip in clips]
    cards: list[Card] = build_cards(
        beats, starts, durations, card_weights, [clip.words for clip in clips],
    )
    provenance: list[dict] = []
    shots = build_shots(board, beats, starts, ends, total, work, provenance)

    print(f"[3/6] Görüntü render ediliyor ({int(total * FPS)} kare, {len(shots)} çekim)")
    silent_track = work / "silent.mp4"
    # CRF ile kodla: v1'in sabit `quality=8` ayarı tüylü/dokulu fotoğraflarda
    # 100 MB+ dosya üretip her seferinde yeniden kodlama gerektiriyordu.
    with imageio.get_writer(
        silent_track, fps=FPS, codec="libx264", macro_block_size=1,
        ffmpeg_params=["-crf", "21", "-preset", "medium", "-pix_fmt", "yuv420p"],
    ) as writer:
        render_timeline(shots, cards, board["source_name"], total, writer)

    if silent:
        print("[4/6] Seslendirme atlandı (--silent) — yalnızca müzik/sessizlik")
        mixed = work / "mixed.m4a"
        music_only_mix(music_path(board.get("music_id", "")), total, mixed)
    else:
        print("[4/6] Seslendirme birleştiriliyor")
        raw_vo = work / "vo_raw.wav"
        lead = work / "lead.wav"
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi",
             "-i", f"anullsrc=r=48000:cl=mono:d={LEAD_IN}", str(lead)],
            check=True,
        )
        padded = [VoiceClip(-1, "", lead, audio_duration(lead))] + clips
        concat_with_gaps(padded, [0.0] + gaps, raw_vo)

        print("[5/6] Ses doğallaştırılıyor (de-esser, EQ, kompresyon, oda)")
        vo_track = work / "vo.wav"
        shape_voice(raw_vo, vo_track)

        print("[6/6] Müzik karıştırılıyor ve birleştiriliyor")
        mixed = work / "mixed.m4a"
        mix_audio(vo_track, music_path(board.get("music_id", "")), total, mixed)

    out_dir.mkdir(parents=True, exist_ok=True)
    output = out_dir / (f"{slug}.silent.mp4" if silent else f"{slug}.mp4")
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(silent_track), "-i", str(mixed),
         "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "copy",
         "-shortest", str(output)],
        check=True,
    )
    shrink_if_needed(output, total)
    if not silent:
        write_manifest(slug, board, total, clips, provenance)
    print(f"      -> {output}  ({output.stat().st_size / 1e6:.1f} MB, {total:.1f} sn)")

    if keep_work:
        print(f"      çalışma klasörü: {work}")
    else:
        shutil.rmtree(work, ignore_errors=True)
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description="Pati Şifresi v2 Reel üretici")
    parser.add_argument("slugs", nargs="+", help="storyboards.json içindeki slug(lar)")
    parser.add_argument("--out-dir", type=Path, default=PROJECT_ROOT / "videos_v2")
    parser.add_argument("--keep-work", action="store_true", help="ara dosyaları silme")
    parser.add_argument("--paid-voice", action="store_true",
                        help="ElevenLabs kullan (ücretli, kota youtube projesiyle ortak)")
    parser.add_argument("--silent", action="store_true",
                        help="Seslendirmesiz önizleme üret ({slug}.silent.mp4) — kullanıcı kendi sesini kaydedecekse")
    args = parser.parse_args()
    for slug in args.slugs:
        print(f"\n=== {slug} ===")
        build(slug, args.out_dir, args.keep_work, args.paid_voice, args.silent)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
