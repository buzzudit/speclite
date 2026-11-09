# Implement A Demo Maker Walkthrough

Use this prompt when asking an agent to produce a narrated walkthrough video of a web app with the Speclite Demo Maker method.

## Prompt

You are working in `{{TARGET_REPO}}`.

Goal:
Produce a narrated walkthrough video of `{{PRODUCT}}` for `{{AUDIENCE}}`, using the Speclite Demo Maker pattern: a scripted browser drives the real UI, an AI voice narrates, and picture and voice are locked in sync.

Rules:

- Work from a story. Create or move one to `doing` before building, and record done evidence at the end.
- Read `planning/demo-maker-workflows.md` first and follow it.
- Check the product carries the journey before recording (guided path, one next action per screen, no placeholder data, no disclaimer banners unless asked). If it does not, fix the product or stop and say so.
- Write the demo plan and the beats table first. Get the owner's approval of the narration before generating any voice.
- The narration text is sent to ElevenLabs. Keep it to fictional or approved content.
- The API key lives in a git-ignored `.env` or the environment. Add `.env` and `.env.*` to `.gitignore` first. Never print the key, echo it, or put it in a committed file. If the key lacks a permission (a 401), do not work around it; say what could not be verified.
- Use a full ffmpeg and ffprobe. Do not rely on Playwright's bundled ffmpeg for H.264 or AAC.
- Use real clicks through the helper. Use stable selectors, not text. Start from a clean, repeatable state.
- Do not mix this with owner-run (OS-level) demo input. This method makes a recorded video.

Implementation steps:

1. Inspect the product, its run command, routes and selectors. Confirm the dev server runs.
2. Write `demos/demo-plan.md` from the template: persona, journey, beats, voice, start state, sync plan, acceptance criteria.
3. Add `.env`, `.env.*` and `tour/out/` to `.gitignore`. Install Playwright and Chromium. Confirm ffmpeg and ffprobe.
4. Copy `tooling/` into `tour/`: `lib.mjs`, `voice.mjs`, `mux.mjs`, and from the templates `script.mjs` and `walkthrough.mjs`. Fill in the script and one action per beat.
5. Generate the voice clips. Report characters sent and each clip's length.
6. Record. Actions must finish before their lines do. If a line runs longer than its action, stretch the holds rather than speeding the voice.
7. Let the tooling calibrate picture time against the clock and mux. Read the calibration output; investigate large residuals.
8. Verify: video length; sample frames at several beat starts and mid-beat; audio onsets against placed times; loudness; any item the tooling could not check.
9. Deliver the mp4 and record done evidence: files, what was run, what was not verified, residual risk.
10. Document how to re-record: one command, and that unchanged lines are cached.

Output expected:

- The demo plan, the script, the tooling in `tour/`, the mp4, and the story's done evidence.
- A short note listing exactly what was not verified.
