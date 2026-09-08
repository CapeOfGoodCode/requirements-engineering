# Advanced Requirements Engineering Cheat Sheet

[![Lint commit message](https://github.com/CapeOfGoodCode/requirements-engineering/actions/workflows/commit-lint.yml/badge.svg)](https://github.com/CapeOfGoodCode/requirements-engineering/actions/workflows/commit-lint.yml)

This is the cheat sheet for the "Advanced Requirements Engineering" training. It maps
Requirement types to SAFe and ISO/IEC/IEEE 29148, shows the formats used at each level, and
covers decomposition, classification, and KANO.

Two variants are published, and the site root is a chooser between them:

- Cheat sheet — https://capeofgoodcode.github.io/requirements-engineering/cheat-sheet/
- Poster — https://capeofgoodcode.github.io/requirements-engineering/poster/, the condensed
  version on one sheet, alongside a print-ready A1 PDF at
  [`poster/are-poster-a1.pdf`](https://capeofgoodcode.github.io/requirements-engineering/poster/are-poster-a1.pdf)
- Cheat sheet in English — https://capeofgoodcode.github.io/requirements-engineering/en/cheat-sheet/
- Poster in English — https://capeofgoodcode.github.io/requirements-engineering/en/poster/,
  with its own [A1 PDF](https://capeofgoodcode.github.io/requirements-engineering/en/poster/are-poster-a1.pdf)

## Setup

Nothing required. Editing any of the four source fragments and pushing to `main`
is all that's needed — deployment, versioning, and the PDF happen in CI.

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
