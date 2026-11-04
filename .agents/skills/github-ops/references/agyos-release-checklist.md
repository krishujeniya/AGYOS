# AGYOS Signed Patch Release Checklist

Use this when preparing and publishing releases for `krishujeniya/AGYOS`, ensuring Git tag identity, provenance, GitHub Release, and verification evidence all align.

## Milestone And Contract

- Milestone: Release verification in the AGYOS train.
- Contract: Ship verified, reproducible artifacts; keep AGYOS authority over release evidence and canonical state.
- Invariants: Green CI, passing machine checks (`scripts/agyos-verify.sh`), clean git worktree.

## Non-Negotiable Invariants

- The release tag must be a signed annotated tag on exact green `origin/main`.
- Never mutate, move, or replace published release tags.
- Run `bash scripts/agyos-verify.sh` and ensure 34/34 checks pass before tagging.

## Pre-Release Verification Commands

```bash
git status --short
bash scripts/agyos-verify.sh
python3 -m unittest discover -s scripts/tests -v
gh run list --repo krishujeniya/AGYOS --branch main --limit 5
```

## Release Procedure

1. Verify HEAD commit is on `main` and matches `origin/main`.
2. Generate tag:
```bash
VERSION="3.1.0"
git tag -a "v${VERSION}" -m "AGYOS release v${VERSION}" HEAD
git push origin "v${VERSION}"
```
3. Create GitHub Release:
```bash
gh release create "v${VERSION}" \
  --repo krishujeniya/AGYOS \
  --title "AGYOS v${VERSION}" \
  --notes "Release v${VERSION} of AGYOS."
```
