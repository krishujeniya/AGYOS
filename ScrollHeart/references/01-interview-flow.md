# Phase 1: Interview Flow

> Ask one question at a time. Validate each answer emotionally before asking the next.
> Never bombard the user with multiple questions. Offer defaults for uncertain users.
> Use simple English — no design jargon.

---

## Interview Philosophy

- **Progressive disclosure:** Easy questions first, deeper ones later
- **Emotional validation:** Acknowledge the user's vulnerability between questions
- **Default suggestions:** Always offer an "easy out" to reduce decision paralysis
- **No jargon:** "Does she like sunset or midnight?" not "What's your hex code?"
- **Conversational bridging:** "That sounds beautiful. What kind of colors does she usually wear?"

---

## The 10 Questions

### Question 1 — The Hook (Warm-up)

**Ask:**
> "Hey! So there's someone special you want to make something for? I'm here to help you build her a little story she can scroll through. No pressure — we can take this one step at a time. Ready?"

**Expected input:** Yes/Ready confirmation
**Validation:** None needed — just acknowledge warmth
**Bridge to next:** "Awesome! Let's start with the easy stuff."

---

### Question 2 — Relationship Stage

**Ask:**
> "How would you describe where you two are right now? Are you best friends? Crushing? Early dating? Or something else entirely? This helps me calibrate the tone so it feels right."

**Options:**
- Best Friends
- Crush (figuring it out)
- Early Dating
- Committed
- Other (free text)

**Expected input:** One of the options above
**Validation:** "That's a really sweet stage. I'll make sure the tone matches where you are."
**Why this matters:** Drives tone calibration, CTA pressure level, and scene intensity
**Store as:** `relationship_stage`

---

### Question 3 — Her Personality

**Ask:**
> "If you had to describe her in three words, what would they be? Like 'funny, kind, mysterious' or 'bubbly, smart, calm' — whatever feels true."

**Expected input:** Free text, 3 words max
**Validation:** "I love that. I can already picture the vibe."
**Default if stuck:** "Most people say something like 'kind, funny, warm' — does that sound close?"
**Why this matters:** Drives typography pairing, animation style, and particle effects
**Store as:** `personality_words` (array of 3 strings)

---

### Question 4 — A Shared Memory

**Ask:**
> "What's one moment with her that still makes you smile? It can be small — a conversation, a walk, something she said. Don't worry, I won't use the exact details unless you say it's okay."

**Expected input:** Free text (1–3 sentences)
**Validation:** "That's a beautiful memory. I'll weave the feeling of that into the design — not the details, just the warmth of it."
**Privacy note:** ALWAYS abstract this. Never use specific names, places, or direct quotes unless the user explicitly says "use this exactly."
**Default if stuck:** "Even something as simple as 'we were just talking and everything felt easy' is perfect."
**Why this matters:** Drives Scene 2 visual theme and color temperature
**Store as:** `shared_memory` (string), `shared_memory_abstract` (agent-generated abstraction)

---

### Question 5 — Favorite Color / Mood

**Ask:**
> "Does she lean more toward warm colors (sunset, gold, rose) or cool colors (midnight, teal, starlight)? Or maybe something else entirely?"

**Options:**
- Warm sunset (golds, roses, amber)
- Cool midnight (teals, navy, silver)
- Soft pastel (dusty rose, lavender, light blue)
- Bold and bright (terracotta, honey, coral)
- I'm not sure

**Expected input:** One of the options above
**Validation:** "Great choice. That's going to set a beautiful mood."
**Default if "I'm not sure":** "No worries! I'll go with a warm sunset palette — it works for almost everything. We can always change it later."
**Why this matters:** Drives the entire color palette selection
**Store as:** `color_preference`

---

### Question 6 — A Song or Sound

**Ask:**
> "Is there a song that reminds you of her? Or a type of music she loves? If you don't have one, I can suggest something that fits the mood."

**Expected input:** Free text (song name, artist, or genre)
**Validation:** "That's a perfect choice. I'll try to match the pacing of the story to the feeling of that song."
**Default if stuck:** "Many people use a soft instrumental or acoustic track. Want me to suggest something calm and dreamy?"
**Copyright warning:** If the user names a specific copyrighted song, note: "I love that song too! I can't embed it directly (copyright), but I can structure the story's pacing to match its emotional arc. For the background audio, I'll suggest a royalty-free track with a similar vibe."
**Why this matters:** Drives audio track selection, scene pacing, and beat-sync transitions
**Store as:** `song_choice`

---

### Question 7 — What You Want to Say

**Ask:**
> "If you could tell her one thing — and you knew she'd really hear it — what would it be? Don't overthink it. Even 'I'm glad I met you' is perfect."

**Expected input:** Free text, max 2 sentences
**Validation:** "That's honestly beautiful. She's going to feel that."
**Default if stuck:** "Something like 'You make everything better just by being you' — simple and real."
**Why this matters:** Becomes the Scene 3 (climax) centerpiece text, paraphrased for safety
**Store as:** `core_message`

---

### Question 8 — Her Comfort Level

**Ask:**
> "How public or private should this feel? Some people love grand gestures, others prefer something quiet and personal."

**Options:**
- Very private (just her — she's the only one who sees it)
- Somewhat private (close friends might see it too, and that's okay)
- I'm not sure

**Expected input:** One of the options above
**Validation:** "Got it. I'll make sure it feels just right for that level of privacy."
**Default if "I'm not sure":** "Let's keep it very private — you can always share it more widely later. Private feels more special anyway."
**Why this matters:** Drives privacy settings (noindex, password protection, obfuscated URL)
**Store as:** `privacy_level`

---

### Question 9 — The Final Moment

**Ask:**
> "How do you want her to feel when she reaches the end? Happy? Warm? Surprised? Hopeful?"

**Options:**
- Warm and appreciated
- Happy and smiling
- Hopeful and curious
- Surprised and touched

**Expected input:** One of the options above
**Validation:** "That's the perfect way to end a story like this."
**Default if stuck:** "Most people go with 'warm and appreciated' — it's genuine without being too much."
**Why this matters:** Drives Scene 5 outro tone, CTA wording, and animation exit style
**Store as:** `final_feeling`

---

### Question 10 — Your Name (Optional)

**Ask:**
> "Last one! Do you want your name on it? Or would you rather keep it anonymous? Both are totally fine."

**Options:**
- My first name
- Just my initial
- Anonymous (no name at all)
- A nickname she calls me (specify)

**Expected input:** One of the options above, with optional free text for nickname
**Validation:** "Perfect. That's a nice touch."
**Default if stuck:** "Going anonymous is actually really romantic — like a secret admirer. Want to try that?"
**Why this matters:** Drives signature placement in Scene 5
**Store as:** `signature_type`, `signature_value` (if applicable)

---

## After All 10 Questions

Once all questions are answered, summarize what you learned:

> "Okay, here's what I know about her: [brief summary]. Now let me run a quick check to make sure everything feels right before I start building."

Then proceed to **Phase 2: Safety Check** by loading `references/02-safety-checklist.md`.

---

## Handling Edge Cases

### User wants to skip a question
> "That's totally fine. I'll use a gentle default for that one. You can always change it later."

### User gives very long answers
Acknowledge, then distill: "I love all of that. Let me capture the essence — [your 1-sentence abstraction]. Sound right?"

### User gets emotional
Validate first, always: "Hey, that's a really beautiful thing to feel. There's nothing wrong with wanting to express it."

### User wants to restart
> "No problem at all. Let's start fresh. Sometimes the second time through feels more natural."

### User asks for technical details
Deflect gently: "I'll handle all the technical stuff — you just focus on the story. Think of me as your creative partner."
