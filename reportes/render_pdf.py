from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Image,
    ListFlowable,
    ListItem,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

BASE_DIR = Path(__file__).resolve().parent
html_path = BASE_DIR / "informe_equipo_tecnico.html"
pdf_path = BASE_DIR / "informe_equipo_tecnico_actualizado.pdf"

metrics = [
    ("GMV analizado", "COP 20.44 B"),
    ("Órdenes procesadas", "62,434"),
    ("Clientes únicos", "36,429"),
    ("Ticket promedio", "COP 327k"),
    ("Órdenes con descuento", "93 %"),
    ("Top SKU", "Whey & Creatina"),
]

bullets_overview = [
    "Extracción y normalización del histórico completo de Shopify (bulk_definitivo.json → CSV).",
    "Análisis descriptivo con analyze_bulk_data.py y métricas en analysis_outputs/.",
    "Investigación de negocio y mercado colombiano (documento RAG y fuentes externas).",
    "Diseño de estrategia prescriptiva para el agente (segmentos, bundles, guiones, descuentos).",
]

process_steps = [
    ("1. Extracción y limpieza", "Conversión del bulk a CSV, validación de montos/fechas y clasificación de productos."),
    ("2. Análisis descriptivo", "KPIs, Pareto del catálogo, estacionalidad y segmentación RFM."),
    ("3. Investigación de mercado", "Revisión del documento ‘IA para Estrategia de Contenido Premium Nutrition’ y estudios del sector."),
    ("4. Estrategia prescriptiva", "Playbook del agente: guiones por objetivo, bundles y reglas de descuentos/horarios."),
]

insights = [
    "El corazón del negocio está en un grupo reducido de productos héroe; debemos contarlo así cuando el agente atienda.",
    "Los clientes ya llevan varios artículos por compra, lo que abre la puerta a sugerir combos y rutinas completas.",
    "Los descuentos funcionan, pero hay que darles propósito: premios para quienes vuelven y empujes suaves para los que se alejaron.",
    "Los mejores resultados llegan en la semana y en horario laboral, así que programaremos allí los mensajes más importantes.",
    "Integraremos estrategia_agente_ventas.md en el prompt para que la IA converse como un asesor real de Zona FIT.",
]

figures = [
    ("img_revenue_trend.png", "Ingresos diarios: picos entre mayo y julio 2025."),
    ("img_sales_by_hour.png", "Horas pico: 9:00 – 17:00 para campañas del agente."),
    ("img_top_products.png", "Top 10 SKU dominados por proteínas y creatinas."),
]

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="Heading1Custom", parent=styles["Heading1"], fontSize=20, textColor=colors.HexColor("#0b7285")))
styles.add(ParagraphStyle(name="Heading2Custom", parent=styles["Heading2"], fontSize=14, textColor=colors.HexColor("#0b7285")))
styles.add(ParagraphStyle(name="Body", parent=styles["BodyText"], leading=14))
styles.add(ParagraphStyle(name="BulletCustom", parent=styles["BodyText"], leftIndent=16, bulletIndent=6, spaceAfter=4))
styles.add(ParagraphStyle(name="Footnote", parent=styles["BodyText"], fontSize=9, textColor=colors.HexColor("#6b7280")))

story = []

title = Paragraph("Informe técnico · Evolución del agente IA comercial", styles["Heading1Custom"])
subtitle = Paragraph(
    "Resumen de actividades para robustecer el agente de ventas de Zona FIT con datos históricos, investigación de mercado y estrategia prescriptiva.",
    styles["Body"],
)

story.extend([title, Spacer(1, 0.15 * inch), subtitle, Spacer(1, 0.3 * inch)])

story.append(Paragraph("Panorama general del proyecto", styles["Heading2Custom"]))

overview_list = ListFlowable(
    [ListItem(Paragraph(item, styles["Body"]), bulletColor=colors.HexColor("#ff6b00")) for item in bullets_overview],
    bulletType="bullet",
)
story.extend([overview_list, Spacer(1, 0.25 * inch)])

metric_data = []
for i in range(0, len(metrics), 3):
    row = []
    for label, value in metrics[i:i + 3]:
        cell = Paragraph(f"<b>{label}</b><br/><font size=14>{value}</font>", styles["Body"])
        row.append(cell)
    metric_data.append(row)

metric_table = Table(metric_data, colWidths=[2.2 * inch] * 3)
metric_table.setStyle(TableStyle([
    ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#0b7285")),
    ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#9ca3af")),
    ("BACKGROUND", (0, 0), (-1, -1), colors.whitesmoke),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("LEFTPADDING", (0, 0), (-1, -1), 10),
    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
    ("TOPPADDING", (0, 0), (-1, -1), 8),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
]))
story.extend([metric_table, Spacer(1, 0.3 * inch)])

story.append(Paragraph("Proceso de trabajo", styles["Heading2Custom"]))

for title_text, desc in process_steps:
    story.append(Paragraph(f"<b>{title_text}</b>: {desc}", styles["Body"]))
    story.append(Spacer(1, 0.1 * inch))

story.append(Spacer(1, 0.3 * inch))
story.append(Paragraph("Insights visuales", styles["Heading2Custom"]))

for image_name, caption in figures:
    image_path = BASE_DIR / image_name
    if image_path.exists():
        img = Image(str(image_path), width=5.8 * inch, height=3.2 * inch, kind='proportional')
        story.extend([img, Paragraph(caption, styles["Body"]), Spacer(1, 0.2 * inch)])

story.append(Paragraph("Conclusiones y próximos pasos", styles["Heading2Custom"]))
conclusions_list = ListFlowable(
    [ListItem(Paragraph(text, styles["Body"]), bulletColor=colors.HexColor("#0b7285")) for text in insights],
    bulletType="bullet",
)
story.extend([conclusions_list, Spacer(1, 0.25 * inch)])

footnote = Paragraph(
    "Referencias: histórico Shopify, analysis_outputs/, documento 'IA para Estrategia de Contenido Premium Nutrition' y reportes de mercado (Euromonitor, ICEX, Portafolio).",
    styles["Footnote"],
)
story.append(footnote)

pdf = SimpleDocTemplate(
    str(pdf_path),
    pagesize=LETTER,
    topMargin=36,
    bottomMargin=36,
    leftMargin=54,
    rightMargin=54,
)

pdf.build(story)
print("PDF generado en", pdf_path)
