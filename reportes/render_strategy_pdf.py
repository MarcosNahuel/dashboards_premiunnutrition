#!/usr/bin/env python3
"""Generate PDF version of the agent strategy document."""

from __future__ import annotations

import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import ListFlowable, ListItem, Paragraph, SimpleDocTemplate, Spacer

BASE_DIR = Path(__file__).resolve().parent
SOURCE_PATH = BASE_DIR.parent / "Estrategia_de_Ventas_Agente_IA_Investigacion_Mercado_CO.md"
OUTPUT_PATH = BASE_DIR / "Estrategia_de_Ventas_Agente_IA_Investigacion_Mercado_CO.pdf"


def build_story(text: str):
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Heading1Custom", parent=styles["Heading1"], textColor=colors.HexColor("#0b7285")))
    styles.add(ParagraphStyle(name="Heading2Custom", parent=styles["Heading2"], textColor=colors.HexColor("#0b7285")))
    styles.add(ParagraphStyle(name="Heading3Custom", parent=styles["Heading3"], textColor=colors.HexColor("#0b7285")))
    styles.add(ParagraphStyle(name="BodyCustom", parent=styles["BodyText"], leading=14))
    styles.add(ParagraphStyle(name="BulletCustom", parent=styles["BodyText"], leftIndent=16, bulletIndent=6, spaceAfter=4))

    story = []
    bullet_buffer: list[str] = []

    def flush_bullets():
        nonlocal bullet_buffer
        if bullet_buffer:
            items = [
                ListItem(Paragraph(item.strip(), styles["BodyCustom"]), bulletColor=colors.HexColor("#0b7285"))
                for item in bullet_buffer
            ]
            story.append(ListFlowable(items, bulletType="bullet"))
            story.append(Spacer(1, 0.12 * inch))
            bullet_buffer = []

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()

        if not stripped:
            flush_bullets()
            story.append(Spacer(1, 0.12 * inch))
            continue

        if stripped.startswith(("* ", "- ")):
            bullet_buffer.append(stripped[2:])
            continue

        flush_bullets()

        if stripped.startswith("# "):
            story.append(Paragraph(stripped[2:], styles["Heading1Custom"]))
        elif stripped.startswith("## "):
            story.append(Paragraph(stripped[3:], styles["Heading2Custom"]))
        elif stripped.startswith("### "):
            story.append(Paragraph(stripped[4:], styles["Heading3Custom"]))
        elif re.match(r"^\d+\.\s", stripped):
            bullet_buffer.append(stripped[stripped.find(" ") + 1 :])
        else:
            story.append(Paragraph(stripped, styles["BodyCustom"]))

    flush_bullets()
    return story


def main() -> None:
    text = SOURCE_PATH.read_text(encoding="utf-8", errors="replace")
    story = build_story(text)

    doc = SimpleDocTemplate(
        str(OUTPUT_PATH),
        pagesize=LETTER,
        topMargin=48,
        bottomMargin=48,
        leftMargin=60,
        rightMargin=60,
    )
    doc.build(story)
    print("Generated strategy PDF at", OUTPUT_PATH)


if __name__ == "__main__":
    main()
