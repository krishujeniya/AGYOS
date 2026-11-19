---
name: manim-video
description: Build reusable Manim explainers for technical concepts, graphs, system diagrams, and product walkthroughs, then hand off to the wider ECC video stack if needed. Use when the user wants a clean animated explainer rather than a generic talking-head script.
metadata:
  origin: ECC
prompt-source: prompt.toon
---
skill: "manim-video"
sections[12]:
  - "\n"
  - "# Manim Video\n\nUse Manim for technical explainers where motion, structure, and clarity matter more than photorealism.\n\n"
  - "## When to Activate\n\n- the user wants a technical explainer animation\n- the concept is a graph, workflow, architecture, metric progression, or system diagram\n- the user wants a short product or launch explainer for X or a landing page\n- the visual should feel precise instead of generically cinematic\n\n"
  - "## Tool Requirements\n\n- `manim` CLI for scene rendering\n- `ffmpeg` for post-processing if needed\n- `video-editing` for final assembly or polish\n- `remotion-video-creation` when the final package needs composited UI, captions, or additional motion layers\n\n"
  - "## Default Output\n\n- short 16:9 MP4\n- one thumbnail or poster frame\n- storyboard plus scene plan\n\n"
  - "## Workflow\n\n1. Define the core visual thesis in one sentence.\n2. Break the concept into 3 to 6 scenes.\n3. Decide what each scene proves.\n4. Write the scene outline before writing Manim code.\n5. Render the smallest working version first.\n6. Tighten typography, spacing, color, and pacing after the render works.\n7. Hand off to the wider video stack only if it adds value.\n\n"
  - "## Scene Planning Rules\n\n- each scene should prove one thing\n- avoid overstuffed diagrams\n- prefer progressive reveal over full-screen clutter\n- use motion to explain state change, not just to keep the screen busy\n- title cards should be short and loaded with meaning\n\n"
  - "## Network Graph Default\n\nFor social-graph and network-optimization explainers:\n\n- show the current graph before showing the optimized graph\n- distinguish low-signal follow clutter from high-signal bridges\n- highlight warm-path nodes and target clusters\n- if useful, add a final scene showing the self-improvement lineage that informed the skill\n\n"
  - "## Render Conventions\n\n- default to 16:9 landscape unless the user asks for vertical\n- start with a low-quality smoke test render\n- only push to higher quality after composition and timing are stable\n- export one clean thumbnail frame that reads at social size\n\n"
  - "## Reusable Starter\n\nUse [assets/network_graph_scene.py](assets/network_graph_scene.py) as a starting point for network-graph explainers.\n\nExample smoke test:\n\n```bash\nmanim -ql assets/network_graph_scene.py NetworkGraphExplainer\n```\n\n"
  - "## Output Format\n\nReturn:\n\n- core visual thesis\n- storyboard\n- scene outline\n- render plan\n- any follow-on polish recommendations\n\n"
  - "## Related Skills\n\n- `video-editing` for final polish\n- `remotion-video-creation` for motion-heavy post-processing or compositing\n- `content-engine` when the animation is part of a broader launch\n"
