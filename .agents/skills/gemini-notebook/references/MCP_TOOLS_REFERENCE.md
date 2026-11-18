# Gemini Notebook MCP Tools Reference

The `gemini-notebook-mcp` daemon implements 53 Model Context Protocol tools. All destructive operations and heavy studio artifact generation actions require explicit operator confirmation (`confirm=True`).

## Tool Catalog by Functional Group

### 1. Notebook Operations

| Tool | Parameters | Description | Approval Required |
| :--- | :--- | :--- | :--- |
| `notebook_list` | `max_results` (optional) | Enumerate user notebooks | No |
| `notebook_get` | `notebook_id` | Retrieve metadata, settings, and sources | No |
| `notebook_create` | `title` | Create a new empty notebook | No |
| `notebook_rename` | `notebook_id`, `new_title` | Update notebook display title | No |
| `notebook_delete` | `notebook_id`, `confirm` | Irreversibly delete a notebook | Yes (`confirm=True`) |

### 2. Source Operations

| Tool | Parameters | Description | Approval Required |
| :--- | :--- | :--- | :--- |
| `source_add` | `notebook_id`, `source_type` (`url`\|`text`\|`drive`\|`file`), `url`, `text`, `document_id`, `file_path` | Ingest new document or link | No |
| `source_list` | `notebook_id` | List ingested sources and indexing status | No |
| `source_get_content` | `notebook_id`, `source_id` | Read parsed plain text content of a source | No |
| `source_rename` | `notebook_id`, `source_id`, `new_title` | Rename an indexed source | No |
| `source_delete` | `notebook_id`, `source_id`, `confirm` | Remove source from notebook | Yes (`confirm=True`) |
| `source_list_drive` | `notebook_id` | List Google Drive sources and check sync state | No |
| `source_sync_drive` | `notebook_id`, `confirm` | Refresh stale Google Drive documents | Yes (`confirm=True`) |

### 3. Source-Grounded Queries & Conversations

| Tool | Parameters | Description | Approval Required |
| :--- | :--- | :--- | :--- |
| `chat_send` | `notebook_id`, `query`, `source_ids` (optional) | Query sources with Gemini citations | No |
| `chat_list` | `notebook_id` | Retrieve conversation history turns | No |
| `chat_delete` | `notebook_id`, `confirm` | Clear conversation history | Yes (`confirm=True`) |
| `chat_save_to_note` | `notebook_id`, `turn_index` (optional) | Convert chat response to a notebook note | No |

### 4. Automated Research Discovery

| Tool | Parameters | Description | Approval Required |
| :--- | :--- | :--- | :--- |
| `research_start` | `query`, `source` (`web`\|`drive`), `mode` (`fast`\|`deep`), `notebook_id` (optional) | Launch automated search for external sources | No |
| `research_status` | `task_id` | Check research run state and review candidate sources | No |
| `research_import` | `task_id`, `notebook_id`, `source_indices` (optional) | Add selected research results to notebook | No |

### 5. Multimodal Studio Artifacts

| Tool | Parameters | Description | Approval Required |
| :--- | :--- | :--- | :--- |
| `studio_create` | `notebook_id`, `artifact_type` (`audio`\|`video`\|`infographic`\|`slides`\|`report`\|`study_guide`\|`quiz`\|`flashcards`\|`mind_map`), `confirm`, `options` | Generate synthesis artifact | Yes (`confirm=True`) |
| `studio_status` | `notebook_id` | List studio artifacts and generation progress | No |
| `studio_delete` | `notebook_id`, `artifact_id`, `confirm` | Delete generated studio artifact | Yes (`confirm=True`) |
| `studio_revise` | `notebook_id`, `artifact_id`, `revision_spec`, `confirm` | Apply revisions to slides or components | Yes (`confirm=True`) |
| `report` | `notebook_id`, `action` (`get`\|`elements`\|`generate`), `confirm` | Manage and expand interactive report plans | Yes for `generate` |

### 6. Artifact Downloads & Exports

| Tool | Parameters | Description | Approval Required |
| :--- | :--- | :--- | :--- |
| `download_artifact` | `notebook_id`, `artifact_id`, `output_path` | Download artifact file (audio, video, PDF, MD) | No |
| `download_all_artifacts` | `notebook_id`, `output_dir` | Batch download all artifacts in a notebook | No |
| `export_artifact` | `notebook_id`, `artifact_id`, `target` (`docs`\|`sheets`) | Export structured content to Google Workspace | No |

### 7. Administration & Identity

| Tool | Parameters | Description | Approval Required |
| :--- | :--- | :--- | :--- |
| `note` | `notebook_id`, `action` (`create`\|`list`\|`update`\|`delete`), `title`, `content`, `note_id`, `confirm` | CRUD operations on notebook notes | Yes for `delete` |
| `label` | `notebook_id`, `action` (`auto`\|`list`\|`create`\|`rename`\|`delete`\|`move_source`) | Tag and group notebook sources | Yes for `delete` |
| `profile` | `action` (`list`\|`status`\|`switch`), `name` | Select active Google credentials profile | No |
| `alias` | `action` (`list`\|`get`\|`set`\|`delete`), `alias`, `notebook_id` | Assign human-readable shortcuts for IDs | No |
| `pipeline` | `action` (`run`\|`list`\|`create`), `pipeline_name`, `params` | Execute scripted multi-step workflows | No |
| `refresh_auth` | `profile` (optional) | Revalidate session cookies or run recovery | No |
| `save_auth_tokens` | `cookies`, `request_body` (optional), `request_url` (optional) | Store extracted credentials | No |
