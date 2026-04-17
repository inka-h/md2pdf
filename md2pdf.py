#!/usr/bin/env python3

import argparse
import subprocess
import tempfile
from pathlib import Path
import sys
import shutil

DARK_CSS = """
@page { margin: 0; }

body {
    margin: 0;
    padding: 2cm;
    background: #3b3b3b;
    color: #f5f5f5;
    font-family: Inconsolata, monospace;
    line-height: 1.6;
}

h1, h2, h3 { color: #ffffff; }

pre, code {
    background: #2b2b2b;
    padding: 0.4em;
    border-radius: 6px;
}

a { color: #8ab4f8; }
"""

LIGHT_CSS = """
@page { margin: 1.5cm; }

body {
    font-family: Inconsolata, monospace;
    line-height: 1.6;
}

pre, code {
    background: #f4f4f4;
    padding: 0.4em;
    border-radius: 6px;
}
"""

HIGHLIGHT_STYLES = {"dark": "breezeDark", "light": "pygments"}

CHROMIUM_CANDIDATES = [
    "chromium",
    "chromium-browser",
    "google-chrome-stable",
    "google-chrome",
]

DISK_CACHE_MAX = 50 * 1024 * 1024  # 50 MB


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


def convert(md_path, pdf_path, theme="dark"):
    md_path = Path(md_path).resolve()
    pdf_path = Path(pdf_path).resolve()

    if not md_path.is_file():
        raise FileNotFoundError(f"Input file not found: {md_path}")

    css = DARK_CSS if theme == "dark" else LIGHT_CSS
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
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
