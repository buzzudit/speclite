// Narration for the demo, one line per beat. Copy to tour/script.mjs and edit.
// Written for ElevenLabs v3 (`eleven_v3`): square-bracket tags direct the performance and are not spoken.
// Punctuation is direction too: ellipses and dashes make pauses, a question mark lifts the voice, CAPITALS add stress.
// Safe, documented tags: [calm] [curious] [excited] [thoughtful] [serious] [whispers] [sighs] [short pause] [long pause].
// Other plain-English tags usually work but are not guaranteed; check by ear (or by speech-to-text if your key allows it).
export const NAME = '{{DEMO_NAME}}' // output file stem, for example "acme-walkthrough"
export const VERSION = 'v1' // bump when the narration changes; clips and outputs are versioned by it
export const VOICE_ID = '{{VOICE_ID}}'
export const MODEL_ID = 'eleven_v3'
// v3 offers stability presets: 0.0 creative, 0.5 natural, 1.0 robust. Lower is more expressive and less predictable.
export const VOICE_SETTINGS = { stability: 0.3, similarity_boost: 0.75, style: 0.4, use_speaker_boost: true }

// Ids are used by walkthrough.mjs. Keep each line to one idea; the action for the beat starts when the line starts.
export const beats = [
  { id: 'T0', text: "[calm] {{Title card line: what this is, who it is for, what you will show.}}" },
  { id: 'P1', text: "[curious] {{Meet the persona and the moment that starts the job.}}" },
  { id: 'P2', text: "[thoughtful] {{The pain today... and the one thing the product changes.}}" },
  // ... one beat per action in the storyboard ...
  { id: 'E1', text: "[warm] {{Closing: what the concept is, and what is still unproven.}}" },
]
