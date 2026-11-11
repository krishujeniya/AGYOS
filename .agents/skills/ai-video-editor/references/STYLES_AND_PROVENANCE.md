# Preset styles and prompt provenance

The supplied toolkit's styles/index.json lists these seven implementation presets:

| Style ID | Use |
|---|---|
| warm-canvas | Talking-head footage with a calm, editorial picture-in-picture and explanatory cards. |
| creator-motion-graphics | Kinetic type and graphic beats over or between footage. |
| clean-tech | Restrained product and technology explainers with UI cards. |
| software-walkthrough | Code-drawn interface walkthroughs with a cursor and step sequence. |
| data-story | Data-led graphics; use only verified values and sources. |
| chalk-talk | Hand-drawn educational scenes on a chalkboard. |
| pop-info | Illustrated explanatory scenes with a character and simple diagrams. |

For each choice, inspect its style.md, style.json, and base.js in the actual toolkit. Use the
toolkit's code and design constraints rather than inferring behavior from a prompt or still image.
Keep mock interface details clearly invented unless the user supplied the actual interface. The
Software Walkthrough preset uses invented UI; for a real product tutorial, use verified screenshots
or interface details and do not present invented controls as real.

The supplied nafay3d_style_prompts_recreated.md describes seven rewritten style prompts and one
screenshot-based style prompt. It explicitly says the text is not the email-unlocked original.
The separate Untitled document.txt contains seven numbered prompt blocks but does not state where
they came from. Neither document establishes official wording or current site content. Do not call
the recreated prompts original or verified, and do not conflate these seven editor presets with the
six styles in the separate faceless-shorts toolkit.

When a user requests a look from screenshots, distinguish visible traits from inferred motion.
Offer one representative frame and a concise style description before completing the animation.
Do not claim a still image proves timing, transitions, or other unseen behavior.

The inspected ai-video-editor tree has no LICENSE file; its README credits Nafay 3D. This AGYOS
skill records how to use the separately supplied toolkit but does not copy its source code, fonts,
or assets into the catalog. Preserve the source attribution and any notices when using that bundle.
