---
name: scientific-plotting-standard
description: >-
  Strict best practices for creating accessible, publication-ready scientific figures using Matplotlib and Seaborn.
  Enforces vector graphics, dynamic sizing matching the document, and colorblind-safe palettes.
date created: 2026-06-19T00:11:24+02:00
date modified: 2026-07-15T20:24:39+02:00
---

## Scientific Plotting Standard

When generating plots or visualizations using Python (`matplotlib`, `seaborn`), you MUST strictly adhere to the following publication-quality standards.

### 1. Core Plotting Guidelines (The Chameleon Rule)

NaN) **Format**: All generated scientific plots MUST be saved as infinite-scale vector graphics (`.svg`). Absolutely no `.png` files.

NaN) **Dynamic Sizing**: You must achieve exact 1:1 scaling between Matplotlib and the document processor. DO NOT hardcode a static dimension like `78mm`.

   - **Extract Target Dimensions:** Look up the exact column width or text width from the target publication's guidelines or the Typst template.
   - **Conversion:** Matplotlib uses inches. Divide metric millimeters by 25.4 (e.g., `figsize=(target_width / 25.4, height / 25.4)`).
   - **Disable BBox:** NEVER use `bbox_inches="tight"` in `savefig()`, as it unpredictably crops the canvas and breaks 1:1 scaling. Use `fig.tight_layout(pad=0.1)` instead.
NaN) **No Baked Labels**: NEVER bake subfigure labels (e.g., "a)", "(Fig. 1a)") directly into the SVG plot. The document processor (e.g., Typst) handles all figure numbering and subfigure tags to ensure perfect grid alignment.

### 2. Typography

The plot must seamlessly adopt the typography of the document it is embedded in.

NaN) **SVG Font Agnosticism:** You MUST configure Matplotlib to embed SVG text correctly without converting to paths:

   ```python
   plt.rc(group="svg", fonttype="none")
   ```

   This guarantees that when Typst or LaTeX renders the SVG, it applies its own global font to the text nodes, achieving perfect typographic harmony.

NaN) **Fallback Font (Static rendering):** If the plot must be rendered to a static PDF where agnosticism isn't possible, use the preferred font **Luciole** (or **Luciole Math**).

NaN) **Dynamic Text Sizing:** Plot text size MUST scale to match the font size of the respective paper perfectly. Only use `9pt` as a default fallback if the target size is unknown.

### 3. Accessible Palettes

Color is critical for accessibility. Do not use default Matplotlib colors (tab10) or red/green combinations.

- **Discrete/Categorical Data:** You MUST use the **Okabe-Ito** colorblind-safe palette.
    - Hex Codes: `#000000` (Black), `#E69F00` (Orange), `#56B4E9` (Sky Blue), `#009E73` (Bluish Green), `#F0E442` (Yellow), `#0072B2` (Blue), `#D55E00` (Vermilion), `#CC79A7` (Reddish Purple).
- **Continuous Data:** You MUST use the **magma** colormap. If contrast issues arise, `cividis` or `viridis` may be used as fallbacks.

### 4. Implementation Example

```python
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.axes import Axes

# Explicit Okabe-Ito Colorblind Safe Palette
OKABE_ITO = ["#000000", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7"]

def generate_figure(df: pd.DataFrame, target_width_mm: float = 78.0) -> None:
    # Font Agnosticism (Chameleon Rule)
    plt.rc(group="svg", fonttype="none")
    plt.rc(group="font", size=9) # Fallback size, dynamically adjust to document
    plt.rc(group="axes", prop_cycle=plt.cycler(color=OKABE_ITO))

    # Convert mm to inches for exact scaling
    width_in = target_width_mm / 25.4
    height_in = (target_width_mm * 0.75) / 25.4 # Example 4:3 aspect ratio
    
    fig, ax = plt.subplots(figsize=(width_in, height_in))
    
    # ... plotting logic ...
    
    # Minimalist adjustments
    ax.grid(False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Vector output using strict pad, NEVER bbox_inches="tight"
    fig.tight_layout(pad=0.1)
    plt.savefig("results/figure.svg", format="svg")
    plt.close(fig)
```
