# Episode assets

Put generated video shots here in story order:
- `clips/scene_001.mp4`
- `clips/scene_002.mp4`
- continue with zero-padded scene numbers

Optional audio stems:
- `audio/narration.wav`
- `audio/music.wav`
- `audio/sfx.wav`
- `audio/subtitles.srt`

Use the 16:9 horizontal framing for the 3–5 minute YouTube episode. Do not commit large generated video binaries to normal Git history; use Git LFS or a private storage/artifact handoff for the actual media. GitHub Actions can assemble files that are available to its runner, but it does not generate AI animation.
