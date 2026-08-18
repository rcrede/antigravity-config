---
name: typst-academic-standard
description: Strict academic typesetting standards for Typst documents. Focuses on structural semantics and delegates visual styling entirely to the selected template.
date created: 2026-06-19T03:16:44+02:00
date modified: 2026-07-09T23:59:12+02:00
---

## Typst Academic Standard

When drafting or updating Typst documents for scientific reports, you MUST adhere to strict structural semantics while deferring visual formatting to the provided template.

### 1. Zero Visual Overrides (Template Delegation)

You MUST NOT use global layout overrides unless explicitly requested by the user.

- Do **not** use `#set page(...)` or `#set text(...)`.
- Do **not** use `#set heading(...)`.
- Do **not** use `#show figure: ...` to override captions.
- Rely entirely on the `#import` and `#show: project.with(...)` commands provided in the document preamble.

#### Fallback Template

If the user does not provide a specific journal template (e.g., `neurips_template.typ`), you MUST explicitly import the user's default fallback template which encodes their personal layout preferences (tight subfigures, no TOC, explicit numbering):

```typst
#import "/home/rcrede/Documents/Obsidian Vault/80_System/Templates/Publishing/rcrede_default_template.typ": *
#show: project.with(
  title: "...",
  authors: (...),
)
```

### 2. Figures and Visuals

- Always wrap images in the native figure block: `#figure(image("path.svg", width: 80%), caption: [Your caption])`.
- **DO NOT BAKE LABELS**: Never bake subfigure tags (e.g., `(a)`, `(b)`) into SVG plots using Python. The Typst template handles all numbering and lettering.
- Do not hardcode "Figure X:" in the caption text. The template's `#show figure` rule will handle numbering and prefixes automatically.

### 3. Cross-Referencing

- Use Typst's native referencing system. To reference a figure or equation, attach a label `<my_label>` and reference it with `@my_label`.
- The template determines if this renders as "Fig. 1", "Figure 1", or "fig. 1". (Note: The prose around it must follow the `scientific_writing_style.md` standard for parenthetical references).

### 4. Tables

- Construct tables using the native `#table()` function, or `#figure(table(...))` if they require captions.
- Extract data dynamically from `ara/evidence/` rather than hardcoding static data if possible.
