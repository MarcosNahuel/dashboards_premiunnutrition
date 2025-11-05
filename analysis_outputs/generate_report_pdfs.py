import os
import glob
import json
import csv
import re
import textwrap
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

BASE_DIR = r'D:\OneDrive\GitHub\premiumnutrition'
EXEC_DIR = os.path.join(BASE_DIR, 'EJECUCIONES')
PATTERN = os.path.join(EXEC_DIR, 'ejecucion-*-success.json')
EXPECTED_CSV = os.path.join(BASE_DIR, 'dashboards_premiunnutrition', 'analysis_outputs', 'tabla_respuestas.csv')

TARGET_MARKDOWN = [
    os.path.join(EXEC_DIR, 'INFORME_ANALISIS_WORKFLOW.md'),
    os.path.join(EXEC_DIR, 'INFORME_FINAL_ANALISIS_KOMMO.md'),
    os.path.join(EXEC_DIR, 'PROMPT_ANALISIS_AGENTE_KOMMO.md'),
]

# Helper to extract plain response from agent generation text
RE_JSON_BLOCK = re.compile(r"`json\s*(\{.*?\})\s*`", re.DOTALL)


def extract_plain_response(text: str) -> str:
    if not text:
        return ''
    match = RE_JSON_BLOCK.search(text)
    if match:
        payload = match.group(1)
        try:
            parsed = json.loads(payload)
        except json.JSONDecodeError:
            pass
        else:
            respuesta = parsed.get('output', {}).get('respuesta')
            if isinstance(respuesta, list):
                return "\n".join(str(item) for item in respuesta)
            if isinstance(respuesta, str):
                return respuesta
    return text

# Gather image URLs from responses
image_urls = set()
for filepath in glob.glob(PATTERN):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    run_data = data.get('data', {}).get('resultData', {}).get('runData', {})
    node_runs = run_data.get('OpenAI Chat Model2')
    if not node_runs:
        continue
    actual_raw = None
    for run in node_runs:
        try:
            gens = run['data']['ai_languageModel'][0][0]['json']['response']['generations']
            if gens and gens[0] and gens[0][0].get('text'):
                actual_raw = gens[0][0]['text']
                break
        except (KeyError, IndexError, TypeError):
            continue
    if not actual_raw:
        continue
    plain = extract_plain_response(actual_raw)
    for url in re.findall(r"https?://\S+", plain):
        # Strip trailing punctuation
        cleaned = url.rstrip('.,);]"\' )')
        if any(ext in cleaned.lower() for ext in ['.png', '.jpg', '.jpeg', '.webp', '.gif', '.svg']):
            image_urls.add(cleaned)

sorted_image_urls = sorted(image_urls)

# Function to write text content to PDF

def write_pdf(output_path: str, content: str):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    margin = 54  # 0.75 inch approx
    text_obj = c.beginText()
    text_obj.setTextOrigin(margin, height - margin)
    text_obj.setFont('Helvetica', 10)
    max_chars = 95
    line_height = 12

    for paragraph in content.split('\n'):
        if paragraph == '':
            text_obj.textLine('')
            continue
        for line in textwrap.wrap(paragraph, width=max_chars) or ['']:
            if text_obj.getY() <= margin:
                c.drawText(text_obj)
                c.showPage()
                text_obj = c.beginText()
                text_obj.setTextOrigin(margin, height - margin)
                text_obj.setFont('Helvetica', 10)
            text_obj.textLine(line)
    c.drawText(text_obj)
    c.save()

# Generate PDFs for target markdown files
for md_path in TARGET_MARKDOWN:
    if not os.path.exists(md_path):
        continue
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read().rstrip()
    annex_lines = ['## Anexo: URLs de imágenes provenientes de respuestas', '']
    if sorted_image_urls:
        annex_lines.extend(f"- {url}" for url in sorted_image_urls)
    else:
        annex_lines.append('No se encontraron URLs de imágenes en las respuestas analizadas.')
    combined_content = md_content + "\n\n" + "\n".join(annex_lines) + "\n"
    pdf_path = os.path.splitext(md_path)[0] + '.pdf'
    write_pdf(pdf_path, combined_content)
    print(f'Creado: {pdf_path}')
