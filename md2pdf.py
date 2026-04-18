#!/usr/bin/env python3

import argparse
import subprocess
import tempfile
from pathlib import Path
import sys
import shutil


# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------

_BASE_CSS = """
@page {{ margin: {page_margin}; }}

body {{
    margin: 0;
    padding: {body_padding};
    background: {bg};
    color: {fg};
    font-family: Inconsolata, monospace;
    line-height: 1.6;
}}

h1, h2, h3 {{
     color: {heading};
     break-after: avoid;
     page-break-after: avoid;
}}

pre, code {{
    background: {code_bg};
    padding: 0.4em;
    border-radius: 6px;
    break-inside: avoid;
    page-break-inside: avoid;
}}

a {{ color: {link}; }}

blockquote {{
    border-left: 4px solid #888;
    margin: 1em 0;
    padding: 0.5em 1em;
    font-style: italic;
    background: {code_bg};
    break-inside: avoid;
    page-break-inside: avoid;
}}

table {{
    border-collapse: collapse;
    width: 100%;
    margin: 1em 0;
}}

th, td {{
    border: 1px solid #888;
    padding: 0.5em;
    text-align: left;
}}

th {{ background: {code_bg}; }}

ol {{ padding-left: 2em; }}
ol ol {{ list-style-type: lower-alpha; }}
ol ol ol {{ list-style-type: lower-roman; }}

hr {{
    border: none;
    border-top: 1px solid #888;
    margin: 1.5em 0;
}}

dl {{ width: 100%; margin: 1em 0; }}
dt {{ font-weight: bold; margin-top: 0.5em; }}
dd {{ margin: 0; padding-left: 1.5em; }}

figcaption {{
    font-size: 0.85em;
    color: #888;
    text-align: center;
    margin-top: 0.3em;
}}
"""

_THEME_OVERRIDES = {
    "dark": {
        "page_margin": "0",
        "body_padding": "2cm",
        "bg": "#3b3b3b",
        "fg": "#f5f5f5",
        "heading": "#ffffff",
        "code_bg": "#2b2b2b",
        "link": "#8ab4f8",
    },
    "light": {
        "page_margin": "1.5cm",
        "body_padding": "1.5cm",
        "bg": "#ffffff",
        "fg": "#1a1a1a",
        "heading": "#1a1a1a",
        "code_bg": "#f4f4f4",
        "link": "#1a73e8",
    },
}

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

HIGHLIGHT_STYLES = {"dark": "breezeDark", "light": "pygments"}

CHROMIUM_CANDIDATES = [
    "chromium",
    "chromium-browser",
    "google-chrome-stable",
    "google-chrome",
]

DISK_CACHE_MAX = 50 * 1024 * 1024  # 50 MB

PANDOC_FORMAT = "markdown-simple_tables-multiline_tables-grid_tables"


# ---------------------------------------------------------------------------
# Functions
# ---------------------------------------------------------------------------

def find_chromium():
    for name in CHROMIUM_CANDIDATES:
        path = shutil.which(name)
        if path:
            return path
    raise FileNotFoundError(
        "No Chromium/Chrome binary found. "
        f"Searched: {', '.join(CHROMIUM_CANDIDATES)}"
    )


def run(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        result.check_returncode()


def validate_args(md_path, pdf_path):
    if md_path.suffix.lower() != ".md":
        raise ValueError(
            f"Input file must be .md, got: '{md_path.name}'"
        )
    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError(
            f"Output file must be .pdf, got: '{pdf_path.name}'"
        )
    if not md_path.is_file():
        raise FileNotFoundError(f"Input file not found: {md_path}")
    if pdf_path.exists():
        response = input(
            f"'{pdf_path.name}' already exists. Overwrite? [y/N] "
        )
        if response.lower() != "y":
            raise SystemExit("Aborted.")


def build_css(theme):
    return _BASE_CSS.format(**_THEME_OVERRIDES[theme])


def convert(md_path, pdf_path, theme="dark"):
    md_path = Path(md_path).resolve()
    pdf_path = Path(pdf_path).resolve()

    validate_args(md_path, pdf_path)

    css = build_css(theme)
    highlight = HIGHLIGHT_STYLES[theme]
    chromium = find_chromium()

    with tempfile.TemporaryDirectory(prefix="md2pdf_") as workdir:
        workdir = Path(workdir)
        html_file = workdir / "out.html"
        css_file = workdir / "style.css"

        css_file.write_text(css)

        run([
            "pandoc",
            str(md_path),
            "-f", PANDOC_FORMAT,
            "-o", str(html_file),
            "--standalone",
            "--embed-resources",
            "--css", str(css_file),
            f"--highlight-style={highlight}",
        ])

        run([
            chromium,
            "--headless",
            "--disable-gpu",
            "--no-first-run",
            "--no-default-browser-check",
            "--no-pdf-header-footer",
            f"--print-to-pdf={pdf_path}",
            f"--user-data-dir={workdir / 'chromium-profile'}",
            f"--disk-cache-dir={workdir / 'chromium-cache'}",
            f"--disk-cache-size={DISK_CACHE_MAX}",
            str(html_file),
        ])

    print(f"✔ PDF created: {pdf_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Convert Markdown to styled PDF"
    )
    parser.add_argument("input", help="Input .md file")
    parser.add_argument("output", help="Output .pdf file")
    parser.add_argument(
        "--theme", choices=["dark", "light"], default="dark"
    )
    args = parser.parse_args()

    try:
        convert(args.input, args.output, args.theme)
    except (
        subprocess.CalledProcessError,
        FileNotFoundError,
        ValueError,
        SystemExit,
    ) as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
