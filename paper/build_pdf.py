#!/usr/bin/env python3
"""Build no-go-theorem.pdf from no-go-theorem.md."""
import re
from pathlib import Path
from markdown_pdf import MarkdownPdf, Section

HERE = Path(__file__).parent
md = (HERE / "no-go-theorem.md").read_text()

CSS = """
body { font-family: Georgia, 'Times New Roman', serif; font-size: 10.5pt;
       line-height: 1.45; color: #1a1a1a; }
h1 { font-size: 17pt; line-height: 1.25; margin-bottom: 4pt; }
h2 { font-size: 13pt; margin-top: 16pt; border-bottom: 0.5pt solid #999;
     padding-bottom: 2pt; }
h3 { font-size: 11pt; margin-top: 12pt; }
code, pre { font-family: 'DejaVu Sans Mono', Menlo, monospace; font-size: 8.4pt; }
pre { background: #f6f6f4; padding: 6pt; border-left: 2pt solid #bbb;
      white-space: pre-wrap; }
table { border-collapse: collapse; font-size: 9.3pt; margin: 8pt 0; }
th, td { border: 0.5pt solid #888; padding: 3pt 7pt; text-align: left; }
th { background: #efefec; }
blockquote { border-left: 2pt solid #999; margin-left: 0; padding-left: 10pt;
             color: #333; }
hr { border: none; border-top: 0.5pt solid #aaa; margin: 14pt 0; }
"""

pdf = MarkdownPdf(toc_level=2, optimize=True)
pdf.add_section(Section(md, paper_size="A4", borders=(50, 45, -50, -45)), user_css=CSS)
pdf.meta["title"] = "Why Rocks Do Not Go 0.99c — A Coupling-Class Impossibility Argument"
pdf.meta["author"] = "Allen Hall"
pdf.save(str(HERE / "no-go-theorem.pdf"))
print("wrote", HERE / "no-go-theorem.pdf")
