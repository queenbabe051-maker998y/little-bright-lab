# GitHub + Blender 3D motion test

This is a real 3D Blender render workflow, not the old Pillow-based procedural 2D animation and not a Higgsfield job.

## Run it
1. Open the GitHub repository's **Actions** tab.
2. Choose **Render Little Bright Lab 3D Motion Test**.
3. Click **Run workflow** and confirm.
4. When complete, open the run and download artifact **little-bright-lab-github-blender-3d-test**.

The artifact contains a character lineup PNG and an 8-second MP4 rendered by Blender and encoded by FFmpeg. The first pass uses primitive-built stylized 3D characters as a technical proof of concept; it is not yet a polished studio-grade rigged character production. The next iteration should replace blockout geometry with carefully modeled, rigged characters and improve facial animation, lighting, and audio.

GitHub Actions provides compute for the render, but its available CPU time and render speed can vary. No external paid video-generation service is called.
