# Advanced Requirements Engineering Cheat Sheet

[![Lint commit message](https://github.com/CapeOfGoodCode/requirements-engineering/actions/workflows/commit-lint.yml/badge.svg)](https://github.com/CapeOfGoodCode/requirements-engineering/actions/workflows/commit-lint.yml)

This is the cheat sheet for the "Advanced Requirements Engineering" training. It maps
Requirement types to SAFe and ISO/IEC/IEEE 29148, shows the formats used at each level, and
covers decomposition, classification, and KANO.

GitHub Pages: https://capeofgoodcode.github.io/requirements-engineering/cheat-sheet/
(the site root redirects there)

## Setup

Nothing required. Editing `cheatsheet-body.html` and pushing to `main` is all that's
needed — deployment and versioning happen in CI.

Optional: `pre-commit install` (requires [pre-commit](https://pre-commit.com/) and Python)
wires up local commit-message linting, so mistakes are caught before you push instead of
after. Not installing it changes nothing except when you find out about a bad commit message
— the same check also runs in CI.

## How versioning works

A GitHub Actions workflow (`.github/workflows/deploy.yml`) runs on every push to `main`.
It stamps the current UTC timestamp and short commit hash into `cheatsheet-body.html`'s own
footer (`<span>Version: …</span>`), wraps the file into a full HTML document, and deploys it
to GitHub Pages. The stamp is applied to the deployed output only — it is never committed
back to the repo.

## Commit messages

Conventional Commits, with an optional issue-id scope: `feat(#12): add KANO section` or
`docs: fix typo`. See `CLAUDE.md` for the full convention and enforcement details, and the
cheat sheet's editorial conventions.
