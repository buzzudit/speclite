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
- Write the narration as a performance, not a flat read: each multi-sentence line shifts feeling where its meaning changes, varied opening tags, capitals on stressed words, a pause before the reveal, the strongest contrast at the "so what" beat (see Voice direction in the workflows doc).
- The narration text is sent to ElevenLabs. Keep it to fictional or approved content.
- The API key lives in a git-ignored `.env` or the environment. Add `.env` and `.env.*` to `.gitignore` first. Never print the key, echo it, or put it in a committed file. If the key lacks a permission (a 401), do not work around it; say what could not be verified.
- Use a full ffmpeg and ffprobe. Do not rely on Playwright's bundled ffmpeg for H.264 or AAC.
- Use real clicks through the helper. Prefer text-based Playwright locators (`page.getByText()`, `page.getByRole()`, `page.getByLabel()`) over CSS class selectors — many apps use CSS-in-JS or generated class names that change between builds. Fall back to `data-demo-*` attributes when text is ambiguous, and to CSS selectors only as a last resort.
- Show the branded splash card as frame 1 of the video. Log in behind the splash card so the viewer never sees a login screen. Record `cards.T0 = now()` and `starts.T0 = cards.T0` right after `showCard()`.
- Read the product's CSS and extract brand colors into a configurable `COLORS` object (or CSS variables) before writing any card HTML, ripple or caption style. Do not use the template's placeholder colors.
- Do not mix this with owner-run (OS-level) demo input. This method makes a recorded video.

Implementation steps:

1. **Preflight.** Run the app, log in with the demo account, and confirm it lands on the expected page — not onboarding, a redirect, or an error. If seed data is missing (practice records, linking tables, demo data the journey needs), fix the seed before proceeding.
2. Inspect the product, its run command, routes and selectors. Confirm the dev server runs.
3. Write `demos/demo-plan.md` from the template: persona, journey, beats, voice, start state, background music, sync plan, acceptance criteria. The storyboard must cover the product's primary happy path end-to-end — if the core action is "submit", "send", "approve" or "create", that action must appear as a beat.
4. Add `.env`, `.env.*` and `tour/out/` to `.gitignore`. Install Playwright and Chromium. Confirm ffmpeg and ffprobe.
5. Copy `tooling/` into `tour/`: `lib.mjs`, `voice.mjs`, `mux.mjs`, and from the templates `script.mjs` and `walkthrough.mjs`. Fill in the script (use `text: null` for silent splash beats) and one action per beat. Extract brand colors from the product's CSS into `lib.mjs`'s `COLORS` object.
6. Generate the voice clips. Report characters sent and each clip's length.
7. Record. Actions must finish before their lines do. If a line runs longer than its action, stretch the holds rather than speeding the voice. The T0 action should show the splash card immediately and log in behind it.
8. Let the tooling calibrate picture time against the clock and mux. Read the calibration output; investigate large residuals.
9. **Background music.** Download a royalty-free instrumental track (Pixabay, Uppbeat, etc.). If shorter than the video, crossfade-loop it. Mix at −20 dB below narration with fade-in (2 s) and fade-out (3 s). Record the track name, author, source URL and license in the demo plan.
10. Verify: video length; sample frames at several beat starts and mid-beat; audio onsets against placed times; loudness; no end-of-clip blips; background music audible but not competing; any item the tooling could not check.
11. **Embed.** Copy the mp4 to the marketing site or landing page (`public/demo.mp4`). Add a click-to-play video component with a play-button overlay (see the React pattern in `planning/demo-maker-workflows.md`).
12. Deliver the mp4 and record done evidence: files, what was run, what was not verified, residual risk.
13. Document how to re-record: one command, and that unchanged lines are cached.

Output expected:

- The demo plan, the script, the tooling in `tour/`, the mp4, and the story's done evidence.
- A short note listing exactly what was not verified.
