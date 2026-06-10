# cdp-use Release Runbook

## Releasing

1. **From `main`, run `task release -- patch`** (or `minor` / `major`). This pulls latest main, creates a fresh `release/<timestamp>` branch off it, bumps `pyproject.toml`, commits as `release: v<NEW_VERSION>`, pushes the branch, and opens a PR.

   Manual alternative (if you don't want the helper):

   ```bash
   git checkout main && git pull --ff-only origin main
   git checkout -b release/$(date +%Y%m%d-%H%M%S)
   # Bump pyproject.toml version manually, then:
   NEW_VERSION=$(grep -E '^version = ' pyproject.toml | head -1 | sed -E 's/version = "(.*)"/\1/')
   git add pyproject.toml
   git commit -m "release: v$NEW_VERSION"
   git push -u origin "$(git rev-parse --abbrev-ref HEAD)"
   gh pr create --base main --title "release: v$NEW_VERSION" --body "Release v$NEW_VERSION"
   ```

2. **Merge to main.**

That's it. The `auto-release-on-version-bump` workflow detects the bump on main and creates a GitHub Release at the bump commit (tag `v<NEW_VERSION>`). It then directly invokes `publish.yml` via `workflow_call`, which runs preflight (env protection + version coherence + already-published guard), pauses at the `release` environment approval gate, and on approval publishes to PyPI via OIDC trusted publishing.

If a publish fails after the Release is created: the Release stays (it's the rollback handle). Investigate, fix on a new patch version, repeat. Re-running the auto-release workflow on the same commit is a no-op, it detects the existing Release and exits cleanly.

Manual `gh release create v<VERSION> --generate-notes --repo browser-use/cdp-use` from the CLI also works as an escape hatch.

## Release authentication

PyPI uses OIDC trusted publishing. **No static tokens, no secrets to rotate.**

- **PyPI**: trusted publishing must be configured at https://pypi.org/manage/project/cdp-use/settings/publishing/ (Owner: browser-use, Repository: cdp-use, Workflow: auto-release-on-version-bump.yml, Environment: release).
- The `release` environment requires approval from a reviewer other than the release author (`prevent_self_review: true`). Reviewers: gregpr07, LarsenCundric, reformedot.

If the trusted publisher binding is revoked or misconfigured, publishing fails at the publish step with a clear OIDC error from PyPI. The release tag stays cut (you can re-dispatch after re-binding).
