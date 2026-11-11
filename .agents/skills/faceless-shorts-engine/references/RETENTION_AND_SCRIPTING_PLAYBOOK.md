# Short-Form Video Retention & Scripting Playbook

Operational rules, hook templates, and algorithmic pacing formulas for vertical video production across YouTube Shorts, TikTok, and Instagram Reels.

---

## 1. The 4 Non-Negotiable Retention Invariants

### 1. In Medias Res Hook (0.00s – 2.00s)
- **Rule**: Ban conversational preambles (*"Hey guys"*, *"Today we are looking at"*, *"Did you know that"*).
- **Execution**: The first spoken sentence must deliver the anomaly, contradiction, or core premise immediately.
- **Visual Sync**: The primary visual subject and the first kinetic title card must appear on frame 1.

### 2. The 2-Second Visual Reset
- **Rule**: No camera perspective, visual plane, or static graphic may persist unchanged for longer than 2.0 seconds.
- **Execution**:
  - Seconds 0–2: Wide establishing shot + kinetic title card.
  - Seconds 2–4: Extreme macro snap zoom onto character expression or key object.
  - Seconds 4–6: Cutaway schematic or secondary split-screen graphic.
  - Seconds 6–8: Directional pan with synchronous whoosh sound effect.

### 3. Algorithmic Loop Chaining
- **Rule**: The closing sentence of the script must grammatically and tonally complete the opening sentence of the video.
- **Example**:
  - *Opening sentence*: "...he discovered the weirdest legal loophole in history."
  - *Body content*: Explains the story, the bank purchase, and the court verdict.
  - *Closing sentence*: "And that is how..."
  - *Resulting Loop*: "And that is how... he discovered the weirdest legal loophole in history."

### 4. Word Density & Delivery Speed
- **Optimal Speed**: 150 to 165 spoken words per minute.
- **Length Targets**:
  - 30-second short: Exactly 75–82 words.
  - 45-second short: Exactly 112–122 words.
  - 58-second short: Exactly 145–158 words (do not exceed 59 seconds to maintain Shorts indexing).

---

## 2. 10 Field-Tested Hook Archetypes

1. **The Anomaly Hook**: "In 1999, a customer bought an entire bank for one dollar."
2. **The Biological Threat Hook**: "If you swallow chewing gum, your stomach acids trigger an unexpected defensive reaction."
3. **The Legal Loophole Hook**: "There is an airline loophole that legally gives you unlimited first-class tickets."
4. **The Scenario Dilemma Hook**: "You have ten seconds to choose between the frozen bunker and the submerged submarine."
5. **The Classified Archive Hook**: "In 1962, a passenger locomotive entered a Swiss tunnel and never came out."
6. **The Inverse Truth Hook**: "Drinking cold water when you are heat-exhausted can actually trigger rapid organ shock."
7. **The Financial Glitch Hook**: "A student discovered an ATM coding glitch that printed 1.6 million dollars in cash."
8. **The Medical Incident Hook**: "A researcher was bitten by a bullet ant, and within three minutes his nervous system did this."
9. **The Clean Heist Hook**: "Two guards walked out of a vault with twenty million dollars in gold without touching an alarm."
10. **The Engineering Threshold Hook**: "If a submarine descends past eight hundred meters, this is the sound the steel hull makes."

---

## 3. Synchronous Foley & Sound Event Cue Sheet

Align sound effects strictly to word timestamp markers:

| Sound Event | Recommended Audio File | Trigger Timing & Context |
|---|---|---|
| **Punchy Pop** | `sfx_pop.wav` | On every character expression swap, text badge reveal, or prop appearance. |
| **Air Whoosh** | `sfx_whoosh.wav` | On every camera snap zoom, perspective shift, or wipe transition. |
| **Counter Ding** | `sfx_ding.wav` | On dollar figure displays, positive loopholes, or successful choices. |
| **Heavy Thud** | `sfx_impact.wav` | On danger moments, organ cutaways, or sudden plot revelations. |
| **Sub Bass Drop** | `sfx_sub_drop.wav` | On the primary hook punchline (0.5s–1.2s into the video). |

---

## 4. Phone Voice Memo Ingestion Protocol

When users provide their own voice recording instead of Kokoro TTS:
1. **Audio Normalization**: Convert source audio (`.m4a`, `.aac`, `.ogg`, `.mp3`) to 24kHz mono WAV.
2. **Dynamic Range Compression & De-noise**: Apply high-pass filter at 80Hz and normalize integrated loudness to −16 LUFS.
3. **Timestamp Alignment**: Feed the normalized WAV into Whisper to generate `captions_word_level.json`.
4. **Scene Timing Calibration**: Adjust visual scene durations to match the natural speech cadences of the human recording.
