# Document Format Processing Details

## DOCX/DOC

### Processing Method
- **DOCX**: Directly use Pandoc conversion
- **DOC**: First convert to DOCX using LibreOffice, then Pandoc processing

### Features
- Preserve formatting (headings, lists, tables)
- Automatically extract images to separate directory
- Preserve links and references

### Image Directory
```
original_filename_images/
├── image1.png
├── image2.jpg
└── ...
```

---

## PDF

### Automatic Type Detection

Script automatically detects PDF type:
- **Electronic**: High text density in first 3 pages (text can be directly extracted)
- **Scanned**: First 3 pages have almost no text but have images

### Electronic PDF
- Use PyMuPDF4LLM for fast conversion
- Second-level processing
- Preserve document structure

### Scanned PDF
- `scripts/smart_convert.py` does not OCR scanned PDFs itself
- It returns `needs_ocr: true` in JSON output
- The calling workflow must invoke `https://clawhub.ai/Bobholamovic/paddleocr-doc-parsing`
- Do not describe the dependency as a generic OCR-capable skill; scanned PDF OCR in this project depends on `paddleocr-doc-parsing`
- If the skill is not installed, stop and report the blocker clearly
- Tell the user that the required free API token can be created at `https://aistudio.baidu.com/account/accessToken`
- If the user has no AI Studio account yet, tell them to register first
- Tell the user the daily free quota is typically enough for personal day-to-day use

### Force OCR Mode
```bash
python scripts/smart_convert.py input.pdf --force-ocr --json-output
```

---

## PPTX/PPT

### Processing Method
- **PPTX**: Use pptx2md professional conversion
- **PPT**: First convert to PPTX using LibreOffice, then pptx2md processing

### Features
- Preserve heading hierarchy
- Preserve list formatting
- Extract slide images
- Preserve notes (Speaker Notes)
- Add slide separators

### Output Structure
```markdown
# Slide Title

Slide content...

![](original_filename_images/slide1_image1.png)

---

# Next Slide Title
...
```

---

## Windows Notes

- `.doc` and `.ppt` conversion require LibreOffice
- Typical Windows lookup paths:
  - `C:\Program Files\LibreOffice\program\soffice.exe`
  - `C:\Program Files (x86)\LibreOffice\program\soffice.exe`
- Pass `--original-name` when the uploaded filename is a temporary path, especially for Chinese filenames

## Dependencies

| Library | Purpose |
|---------|---------|
| pypandoc | DOCX → Markdown |
| PyMuPDF (fitz) | PDF type detection |
| pymupdf4llm | Electronic PDF conversion |
| pptx2md | PPTX conversion |

---

## Error Handling

### LibreOffice Not Installed
```
LibreOffice (soffice) not found. Please install LibreOffice or add it to PATH.
```

### OCR Skill Missing For Scanned PDF
```
Scanned PDF detected. This project explicitly depends on https://clawhub.ai/Bobholamovic/paddleocr-doc-parsing for OCR. Install and configure that Skill first, then onboard the OCR-generated Markdown result. The required free API token can be created at https://aistudio.baidu.com/account/accessToken (register an AI Studio account first if needed).
```

### Unsupported Format
```
Unsupported file format: .xyz
```
