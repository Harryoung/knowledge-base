# Excel Routing Reference

## Bedrock Facts

- Excel files are not one format in practice. Some are plain tables, some are presentation-heavy reports.
- Reading every workbook the same way is wasteful. Large standard sheets want native tabular tooling. Small irregular sheets need structure-preserving interpretation.
- The cheapest reliable signal comes from metadata: merged cells, row count, and empty-row interruptions.

## Routing Principle

Use a lightweight scout first, then choose the heavy path.

1. Run `python scripts/complexity_analyzer.py <file_path> [sheet_name]`.
2. Inspect `recommended_strategy`.
3. Route to one of two paths.

## Path A: Pandas Mode

Use when:

- `recommended_strategy` is `pandas`
- The sheet is large
- The sheet is a standard continuous table

Workflow:

1. Read only the first 20 rows to detect the real header row.
2. Load the full sheet with Pandas using that header row.
3. Generate a short metadata summary for `README.md`.
4. Keep the original Excel file in the knowledge base. Do not convert it to Markdown.

## Path B: HTML Semantic Mode

Use when:

- `recommended_strategy` is `html`
- The workbook has deep merged cells or multiple table regions
- Layout meaning matters more than bulk row throughput

Workflow:

1. Preserve the workbook structure.
2. Describe the sheet in a semantic summary instead of pretending it is a flat table.
3. Store the original file and the generated metadata summary.

## Why This Beats Convention

Conventional handling says “always use Pandas” or “always ask the model to read everything”. Both are wrong. Pandas destroys semantic layout in complex reports, and raw full-sheet reading explodes token cost. Metadata-first routing uses the cheapest true signal, then spends effort only where justified.
