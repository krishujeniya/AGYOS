# Local video toolkits

These are complete source packages used by AGYOS video runbooks. The skills remain in
`.agents/skills/`; the renderers and their examples stay here so the skill catalog does not
contain duplicate tool implementations.

| Toolkit | Purpose | Runbook |
| --- | --- | --- |
| [`ai-video-editor/`](ai-video-editor/README.md) | Local editing of an existing talking-head recording, with transcription, reviewed cuts, and optional motion graphics. | [ai-video-editor](../../.agents/skills/ai-video-editor/SKILL.md) |
| [`faceless-shorts/`](faceless-shorts/README.md) | Local code-rendered narrated vertical shorts with word-timed captions and animated scenes. | [faceless-shorts-engine](../../.agents/skills/faceless-shorts-engine/SKILL.md) |

Use each toolkit's own README and setup scripts as the source of truth for dependencies and
commands. Setup may download model weights; the runbooks require approval before doing so.
No toolkit setup, model download, or render was run as part of this file relocation.
Tests, builds, dependency resolution, setup, and renders for this repository run only in GitHub
Actions. The [`Video Toolkits` workflow](../../.github/workflows/video-toolkits.yml) runs static
package checks and the faceless renderer's no-model smoke render; it does not download speech
models or voice weights.

## Provenance and licensing

The package READMEs identify these as Nafay 3D skills. Keep those READMEs, bundled notices,
example assets, and attribution with the packages. The `ai-video-editor` package did not include
a top-level license file at intake; do not treat AGYOS's repository license as a license grant for
imported material. Check rights before redistributing or publishing the package contents. The
faceless-shorts package includes a Three.js notice in its example vendor directory; preserve it.
