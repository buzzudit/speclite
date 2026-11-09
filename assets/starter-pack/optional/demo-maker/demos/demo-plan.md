# {{PROJECT_NAME}} Demo Plan

Status: draft
Story: `{{STORY_ID}}`
Last Updated: {{DATE}}

## Demo Summary

- Product and build: {{PRODUCT}}, run with {{RUN_COMMAND}} at {{URL}}
- Audience and purpose: {{AUDIENCE}}
- Length target: {{MINUTES}} minutes, about {{BEATS}} beats
- Format: 1280 x 720 mp4 (H.264 and AAC)

## Journey

Persona: {{NAME, role, team size}}
Trigger (the moment that starts the job): {{TRIGGER}}

| # | Step | Screen | Feeling |
|---|---|---|---|
| 1 | | | |

The strongest moment ("so what"): {{WHICH STEP AND WHY}}

Product readiness: the journey is built into the screens (guided path, one next action per screen). Yes / No. If no, fix the product first.

## Voice

- Service and model: ElevenLabs `eleven_v3`
- Voice ID: {{VOICE_ID}}
- Settings: stability {{0.3}}, similarity 0.75, style 0.4
- Key location: git-ignored `.env` as `ELEVENLABS_API_KEY` (never committed, never printed)
- Approximate characters: {{N}} (credits on first run; none for unchanged lines)

## Beats

Numbers and units are written as words. Tags are directions and are not spoken.

| Id | Scene | On screen | Narration (with direction tags) |
|---|---|---|---|
| T0 | Title card | Dark card with the product name | |
| P1 | 1. | | |
| E1 | Close | Dark card with what is still unproven | |

## Start State And Data

- How the demo resets to a clean state:
- Fictional data used and where it lives:
- Selectors used (prefer `data-demo-*`):

## Sync Plan

- Anchors: title card, closing card, chapter labels.
- Expected slope near 1.0; investigate a worst residual above 0.35 s.
- Tail after the last line: about 2.5 s.

## Acceptance Criteria

- [ ] Script approved by the owner before voice generation
- [ ] Voice clips generated, one per beat, cached
- [ ] Recorder runs the whole workflow from a clean state in one command
- [ ] mp4 written with each clip at its beat's calibrated time
- [ ] Sync verified: length, calibration residuals, frames at beat starts, audio onsets
- [ ] Listened to once by a person; unverified items recorded
- [ ] Video delivered; re-recording is one command

## Test Plan

- Level: 2 (smoke plus manual confirmation)
- Checks run and results:
- Not verified and residual risk:
