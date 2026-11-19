---
name: image-compress
description: Compresses images to WebP (default) or PNG with automatic tool selection. Use when user asks to "compress image", "optimize image", "convert to webp", or reduce image file size.
version: 1.56.1
metadata:
  openclaw:
    homepage: https://github.com/JimLiu/baoyu-skills#baoyu-compress-image
    requires:
      anyBins:
        - bun
        - npx
prompt-source: prompt.toon
---
skill: "image-compress"
sections[8]:
  - "\n"
  - "# Image Compressor\n\nCompresses images using best available tool (sips → cwebp → ImageMagick → Sharp).\n\n"
  - "## Script Directory\n\nScripts in `scripts/` subdirectory. `{baseDir}` = this SKILL.md's directory path. Resolve `${BUN_X}` runtime: if `bun` installed → `bun`; if `npx` available → `npx -y bun`; else suggest installing bun. Replace `{baseDir}` and `${BUN_X}` with actual values.\n\n| Script | Purpose |\n|--------|---------|\n| `scripts/main.ts` | Image compression CLI |\n\n"
  - "## Preferences (EXTEND.md)\n\nCheck EXTEND.md in priority order — the first one found wins:\n\n| Priority | Path | Scope |\n|----------|------|-------|\n| 1 | `.baoyu-skills/baoyu-compress-image/EXTEND.md` | Project |\n| 2 | `${XDG_CONFIG_HOME:-$HOME/.config}/baoyu-skills/baoyu-compress-image/EXTEND.md` | XDG |\n| 3 | `$HOME/.baoyu-skills/baoyu-compress-image/EXTEND.md` | User home |\n\nIf none found, use defaults.\n\n**EXTEND.md supports**: Default format, default quality, keep-original preference.\n\n"
  - "## Usage\n\n```bash\n${BUN_X} {baseDir}/scripts/main.ts <input> [options]\n```\n\n"
  - "## Options\n\n| Option | Short | Description | Default |\n|--------|-------|-------------|---------|\n| `<input>` | | File or directory | Required |\n| `--output` | `-o` | Output path | Same path, new ext |\n| `--format` | `-f` | webp, png, jpeg | webp |\n| `--quality` | `-q` | Quality 0-100 | 80 |\n| `--keep` | `-k` | Keep original | false |\n| `--recursive` | `-r` | Process subdirs | false |\n| `--json` | | JSON output | false |\n\n"
  - "## Examples\n\n```bash\n# Single file → WebP (replaces original)\n${BUN_X} {baseDir}/scripts/main.ts image.png\n\n# Keep PNG format\n${BUN_X} {baseDir}/scripts/main.ts image.png -f png --keep\n\n# Directory recursive\n${BUN_X} {baseDir}/scripts/main.ts ./images/ -r -q 75\n\n# JSON output\n${BUN_X} {baseDir}/scripts/main.ts image.png --json\n```\n\n**Output**:\n```\nimage.png → image.webp (245KB → 89KB, 64% reduction)\n```\n\n"
  - "## Extension Support\n\nCustom configurations via EXTEND.md. See **Preferences** section for paths and supported options.\n"
