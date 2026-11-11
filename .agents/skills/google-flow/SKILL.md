---
name: google-flow
description: >-
  Headless video generation and media retrieval using Google Flow and Veo 3.1. Enforces zero visible
  browser windows (--headless=new), automatic local downloads, machine-verified media integrity,
  and mandatory skill-first research routing before crafting prompts.
metadata:
  version: 1.0.0
license: MIT
---

# Google Flow (Headless Video Generation & Automation)

Automate video generation, tile inspection, and media downloading from **Google Flow** via the `google-flow-mcp` service. All operations execute strictly headless without launching visible Chrome windows.

## Core Operating Invariants

1. **Headless Execution Only (Zero Visible Browser Windows)**:
   - Chrome must run in `--headless=new` mode at all times.
   - `FLOW_MCP_HEADLESS=true` is enforced in [google-flow-mcp.sh](../../../mcp/google-flow-mcp.sh).
   - Use dedicated user data directory `~/.google-flow-chrome` synchronized from the local user profile (`~/.config/google-chrome`).
   - Never launch standard desktop Chrome windows or interfere with the user's active browsing session.

2. **Skill-First Research & Prompt Crafting Protocol**:
   - Never generate raw or speculative prompts directly from user queries.
   - Always research the domain and consult existing specialist skills before crafting video instructions:
     - [veo-3](../veo-3/SKILL.md): Director prompt anatomy (Subject, Action, Setting, Camera movement/angle/lens, Lighting/mood, Style, Audio cues with quoted dialogue, SFX, ambient sound, musical score).
     - [ai-video](../ai-video/SKILL.md): The BRIEF framework (portable specifications, duration pacing, scene composition).
     - [scripting-and-storyboarding](../scripting-and-storyboarding/SKILL.md): Scene breakdowns, visual timing, narrative arcs.
     - Format-specific skills when targeting social channels: [reels-script](../reels-script/SKILL.md), [tiktok-script](../tiktok-script/SKILL.md), [youtube-shorts](../youtube-shorts/SKILL.md).
     - Domain research skills (`research`, `search-specialist`, `deep-research`) to ground technical details, physical realism, or factual environments.

3. **Mandatory Local Download & Verification**:
   - All generated clips must be saved to the local workspace directory (e.g. `/home/ai/Documents/projects/Freelance/AGYOS`).
   - The tool automatically downloads outputs as `flow_<media_id>_<job_id>.mp4`.
   - Run `ffprobe` to verify media integrity: container, resolution, frame rate, duration, and audio track.

---

## Google Flow MCP Architecture

- **MCP Server Repository**: [integrations/google-flow-mcp](../../../integrations/google-flow-mcp)
- **Launcher Script**: [mcp/google-flow-mcp.sh](../../../mcp/google-flow-mcp.sh)
- **Configuration**: [config.ts](../../../integrations/google-flow-mcp/src/config.ts)
- **Active Studio Project URL**: `https://flow.google.com/project/2d5fbde7-3875-41dc-9ecc-9a3f9881da6d`
- **CDP Debug Port**: `9333`

### Environment Variables
```bash
FLOW_MCP_CHROME_PATH="/usr/bin/google-chrome"
FLOW_MCP_USER_DATA_DIR="$HOME/.google-flow-chrome"
FLOW_MCP_PROFILE_DIRECTORY="Default"
FLOW_MCP_CDP_PORT="9333"
FLOW_MCP_STATE_DIR="$HOME/.google-flow-mcp"
FLOW_MCP_HEADLESS="true"
```

---

## MCP Tools Reference

### 1. `flow_generate_video`
Generates a video through the Google Flow agent composer and automatically downloads the completed MP4.

Parameters:
- `prompt` (string, required): Full directed scene description including action, camera motion, lighting, and explicit audio cues.
- `model` (string, default: `veo-3.1-fast`): Veo model variant (`veo-3.1-quality`, `veo-3.1-fast`, `veo-3.1-lite`, `omni-flash`).
- `ratio` (string, default: `9:16`): Aspect ratio (`9:16` for mobile vertical, `16:9` for widescreen horizontal).
- `duration` (integer, default: `8`): Clip duration in seconds (`4`, `6`, `8`, `10` where `10` is supported by Omni Flash).
- `project_url` (string, required): Destination project URL (`https://flow.google.com/project/<project_id>`).
- `output_dir` (string, required): Local path where the MP4 will be downloaded (`flow_<id8>_<job>.mp4`).
- `auto_confirm` (boolean, default: `false`): Set `false` to dry-run/preview instruction; set `true` to commit credits and generate.
- `reference_images` (array of strings, optional): Local file paths for first-frame or image-to-video conditioning.
- `edit_mode` (boolean, default: `false`): Edit the last video of the active session instead of generating a new one.
- `resume` (boolean, optional): Set `true` to reconnect to an in-flight job.
- `job_id` (string, optional): Specific job ID to resume after restart.

### 2. `flow_scene_add` (Scene Builder Initialization)
Creates a new multi-clip Scene Builder timeline from an existing project media asset.

Parameters:
- `project_url` (string, required): Destination project URL.
- `media_id` (string, required): The 8-character media ID or title of the base video clip.
Returns: `scene_url`, `scene_id`, and initial clip timeline.

### 3. `flow_scene_extend` (Scene Builder Extension)
Generates a continuation of the last clip in the scene timeline with matching physical motion and synchronized audio.

Parameters:
- `scene_url` (string, required): Scene URL returned by `flow_scene_add`.
- `prompt` (string, required): Narrative description of what happens next in the scene.
- `after_clip_index` (integer, required): Index of the clip to extend (0-based; must be the last clip).
- `output_dir` (string, required): Local target folder for downloading the extension clip.
- `auto_confirm` (boolean, default: `false`): `false` dry-runs and takes screenshot; `true` commits credits and generates.
- `resume` (boolean, optional): Set `true` to reconnect to an in-flight extension.

### 4. `flow_scene_status`
Reads the current timeline clips, total duration, and rendering status of an active Scene Builder scene.

Parameters:
- `scene_url` (string, required): Scene URL.

### 5. `flow_generate_image`
Generates high-resolution images via Nano Banana models for video reference conditioning, storyboard frames, or YouTube thumbnails.

Parameters:
- `prompt` (string, required): Visual description.
- `model` (string, default: `nano-banana-pro`): Image model variant (`nano-banana-pro`, `nano-banana-2`, `nano-banana-2-lite`).
- `ratio` (string, default: `16:9`): Aspect ratio (`16:9`, `9:16`, `1:1`, `4:3`).
- `project_url` (string, required): Flow project URL.
- `output_dir` (string, required): Local directory for downloaded image.
- `auto_confirm` (boolean, default: `false`): Commit generation.

### 6. `flow_project_open`
Opens and inspects the Google Flow project canvas headlessly, returning project title, media count, tiles, and agent session history.

Parameters:
- `url` (string, required): Flow project URL.

### 7. `flow_media_download`
Downloads a specific media asset from the Flow project by UUID.

Parameters:
- `media_id` (string, required): Asset identifier.
- `output_dir` (string, required): Target folder on disk.
- `suffix` (string, default: `manual`): Filename suffix.

### 8. `flow_status`
Checks the current CDP connection state, active session, and running jobs.

---

## Workflow: From Query to Downloaded Video

```
1. User Query
      │
      ▼
2. Skill-First Research & Prompt Engineering
   ├── Ingest: veo-3 (director prompt structure: subject, action, camera, lighting, audio)
   ├── Ingest: ai-video / format skills (retention hook, 9:16 ratio, timing)
   └── Run research if query requires domain-specific facts or visual accuracy
      │
      ▼
3. Format Directed Prompt
   ├── Subject + Action: Concrete, single primary motion
   ├── Camera: Angle, lens, trajectory (e.g. low-angle push-in, 35mm anamorphic)
   ├── Lighting & Atmosphere: Volumetric, directional, color palette
   └── Synchronized Audio: Explicit dialogue, ambient background, SFX
      │
      ▼
4. Headless Generation (flow_generate_video)
   ├── auto_confirm: true
   ├── project_url: active project URL
   └── output_dir: local workspace directory
      │
      ▼
5. Media Download & Verification
   ├── Tool automatically downloads flow_<id8>_<job>.mp4
   └── ffprobe verification: resolution, codec, duration, audio presence
      │
      ▼
6. Automated Watermark Removal (Optional Post-Process)
   └── Run python3 scripts/remove_flow_watermark.py <video.mp4>
```

---

## Automated Watermark Removal Workflow

Veo video generations include a small corner watermark mark in the bottom-right corner. The automated script detects the resolution and corner coordinates dynamically and applies inpainting via the FFmpeg `delogo` filter:

```bash
# Automated dynamic watermark removal
python3 scripts/remove_flow_watermark.py <input_video.mp4> [output_clean.mp4]

# Direct FFmpeg delogo command for standard 1280x720 video:
ffmpeg -i input.mp4 -vf "delogo=x=1236:y=688:w=36:h=22" -c:a copy output_clean.mp4

# Direct FFmpeg delogo command for 9:16 vertical 720x1280 video:
ffmpeg -i input.mp4 -vf "delogo=x=676:y=1248:w=36:h=22" -c:a copy output_clean.mp4
```

---

## Prompt Engineering Standard (via `veo-3`)

Every prompt sent to `flow_generate_video` must follow the director anatomy:

```text
[Subject & Core Action]: High-contrast subject performing one coherent movement.
[Camera Work]: Explicit camera type, angle, movement, and lens focal length.
[Lighting & Setting]: Specific environment details, color temperature, and atmospheric texture.
[Style & Grading]: Film stock, visual grain, photorealistic rendering details.
[Synchronized Audio]: Ambient environment track, sound effects matching on-screen motion, and any dialogue in quotation marks.
```

### Prompt Example
```text
Cinematic eye-level medium shot of an artisan watchmaker in a moody wooden workshop assembling the gears of an intricate mechanical balance wheel. Slow subtle push-in camera movement with a shallow depth of field, 50mm lens at f/1.8. Warm directional tungsten lamplight illuminates brass gears, while soft dust motes drift through background shadows. Photorealistic 35mm film texture with natural color grading. Audio: Rhythmic, precise metallic ticking of clockwork, delicate clicking of miniature tweezers setting a gear into place, accompanied by a quiet, warm ambient room tone.
```

---

## Verification & Error Recovery

- **Check Download**: Ensure file exists in `output_dir` and size > 0 bytes.
- **Run ffprobe**:
  ```bash
  ffprobe -v error -show_entries stream=width,height,r_frame_rate,codec_name -show_entries format=duration,size -of default=noprint_wrappers=1 <downloaded_video.mp4>
  ```
- **Session Timeout / Auth Refresh**:
  If Flow redirects to login, run [google-flow-mcp.sh](../../../mcp/google-flow-mcp.sh) to copy updated cookies from `~/.config/google-chrome` to `~/.google-flow-chrome`.
