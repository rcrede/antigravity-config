---
name: markitdown-extractor
description: Extracts full-text Markdown from PDFs and other documents using Microsoft MarkItDown via Pixi. Use this as the first step in the Agentic Literature Pipeline to convert Zotero PDFs into Raw Markdown.
---

# markitdown-extractor

This skill converts PDF documents into high-quality Raw Markdown using Microsoft's MarkItDown library. It preserves tables, equations, and structural elements better than traditional OCR tools.

## Prerequisites
1. The input file can be an absolute or relative path to the downloaded PDF.

## Usage Instructions

### Execution Steps

### 1. Execute Extraction
- Identify the target file(s) to process.
- **MANDATORY**: Run the provided extraction script located at `scripts/extract.sh <path_to_input> <path_to_output>`. 
- **DO NOT** use `uvx` or global `pip install` directly. The `extract.sh` script relies on an isolated `pixi` environment defined in `scripts/pixi.toml` to safely execute MarkItDown.
- Check `standards/markitdown_extractor_standard.md` for specific formatting rules.

2. **Handle Output:**
   - The resulting `.md` file should be placed in the user's Raw Markdown directory (e.g., `50_Literature/raw/`).
   - Ensure the filename cleanly represents the paper (e.g., `Author_Year_Title.md`).
3. **Return:**
   - Yield the absolute path of the generated Raw Markdown file back to the orchestrating agent or the user so it can be passed to the `dual-sided-compiler`.
