
Quick thing to convert .md into pretty .pdf with some syntax highlighting - I needed this for uni hand-ins and didn't want to install 2 gigs of Latex stuff :)

# README

A simple Markdown → PDF converter using Pandoc and headless Chromium.
It uses CSS-based styling (no LaTeX required).


## FEATURES

- Markdown to PDF conversion
- CSS-based styling (dark/light themes)
- Syntax highlighting (via Pandoc)
- No LaTeX / TeX Live required
- No temporary files left behind
- Lightweight CLI tool


## HOW IT WORKS

Markdown → Pandoc → HTML → Chromium → PDF

- Pandoc converts Markdown into HTML
- Chromium renders HTML and prints it as PDF (headless mode)


## DEPENDENCIES

Required:

- Python 3
- Pandoc
- Chromium (or Google Chrome)

Optional:

- Inconsolata font


## INSTALLATION

If you want to use it as a system-wide tool:
```
sudo mv md2pdf.py /usr/local/bin/md2pdf
sudo chmod +x /usr/local/bin/md2pdf
```

## USAGE

```
python md2pdf.py file.md output.pdf
```
Or if installed:

```
md2pdf input.md output.pdf
```
Optional theme:

```
md2pdf input.md output.pdf --theme dark  
md2pdf input.md output.pdf --theme light
```

## SYNTAX HIGHLIGHTING


Handled by Pandoc using built-in styles.


## NOTES

- Chromium is used as a headless rendering engine
- Pandoc handles Markdown → HTML conversion
- No LaTeX or TeX Live is required
- Works on most Linux distributions (not distro-specific)
- Requires a graphical Chromium/Chrome installation, even in headless mode
