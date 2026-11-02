# Phase 3: Design Brief Generator

> Convert the user's interview answers into a structured design specification.
> Present a plain-text summary for user approval before building.
> Never write code without the user explicitly approving the design brief.

---

## Answer-to-Design Mapping

| Answer Category | Design Output |
|---|---|
| `relationship_stage` → | Tone calibration (playful/warm/romantic/deep), CTA directness level |
| `personality_words` → | Animation style (bouncy/gentle/mysterious/calm), text entrance type, particle effects |
| `shared_memory_abstract` → | Scene 2 visual theme (abstracted), color temperature bias |
| `color_preference` → | Primary color palette (warm/cool/pastel/bold) |
| `song_choice` → | Audio track, tempo-driven scene pacing, beat-sync transition points |
| `core_message` → | Scene 3 climax text (paraphrased for copyright/safety) |
| `privacy_level` → | Privacy settings (noindex, password protection, obfuscated URL) |
| `final_feeling` → | Scene 5 outro tone, CTA wording, animation exit style |
| `signature_type` → | Signature placement in Scene 5 (or none if anonymous) |

---

## JSON Design Brief Schema

Generate this JSON object from the user's answers. This is your internal specification — do NOT show raw JSON to the user. Show the plain-text summary instead.

```json
{
  "version": "1.0",
  "relationship_stage": "best_friends | crush | early_dating | committed",
  "tone": "playful | warm | romantic | deep",
  "personality_words": ["word1", "word2", "word3"],
  "color_palette": {
    "primary": "#hex",
    "background": "#hex",
    "accent": "#hex",
    "text": "#hex"
  },
  "typography": {
    "display_font": "Font Name",
    "display_font_url": "https://fonts.googleapis.com/css2?family=...",
    "body_font": "Font Name",
    "body_font_url": "https://fonts.googleapis.com/css2?family=..."
  },
  "animation_style": {
    "text_entrance": "bounce_fade | gentle_fade_up | typewriter | fade_scale",
    "layer_motion": "fast_elastic | slow_parallax | horizontal_drift | minimal_precise",
    "particle_style": "bubbles_sparkles | bokeh_orbs | drifting_stars | geometric_shapes"
  },
  "shared_memory_abstract": "A warm abstraction of the user's memory",
  "song_choice": {
    "user_input": "What the user said",
    "resolved_track": "Actual track to use (royalty-free alternative if needed)",
    "tempo_bpm": 80,
    "mood": "calm | nostalgic | epic | playful"
  },
  "core_message": "The user's message, paraphrased for safety",
  "privacy_level": "very_private | somewhat_private",
  "final_feeling": "warm_appreciated | happy_smiling | hopeful_curious | surprised_touched",
  "signature": {
    "type": "name | initial | anonymous | nickname",
    "value": "The name/initial/nickname or null"
  },
  "scene_count": 5,
  "total_duration_estimate": "2-4 minutes",
  "scenes": [
    {
      "number": 1,
      "name": "The First Glance",
      "text_line_1": "...",
      "text_line_2": "...",
      "visual_direction": "...",
      "motion_direction": "...",
      "duration_seconds": 30
    }
  ]
}
```

---

## Color Palette Selection

Read from `resources/color-palettes.json` and select based on `color_preference`:

| User Preference | Primary | Background | Accent | Text |
|---|---|---|---|---|
| **Warm sunset** | `#DEA193` (rose gold) | `#0F0F1A` (midnight) | `#C9A96E` (gold dust) | `#FDFBD4` (cream) |
| **Cool midnight** | `#069494` (teal glow) | `#0A0A1A` (deep navy) | `#8A9A5B` (moss) | `#E8E6D9` (soft white) |
| **Soft pastel** | `#D4A5A5` (dusty rose) | `#1A1A2E` (soft midnight) | `#B8C5D6` (soft blue) | `#F5F0E8` (warm white) |
| **Bold and bright** | `#E07A5F` (terracotta) | `#1D1D2E` (charcoal) | `#F2CC8F` (honey) | `#FFF8E7` (ivory) |

**Colors to ALWAYS AVOID:**
- Hot pink, bright red — "aggressive romance" or "Valentine's commercial"
- Lime green, bright orange, electric blue, neon yellow — cheap/digital feel
- Pure white `#FFFFFF` backgrounds — feels like a billboard, not a whisper
- Pure black `#000000` backgrounds — feels void, not intimate

---

## Typography Pairing Selection

Read from `resources/font-pairings.json` and select based on `personality_words`:

| Personality Match | Display Font | Body Font | Feeling |
|---|---|---|---|
| Funny, bubbly, playful | "Dancing Script" (handwritten) | "Inter" (clean sans) | Playful, personal |
| Kind, warm, gentle | "Great Vibes" (elegant script) | "Lora" (soft serif) | Gentle, intimate |
| Mysterious, deep, quiet | "Cinzel" (dramatic serif) | "Source Sans 3" (neutral) | Cinematic, poetic |
| Smart, calm, thoughtful | "Playfair Display" (editorial serif) | "Open Sans" (friendly sans) | Sophisticated, thoughtful |

**Font rules:**
- Always load from Google Fonts with `display=swap`
- Use `wght@300;400;600` (light, regular, semibold) — no more
- Prefer variable fonts when available for smaller payload
- Subset if text is static: `&text=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789`

---

## Animation Style Selection

Select based on `personality_words` and `tone`:

| Personality Match | Text Entrance | Layer Motion | Particle Style |
|---|---|---|---|
| Funny, bubbly, playful | Bounce in + fade | Fast drift, elastic easing | Floating bubbles, sparkles |
| Kind, warm, gentle | Gentle fade up from below | Slow parallax, smooth | Soft bokeh, glowing orbs |
| Mysterious, deep, quiet | Typewriter character reveal | Horizontal drift, subtle | Drifting stars, mist wisps |
| Smart, calm, thoughtful | Fade + slight scale up | Minimal, precise motion | Clean geometric shapes |

**Easing rules by tone:**
- Playful → `elastic.out(1, 0.3)` or `back.out(1.7)`
- Warm → `power2.inOut`
- Romantic → `power3.inOut`
- Deep → `power4.inOut` or `expo.inOut`

---

## Scene Content Generation

For each of the 5 scenes, generate:
- `text_line_1` — max 15 words, poetic not prose
- `text_line_2` — max 15 words, optional (some scenes work with 1 line)
- `visual_direction` — 1-sentence visual instruction for CSS/SVG
- `motion_direction` — 1-sentence animation instruction for GSAP

### Content Rules:
- **No copyrighted lyrics** — paraphrase emotional themes only
- **No real names** — use nicknames, initials, "you", or abstract references
- **No private details** — abstract shared memories
- **Max 2 lines per scene** — poetry, not paragraphs
- **One focal visual element per scene** — prevents cognitive overload
- **Progressive emotional arc** — build from gentle to peak to resolution

### Scene Arc Template:

| Scene | Narrative Role | Emotional Weight | Text Style |
|---|---|---|---|
| 1 — Intro | Setting the mood | Light, curious | Invitational, dreamy |
| 2 — Verse | Context building | Moderate, nostalgic | Observational, warm |
| 3 — Chorus | Emotional peak | Heavy, vulnerable | Direct, heartfelt |
| 4 — Bridge | Perspective shift | Reflective, quiet | Philosophical, calm |
| 5 — Outro | Resolution | Gentle, hopeful | Grateful, no-pressure CTA |

---

## Plain-Text Summary Template

After generating the JSON design brief internally, present this to the user:

```
"Here's what we're building:

🎨 Mood: [tone] with [color_preference] colors
✍️ Fonts: [display_font] for headings, [body_font] for text
🌙 Background: Dark [background color name] — intimate, like a late-night conversation
✨ Animations: [text_entrance description] text, [particle_style description] floating in the background
🎵 Music: [song_choice summary]
📖 Story: 5 scenes, starting gently, building to '[core_message summary]', ending with [final_feeling]
🔒 Privacy: [privacy_level description]
✒️ Signed: [signature description]

Total scroll time: about 2–3 minutes.

Sound right? I can change any of this before I start building."
```

**Wait for explicit user approval before proceeding to Phase 4.**

---

## Handling Design Brief Revisions

If the user wants changes:
- "Can we change the colors?" → Show the 4 palette options again
- "Can we change what it says?" → Re-ask Question 7 only
- "I want to add more scenes" → "5 scenes is the sweet spot — it keeps the story tight and prevents scrolling fatigue. But I can make each scene richer if you want."
- "Can we use a different font?" → Show the 4 typography options again
- "I changed my mind about the song" → Re-ask Question 6 only

After revisions, regenerate the summary and ask for approval again.
