// Demo Maker (Speclite). Generate one ElevenLabs clip per beat. Clips are cached by text, voice and settings, so unchanged lines cost nothing.
import fs from 'node:fs'
import path from 'node:path'
import crypto from 'node:crypto'
import { spawnSync } from 'node:child_process'
import { beats, MODEL_ID, VOICE_ID, VOICE_SETTINGS } from './script.mjs'

const dir = path.resolve('tour/audio')
fs.mkdirSync(dir, { recursive: true })

function readKey() {
  if (process.env.ELEVENLABS_API_KEY) return process.env.ELEVENLABS_API_KEY.trim()
  if (process.env.elevenlabs_key) return process.env.elevenlabs_key.trim()
  try {
    for (const line of fs.readFileSync('.env', 'utf8').split(/\r?\n/)) {
      const m = line.match(/^\s*(elevenlabs_key|ELEVENLABS_API_KEY)\s*=\s*(.*)\s*$/i)
      if (m) return m[2].replace(/^["']|["']$/g, '').trim()
    }
  } catch { /* no .env */ }
  return null
}

export function duration(file) {
  const r = spawnSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', file], { encoding: 'utf8' })
  return parseFloat(r.stdout)
}

export function clipPath(beat) {
  const h = crypto.createHash('sha1').update(JSON.stringify([beat.text, VOICE_ID, MODEL_ID, VOICE_SETTINGS])).digest('hex').slice(0, 8)
  return path.join(dir, `${beat.id}-${h}.mp3`)
}

export async function generate() {
  const key = readKey()
  let spent = 0
  for (let i = 0; i < beats.length; i++) {
    const b = beats[i]
    if (process.env.ONLY && !process.env.ONLY.split(',').includes(b.id)) continue
    const file = clipPath(b)
    if (fs.existsSync(file)) { console.log(`cached  ${b.id}`); continue }
    if (!key) throw new Error('No ElevenLabs key found (.env elevenlabs_key or ELEVENLABS_API_KEY).')
    const res = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${VOICE_ID}?output_format=mp3_44100_128`, {
      method: 'POST',
      headers: { 'xi-api-key': key, 'Content-Type': 'application/json', Accept: 'audio/mpeg' },
      body: JSON.stringify({
        text: b.text,
        model_id: MODEL_ID,
        voice_settings: VOICE_SETTINGS,
        // request stitching is not available on eleven_v3
        ...(MODEL_ID === 'eleven_v3' ? {} : { previous_text: beats[i - 1]?.text, next_text: beats[i + 1]?.text }),
      }),
    })
    if (!res.ok) {
      const body = (await res.text()).slice(0, 300)
      throw new Error(`ElevenLabs ${res.status} on beat ${b.id}: ${body}`)
    }
    fs.writeFileSync(file, Buffer.from(await res.arrayBuffer()))
    spent += b.text.length
    console.log(`made    ${b.id}  ${duration(file).toFixed(2)}s`)
  }
  console.log(`characters sent this run: ${spent}`)
}

if (import.meta.url === `file:///${process.argv[1].replace(/\\/g, '/')}`) await generate()
