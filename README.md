# The Little Bright Lab — Animal Sounds Safari

This repository is the production workspace for original educational cartoons for children ages 4–10.

## Episode 01: Who Says Moo?

The approved 60-second storyboard, scene prompts, character continuity rules, sound cues, and motion prompts are in [docs/ANIMAL_SOUNDS_SAFARI_EPISODE_01.md](docs/ANIMAL_SOUNDS_SAFARI_EPISODE_01.md).

### Create the final MP4 with GitHub Actions

1. Generate or animate the five scene clips using the approved prompts and the same character reference images for every shot.
2. Add the five approved MP4 files to `video/episode/clips/` using these exact names and durations:
   - `scene_001.mp4` — 10 seconds
   - `scene_002.mp4` — 12 seconds
   - `scene_003.mp4` — 13 seconds
   - `scene_004.mp4` — 15 seconds
   - `scene_005.mp4` — 10 seconds
3. Optionally add audio stems to `video/episode/audio/`: `narration.wav`, `music.wav`, `sfx.wav`, and `subtitles.srt`.
4. Open the **Actions** tab and select **Assemble Animal Sounds Safari Episode 01**.
5. Click **Run workflow**. When it finishes, download the artifact named `little-bright-lab-animal-sounds-safari-episode-01`.

The workflow normalizes the scene clips to 1920×1080 at 24 fps, assembles the five scenes in order, mixes available audio stems, burns subtitles if supplied, validates the final duration, and uploads the MP4 artifact.

**Important:** GitHub Actions automates editing and rendering; it does not generate studio-quality AI video on its own. The five approved animated clips must exist before assembly. The old procedural sampler is only a prototype and is not the target visual quality for this episode.
