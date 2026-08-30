"""Create PDF companions for the Markdown and HTML documentation sources.

Run from the repository root:
    .\.venv\Scripts\python.exe documentation_workspace\render_pdfs.py
"""
from __future__ import annotations

import html
import re
from html.parser import HTMLParser
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    HRFlowable,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parent / "source"
PAGE_WIDTH, PAGE_HEIGHT = A4


def safe_text(value: str) -> str:
    """Use characters supported by ReportLab's built-in Helvetica fonts."""
    replacements = {
        "–": "-", "—": "-", "“": '"', "”": '"', "‘": "'", "’": "'",
        "…": "...", "₹": "INR ", "µ": "micro", "²": "^2", "³": "^3",
        "≤": "<=", "≥": ">=", "×": "x", "→": "->", "•": "-",
    }
    for old, new in replacements.items():
        value = value.replace(old, new)
    return value.encode("ascii", "replace").decode("ascii")


class SourceHTMLParser(HTMLParser):
    """Convert the report HTML into simple Markdown before PDF rendering."""

    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.tag_stack: list[str] = []
        self.cells: list[str] = []
        self.row: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "br":
            self.parts.append("\n")
            return
        if tag in {"meta", "link", "img", "input"}:
            return
        self.tag_stack.append(tag)
        if tag in {"h1", "h2", "h3", "h4"}:
            self.parts.append("\n" + "#" * int(tag[1]) + " ")
        elif tag in {"p", "pre", "ul", "ol", "hr"}:
            self.parts.append("\n")
        elif tag == "li":
            self.parts.append("\n- ")
        elif tag in {"td", "th"}:
            self.cells = []

    def handle_endtag(self, tag: str) -> None:
        if tag in {"td", "th"}:
            self.row.append("".join(self.cells).strip())
        elif tag == "tr" and self.row:
            self.parts.append("\n| " + " | ".join(self.row) + " |\n")
            self.row = []
        elif tag in {"p", "pre", "h1", "h2", "h3", "h4", "li"}:
            self.parts.append("\n")
        for position in range(len(self.tag_stack) - 1, -1, -1):
            if self.tag_stack[position] == tag:
                del self.tag_stack[position:]
                break

    def handle_data(self, data: str) -> None:
        if any(tag in {"head", "style", "script", "title"} for tag in self.tag_stack):
            return
        if self.tag_stack and self.tag_stack[-1] in {"td", "th"}:
            self.cells.append(data)
        else:
            self.parts.append(data)

    def markdown(self) -> str:
        return html.unescape("".join(self.parts))


def html_as_markdown(path: Path) -> str:
    parser = SourceHTMLParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser.markdown()


def styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle("DocTitle", parent=base["Title"], fontName="Helvetica-Bold", fontSize=20, leading=24, textColor=colors.HexColor("#0b1f3a"), spaceAfter=12),
        "h1": ParagraphStyle("H1", parent=base["Heading1"], fontName="Helvetica-Bold", fontSize=15, leading=19, textColor=colors.HexColor("#0b4f6c"), spaceBefore=14, spaceAfter=7),
        "h2": ParagraphStyle("H2", parent=base["Heading2"], fontName="Helvetica-Bold", fontSize=12, leading=15, textColor=colors.HexColor("#0b4f6c"), spaceBefore=11, spaceAfter=5),
        "h3": ParagraphStyle("H3", parent=base["Heading3"], fontName="Helvetica-Bold", fontSize=10.5, leading=13, textColor=colors.HexColor("#334155"), spaceBefore=8, spaceAfter=3),
        "body": ParagraphStyle("Body", parent=base["BodyText"], fontName="Helvetica", fontSize=9.2, leading=13, spaceAfter=6),
        "bullet": ParagraphStyle("Bullet", parent=base["BodyText"], fontName="Helvetica", fontSize=9.2, leading=13, leftIndent=12, firstLineIndent=-8, spaceAfter=3),
        "code": ParagraphStyle("Code", fontName="Courier", fontSize=7.5, leading=9.5, textColor=colors.HexColor("#172033")),
        "table": ParagraphStyle("Table", parent=base["BodyText"], fontName="Helvetica", fontSize=7.2, leading=9),
    }


def paragraph(text: str, style: ParagraphStyle) -> Paragraph:
    inline = escape(safe_text(text.strip()))
    inline = re.sub(r"`([^`]+)`", r"<font name='Courier'>\1</font>", inline)
    inline = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", inline)
    inline = re.sub(r"\*([^*]+)\*", r"<i>\1</i>", inline)
    return Paragraph(inline.replace("\n", "<br/>"), style)


def table_from_rows(rows: list[list[str]], style: ParagraphStyle) -> Table:
    columns = max(len(row) for row in rows)
    normalised = [row + [""] * (columns - len(row)) for row in rows]
    cells = [[paragraph(cell, style) for cell in row] for row in normalised]
    width = 174 * mm
    table = Table(cells, colWidths=[width / columns] * columns, repeatRows=1, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0b4f6c")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#cbd5e1")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f8fa")]),
    ]))
    return table


def render_markdown(markdown: str, output: Path, source_name: str) -> None:
    doc = SimpleDocTemplate(
        str(output), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
        topMargin=18 * mm, bottomMargin=18 * mm, title=source_name,
    )
    style = styles()
    story: list[object] = []
    lines = markdown.splitlines()
    index = 0
    in_code = False
    code_lines: list[str] = []

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        if stripped.startswith("```"):
            if in_code:
                story.append(Preformatted(safe_text("\n".join(code_lines)), style["code"]))
                story.append(Spacer(1, 5))
                code_lines = []
            in_code = not in_code
            index += 1
            continue
        if in_code:
            code_lines.append(line)
            index += 1
            continue
        if not stripped:
            index += 1
            continue
        if stripped == "---":
            story.extend([Spacer(1, 3), HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#d8a84e")), Spacer(1, 5)])
            index += 1
            continue
        if stripped.startswith("|"):
            rows: list[list[str]] = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                candidate = lines[index].strip()
                cells = [cell.strip() for cell in candidate.strip("|").split("|")]
                if not all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
                    rows.append(cells)
                index += 1
            if rows:
                story.extend([table_from_rows(rows, style["table"]), Spacer(1, 7)])
            continue
        heading = re.match(r"^(#{1,4})\s+(.*)$", stripped)
        if heading:
            level, text = heading.groups()
            story.append(paragraph(text, style["title"] if len(level) == 1 and not story else style[f"h{len(level)}"]))
            index += 1
            continue
        if re.match(r"^(?:[-*]|\d+\.)\s+", stripped):
            text = re.sub(r"^(?:[-*]|\d+\.)\s+", "", stripped)
            story.append(paragraph("- " + text, style["bullet"]))
            index += 1
            continue
        if stripped.startswith("> "):
            story.append(paragraph(stripped[2:], style["bullet"]))
            index += 1
            continue
        block = [stripped]
        index += 1
        while index < len(lines):
            next_line = lines[index].strip()
            if not next_line or next_line.startswith(("#", "|", "```", "- ", "* ", "> ")) or next_line == "---" or re.match(r"^\d+\.\s+", next_line):
                break
            block.append(next_line)
            index += 1
        story.append(paragraph(" ".join(block), style["body"]))

    def page_number(canvas, document):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#64748b"))
        canvas.drawRightString(PAGE_WIDTH - 18 * mm, 11 * mm, f"{source_name} | Page {document.page}")
        canvas.restoreState()

    doc.build(story, onFirstPage=page_number, onLaterPages=page_number)


def main() -> None:
    inputs = sorted(ROOT.glob("*.md")) + sorted(ROOT.glob("*.html"))
    for source in inputs:
        markdown = source.read_text(encoding="utf-8") if source.suffix == ".md" else html_as_markdown(source)
        output = source.with_suffix(".pdf")
        if source.suffix == ".html":
            output = source.with_name(f"{source.stem}_from_html.pdf")
        render_markdown(markdown, output, source.name)
        print(f"Created {output.relative_to(ROOT.parent.parent)}")


if __name__ == "__main__":
    main()
