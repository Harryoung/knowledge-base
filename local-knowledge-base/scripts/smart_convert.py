#!/usr/bin/env python3
"""Smart document to Markdown converter for the local-knowledge-base skill."""

from __future__ import annotations

import argparse
import contextlib
import io
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import fitz  # PyMuPDF
import pypandoc
from pptx2md import ConversionConfig, convert as pptx2md_convert

MAC_SOFFICE_PATH = Path("/Applications/LibreOffice.app/Contents/MacOS/soffice")


def json_result(**payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2)


def count_images(image_dir: Path) -> int:
    if not image_dir.exists():
        return 0
    suffixes = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".svg", ".emf", ".wmf"}
    return sum(1 for path in image_dir.rglob("*") if path.is_file() and path.suffix.lower() in suffixes)


def is_scanned_pdf(pdf_path: Path) -> bool:
    """Treat a PDF as scanned when early pages contain images but almost no text."""
    try:
        doc = fitz.open(pdf_path)
        if len(doc) == 0:
            return False

        pages_to_check = min(3, len(doc))
        text_length = 0
        has_images = False

        for index in range(pages_to_check):
            page = doc[index]
            text_length += len(page.get_text().strip())
            has_images = has_images or bool(page.get_images())

        doc.close()
        return has_images and text_length < 50
    except Exception as exc:  # pragma: no cover - defensive fallback
        print(f"[warn] PDF scan detection failed, assuming digital PDF: {exc}", file=sys.stderr)
        return False


def get_soffice_cmd() -> str:
    """Locate LibreOffice on macOS, Windows, or PATH."""
    if shutil.which("soffice"):
        return "soffice"

    if sys.platform == "darwin" and MAC_SOFFICE_PATH.exists():
        return str(MAC_SOFFICE_PATH)

    if sys.platform == "win32":
        candidates = [
            Path(os.environ.get("PROGRAMFILES", r"C:\Program Files")) / "LibreOffice" / "program" / "soffice.exe",
            Path(os.environ.get("PROGRAMFILES(X86)", r"C:\Program Files (x86)")) / "LibreOffice" / "program" / "soffice.exe",
        ]
        for candidate in candidates:
            if candidate.exists():
                return str(candidate)

    raise FileNotFoundError(
        "LibreOffice (soffice) was not found. Install LibreOffice or add soffice to PATH."
    )


def convert_with_soffice(input_path: Path, target_ext: str) -> Path:
    print(f" -> Converting {input_path.suffix.lower()} to {target_ext} with LibreOffice...", file=sys.stderr)
    soffice_cmd = get_soffice_cmd()
    output_dir = input_path.resolve().parent
    cmd = [soffice_cmd, "--headless", "--convert-to", target_ext.lstrip("."), str(input_path.resolve()), "--outdir", str(output_dir)]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "LibreOffice conversion failed")

    candidate = input_path.with_suffix(target_ext)
    if not candidate.exists():
        raise RuntimeError(f"LibreOffice reported success but {candidate.name} was not created")
    return candidate


def process_pandoc(input_file: Path, output_file: Path, images_base_name: str | None) -> dict[str, Any]:
    media_dir_name = f"{images_base_name}_images" if images_base_name else f"{output_file.stem}_images"
    media_dir = output_file.parent / media_dir_name
    print(" -> Converting with Pandoc...", file=sys.stderr)

    pypandoc.convert_file(
        input_file,
        "markdown",
        outputfile=output_file,
        extra_args=[f"--extract-media={media_dir}", "--wrap=none", "--standalone"],
    )

    return {
        "images_dir": media_dir_name if media_dir.exists() else None,
        "image_count": count_images(media_dir),
    }


def process_pymupdf(input_file: Path, output_file: Path, images_base_name: str | None) -> dict[str, Any]:
    images_folder_name = f"{images_base_name}_images" if images_base_name else f"{output_file.stem}_images"
    print(" -> Converting digital PDF with PyMuPDF4LLM...", file=sys.stderr)
    with contextlib.redirect_stdout(io.StringIO()):
        import pymupdf4llm

    markdown_text = pymupdf4llm.to_markdown(
        str(input_file),
        write_images=True,
        image_path=images_folder_name,
        image_format="png",
    )
    output_file.write_text(markdown_text, encoding="utf-8")

    cwd_image_dir = Path.cwd().resolve() / images_folder_name
    target_image_dir = output_file.parent.resolve() / images_folder_name
    if cwd_image_dir.exists() and cwd_image_dir != target_image_dir:
        if target_image_dir.exists():
            shutil.rmtree(target_image_dir)
        shutil.move(str(cwd_image_dir), str(target_image_dir))

    image_count = count_images(target_image_dir)
    if image_count == 0 and target_image_dir.exists():
        try:
            target_image_dir.rmdir()
        except OSError:
            pass

    return {
        "images_dir": images_folder_name if target_image_dir.exists() and image_count > 0 else None,
        "image_count": image_count,
    }


def process_pptx(input_file: Path, output_file: Path, images_base_name: str | None) -> dict[str, Any]:
    images_folder_name = f"{images_base_name}_images" if images_base_name else f"{output_file.stem}_images"
    images_dir = output_file.parent / images_folder_name
    print(" -> Converting PPTX with pptx2md...", file=sys.stderr)

    images_dir.mkdir(parents=True, exist_ok=True)
    pptx2md_convert(
        ConversionConfig(
            pptx_path=input_file,
            output_path=output_file,
            image_dir=images_dir,
            disable_notes=False,
            enable_slides=True,
        )
    )

    image_count = count_images(images_dir)
    if image_count == 0:
        try:
            images_dir.rmdir()
        except OSError:
            pass

    return {
        "images_dir": images_folder_name if image_count > 0 else None,
        "image_count": image_count,
    }


def emit_scan_required(input_file: Path, output_file: Path, json_output: bool) -> int:
    message = (
        "Scanned PDF detected. Use an OCR skill such as paddleocr-doc-parsing, "
        "then onboard the OCR-generated Markdown result."
    )
    print(f" -> {message}", file=sys.stderr)
    if json_output:
        print(
            json_result(
                success=False,
                scanned=True,
                needs_ocr=True,
                error=message,
                input_file=str(input_file.resolve()),
                suggested_output=str(output_file.resolve()),
            )
        )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert DOC/DOCX/PDF/PPT/PPTX files to Markdown.")
    parser.add_argument("input", help="Input document path")
    parser.add_argument("-o", "--output", help="Output Markdown path")
    parser.add_argument("--force-ocr", action="store_true", help="Treat PDF as scanned and request OCR workflow")
    parser.add_argument("--json-output", action="store_true", help="Emit machine-readable JSON")
    parser.add_argument("--original-name", help="Original filename used for image directory naming")
    args = parser.parse_args()

    input_file = Path(args.input).expanduser()
    if not input_file.exists():
        error = f"Input file does not exist: {input_file}"
        print(f"❌ {error}", file=sys.stderr)
        if args.json_output:
            print(json_result(success=False, error=error))
        return 1

    output_file = Path(args.output).expanduser() if args.output else input_file.with_suffix(".md")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    images_base_name = Path(args.original_name).stem if args.original_name else None

    temp_converted_file: Path | None = None
    ext = input_file.suffix.lower()

    try:
        if ext == ".doc":
            temp_converted_file = convert_with_soffice(input_file, ".docx")
            info = process_pandoc(temp_converted_file, output_file, images_base_name)
        elif ext == ".docx":
            info = process_pandoc(input_file, output_file, images_base_name)
        elif ext == ".pdf":
            scanned = args.force_ocr or is_scanned_pdf(input_file)
            print(f" -> PDF type detected: {'scanned' if scanned else 'digital'}", file=sys.stderr)
            if scanned:
                return emit_scan_required(input_file, output_file, args.json_output)
            info = process_pymupdf(input_file, output_file, images_base_name)
        elif ext == ".ppt":
            temp_converted_file = convert_with_soffice(input_file, ".pptx")
            info = process_pptx(temp_converted_file, output_file, images_base_name)
        elif ext == ".pptx":
            info = process_pptx(input_file, output_file, images_base_name)
        else:
            error = f"Unsupported file format: {ext}"
            print(f"❌ {error}", file=sys.stderr)
            if args.json_output:
                print(json_result(success=False, error=error))
            return 1

        print(f"✅ Conversion succeeded: {output_file}", file=sys.stderr)
        if args.json_output:
            print(
                json_result(
                    success=True,
                    markdown_file=str(output_file.resolve()),
                    images_dir=info.get("images_dir"),
                    image_count=info.get("image_count", 0),
                    input_file=str(input_file.resolve()),
                )
            )
        return 0
    except Exception as exc:
        print(f"❌ Conversion failed: {exc}", file=sys.stderr)
        if args.json_output:
            print(json_result(success=False, error=str(exc), input_file=str(input_file.resolve())))
        return 1
    finally:
        if temp_converted_file and temp_converted_file.exists():
            temp_converted_file.unlink()


if __name__ == "__main__":
    raise SystemExit(main())
