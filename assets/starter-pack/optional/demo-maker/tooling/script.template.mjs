// Narration for the demo, one line per beat. Copy to tour/script.mjs and edit.
// Written for ElevenLabs v3 (`eleven_v3`): square-bracket tags direct the performance and are not spoken.
// Punctuation is direction too: ellipses and dashes make pauses, a question mark lifts the voice, CAPITALS add stress.
// Safe, documented tags: [calm] [curious] [excited] [thoughtful] [serious] [whispers] [sighs] [short pause] [long pause].
// Other plain-English tags (for example [warm] or [softly]) usually work but can be read aloud; avoid them unless you can check by ear.
// A flat read is a defect. Give every multi-sentence line an arc: a new tag where the meaning changes, CAPITALS on one or two stressed words,
// a pause before a reveal, and a different opening tag from the beat before it. See planning/demo-maker-workflows.md, "Voice direction".
export const NAME = '{{DEMO_NAME}}' // output file stem, for example "acme-walkthrough"
export const VERSION = 'v1' // bump when the narration changes; clips and outputs are versioned by it
export const VOICE_ID = '{{VOICE_ID}}'
export const MODEL_ID = 'eleven_v3'
// v3 offers stability presets: 0.0 creative, 0.5 natural, 1.0 robust. Lower is more expressive and less predictable.
export const VOICE_SETTINGS = { stability: 0.3, similarity_boost: 0.75, style: 0.4, use_speaker_boost: true }

// Ids are used by walkthrough.mjs. Keep each line to one idea; the action for the beat starts when the line starts.
export const beats = [
  { id: 'T0', text: "[calm] {{Title line: what this is, and who it is for.}} [short pause] [curious] {{What you will show... and the questions that are STILL open.}}" },
  { id: 'P1', text: "[curious] {{Meet the persona.}} [short pause] [thoughtful] {{The moment that starts the job...}} [serious] {{and the decision they have to make.}}" },
  { id: 'P2', text: "[thoughtful] {{The pain today.}} [short pause] [curious] {{The question the product asks FIRST?}} [calm] {{The one thing it changes.}}" },
  // ... one beat per action in the storyboard; make the "so what" beat the strongest contrast ...
  // { id: 'S2', text: "[serious] {{The moment that matters.}} [short pause] [thoughtful] {{Why it matters, in short sentences.}} [excited] {{The release!}} [calm] {{What it means in practice.}}" },
  { id: 'E1', text: "[calm] {{Closing: what the concept is.}} [long pause] [thoughtful] {{What we do not know yet...}} [curious] {{The open questions, one clause each...}} [calm] {{What happens next.}}" },
]
