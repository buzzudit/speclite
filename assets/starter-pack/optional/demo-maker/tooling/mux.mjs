// Demo Maker (Speclite). Calibrate recording time against the real video, then place each narration clip and write the mp4.
// Anchors: the title card, the closing card, and every chapter label (all high-contrast changes with known wall-clock times).
// Run on its own to re-mux an existing recording:  node tour/mux.mjs
import fs from 'node:fs'
import path from 'node:path'
import { spawnSync } from 'node:child_process'
import { beats, NAME, VERSION } from './script.mjs'
import { clipPath, duration } from './voice.mjs'

function frames(video, vf, limit) {
  const args = ['-hide_banner', ...(limit ? ['-t', String(limit)] : []), '-i', video, '-vf', vf + ',signalstats,metadata=print:file=-', '-an', '-f', 'null', '-']
  const r = spawnSync('ffmpeg', args, { encoding: 'utf8', maxBuffer: 1 << 29 })
  const out = []
  let t = null
  for (const ln of r.stdout.split(/\r?\n/)) {
    const m = ln.match(/pts_time:([\d.]+)/)
    if (m) t = parseFloat(m[1])
    const y = ln.match(/lavfi\.signalstats\.YAVG=([\d.]+)/)
    if (y && t !== null) out.push([t, parseFloat(y[1])])
  }
  return out
}
function risingEdges(series, dark, bright, after = 0) {
  const edges = []
  let state = 'bright'
  for (const [t, y] of series) {
    if (y >= bright) state = 'bright'
    else if (y < dark && state === 'bright') { state = 'dark'; if (t >= after) edges.push(t) }
  }
  return edges
}

export function mux(video, timings, name = `${NAME}-${VERSION}`) {
  const { starts, cards, chapters } = timings
  const full = frames(video, 'scale=160:-1')
  const cardEdges = risingEdges(full, 60, 120)
  if (cardEdges.length < 2) throw new Error(`Expected two dark-card edges, found ${cardEdges.length}`)
  const anchors = [
    { what: 'title card', wall: cards.T0, video: cardEdges[0] },
    { what: 'closing card', wall: cards.E1, video: cardEdges[cardEdges.length - 1] },
  ]
  // first estimate from the two cards, then refine with the chapter labels
  const a0 = (anchors[1].video - anchors[0].video) / (anchors[1].wall - anchors[0].wall)
  const b0 = anchors[0].video - a0 * anchors[0].wall
  const pill = frames(video, 'crop=150:24:40:664')
  const pillEdges = risingEdges(pill, 110, 170)
  for (const [num, wall] of Object.entries(chapters)) {
    if (num === '1') continue // sits on top of the title card; no contrast to detect
    const expect = a0 * wall + b0
    const hit = pillEdges.filter((t) => Math.abs(t - expect) < 6).sort((x, y) => Math.abs(x - expect) - Math.abs(y - expect))[0]
    if (hit !== undefined) anchors.push({ what: `chapter ${num}`, wall, video: hit - 0.12 }) // label fades in over ~0.25s; compensate to its start
  }
  const n = anchors.length
  const mx = anchors.reduce((s, p) => s + p.wall, 0) / n
  const my = anchors.reduce((s, p) => s + p.video, 0) / n
  const a = anchors.reduce((s, p) => s + (p.wall - mx) * (p.video - my), 0) / anchors.reduce((s, p) => s + (p.wall - mx) ** 2, 0)
  const b = my - a * mx
  const resid = anchors.map((p) => p.video - (a * p.wall + b))
  console.log(`calibration: ${n} anchors, video = ${a.toFixed(4)} x wall + ${b.toFixed(2)}; residuals (s): ${resid.map((r) => r.toFixed(2)).join(' ')}`)
  const worst = Math.max(...resid.map(Math.abs))
  if (worst > 0.35) console.warn(`WARNING: worst anchor residual ${worst.toFixed(2)}s`)

  const lastClip = duration(clipPath(beats[beats.length - 1]))
  const total = Math.max(0, a * starts.E1 + b) + lastClip + 2.5
  const out = path.resolve('tour/out', `${name}.mp4`)
  const inputs = ['-i', video]
  const filters = []
  const placed = {}
  beats.forEach((bt, i) => {
    inputs.push('-i', clipPath(bt))
    const at = Math.max(0, a * starts[bt.id] + b)
    placed[bt.id] = at
    const ms = Math.round(at * 1000)
    filters.push(`[${i + 1}:a]adelay=${ms}|${ms}[a${i}]`)
  })
  const mix = beats.map((_, i) => `[a${i}]`).join('') + `amix=inputs=${beats.length}:dropout_transition=0:normalize=0[a]`
  const m = spawnSync('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-y', ...inputs,
    '-filter_complex', filters.join(';') + ';' + mix,
    '-map', '0:v', '-map', '[a]', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-preset', 'medium',
    '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', '-t', total.toFixed(2), out], { encoding: 'utf8', maxBuffer: 1 << 28 })
  if (m.status !== 0) throw new Error('ffmpeg mux failed: ' + m.stderr)
  fs.writeFileSync(`tour/out/placed-${VERSION}.json`, JSON.stringify(placed, null, 2))
  const lastEnd = placed.E1 + duration(clipPath(beats[beats.length - 1]))
  console.log(`mp4: ${out}  length ${duration(out).toFixed(1)}s; last line ends at ${lastEnd.toFixed(1)}s`)
  return out
}

if (import.meta.url === `file:///${process.argv[1].replace(/\\/g, '/')}`) {
  const timings = JSON.parse(fs.readFileSync(`tour/out/timings-${VERSION}.json`, 'utf8'))
  mux(path.resolve(`tour/out/${NAME}-${VERSION}.webm`), timings)
}
