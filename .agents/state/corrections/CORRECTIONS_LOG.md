# AGYOS Skill Catalog Corrections & Evolution Log

This log tracks autonomous self-corrections, principle additions, and industry adaptations across all AGYOS skills.

## [2026-11-11T09:34:30Z] agyos-self-improvement

- **Category**: `factual_fix`
- **Section**: frontmatter description
- **Before**:
  ```
  Autonomous self-correction and continuous improvement protocol for the entire AGYOS skill catalog. Captures user corrections, integrates industry trends, maintains cross-skill dependencies, enforces quality gates, and preserves test ratchets across all 1970+ skills.
  ```
- **After**:
  ```
  Use when maintaining the AGYOS skill catalog or improving a skill's correctness, discovery, references, or quality gates. Captures corrections, source checks, cross-skill dependencies, and test ratchets.
  ```
- **Rationale**: Removed the stale hard-coded catalog count and made the maintenance trigger explicit.

## [2026-11-10T19:35:00Z] video-editing-principles
- **Category**: `principle_addition`
- **Section**: Full Master Reference (20 Sections)
- **Before**:
  ```
  No dedicated comprehensive video editing principles skill in catalog.
  ```
- **After**:
  ```
  Created video-editing-principles skill with 440 principles across 20 sections, Walter Murch's Rule of Six, format priority matrix, mastery hierarchy, and autonomous self-improvement protocol.
  ```
- **Rationale**: User requested complete master reference for video editing principles based on 2026 industry research (Hollywood, YouTube, social, documentary).

## [2026-11-10T19:35:00Z] agyos-self-improvement
- **Category**: `workflow_update`
- **Section**: Universal Catalog Protocol
- **Before**:
  ```
  No centralized protocol for logging corrections, updating dependent skills, and preserving test ratchets.
  ```
- **After**:
  ```
  Implemented agyos-self-improvement protocol: 5-step correction logging, trend integration, cross-skill dependency graph update, quality gates, and session learning capture.
  ```
- **Rationale**: Establish an autonomous self-improvement loop across all 1,970+ AGYOS skills.

## [2026-11-10T19:40:00Z] scriptwriting-principles
- **Category**: `principle_addition`
- **Section**: Full Master Reference (22 Sections)
- **Before**:
  ```
  No dedicated comprehensive scriptwriting principles skill in catalog.
  ```
- **After**:
  ```
  Created scriptwriting-principles skill with 440 principles across 22 sections, Craig Mazin dramatic argument model, category priority matrix, 12 foundational competencies, and autonomous self-improvement protocol.
  ```
- **Rationale**: User requested complete master reference for scriptwriting principles spanning cinema, YouTube long-form, social media, documentaries, advertising, education, and AI-era writing.

## [2026-11-10T19:50:00Z] google-flow & ffmpeg-video-editor
- **Category**: `workflow_update`
- **Section**: Watermark Removal & Delogo Inpainting
- **Before**:
  ```
  Generated Google Flow / Veo videos retained bottom-right corner watermark marks.
  ```
- **After**:
  ```
  Added automated scripts/remove_flow_watermark.py with dynamic corner detection and FFmpeg delogo inpainting filter. Integrated step 6 into the Google Flow workflow.
  ```
- **Rationale**: User requested workflow and tooling to remove watermarks from Flow video generations.

## [2026-11-10T20:00:00Z] ai-video-detection-forensics
- **Category**: `principle_addition`
- **Section**: Full Master Reference (11 Sections)
- **Before**:
  ```
  No dedicated skill cataloging AI video forensic detection principles, SynthID analysis, and C2PA credentials.
  ```
- **After**:
  ```
  Created ai-video-detection-forensics skill with 200 principles across 11 sections covering Google SynthID detection, C2PA Content Credentials, container metadata analysis, temporal consistency, biological and physical heuristics, audio-visual alignment, reverse keyframe analysis, and production mastering standards.
  ```
- **Rationale**: User requested deep research and reference for AI video detection principles (Google Flow / Veo 2026) to understand forensic signatures, metadata traces, and pristine master production.

## [2026-11-10T20:10:00Z] ai-video-quality-enhancement
- **Category**: `principle_addition`
- **Section**: Quality Improvement & CLI Repair Toolkit
- **Before**:
  ```
  No dedicated runbook mapping the 200 forensic detection principles to actionable repair pipelines and Linux CLI tools (CodeFormer, Real-ESRGAN, ProPainter, DeepFilterNet, Demucs, whisper.cpp, VidStab, VMAF).
  ```
- **After**:
  ```
  Created ai-video-quality-enhancement skill and scripts/repair_ai_video.py providing end-to-end defect triage, stabilization, deflicker, deband, audio mastering (-14 LUFS), CodeFormer face recovery, and Google Flow anti-hallucination prompt directives.
  ```
- **Rationale**: User requested complete video quality improvement & CLI toolkit addressing AI video defects from the 200 forensic principles.

## [2026-11-10T20:25:00Z] organic-film-de-ai
- **Category**: `principle_addition`
- **Section**: Organic Cinema Transformation & De-AI Craft
- **Before**:
  ```
  AI video outputs exhibited characteristic 'AI sheen': waxy skin, hyper-saturation, mechanical slider camera motion, sterile digital silence, and staccato frame stepping.
  ```
- **After**:
  ```
  Created organic-film-de-ai skill and scripts/organic_film_engine.py implementing photochemical halation bloom, Kodak 2383 S-curve tonemapping, 35mm silver halide grain synthesis, lens vignetting/barrel distortion, 2D handheld breathing drift, and acoustic room warmth.
  ```
- **Rationale**: User requested deep research and master workflow across all AGYOS skills so output videos do not look AI-generated or AI-edited.

## [2026-11-10T20:30:00Z] universal-ai-research
- **Category**: `principle_addition`
- **Section**: Universal Autonomous Research Pipeline v3.0
- **Before**:
  ```
  Academic research skills lacked end-to-end multi-agent orchestration, the 214-principle register across 8 research domains, noncompensatory novelty/feasibility gates, 6-artifact deliverables, and 26 Humanizer anti-slop rules.
  ```
- **After**:
  ```
  Created universal-ai-research skill and scripts/universal_research_runner.py based on Research Prompt.pdf, RESEARCH_SKILL_PRINCIPLES.md, and UNIVERSAL_AI_RESEARCH_MASTER_PROMPT_v3.md. Implemented 4 execution modes (A/B/C/D), 6 mandatory artifacts, 11 topic fields, 13 paper fields, 11 synthesis sections, Q1-Q10 quality gates, and automated workspace validation.
  ```
- **Rationale**: User requested adding an AI research skill based on the uploaded research prompt files.
## [2026-11-11T10:56:13Z] openwhispr

- **Category**: `principle_addition`
- **Section**: Frontmatter and desktop/MCP workflow
- **Before**:
  ```
  No OpenWhispr-specific runbook was present in the AGYOS catalog.
  ```
- **After**:
  ```
  Added openwhispr v1.0.0 with source-linked setup, per-activity privacy checks, local/cloud guidance, and least-privilege MCP integration steps.
  ```
- **Rationale**: The user requested an AGYOS skill for the OpenWhispr repository; factual workflow details were checked against its repository and current official documentation.

## [2026-11-11T11:11:54Z] tech-debt-cleanup

- **Category**: `cross_reference`
- **Section**: `references/FULL_RUNBOOK.md`
- **Before**:
  ```
  The legacy full-runbook path contained a near-complete copy of the canonical codebase-tech-debt procedure.
  ```
- **After**:
  ```
  Use the canonical [codebase-tech-debt full runbook](../../codebase-tech-debt/references/FULL_RUNBOOK.md). This path remains for compatibility with existing links.
  ```
- **Rationale**: Keep the stable legacy ID and local reference path while preventing the procedures from drifting apart.

## [2026-11-11T11:22:26Z] openwhispr

- **Category**: `factual_fix`
- **Section**: macOS permissions and MCP authorization
- **Before**:
  ```
  Screen Recording (macOS) for meeting audio capture.
  Create a key with only the scopes needed. Start with read-only note/transcription scopes.
  ```
- **After**:
  ```
  System Audio is the macOS permission for capturing other meeting participants and is listed under Screen Recording settings. The separate Screen Recording permission enables optional voice-agent screenshots. Claude Connector OAuth requests all documented scopes; API-key clients can be restricted to selected scopes.
  ```
- **Rationale**: Corrected wording against OpenWhispr's current [macOS permission guide](https://docs.openwhispr.com/platform/macos) and [MCP scope guide](https://docs.openwhispr.com/integrations/mcp), following independent review.

## [2026-11-11T11:23:26Z] remotion-best-practices

- **Category**: `cross_reference`
- **Section**: `rules/` compatibility assets
- **Before**:
  ```
  The legacy Remotion skill retained duplicate Markdown rule bodies alongside the canonical remotion-video-creation rules.
  ```
- **After**:
  ```
  All 28 legacy Markdown rule paths point to matching canonical rule files. Three matching TSX example assets remain at both paths so existing references continue to resolve.
  ```
- **Rationale**: Avoid copied rule drift while preserving the legacy skill ID, documentation paths, and executable example assets.

## [2026-11-11T11:51:22Z] openwhispr

- **Category**: `factual_fix`
- **Section**: MCP OAuth and API-key verification
- **Before**:
  ```
  Verify the endpoint and selected scopes in the client's consent/configuration UI, then make a read-only request before enabling writes.
  ```
- **After**:
  ```
  Claude Connectors OAuth permission review is explicitly separate from API-key scope configuration. A read-only smoke test does not narrow OAuth permissions; selected scopes apply to API-key clients.
  ```
- **Rationale**: Clarified the distinction identified during independent review and aligned the skill with OpenWhispr's current MCP scope guide.
