# Instructions for AI Assistants (Copilot / Antigravity)

Maintain these repository invariants at all times:

1. **Single Git Branch Discipline (`main` only)**:
   - Never create feature branches or worktrees.
   - Maintain exclusively the `main` branch.

2. **Commit Profile**:
   - Name: `Krish Ujeniya`
   - Email: `krishujeniya@users.noreply.github.com`

3. **Python Invariant (`uv` Only)**:
   - Exclusively use `uv run`, `uv sync`, `uv add`. Never execute unmanaged `python` or `pip`.

4. **Zero Local Heavy Builds**:
   - Run only fast, loadless checks locally (`tsc --noEmit`, syntax check).
   - Full builds and test execution belong in GitHub Actions CI.

5. **Repository Layout**:
   - Root files strictly restricted to: `.editorconfig`, `.gitignore`, `CHANGELOG.md`, `LICENSE`, `Makefile`, `README.md`, `wrangler.jsonc`.
   - Core subsystems reside under `.github/`, `assets/`, `deploy/`, `docs/`, `frontend/`, and `gemini/`.
   - Never place stray files in root.
