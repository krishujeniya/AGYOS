# Anti-Slop Engineering & Writing Law

Merged and deduplicated from five foundational anti-slop skills:
`blader/humanizer`, `theclaymethod/unslop`, `Nutlope/hallmark`, `conorbronsdon/avoid-ai-writing`, and `hardikpandya/stop-slop`.

## 1. Scope & Jurisdiction
This law governs every string produced for web interfaces, UI components, section copy, capability descriptions, workflow cards, showcase captions, FAQ entries, dialogs, tooltips, code comments, and technical reports.

---

## 2. Voice Law (Authorial Stance)

1. **Lead with the Point**: State the core message immediately. Eliminate throat-clearing, preambles, and conversational warm-ups.
2. **Trust the Reader**: State each fact once. Eliminate over-explaining, "in other words", didactic restatements, and patronizing simplifications.
3. **Take a Specific Stance**: A concrete technical viewpoint outperforms false neutrality or balanced-to-a-fault hedging. Address the reader directly as "you"; avoid detached third-person narration ("users", "one might find").
4. **Concrete Verbs over Abstract Concepts**:
   - Use physical, imaginable actions: *build, cut, measure, send, write, ship, test, verify*.
   - Ban abstract Latinate verbs: *leverage, utilize, facilitate, implement, optimize, navigate, unpack, foster, elevate*.
   - Use active voice with clear human agency. Ban false inanimate agency (*"the dashboard empowers"*, *"the metrics tell a story"*, *"the code speaks for itself"*).
5. **Plain over Impressive**: Prefer *is* and *has* over copula-avoiding flourishes (*serves as*, *features*, *boasts*, *showcases*). If a sentence resembles an advertising tagline or pull-quote, rewrite it plainly.
6. **Information Density over Filler**: Every word must carry distinct meaning. If a phrase can be deleted without altering the factual content, delete it immediately.

---

## 3. Hard Banned Constructions

The following constructions are prohibited in all interface strings, copy, and documentation:

### Negative Parallelism & Binary Contrasts
- Prohibited: *"It's not just X, it's Y"*, *"Not only... but also"*, *"No prior. No nostalgia."*
- Rule: State the positive claim directly. Genuine factual corrections (e.g. *"Use pnpm, not npm."*) remain valid.

### Throat-Clearing & Staged Run-Ups
- Prohibited: *"Here's the thing:"*, *"Let me be clear"*, *"It turns out"*, *"Let's dive in"*, *"Let's unpack"*, *"In today's fast-paced world..."*, *"Honestly?"*, *"Let me explain"*

### Artificial Emphasis Crutches
- Prohibited: *"Full stop."*, *"Let that sink in."*, *"Read that again."*, *"Make no mistake"*, *"This cannot be overstated"*, *"The struggle is real."*

### Dramatic One-Line Staccato
- Prohibited: *"That's it. That's the thing."*, dramatic single-sentence paragraph closers that simulate epiphany.

### Deep-Sounding Maxims
- Prohibited: *"At its core, what really matters is..."*, pseudo-philosophical platitudes.

### Disputation with Imaginary Opponents
- Prohibited: *"I'm not saying X, but..."*, *"A tempting approach would be to think..."*

### Rhetorical Question Self-Answers
- Prohibited: *"Why does this matter? Because..."*, *"What does this mean for you? It means..."*

### Forced Triads
- Prohibited: Artificially forcing lists, adjectives, or bullet points into groups of three. Use the exact count demanded by the facts.

### Significance & Legacy Inflation
- Prohibited: *"stands as a testament to"*, *"pivotal moment"*, *"watershed development"*, *"rich tapestry"*, *"enduring legacy"*, *"cornerstone"*, *"game-changing"*, *"the future looks bright"*, *"beacon of innovation"*.
- Rule: Report the concrete data point; omit the rhetorical significance.

### Vague Attribution & Pseudo-Authority
- Prohibited: *"Experts believe"*, *"Studies show"*, *"Industry leaders agree"*.
- Rule: Provide the primary source or delete the sentence.

### Reader Flattery & Marketing Pandering
- Prohibited: *"Here's what is interesting:"*, *"Worth your time"*, *"Whether you're a seasoned pro or just starting out..."*

### Corporate & Jargon Buzzwords
- Prohibited: *delve, leverage, utilize, robust, seamless, streamline, foster, pivotal, crucial, elevate, beacon, tapestry, testament, embark, unleash, game-changer, move the needle, circle back, low-hanging fruit, world-class, state-of-the-art, hidden gem*.

### Chatbot Residue & Meta-Commentary
- Prohibited: *"Certainly!"*, *"Great question!"*, *"I'd be happy to help"*, *"As an AI..."*, *"Let me think step by step"*, *"In conclusion..."*, *"Ultimately, this reminds us that..."*, *"The table below compares..."*

### Hedge Stacking & Over-Caution
- Prohibited: *"could potentially possibly"*, *"While X is promising, Y remains a challenge"*.
- Rule: State real technical uncertainties once, plainly and quantitatively.

---

## 4. Typography & Mechanical Execution

1. **Em-Dash Discipline**: Zero em-dashes by default; never more than one in an entire document. Use periods, commas, colons, or parentheses instead.
2. **No Decorative Bold Listicles**: Avoid bolded lead-ins in lists (e.g. `**Speed:** Speed improved...`). Write continuous prose.
3. **Sentence Case Headings**: Headings must be in sentence case, naming exactly what the section contains. Never insert emojis into headings.
4. **Natural Sentence Variance**: Sentences should vary between 8 and 25 words. Avoid three consecutive sentences of identical length.
5. **Typographic Punctuation**: Always use curly typographic apostrophes (`’`) and quotation marks (`“”`) in user-facing copy.

---

## 5. Document Silhouette & Structure

1. **Autonomous Paragraph Openers**: Paragraphs must open with a substantive factual claim, never with connective discourse scaffolding (*"Moreover,"*, *"Furthermore,"*, *"Additionally,"*).
2. **No Recap Loops**: Concluding sections must never repeat the vocabulary or metaphors introduced in the opening section.
3. **Terminal Action Focus**: Conclude sections on the last concrete fact or the immediate interactive call-to-action, never on an overarching summary or moralizing coda.

---

## 6. Hallmark Gate Tiers

- **Floor (Never Ships)**: Failing WCAG color contrast, invisible keyboard focus, broken reduced motion, invented metrics/testimonials, broken mobile viewport layout. Any single violation halts release.
- **Reflex Gates (Default Banned)**: Eyebrow micro-labels, tracked all-caps labels, single accent-colored words in headlines, empty placeholder cards, trailing newsletter forms. Allowed only when explicitly recorded in the design system decision stamp.
- **Decision Stamping**: The first comment in the primary stylesheet must explicitly record design decisions and approved exceptions.

---

## 7. 8-Criteria Quality Rubric (Passing Score >= 32/40)

Evaluate prose across 8 dimensions scored 1 to 5:
1. **Directness**: States the thesis immediately with zero throat-clearing.
2. **Natural Rhythm**: Varied sentence lengths with authentic human cadence.
3. **Concrete Verbs**: Physical, verifiable actions; zero buzzwords.
4. **Reader Trust**: Avoids patronizing explanations and false urgency.
5. **Human Authenticity**: Sounds like an experienced engineer or craftsperson, not an automated summary.
6. **Density**: High ratio of information to word count.
7. **Fact Preservation**: Never invents or inflates numbers, clients, or certifications.
8. **Template Avoidance**: Avoids formulaic challenge-redemption arcs and repetitive structural clichés.

*Threshold*: Minimum composite score of 32/40, with no individual criterion below 3.
