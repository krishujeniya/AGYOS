# nlm Command-Line Interface Guide

The `nlm` binary is the direct CLI companion for Gemini Notebook. In AGYOS, run it through `bin/agyos nlm <command>` or `bin/agyos gemini-notebook cli <command>`.

## Core Commands

### Notebook Management

- **List notebooks**:
  ```bash
  bin/agyos nlm notebook list
  ```
- **Inspect notebook details**:
  ```bash
  bin/agyos nlm notebook get <notebook_id_or_alias>
  ```
- **Create a notebook**:
  ```bash
  bin/agyos nlm notebook create "Research: Distributed Consensus"
  ```
- **Rename a notebook**:
  ```bash
  bin/agyos nlm notebook rename <notebook_id> "Updated Title"
  ```
- **Delete a notebook**:
  ```bash
  bin/agyos nlm notebook delete <notebook_id> --confirm
  ```

### Source Management

- **Add web URL source**:
  ```bash
  bin/agyos nlm source add <notebook_id> --type url --url "https://example.com/spec"
  ```
- **Add local file source**:
  ```bash
  bin/agyos nlm source add <notebook_id> --type file --path "./docs/architecture.pdf"
  ```
- **Add raw text source**:
  ```bash
  bin/agyos nlm source add <notebook_id> --type text --title "Meeting Notes" --content "..."
  ```
- **List sources**:
  ```bash
  bin/agyos nlm source list <notebook_id>
  ```
- **Read extracted source content**:
  ```bash
  bin/agyos nlm source content <notebook_id> <source_id>
  ```
- **Sync Google Drive sources**:
  ```bash
  bin/agyos nlm source sync-drive <notebook_id> --confirm
  ```

### Query and Conversation

- **Query a notebook**:
  ```bash
  bin/agyos nlm chat query <notebook_id> "What are the fault tolerance bounds stated in the spec?"
  ```
- **Interactive chat session**:
  ```bash
  bin/agyos nlm chat interactive <notebook_id>
  ```
- **View conversation history**:
  ```bash
  bin/agyos nlm chat history <notebook_id>
  ```

### Automated Research

- **Initiate Web research**:
  ```bash
  bin/agyos nlm research start --query "Post-quantum cryptographic algorithms NIST standards" --source web --mode deep
  ```
- **Check research progress**:
  ```bash
  bin/agyos nlm research status <task_id>
  ```
- **Import discovered research sources into notebook**:
  ```bash
  bin/agyos nlm research import <task_id> <notebook_id>
  ```

### Studio Artifact Generation

- **Create Audio Overview (Podcast)**:
  ```bash
  bin/agyos nlm studio create audio <notebook_id> --confirm
  ```
- **Create Slide Deck**:
  ```bash
  bin/agyos nlm studio create slides <notebook_id> --confirm
  ```
- **Create Study Guide / Report**:
  ```bash
  bin/agyos nlm studio create report <notebook_id> --format "Interactive" --confirm
  ```
- **Check studio generation status**:
  ```bash
  bin/agyos nlm studio status <notebook_id>
  ```
- **Download artifact**:
  ```bash
  bin/agyos nlm studio download <notebook_id> <artifact_id> --output-dir ./artifacts
  ```

### Notes and Workspace Export

- **Create note**:
  ```bash
  bin/agyos nlm note create <notebook_id> --title "Summary" --content "..."
  ```
- **Export report to Google Docs**:
  ```bash
  bin/agyos nlm export doc <notebook_id> <artifact_id>
  ```
- **Export data table to Google Sheets**:
  ```bash
  bin/agyos nlm export sheet <notebook_id> <artifact_id>
  ```
