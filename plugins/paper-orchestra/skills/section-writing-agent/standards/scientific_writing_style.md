---
name: scientific-writing-style
description: >-
  Applies a rigorous, data-centric writing style for drafting and editing scientific texts. Eliminates AI-isms, uses the Known/New Contract for logical flow, and mandates specific formatting for Methods and Conclusion sections.
date created: 2026-06-15T15:20:30+02:00
date modified: 2026-07-15T20:23:42+02:00
---

## Scientific Writing Style

### Overview

This instruction-only skill ensures that the agent adopts a rigorous, objective, and highly readable writing style when drafting or editing scientific papers. It enforces the "Known/New Contract" for seamless sentence flow and actively suppresses common LLM clichés and pretentious narrative framing.

### Dependencies

None.

### Quick Start

When a user asks you to "write a scientific abstract," "draft a methods section," or "apply the scientific writing style to this text," immediately adopt the rules outlined in the Workflow below.

### Workflow

#### 1. Adopt the Tone and Voice (Empirical Precision)

- **Data-Centric Focus:** Focus solely on direct observations and verifiable data. Prioritize specific numbers and relationships extracted from datasets or figures. Avoid interpretive fluff.
- **Objective Professionalism:** Maintain a clinically neutral tone. Do NOT "celebrate" findings; report them. Do not use hyperbolic or pretentious framing (e.g., avoid "critical gap", "challenge", "profound").
- **Attribution & Neutrality:** Attribute all claims to specific sources or explicit data points. Avoid "weasel words" like "experts suggest" or "it is believed."
- **Analytical Voice:** When expressing interpretations or conclusions, use the passive voice or phrases like "It is the authors' opinion that..." instead of the active "we".
- **No Moralizing:** Do not end sections with statements like "It is important to remember" or preach about the "significance" of a topic unless the data explicitly supports a quantitative measure of significance.

#### 2. Apply the Known/New Contract (Sentence-Level Flow)

- **Subject-Predicate Chaining:** Eliminate traditional transition words ("Moreover", "Furthermore", "Additionally", "However" at the start of sentences).
- **Information Hierarchy:** Structure sentences so that they begin with "Known" information (concepts established in the previous sentence) and end with "New" information (novel data or claims). The end of one sentence should seamlessly link to the subject of the next.

### In-Text Citations & Figures

NaN) **References:** Use bracketed inline citations (e.g. [1]) or standard format based on the style guide. Avoid narrative citation framing ("As Smith et al. demonstrated [1]"). Let the claim stand on its own, followed by the reference.

NaN) **Visual & Math Grounding:** When referencing a chart, image, or equation, specify the location explicitly in parentheses. NEVER mention figures or equations directly as the subject of the prose (e.g., "Figure 1a shows..."). Always make the scientific claim directly, grounded in the numbers or logic, followed by the specific parenthetical reference formatted exactly as **`(Fig. 1)`**, **`(Fig. 1a)`**, or **`(Eq. 1)`**. Do NOT spell out "Figure" or "Equation" inside the prose.

#### 3. Handle Section-Specific Rules

**Introductions:**

NaN) **Literature Grounding:** Never write an introduction straight away. First, define the conceptual points to cover, and then conduct a literature search (using skills like PubMed or OpenAlex) to ground all introductory claims in factually correct review studies or meta-analyses. Avoid hallucinating generalities (e.g., "MD lacks chemical accuracy"); instead, cite specific limitations with empirical boundaries.

**Methods:**

NaN) **Narrative Framing:** Briefly explain *why* the specific methods were chosen and why they are appropriate for the research goals. Use the Known/New contract for flow.

NaN) **Procedural Recipe:** Provide the actual steps for reproduction. For this procedural part, **strictly use only main clauses**. Do not use subordinate or dependent clauses. Keep sentences extremely direct and simple (e.g., "The protein was crystallized. The temperature was maintained at 300K.").

#### 4. Filter Banned Vocabulary

Strictly avoid using any of the following:

- **AI-isms & Metaphors:** "Delve," "leverage," "tapestry," "landscape," "realm," "testament," "game-changer," "cornerstone."
- **Adjectives:** "Robust," "crucial," "pivotal," "dynamic," "vibrant."
- **Pretentious Framing:** "Challenge," "critical gap," "profound."
- **Transitions:** "Moreover," "Furthermore," "In addition," "It is worth noting that," "However" (at the start of sentences).

### Typography Size Chart

When writing and generating documents (e.g., in Typst), you must adhere to the following sizes:

- **Font Family**: `Atkinson Hyperlegible Next`
- **Document Title**: 16pt, Bold. Only use this once at the top of the document.
- **Section Title (H1)**: 14pt, Bold. Leave ample whitespace above it.
- **Subsection (H2)**: 12pt, Bold.
- **Prose (Body Text)**: 11pt, Regular weight.
- **Table & Figure Content**: 9pt. Drop the size slightly below the prose to separate data from narrative text.
- **Captions / Legends**: 9pt, Regular or Italic.
- **Footnotes / Subscripts**: 8pt. The absolute floor for print legibility. Do not go smaller.
- **Math Typography**: When using Atkinson Hyperlegible Next for prose, mathematical formulas can drown out if rendered in geometric sans-serif fonts. Use **`New Computer Modern Math`** for all math equations to provide a distinct, recognizable serif hierarchy. To match the heavy stroke weight of Atkinson, explicitly load the **Book Weight** (`NewCMMath-Book.otf`) of New Computer Modern via a local `fonts/` directory and configure Typst to load it with `--font-path fonts`.

### Common Mistakes

NaN) **Forgetting the Methods Split:** Writing the entire methods section as a narrative instead of separating the "why" (narrative) from the "how" (strict main-clause recipe).

NaN) **Using Transition Words:** Falling back on "Moreover" or "Additionally" instead of rewriting the sentence to follow the Known/New chaining structure.

NaN) **Rehashing Results in Conclusion:** Wasting the conclusion by restating the findings instead of providing analytical judgment in the passive voice.
