# {{PROJECT_NAME}} Demo Maker Workflows

Status: optional module
Last Updated: {{DATE}}

## Purpose

Use this module to produce a narrated walkthrough video of a web app or prototype: a scripted browser drives the real UI, an AI voice narrates, and picture and voice are locked in sync. The result is an mp4 you can send, embed or show in a review, and it can be re-recorded with one command after the product changes.

Core framing:

> Demo Maker: write the story as beats, generate the voice first, then record the real product at the pace of the voice, and place every line exactly where its action starts.

This is for concept walkthroughs, prototype reviews, founder and investor updates, and pre-interview material. It makes a video. It is not a live demo.

## Demo Maker versus the owner-run demo

| | Demo Maker | Owner-run demo |
|---|---|---|
| Output | A finished mp4 | A live run on the owner's machine |
| Input | Headless browser with an injected cursor and click ripples | Real OS cursor, clicks and scrolling |
| Voice | Pre-generated clips, placed by timing | Live narration synchronised to app state |
| Use for | Sharing, review, repeatable recordings | Showing the product live, OS-level realism |

If you need the real OS cursor, use the owner-run demo module. Do not mix the two methods in one demo.

## When to use

- The product runs in a browser on your machine (a dev server or a built preview).
- The workflow can be driven by stable selectors and starts from a clean, repeatable state.
- You can write the story as a sequence of short beats.

Avoid it when the product needs native desktop input, depends on live third-party data that changes between runs, or cannot be reset to a known start state.

## Before you record: the product must carry the journey

A good demo shows a journey, not a tour of tabs. Check the product first:

- The first screen sets up the person and the moment that starts the job.
- The path through the product is visible and guided (a story rail or step bar, one next action per screen, progress that follows what the person has done).
- The strongest moment in the story is built as a screen, not only described in the narration.
- No placeholder data. Use fictional but self-consistent data, with units on every number.
- Do not add disclaimer banners unless the owner asks for them.

If the product does not carry the journey, fix the product first. Narration cannot rescue a screen that does not show it.

## Pipeline

```
storyboard (beats) -> script -> voice clips -> record -> calibrate -> mux -> verify
```

1. **Storyboard.** One table: beat id, scene, what happens on screen, what the narrator says. One idea per beat. Aim for 12 to 25 beats and 3 to 5 minutes.
2. **Script approval.** The narration text is sent to the voice service. Get the owner's approval of the script before spending credits.
3. **Voice clips.** Generate one clip per beat. Cache by text, voice, model and settings so unchanged lines cost nothing on re-runs. Measure every clip's length.
4. **Record.** Run the real app in headless Chromium. At the start of each beat, start its action and note the clock time. A beat lasts as long as its clip plus a short pause, or as long as its action if that is longer. Write actions to finish before the line does.
5. **Calibrate.** Picture time is not the same as the clock. Find high-contrast moments in the recorded video (the dark title card, the dark closing card, chapter labels) whose clock times you noted, and fit picture time against clock time. The offset has been measured at 0.2 s on one run and 2.9 s on the next, so always calibrate; never assume.
6. **Mux.** Place each clip at its beat's calibrated time, mix, and write H.264 plus AAC. Trim the silent tail after the last line.
7. **Verify.** See the checklist below.

Files the tooling uses (copy from `tooling/` into `tour/` in the project):

- `script.mjs`: name, version, voice, model, settings and the beats (from `script.template.mjs`).
- `voice.mjs`: ElevenLabs text-to-speech with caching.
- `lib.mjs`: browser, injected cursor and ripples, chapter labels, cards, move and click helpers.
- `walkthrough.mjs`: the actions per beat and the run order (from `walkthrough.template.mjs`).
- `mux.mjs`: calibration and mixing.

## Prerequisites

- Node 20 or later and the project's dev server.
- Playwright and its Chromium: `npm i -D playwright` then `npx playwright install chromium`. This also gives you the browser video, as webm.
- A **full ffmpeg and ffprobe** on the PATH. Playwright's bundled ffmpeg is stripped: it writes webm only and cannot make H.264 or AAC. Windows: `winget install Gyan.FFmpeg`. macOS: `brew install ffmpeg`.
- An ElevenLabs API key in a git-ignored `.env` as `ELEVENLABS_API_KEY=...` (or in the environment). Add `.env` and `.env.*` to `.gitignore` before anything else. Never print the key or put it in a committed file.
- The key's permissions may cover text-to-speech only. A 401 from speech-to-text means the key cannot transcribe; do not work around it, verify by ear instead.

Suggested npm scripts: `tour:voice` (`node tour/voice.mjs`), `tour:record` (`node tour/walkthrough.mjs`), `tour:remux` (`node tour/mux.mjs`). Add `tour/out/` to `.gitignore`.

## Voice direction (ElevenLabs)

- Use `eleven_v3` for expressive delivery. It follows performance tags in square brackets and the punctuation of the text.
- Documented tags to prefer: `[calm]`, `[curious]`, `[excited]`, `[thoughtful]`, `[serious]`, `[whispers]`, `[sighs]`, `[short pause]`, `[long pause]`. Other plain-English tags usually work but can be read aloud; check by ear.
- Direct with punctuation: ellipses and dashes for pauses, a question mark to lift the voice, capitals for stress, short sentences.
- v3 offers stability presets (0.0 creative, 0.5 natural, 1.0 robust). 0.3 is a good expressive default. v3 does not support request stitching (`previous_text` and `next_text`); older models do.
- Spell numbers and units as words in the text ("five point four micromolar", "forty-five times").
- Expressive delivery runs longer than flat delivery because of the pauses. Re-record the picture at the new pace rather than squeezing audio to fit the old timings.

## Authoring the actions

- Start from a clean state: clear storage once per run and apply any start state (for example a theme) through `start({ storage })`.
- Use real clicks through the helper so the cursor moves and a ripple shows. Use stable selectors (`data-demo-*`, roles, labels). Avoid brittle text selectors.
- If the app scrolls inside a container, pass `scrollSelector`; scrolling the window does nothing.
- Grant clipboard permission (the helper does) if a beat copies a link.
- Add a title card first (it is the first calibration anchor) and a closing card last (the second). Chapter labels at scene starts add more anchors.
- Hotkeys must not fire while a field has focus; press them after a click on the page body.
- If you edit source files while a Vite dev server runs and the served page looks stale, restart the server.
- On Windows shells, heredocs with non-ASCII characters can break; write files with the editor tool.
- Do not end a browser-automation script with a navigation if you still need its return value.

## Verification checklist

- Video length equals the planned length (last line end plus the tail).
- Calibration reports at least two anchors and a slope near 1.0. Investigate a worst residual above 0.35 s.
- Sample frames at several beat starts and mid-beat; each shows the screen the line talks about.
- Measure speech onsets in the final audio (ffmpeg `silencedetect`) and compare with the placed times for several beats.
- Clip loudness is comparable across beats.
- A person has listened to it at least once. Record what the tooling could not verify (for example that no direction tag was spoken).

## Privacy and approvals

- Narration text leaves the machine for the voice service. Keep it to fictional or approved content and get the owner's approval first.
- Do not record real customer data, credentials or private records.
- Voice, claims and numbers in the video must match what the product actually does. Say "concept" or "draft" when it is one.

## Done evidence to record in the story

- The files: script, clips, recorder, output path.
- What was run: voice generation (characters sent), recording, calibration output, checks above.
- What was not verified, and the residual risk.
