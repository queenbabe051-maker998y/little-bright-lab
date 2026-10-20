#!/usr/bin/env python3
"""Assemble five approved scene clips into the 60-second episode master.

This script assembles footage; it does not generate AI animation. See
docs/ANIMAL_SOUNDS_SAFARI_EPISODE_01.md for the approved shot prompts.
"""
from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
EPISODE = ROOT / "video" / "episode"
CLIPS = EPISODE / "clips"
AUDIO = EPISODE / "audio"
OUT = ROOT / "output" / "little-bright-lab-animal-sounds-safari-episode-01.mp4"
WIDTH, HEIGHT, FPS = 1920, 1080, 24
SCENE_DURATIONS = [10, 12, 13, 15, 10]
EXPECTED_SCENES = 5
TOTAL_DURATION = 60.0


def run(cmd):
    subprocess.run([str(x) for x in cmd], check=True)


def duration(path):
    raw = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(path)
    ], text=True).strip()
    return float(raw)


def main():
    clips = [CLIPS / f"scene_{i:03d}.mp4" for i in range(1, EXPECTED_SCENES + 1)]
    missing = [p.name for p in clips if not p.is_file()]
    if missing:
        sys.exit(
            "Missing approved scene clips: " + ", ".join(missing) + "\n"
            f"Place all five generated/animated MP4s in {CLIPS}. "
            "See docs/ANIMAL_SOUNDS_SAFARI_EPISODE_01.md for scene prompts. "
            "This workflow assembles footage; it does not create AI animation."
        )

    tmp = EPISODE / "normalized"
    tmp.mkdir(parents=True, exist_ok=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    normalized = []
    for i, (clip, target_seconds) in enumerate(zip(clips, SCENE_DURATIONS), 1):
        source_seconds = duration(clip)
        if source_seconds + 0.05 < target_seconds:
            sys.exit(
                f"{clip.name} is only {source_seconds:.2f}s; scene {i} requires "
                f"{target_seconds}s. Regenerate or edit this clip before assembly."
            )
        target = tmp / f"part_{i:03d}.mp4"
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", clip,
            "-t", str(target_seconds), "-map", "0:v:0", "-an",
            "-vf", f"scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=decrease,"
                   f"pad={WIDTH}:{HEIGHT}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps={FPS},format=yuv420p",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-movflags", "+faststart", target
        ])
        normalized.append(target)

    concat_file = tmp / "concat.txt"
    concat_file.write_text(
        "".join(f"file '{p.resolve().as_posix()}'\n" for p in normalized),
        encoding="utf-8"
    )
    silent_video = tmp / "picture.mp4"
    run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-f", "concat", "-safe", "0", "-i", concat_file,
        "-t", f"{TOTAL_DURATION:.3f}", "-c", "copy", silent_video
    ])

    narration = AUDIO / "narration.wav"
    music = AUDIO / "music.wav"
    sfx = AUDIO / "sfx.wav"
    subtitles = AUDIO / "subtitles.srt"
    stems = []
    for path, volume in ((narration, 1.0), (sfx, 0.8), (music, 0.13)):
        if path.exists():
            stems.append((path, volume))

    audio_mix = tmp / "audio_mix.m4a"
    if stems:
        cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"]
        for path, _ in stems:
            if path == music:
                cmd += ["-stream_loop", "-1", "-i", path]
            else:
                cmd += ["-i", path]
        filters, labels = [], []
        for i, (_, volume) in enumerate(stems):
            filters.append(f"[{i}:a]aresample=48000,volume={volume}[a{i}]")
            labels.append(f"[a{i}]")
        filters.append(
            "".join(labels) + f"amix=inputs={len(labels)}:duration=longest:dropout_transition=2,"
            "alimiter=limit=0.95[aout]"
        )
        run(cmd + [
            "-filter_complex", ";".join(filters), "-map", "[aout]",
            "-t", f"{TOTAL_DURATION:.3f}", "-c:a", "aac", "-b:a", "192k", audio_mix
        ])

    muxed = tmp / "muxed.mp4"
    mux_cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", silent_video]
    if stems:
        mux_cmd += ["-i", audio_mix, "-map", "0:v:0", "-map", "1:a:0",
                    "-c:v", "copy", "-c:a", "copy", "-t", f"{TOTAL_DURATION:.3f}"]
    else:
        mux_cmd += ["-map", "0:v:0", "-c:v", "copy", "-an", "-t", f"{TOTAL_DURATION:.3f}"]
    run(mux_cmd + [muxed])

    if subtitles.exists():
        subtitle_filter = (
            f"subtitles={subtitles.as_posix()}:"
            "force_style='FontName=Arial,FontSize=26,Outline=2,Shadow=1,Alignment=2'"
        )
        final_cmd = [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", muxed,
            "-vf", subtitle_filter, "-map", "0:v:0"
        ]
        if stems:
            final_cmd += ["-map", "0:a:0", "-c:a", "copy"]
        else:
            final_cmd += ["-an"]
        final_cmd += ["-t", f"{TOTAL_DURATION:.3f}", "-c:v", "libx264", "-preset", "medium",
                      "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart", OUT]
        run(final_cmd)
    else:
        OUT.write_bytes(muxed.read_bytes())

    final_seconds = duration(OUT)
    if abs(final_seconds - TOTAL_DURATION) > 0.15:
        sys.exit(f"Final render duration is {final_seconds:.2f}s, expected exactly 60s.")

    print(json.dumps({
        "output": str(OUT),
        "scenes": len(clips),
        "scene_durations_seconds": SCENE_DURATIONS,
        "final_duration_seconds": round(final_seconds, 3),
        "resolution": f"{WIDTH}x{HEIGHT}",
        "fps": FPS,
        "audio_stems": [p.name for p, _ in stems],
        "subtitles_burned_in": subtitles.exists()
    }, indent=2))


if __name__ == "__main__":
    main()
