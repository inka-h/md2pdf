#!/usr/bin/env python3

import argparse
import subprocess
import tempfile
from pathlib import Path
import sys


DARK_CSS = """
@page {
    margin: 0;
}

body {
    margin: 0;
    padding: 2cm;
    background: #3b3b3b;
    color: #f5f5f5;
    font-family: Inconsolata, monospace;
    line-height: 1.6;
}

h1, h2, h3 {
    color: #ffffff;
}

pre, code {
    background: #2b2b2b;
    padding: 0.4em;
    border-radius: 6px;
}

a {
    color: #8ab4f8;
}
"""


LIGHT_CSS = """
@page {
    margin: 1.5cm;
}

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


def run(cmd):
    subprocess.run(cmd, check=True)


def convert(md_path, pdf_path, theme="dark"):
    md_path = Path(md_path).resolve()
    pdf_path = Path(pdf_path).resolve()

    css = DARK_CSS if theme == "dark" else LIGHT_CSS

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        html_file = tmpdir / "out.html"
        css_file = tmpdir / "style.css"

        css_file.write_text(css)

        # Markdown → HTML
        run([
            "pandoc",
            str(md_path),
            "-o",
            str(html_file),
            "--standalone",
            "--css",
            str(css_file),
            "--highlight-style=breezeDark",
        ])

        # HTML → PDF (Chromium)
        run([
            "chromium",
            "--headless",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={pdf_path}",
            str(html_file),
        ])

    print(f"✔ PDF created: {pdf_path}")


def main():
    parser = argparse.ArgumentParser(description="Convert Markdown to styled PDF")
    parser.add_argument("input", help="Input .md file")
    parser.add_argument("output", help="Output .pdf file")
    parser.add_argument("--theme", choices=["dark", "light"], default="dark")

    args = parser.parse_args()

    try:
        convert(args.input, args.output, args.theme)
    except subprocess.CalledProcessError as e:
        print("❌ Conversion failed:", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
