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
preflight -> storyboard (beats) -> script -> voice clips -> record -> calibrate -> mux (+ bg music) -> verify
```

1. **Preflight.** Run the app, log in with the demo account, and confirm the demo account lands on the expected page — not an onboarding flow, a redirect, or an error. If seed data is missing (for example a practice field, a linking table, or demo records the journey needs), fix the seed before proceeding. This catches problems that would waste a full recording.
2. **Storyboard.** One table: beat id, scene, what happens on screen, what the narrator says. One idea per beat. Aim for 12 to 25 beats and 3 to 5 minutes. The storyboard must cover the product's primary happy path end-to-end — not just a tour of screens. If the product's core action is "submit", "send", "approve" or "create", that action must appear as a beat.
3. **Script approval.** The narration text is sent to the voice service. Get the owner's approval of the script before spending credits. This is a hard gate — it catches missing beats, wrong persona, flat narration and scope creep before anything costs money.
4. **Voice clips.** Generate one clip per beat. Cache by text, voice, model and settings so unchanged lines cost nothing on re-runs. Measure every clip's length. Apply an 80 ms fade-out to every clip after download to remove end-of-clip blips (ElevenLabs clips consistently end with a small artifact).
5. **Record.** Run the real app in headless Chromium. At the start of each beat, start its action and note the clock time. A beat lasts as long as its clip plus a short pause, or as long as its action if that is longer. Write actions to finish before the line does. Show the branded splash card as frame 1; log in behind it so the video never opens on a login screen.
6. **Calibrate.** Picture time is not the same as the clock. Find high-contrast moments in the recorded video (the dark title card, the dark closing card, chapter labels) whose clock times you noted, and fit picture time against clock time. The offset has been measured at 0.2 s on one run and 2.9 s on the next, so always calibrate; never assume.
7. **Mux.** Place each clip at its beat's calibrated time, mix, and write H.264 plus AAC. Trim the silent tail after the last line. If a background music track is provided, loop it with crossfade at the joins, mix at −20 dB below narration, and fade in over the first 2 s and out over the last 3 s.
8. **Verify.** See the checklist below.

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

A flat read is a defect, not a neutral default. The narration must have intonation: pace, pitch and feeling that move with the meaning of each line. Write every line as a small performance with an arc, not as text with one tag in front.

**Tools**
- Use `eleven_v3` for expressive delivery. It follows performance tags in square brackets and the punctuation of the text.
- Documented tags to prefer: `[calm]`, `[curious]`, `[excited]`, `[thoughtful]`, `[serious]`, `[whispers]`, `[sighs]`, `[short pause]`, `[long pause]`. Other plain-English tags (for example `[warm]`, `[softly]`, `[upbeat]`) usually work but can be read aloud; avoid them unless you can check by ear.
- v3 offers stability presets (0.0 creative, 0.5 natural, 1.0 robust). Use 0.25 to 0.3 with style 0.4 to 0.5 for narration. If a take sounds flat, lower stability before anything else. v3 does not support request stitching (`previous_text` and `next_text`); older models do.

**Rules for a performance, not a read**
1. **Give each line an arc.** A line longer than one sentence changes feeling at least once, at the point where its meaning changes: setup, then reveal, then consequence. Put a new tag at that point. Example: `[curious] Two analogues look threefold apart... [short pause] [serious] but the interval says otherwise.`
2. **Vary the openers.** No single tag opens more than about a third of the beats. Mostly `[calm]` and `[curious]` is a flat video with two flavours.
3. **Make the "so what" beat the strongest contrast.** Pause before it, drop to `[serious]` or `[thoughtful]`, short sentences, and one stressed word. Let the lines either side be quieter so it stands out.
4. **Stress with capitals.** One or two words per line in CAPITALS where a person would lean on them ("the interval includes NO difference"). Do not capitalise whole sentences.
5. **Direct with punctuation.** Ellipses for a trailing thought, a dash for a turn, a short sentence for impact, a question mark to lift the voice, an exclamation mark for a real release ("The flag clears!"). Use pause tags before reveals and after a line that needs to land.
6. **Match the feeling to the moment.** Curious when posing a question; serious when stating a risk or a limit; excited only for a genuine resolution; calm for orientation; thoughtful for trade-offs. Do not use excitement as a default positive.
7. **Open and close with intent.** The title line sets the promise; the closing line ends with a quiet, honest tone about what is still unknown.

**Text for the ear**
- Spell numbers and units as words ("five point four micromolar", "forty-five times", "pIC fifty"). Hyphenate ids so they are read cleanly ("A-seventeen").
- Short sentences. One idea per beat. Read it aloud before sending it.
- Expressive delivery runs longer than flat delivery because of the pauses. Re-record the picture at the new pace rather than squeezing audio to fit the old timings. If the actions were timed for older clips, scale their offsets by the ratio of the new clip length to the old one so each action still lands on its words.

**Checks**
- Before generating, read the script and mark where each line shifts. A line with no shift needs one, or needs to be a single short sentence.
- After generating, listen for variety: the opening, the reveal and the close should each sound different from a routine beat. Speech-to-text cannot judge this; a person must.
- Record in the story that tags were not verified as unspoken if the key has no speech-to-text permission.

## Brand colors

Do not hard-code colors. Before writing any card HTML, ripple, chapter label, or caption style, read the product's CSS — `globals.css`, CSS custom properties, or the marketing site's palette — and extract the brand colors. Write them as constants (or CSS variables on `:root`) so the entire demo uses the same palette. The tooling's defaults (`#0f766e` teal ripple, `#5eead4` accent) are placeholders; replace them.

Typical tokens to extract: accent, accent-light, background, foreground, muted, card, card-border. Map them to:

- **Ripple border and background:** accent, with 18 % opacity fill.
- **Chapter label bold text:** accent-light.
- **Card background:** background. Card heading `em` gradient: accent → accent-light. Card paragraph: muted.
- **Caption bold:** accent-light.

## Persona-driven narrative

The narration is a story, not a feature tour. Before writing the beats:

1. **Name a persona.** A role, a practice or company size, and a specific workload ("Lisa runs the front desk at a 3-clinician SLP practice, 25 patients, 6 payers").
2. **Set a moment.** A day, time and trigger ("Monday morning, opens the priority queue").
3. **Write from their point of view.** "Lisa has the full picture" — not "here you can see the full picture." Use their name once early, then "she" or "they."
4. **End on their outcome.** What changed for the persona, then a CTA.

A persona-driven narrative is dramatically more engaging than "this is the queue page, this is the patient page." It also forces the storyboard to cover the core workflow end-to-end, because the persona has a job to finish.

## Silent beats (splash cards)

A beat can have `text: null` in `script.mjs` to mark a silent beat — typically the opening splash and closing splash. Silent beats:

- Are skipped by voice generation (no API call, no clip).
- Use `SPLASH_DUR` (default 4.0 s) instead of clip duration for timing.
- Are excluded from the mux audio filter chain (only voiced beats get `adelay` and `amix` inputs).

The opening splash should be frame 1 of the video: show it before anything else, then log in behind it. This avoids dead time at the start.

## Background music

A soft instrumental track under the narration improves perceived quality. The muxer supports an optional background music file:

- **Source:** Download a royalty-free track (Pixabay, Uppbeat, etc.) — do not generate synthetic ambient. Prefer "soft corporate" or "gentle piano" styles for product demos.
- **Looping:** If the track is shorter than the video, crossfade-loop it with 2 s `acrossfade` at each join.
- **Mix level:** −18 dB to −20 dB below narration (narration stays at 0 dB).
- **Fades:** Fade in over the first 2 s, fade out over the last 3 s.
- **License:** Record the track name, author, source URL, and license in the demo plan.

## Authoring the actions

- Start from a clean state: clear storage once per run and apply any start state (for example a theme) through `start({ storage })`.
- Use real clicks through the helper so the cursor moves and a ripple shows.
- **Prefer text-based Playwright locators** (`page.getByText()`, `page.getByRole()`, `page.getByLabel()`) over CSS class selectors. Many apps use CSS-in-JS, inline styles, or generated class names that change between builds. Text locators are resilient. Fall back to `data-demo-*` attributes when text is ambiguous, and to CSS selectors only as a last resort.
- If the app scrolls inside a container, pass `scrollSelector`; scrolling the window does nothing.
- Grant clipboard permission (the helper does) if a beat copies a link.
- **Splash card as frame 1.** The T0 action should call `showCard()` immediately (before login or navigation), then log in behind the card. Record `cards.T0 = now()` and `starts.T0 = cards.T0` right after `showCard()`. This ensures the video opens on the branded card with no dead time.
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
- Clip loudness is comparable across beats. No end-of-clip blips (the fade-out should have removed them).
- If background music is present: it is audible but does not compete with narration; loop joins are not noticeable; fade-in and fade-out are smooth.
- A person has listened to it at least once and judged that the delivery has intonation (no flat read, a clear contrast at the "so what" beat). Record what the tooling could not verify (for example that no direction tag was spoken).

## Embedding the video

A self-hosted mp4 with a click-to-play overlay is the simplest and fastest embed for a marketing site or landing page. No YouTube or Vimeo dependency, no third-party tracking, no iframe.

Pattern (React / Next.js example):

```jsx
function DemoVideo() {
  const ref = useRef(null)
  const [playing, setPlaying] = useState(false)
  function toggle() {
    const v = ref.current
    if (!v) return
    v.paused ? (v.play(), setPlaying(true)) : (v.pause(), setPlaying(false))
  }
  return (
    <div onClick={toggle} className="relative cursor-pointer overflow-hidden rounded-2xl border">
      <video ref={ref} src="/demo.mp4" playsInline onEnded={() => setPlaying(false)} />
      {!playing && (
        <div className="absolute inset-0 flex items-center justify-center bg-black/40">
          <PlayIcon />
        </div>
      )}
    </div>
  )
}
```

Place the video in the hero section between the CTA and trust badges, or in a dedicated "See How It Works" section. Copy the mp4 to `public/demo.mp4`. Consider adding a poster frame (`poster="/demo-poster.jpg"`) extracted from the splash card for a preview before playback.

## Privacy and approvals

- Narration text leaves the machine for the voice service. Keep it to fictional or approved content and get the owner's approval first.
- Do not record real customer data, credentials or private records.
- Voice, claims and numbers in the video must match what the product actually does. Say "concept" or "draft" when it is one.

## Done evidence to record in the story

- The files: script, clips, recorder, output path.
- What was run: voice generation (characters sent), recording, calibration output, checks above.
- What was not verified, and the residual risk.
