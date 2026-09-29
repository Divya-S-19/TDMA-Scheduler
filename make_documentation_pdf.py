from pathlib import Path
from html import escape
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted


INPUT = Path("documentation/project_documentation.md")
OUTPUT = Path("documentation/project_documentation.pdf")


styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "TitleCustom",
    parent=styles["Title"],
    fontSize=20,
    leading=25,
    alignment=TA_CENTER,
    spaceAfter=18,
)

h1_style = ParagraphStyle(
    "H1Custom",
    parent=styles["Heading1"],
    fontSize=16,
    leading=20,
    spaceBefore=14,
    spaceAfter=8,
)

h2_style = ParagraphStyle(
    "H2Custom",
    parent=styles["Heading2"],
    fontSize=13,
    leading=17,
    spaceBefore=10,
    spaceAfter=6,
)

body_style = ParagraphStyle(
    "BodyCustom",
    parent=styles["BodyText"],
    fontSize=9.5,
    leading=14,
    spaceAfter=6,
)

bullet_style = ParagraphStyle(
    "BulletCustom",
    parent=body_style,
    leftIndent=15,
    firstLineIndent=-8,
    spaceAfter=4,
)

code_style = ParagraphStyle(
    "CodeCustom",
    parent=body_style,
    fontName="Courier",
    fontSize=7.5,
    leading=10,
    leftIndent=8,
    rightIndent=8,
    spaceAfter=4,
)


def inline_format(text):
    """Clean simple Markdown formatting."""
    text = escape(text)

    # Bold
    text = text.replace("**", "")

    # Inline code
    text = text.replace("`", "")

    return text


def build_pdf():
    if not INPUT.exists():
        raise FileNotFoundError(
            f"Documentation file not found: {INPUT}"
        )

    text = INPUT.read_text(encoding="utf-8")

    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title="TDMA Schedule Planner and Optimizer - Project Documentation",
        author="Divya S",
    )

    story = []

    lines = text.splitlines()
    in_code = False
    code_lines = []

    for raw_line in lines:
        line = raw_line.rstrip()

        # Code block
        if line.startswith("```"):
            if in_code:
                if code_lines:
                    story.append(
                        Preformatted(
                            "\n".join(code_lines),
                            code_style
                        )
                    )
                    story.append(Spacer(1, 4))

                code_lines = []
                in_code = False
            else:
                in_code = True

            continue

        if in_code:
            code_lines.append(line)
            continue

        # Empty line
        if not line.strip():
            story.append(Spacer(1, 4))
            continue

        # Horizontal rule
        if line.strip() in ("---", "***", "___"):
            story.append(Spacer(1, 5))
            continue

        # Main title
        if line.startswith("# "):
            story.append(
                Paragraph(
                    inline_format(line[2:].strip()),
                    title_style
                )
            )
            continue

        # Heading 1
        if line.startswith("## "):
            story.append(
                Paragraph(
                    inline_format(line[3:].strip()),
                    h1_style
                )
            )
            continue

        # Heading 2
        if line.startswith("### "):
            story.append(
                Paragraph(
                    inline_format(line[4:].strip()),
                    h2_style
                )
            )
            continue

        # Markdown bullet
        if line.startswith("- "):
            story.append(
                Paragraph(
                    "• " + inline_format(line[2:].strip()),
                    bullet_style
                )
            )
            continue

        # Numbered list
        if len(line) >= 3 and line[0].isdigit() and line[1:3] == ". ":
            story.append(
                Paragraph(
                    inline_format(line),
                    body_style
                )
            )
            continue

        # Markdown table separator
        if line.startswith("|") and set(
            line.replace("|", "").replace("-", "").replace(":", "").strip()
        ) == set():
            continue

        # Markdown table rows
        if line.startswith("|"):
            cells = [
                cell.strip()
                for cell in line.strip("|").split("|")
            ]

            formatted = " &nbsp;&nbsp;|&nbsp;&nbsp; ".join(
                inline_format(cell) for cell in cells
            )

            story.append(
                Paragraph(formatted, body_style)
            )
            continue

        # Normal paragraph
        story.append(
            Paragraph(
                inline_format(line),
                body_style
            )
        )

    doc.build(story)

    print("PDF created successfully.")
    print(f"Output: {OUTPUT}")


if __name__ == "__main__":
    build_pdf()