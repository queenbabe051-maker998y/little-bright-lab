# The Little Bright Lab — 3D Episode Production Workflow

## Decision
The earlier procedural Pillow animation is a rejected prototype, not the production path for the new episode. Keep it for history, but do not use it to create the new 3–5 minute episode.

## Episode 001
**Working title:** Animal Sounds Safari: Who Made That Sound?
**Audience:** Ages 4–10
**Master:** 16:9, 1920×1080, 24 fps, H.264 MP4, AAC audio
**Target duration:** 3:30–4:00
**Visual target:** polished, friendly 3D children's TV animation; expressive faces, readable silhouettes, motivated camera moves, detailed but uncluttered environments, consistent color palette.
**Main cast:** Mimi (pink bunny), Moomo (cream cow with brown patches), Dott (lavender owl), Rumble (golden-orange lion cub). No dragon mascot.

## Production pipeline

1. **Character bible and reference pack**
   - Finalize a front/three-quarter/full-body reference for each character.
   - Keep eye shape, proportions, fur colors, clothing/accessories, and scale fixed.
   - Use the same approved reference images as image references for every shot. Do not rely on text descriptions alone for identity consistency.
2. **Look development**
   - Approve one hero frame showing the cast in a lush, sunny, whimsical 3D safari clearing.
   - Lock lighting, material style, color palette, lens feel, and background detail.
3. **Storyboard and animatic**
   - Build the scene list below before generating full-quality shots.
   - Generate a few low-cost test shots and inspect faces, limbs, motion, sound and continuity before scaling up.
4. **Shot generation**
   - Prefer reference-driven image-to-video generation for the cast and scene continuity.
   - Generate each shot as a short clip (typically 5–12 seconds; model limits vary). Use wide/medium/close-up variety, clear action verbs, one main action per shot, and explicit camera direction.
   - Generate clean visuals with native audio disabled when separate narration/SFX gives better control. Use native audio only when it clearly helps.
5. **Voice and sound**
   - Record/generate one warm, clear narrator voice; allow pauses for children to answer.
   - Add licensed/original cow moo, dog bark, cat meow, duck quack and lion roar; do not depend on inaccurate generated sound effects.
   - Use original or properly licensed music and keep it below dialogue.
6. **Edit and quality control**
   - Assemble clips in storyboard order using `video/assemble_episode.py`.
   - Add narration, music, SFX, and captions/subtitles.
   - Watch the complete export for character drift, malformed anatomy, audio clipping, pacing, spelling, safe kid-friendly visuals, and lesson accuracy.
7. **Publish**
   - Export a clean 16:9 master for YouTube. Make a separate vertical cut for Shorts only after the long-form master is approved.

## Episode storyboard (approx. 3:45)

| Scene | Approx. time | Beat and learning objective |
|---|---:|---|
| 01 | 0:00–0:12 | Bright opening in the safari clearing; Mimi invites viewers to play a listening game. |
| 02 | 0:12–0:28 | The friends hear a mystery sound from behind leafy bushes; ask children to listen carefully. |
| 03 | 0:28–0:42 | Sound clue: “Moo!” Pause for a guess; Moomo steps out, smiles, and says “I’m a cow!” |
| 04 | 0:42–0:58 | Repeat cow sound and name; show cow in a gentle farm/safari meadow context. |
| 05 | 0:58–1:12 | New clue: “Woof, woof!” friends guess together; reveal a friendly dog visitor. |
| 06 | 1:12–1:28 | Say “dog” and “bark”; dog trots and wags its tail. |
| 07 | 1:28–1:42 | New clue: “Meow!” hold a beat for audience response. |
| 08 | 1:42–1:58 | Reveal a cute cat; say “cat” and “meow,” then repeat the sound. |
| 09 | 1:58–2:12 | New clue: “Quack, quack!” Dott points toward a pond. |
| 10 | 2:12–2:28 | Reveal a duck paddling; say “duck” and “quack.” |
| 11 | 2:28–2:45 | Quick listening round: replay four short sounds; children name the animals. |
| 12 | 2:45–3:05 | Rumble asks which sound was easiest to remember; repeat names and sounds clearly. |
| 13 | 3:05–3:25 | Gentle recap song/chant with all four friends; one animal sound at a time. |
| 14 | 3:25–3:45 | Celebrate the viewer, invite them to learn again next time, cheerful end card. |

The dog and cat are guest animals for this episode; design them as reusable assets if they return.

## Shot prompt template
Use the same approved character reference images each time. Replace bracketed details for each shot:

“Polished original 3D animated children's television scene, [approved character names and exact action], in the established Little Bright Lab world. Preserve the reference characters' exact colors, face shapes, proportions and markings. Clear readable body language, appealing eye animation, natural secondary motion, smooth purposeful camera move [camera direction], soft cinematic daylight, colorful high-quality materials, clean composition, joyful gentle comedy, age-appropriate, 16:9. One continuous shot. No text, captions, logos, extra limbs, character redesigns, scary expressions or abrupt cuts.”

## Repository roles
- `docs/3D_EPISODE_WORKFLOW.md`: production bible, storyboard and quality gates.
- `video/assemble_episode.py`: deterministic post-production assembly for generated scene clips and audio files.
- `.github/workflows/assemble-3d-episode.yml`: optional GitHub Actions assembly/export workflow.
- `video/episode/clips/scene_001.mp4` etc.: generated clips, kept outside Git when files are large; put them in the workflow workspace or a release asset source as appropriate.
- `video/episode/audio/narration.wav`, `music.wav`, `sfx.wav`: optional audio stems.
- `video/episode/audio/subtitles.srt`: optional subtitle file.

## Cost and quality gate
Do not generate all 3–5 minutes in one untested batch. First approve character reference art and a 5–10 second motion test, inspect results, and check the exact current cost. Generate the remaining shots only after style and character consistency are acceptable. AI video generation may cost credits; this repository workflow does not itself generate AI footage.
