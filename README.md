Quick thing to convert .md into pretty .pdf with some syntax highlighting - I needed this for uni hand-ins and didn't want to install 2 gigs of Latex stuff :)

# README

A simple Markdown → PDF converter using Pandoc and headless Chromium. It uses CSS-based styling (no LaTeX required).

## FEATURES

- Markdown to PDF conversion
- CSS-based styling (dark/light themes)
- Syntax highlighting (via Pandoc, matched to theme)
- No LaTeX / TeX Live required
- No temporary files left behind
- Sandboxed Chromium with capped disk cache (50 MB)
- Auto-detects Chromium/Chrome binary
- Lightweight CLI tool

## HOW IT WORKS

Markdown → Pandoc → HTML → Chromium → PDF

- Pandoc converts Markdown into HTML
- Chromium renders HTML and prints it as PDF (headless mode)
- All temp files and Chromium profile data are created in an isolated directory and cleaned up automatically

## DEPENDENCIES

Required:

- Python 3
- Pandoc
- Chromium (or Google Chrome)

Optional:

- Inconsolata font

## INSTALLATION

If you want to use it as a system-wide tool:

```bash
sudo mv md2pdf.py /usr/local/bin/md2pdf
sudo chmod +x /usr/local/bin/md2pdf
```

## USAGE

```bash
python md2pdf.py file.md output.pdf
```

Or if installed:

```bash
md2pdf input.md output.pdf
```

Optional theme:

```bash
md2pdf input.md output.pdf --theme dark
md2pdf input.md output.pdf --theme light
```

## SYNTAX HIGHLIGHTING

Handled by Pandoc using built-in styles. The highlight style is matched to the selected theme (`breezeDark` for dark, `pygments` for light).

## NOTES

- Chromium is used as a headless rendering engine
- Pandoc handles Markdown → HTML conversion
- No LaTeX or TeX Live is required
- Works on most Linux distributions (not distro-specific)
- Requires a graphical Chromium/Chrome installation, even in headless mode
- Chromium profile and cache are isolated per run and cleaned up automatically — no leftover data in `~/.cache`
