# CLAUDE.md

This repo holds the Advanced Requirements Engineering (ARE) teaching material as two
German-language HTML *fragments* (no `<!doctype>`, `<html>`, `<head>` or `<body>`):
`cheatsheet-body.html`, the full sheet, and `poster-body.html`, a condensed A1 poster,
plus `poster-body.en.html`, the poster's English translation. They are the only source
files. `.github/workflows/deploy.yml` wraps each into a full
document and publishes both to GitHub Pages on every push to `main`.

**Everything in this repo is English — code, comments, filenames, commit messages, this
file — except what the sheet and the poster themselves say**, which is German (see
"Language split").

## Deploy and versioning

Handled entirely in CI; there is nothing to build or install locally.

- `deploy.yml` stamps `<span>Version: …</span>` in `footer.colophon` with the UTC timestamp
  plus short commit hash, wraps each fragment, and writes `dist/cheat-sheet/index.html`,
  `dist/poster/index.html`, the poster's PDF, and a generated root chooser page. Nothing
  built is committed — there is no `index.html` and no PDF in git.
- The stamp exists only in the deployed output and is never committed back, so the value in
  git is always a placeholder. That is expected.
- The workflow matches the span literally via `sed` (`<span>Version: [^<]*</span>`). Keep
  that exact markup — a changed footer structure breaks stamping **silently**, with no error.
- GitHub Pages must stay configured with source **"GitHub Actions"**, not "Deploy from a
  branch", or the workflow cannot publish.

## Editing the fragments

- Each file must stay a fragment, and each opens with a bare `<title>` — the wrapper adds none,
  so do not remove it and do not add a second.
- Fully self-contained: **no external** CSS, scripts, images or web fonts. One inline
  `<script>` (Format-Finder, panel toggle, scrollspy) and one inline `<style>`.
- Themes come from `prefers-color-scheme` plus `data-theme="light"/"dark"` on the root
  element. Nothing in the page sets that attribute — on GitHub Pages only the system setting
  applies unless a switcher is added.
- `input.svg` is a Lucidchart export of the original overview drawing, kept for reference
  only. Nothing in the build reads it.

## Editorial rules not stated in the page

- **No customer's company name** anywhere in the text. The proprietary Sub-System
  Requirement is described neutrally ("proprietär" / "manche Organisationen"). This is
  about the organisations whose practices are described — the publisher's own name and
  logo are a different matter and appear in the poster's colophon.
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

- **One editorial change per commit.** The body is optional — a self-explanatory subject
  needs none. But where the subject does not carry the reasoning, the body argues *why*: what
  prompted the change and what it buys the reader. The sheet is a teaching artifact whose
  wording is the product, so a diff alone often does not explain itself later.
- **Which type applies.** The sheet is the product, not documentation *about* a product, so
  changes to it are `feat` — rewording included, because a sheet that reads better is the
  improvement itself. `fix` is for what the sheet got wrong or contradicted; an unclear
  sentence is not a defect. `docs` is reserved for the repo's own documentation — this file,
  the README. `style` and `refactor` cover markup and presentation that change nothing the
  reader takes away, `ci` and `build` the pipeline.
- The format is a hard gate. The `#N` scope is not: `scripts/check-issue-scope.py` only
  warns and always exits 0. Most commits here aren't tied to an issue, and that's fine.
- `pre-commit install` wires the same checks into a local `commit-msg` hook. Optional —
  nothing else depends on it.
- Direct pushes to `main` are fine; there is no PR requirement. Deploy triggers on `main` only.

## Site layout

Neither variant sits at the site root. The sheet deploys under `/cheat-sheet/`, the poster
under `/poster/`, its English translation under `/en/poster/`, and the root is a generated
chooser page built inline in `deploy.yml`. A new variant or language is one more `build`
call in the "Stamp and assemble every variant" step plus an entry in that chooser.

**German keeps the unprefixed paths and always will.** The poster prints its own URL in its
colophon, so once a copy is on a wall that path can never move. English is prefixed for the
same reason — symmetry would have cost two permanent redirects.

## The poster

`poster-body.html` is a fixed 2245 x 3179 px canvas — exactly A1 at 96 dpi — that must stay
on **one page**. It carries its own stylesheet and shares no CSS with the cheat sheet, so a
token renamed in one does not follow into the other.

- **Overflow is silent.** The canvas sets `overflow: hidden`, so content that outgrows a
  column is cut off with no error and no visible sign. Never judge a change by eye; run
  `scripts/check-poster-layout.py <chrome> <built-html>`, which measures column capacity and
  every SVG label against its viewBox from inside the rendered page. CI runs it as a hard
  gate before the PDF is built.
- **The three columns are packed by height, not by theme.** Formate (871 px) and KANO
  (875 px) each fit only alongside one of the two small blocks, which forces Dekomposition
  and Klassifikation to share a column. Any block that grows re-opens that packing.
- **Numbering encodes the reading order**, which runs left to right across the top three
  blocks and then across the bottom three — not down each column. Moving a block means
  renumbering.
- **Print only, single theme.** No dark mode: the poster is a print deliverable, and a dark
  variant would waste toner. Colours are painted explicitly rather than inherited.
- **The logo is a colophon mark in both artefacts.** In the cheat sheet it needs a light
  plate in dark mode: the wordmark is fixed brand violet and unreadable on the dark ground,
  and recolouring someone else's logo is not ours to do. The plate is `content-box`, so it
  grows outward instead of shrinking the mark to a different size per theme.
- **In the poster it costs layout height.** It is embedded as a base64
  data URI to keep the fragment self-contained, downscaled to 400px wide and quantised to
  128 colours — the untouched PNG would have been 98KB of base64 in a 40KB file. At 130px
  it is taller than the colophon's text line, which is why the sheet's bottom padding was
  reduced to pay for it. Enlarging it means finding that height somewhere else.
- **Print rules live at the end of the stylesheet.** They are single-class
  selectors, so a component rule further down outranks them at equal specificity
  — which is how the screen-only buttons once ended up in the PDF. Anything added
  after them silently wins.
- **The preview scale never touches inline styles.** The fit script sets only a
  `--fit` custom property; the geometry is a `@media screen` rule. Written inline
  it survives into print, where it shifts the sheet off the paper and crops a
  third of it while still reporting one correctly sized A1 page.
- **The PDF is checked for coverage, not just size.** `scripts/check-poster-pdf.py`
  measures where the ink actually lands, because a cropped sheet still passes a
  page-count and page-size check.
- **The PDF needs `--headless=new`.** The old headless mode ignores `@page { size }` and
  emits a Letter page that still reports as one page, cropping the poster in silence. The
  workflow asserts the page size in points as well as the page count.
- **CI installs metric-compatible fonts.** The stack names Segoe UI, Palatino Linotype and
  Cascadia Mono; the runner has none of the first two, so `deploy.yml` installs Selawik and
  P052 and aliases them through fontconfig. Changing the font stack means changing that step
  too, or the layout check will fail.

## Translations

`poster-body.en.html` is derived from the German poster by replacing prose only: the markup,
the SVG geometry and every class name stay identical, so the two files diff cleanly against
each other. Keep it that way — a structural change belongs in both.

- **Terminology comes from the course slides**, not from translating the German back. The
  three ladder examples are the slides' own sentences verbatim.
- **A translation re-flows the fixed canvas.** English is not uniformly shorter: the first
  English draft overran column 1 by 6px and two diagram labels by a unit, because different
  words wrap differently. Run the layout check on every language, which CI does.
- **Established terms stay put** (Acceptance Criteria, Use Case, shall/should/will), but
  German compound hyphenation does not survive: `User-Story-Format` becomes `User-Story
  format`. US spelling throughout, to match Artifact and the other source terms.
- The language switcher names languages, never flags — a flag denotes a country, and neither
  language belongs to one.

## External references

Behind the Constraint discussion: Bass/Clements/Kazman ("a design decision with zero degrees
of freedom"), the Volere template, IREB CPRE Foundation, INCOSE GtWR.
