# CLAUDE.md

This repo holds the Advanced Requirements Engineering (ARE) cheat sheet:
`cheatsheet-body.html`, a German-language HTML
*fragment* (no `<!doctype>`, `<html>`, `<head>` or `<body>`). It is the only source file.
`.github/workflows/deploy.yml` wraps it into a full document and publishes it to GitHub
Pages on every push to `main`.

**Everything in this repo is English — code, comments, filenames, commit messages, this
file — except the cheat sheet's own content**, which is German (see "Language split").

## Deploy and versioning

Handled entirely in CI; there is nothing to build or install locally.

- `deploy.yml` stamps `<span>Version: …</span>` in `footer.colophon` with the UTC timestamp
  plus short commit hash, wraps the fragment, and writes `dist/cheat-sheet/index.html` plus
  a generated root redirect page. There is no committed `index.html`.
- The stamp exists only in the deployed output and is never committed back, so the value in
  git is always a placeholder. That is expected.
- The workflow matches the span literally via `sed` (`<span>Version: [^<]*</span>`). Keep
  that exact markup — a changed footer structure breaks stamping **silently**, with no error.
- GitHub Pages must stay configured with source **"GitHub Actions"**, not "Deploy from a
  branch", or the workflow cannot publish.

## Editing the fragment

- The file must stay a fragment, and it opens with a bare `<title>` — the wrapper adds none,
  so do not remove it and do not add a second.
- Fully self-contained: **no external** CSS, scripts, images or web fonts. One inline
  `<script>` (Format-Finder, panel toggle, scrollspy) and one inline `<style>`.
- Themes come from `prefers-color-scheme` plus `data-theme="light"/"dark"` on the root
  element. Nothing in the page sets that attribute — on GitHub Pages only the system setting
  applies unless a switcher is added.
- `input.svg` is a Lucidchart export of the original overview drawing, kept for reference
  only. Nothing in the build reads it.

## Editorial rules not stated in the page

- **No company name** anywhere in the text. The proprietary Sub-System Requirement is
  described neutrally ("proprietär" / "manche Organisationen").
- **"Story" never stands alone** — always "User Story". The only exceptions are SAFe's own
  term in the Enabler card and the `ENABLER STORY` label in the structure panel.
- **Language split.** The document is German. Established terminology stays English and
  untranslated (Acceptance Criteria, Imperative, Trigger, Normal/Peak/Overload, Error Case,
  Refinement, Constraint, the three category names). Explanatory and connective vocabulary
  stays German (Betriebszustand, Nutzerinteraktion, Wertebereich, Ausarbeitung, Prüffrage).

## SVG and panel mechanics

- `.we` renders its label via `::before { content: "WE" }` — write it as an empty
  `<span class="we"></span>`. Inside SVG, use the separate `.we-svg` rect+text pattern.
- The structure panel toggles via `data-view="base"|"prop"` on `#modelpanel`; `.only-base` /
  `.only-prop` show and hide the two variants, and the prose for each lives in `PNOTES` in
  the inline script. Anything added to that diagram needs a decision about which view it
  belongs to, and `PNOTES` must be updated alongside it.
- In that panel SAFe and ISO sit in two separate shaded `.side` fields. Only the `d-map` ≙
  lines may cross the boundary.
- The System Boundaries and Domain Model sections use **this cheat sheet itself** as their
  worked example — its actors, neighbour systems, and its own building blocks (Abschnitt,
  Baustein, Tabelle/Diagramm/Karte, Requirement-Typ). Adding or removing a section, or a new
  kind of block, makes those two diagrams wrong. Update them together.
- Check SVG geometry arithmetically, not by rendering: estimate text width from character
  count (~0.62 × font-size for monospace) and test for collisions and box overflow.
  Rendering the SVGs standalone is useless — their CSS classes come from the page stylesheet.

## Commit messages

Conventional Commits with an optional issue-id scope (`feat(#12): …` or `docs: …`), enforced
by commit-check via `commit-check.toml` and `.github/workflows/commit-lint.yml`.

- The format is a hard gate. The `#N` scope is not: `scripts/check-issue-scope.py` only
  warns and always exits 0. Most commits here aren't tied to an issue, and that's fine.
- `pre-commit install` wires the same checks into a local `commit-msg` hook. Optional —
  nothing else depends on it.
- Direct pushes to `main` are fine; there is no PR requirement. Deploy triggers on `main` only.

## Site layout

The sheet deploys under `/cheat-sheet/`, not the site root; the root is a generated redirect
page built inline in `deploy.yml`. To add a second variant, give it its own source fragment
and its own `dist/<slug>/` build step, and turn the root page into a real chooser instead of
an auto-redirect.

## External references

Behind the Constraint discussion: Bass/Clements/Kazman ("a design decision with zero degrees
of freedom"), the Volere template, IREB CPRE Foundation, INCOSE GtWR.
