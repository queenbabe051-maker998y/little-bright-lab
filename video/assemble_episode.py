#!/usr/bin/env python3
"""Assemble pre-generated Little Bright Lab 3D scene clips into a YouTube master.

This script does NOT generate AI footage. Place ordered MP4 scene clips in
video/episode/clips/scene_001.mp4, scene_002.mp4, ... and optional audio stems
in video/episode/audio/. Requires ffmpeg and ffprobe on PATH.
"""
from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
EPISODE = ROOT / "video" / "episode"
CLIPS = EPISODE / "clips"
AUDIO = EPISODE / "audio"
OUT = ROOT / "output" / "little-bright-lab-animal-sounds-safari.mp4"
WIDTH, HEIGHT, FPS = 1920, 1080, 24

def run(cmd):
    subprocess.run([str(x) for x in cmd], check=True)

def duration(path):
    raw = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(path)
    ], text=True).strip()
    return float(raw)

def main():
    clips = sorted(CLIPS.glob("scene_[0-9][0-9][0-9].mp4"))
    if not clips:
        sys.exit(f"No scene clips found in {CLIPS}. Add scene_001.mp4, scene_002.mp4, ...")
    total_input = sum(duration(p) for p in clips)
    if total_input < 170 or total_input > 310:
        print(f"WARNING: source clips total {total_input:.1f}s; target is about 180–300s.", file=sys.stderr)

    tmp = EPISODE / "normalized"
    tmp.mkdir(parents=True, exist_ok=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    normalized = []
    for i, clip in enumerate(clips, 1):
        target = tmp / f"part_{i:03d}.mp4"
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", clip,
            "-map", "0:v:0", "-an",
            "-vf", f"scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=decrease,"
                   f"pad={WIDTH}:{HEIGHT}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps={FPS},format=yuv420p",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-movflags", "+faststart", target
        ])
        normalized.append(target)

    concat_file = tmp / "concat.txt"
    concat_file.write_text("".join(f"file '{p.resolve().as_posix()}'\n" for p in normalized), encoding="utf-8")
    silent_video = tmp / "picture.mp4"
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0",
         "-i", concat_file, "-c", "copy", silent_video])

    narration = AUDIO / "narration.wav"
    music = AUDIO / "music.wav"
    sfx = AUDIO / "sfx.wav"
    subtitles = AUDIO / "subtitles.srt"
    inputs = ["-i", silent_video]
    filters = []
    labels = []
    next_input = 1
    if narration.exists():
        inputs += ["-i", narration]
        filters.append(f"[{next_input}:a]aresample=48000,volume=1.0[narr]")
        labels.append("[narr]")
        next_input += 1
    if sfx.exists():
        inputs += ["-i", sfx]
        filters.append(f"[{next_input}:a]aresample=48000,volume=0.8[sfx]")
        labels.append("[sfx]")
        next_input += 1
    if music.exists():
        inputs += ["-stream_loop", "-1", "-i", music]
        filters.append(f"[{next_input}:a]aresample=48000,volume=0.13[music]")
        labels.append("[music]")
        next_input += 1

    if labels:
        filters.append("".join(labels) + f"amix=inputs={len(labels)}:duration=longest:dropout_transition=2,"
                       "alimiter=limit=0.95[aout]")
        cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *inputs,
               "-filter_complex", ";".join(filters), "-map", "0:v:0", "-map", "[aout]",
               "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest"]
    else:
        cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *inputs,
               "-map", "0:v:0", "-c:v", "copy", "-an"]
    if subtitles.exists():
        # Burn captions after concat; ffmpeg's subtitles filter reads the SRT.
        cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *inputs,
               "-vf", f"subtitles={subtitles.as_posix()}:force_style='FontName=Arial,FontSize=26,Outline=2,Shadow=1,Alignment=2'",
               "-map", "0:v:0", "-map", "[aout]" if labels else "0:a?", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
               "-c:a", "aac", "-b:a", "192k", "-shortest"] if labels else [
               "ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", silent_video,
               "-vf", f"subtitles={subtitles.as_posix()}:force_style='FontName=Arial,FontSize=26,Outline=2,Shadow=1,Alignment=2'",
               "-map", "0:v:0", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-an"]
    run(cmd + [OUT])
    print(json.dumps({"output": str(OUT), "scenes": len(clips), "source_duration_seconds": round(total_input, 2)}, indent=2))

if __name__ == "__main__":
    main()
