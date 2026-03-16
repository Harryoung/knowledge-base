# Ingestion Workflow

## Assumptions To Challenge

- File extension alone is not enough to decide the final storage location.
- Converting everything to Markdown is not always correct. Excel should usually remain in its original format.
- “No conflict by filename” means nothing. Conflict is semantic, not lexical.

## Stage 1: Reception And Validation

1. Confirm the user wants to onboard the file into the knowledge base.
2. Resolve the configured KB path with `python scripts/kb_config.py --get`.
3. Inspect file type from extension and actual content when needed.
4. If the file is already Markdown or plain text, skip conversion.

## Stage 2: Format Conversion

### DOCX / DOC / PDF / PPTX / PPT

Run:

```bash
python scripts/smart_convert.py <file_path> --original-name "<original_filename>" --json-output
```

Interpret the JSON:

- `success: true`: use `markdown_file` and optional `images_dir`
- `needs_ocr: true`: scanned PDF detected, pause normal ingestion and call an OCR skill if available
- `success: false` without `needs_ocr`: stop and report the conversion error

### Excel / CSV

Run:

```bash
python scripts/complexity_analyzer.py <file_path>
```

Keep the original spreadsheet. Generate only a metadata description and route according to [EXCEL_ROUTING.md](./EXCEL_ROUTING.md).

## Stage 3: Semantic Conflict Detection

1. Read `README.md` to understand the current directory map.
2. Read candidate neighboring files.
3. Judge overlap by meaning:
   - Is this a new source of truth?
   - Is it a duplicate in another format?
   - Does it conflict with an existing policy or procedure?
4. If there is material conflict, stop and tell the user exactly which files disagree.

## Stage 4: Intelligent Filing

1. Decide location by document purpose, audience, and topic.
2. Prefer stable category directories over one-off dumping grounds.
3. For large topics, create subdirectories instead of bloating the root.

## Stage 5: Write And Update

1. Move the converted Markdown file or original spreadsheet into the chosen directory.
2. Move the image directory beside the Markdown file when present.
3. For large Markdown files, create an overview file using [TOC_TEMPLATE.md](./TOC_TEMPLATE.md).
4. Update `README.md`:
   - directory tree
   - file size
   - short description
   - overview link when applicable

## Windows Notes

- Always pass `--original-name` when the upload temp filename is opaque. This preserves readable image folder names for Chinese filenames.
- For `.doc` and `.ppt`, LibreOffice is optional but required if those legacy formats must be converted.
- If scanned PDF OCR is blocked because no OCR skill exists, stop and tell the user the exact blocker instead of pretending conversion succeeded.
