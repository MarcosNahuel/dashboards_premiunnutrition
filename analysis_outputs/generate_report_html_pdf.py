import os
import glob
import json
import re
from markdown import markdown
from xhtml2pdf import pisa

BASE_DIR = r'D:\OneDrive\GitHub\premiumnutrition'
EXEC_DIR = os.path.join(BASE_DIR, 'EJECUCIONES')
PATTERN = os.path.join(EXEC_DIR, 'ejecucion-*-success.json')
TARGET_MARKDOWN = [
    os.path.join(EXEC_DIR, 'INFORME_ANALISIS_WORKFLOW.md'),
    os.path.join(EXEC_DIR, 'INFORME_FINAL_ANALISIS_KOMMO.md'),
    os.path.join(EXEC_DIR, 'PROMPT_ANALISIS_AGENTE_KOMMO.md'),
]

RE_JSON_BLOCK = re.compile(r"`json\s*(\{.*?\})\s*`", re.DOTALL)
RE_URL = re.compile(r"https?://\S+")
IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.webp', '.gif', '.svg')


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


def gather_image_urls() -> list[str]:
    urls = set()
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
        for url in RE_URL.findall(plain):
            cleaned = url.rstrip('.,);]"\'")')
            if cleaned.lower().endswith(IMAGE_EXTENSIONS):
                urls.add(cleaned)
    return sorted(urls)


def html_template(title: str, body_html: str, image_urls: list[str]) -> str:
    annex = ['<h2>Anexo: URLs de imágenes provenientes de respuestas</h2>']
    if image_urls:
        annex.append('<ul>')
        annex.extend(f'<li><a href="{url}">{url}</a></li>' for url in image_urls)
        annex.append('</ul>')
    else:
        annex.append('<p>No se encontraron URLs de imágenes en las respuestas analizadas.</p>')
    annex_html = '\n'.join(annex)
    return f"""
<!DOCTYPE html>
<html lang='es'>
<head>
<meta charset='utf-8'>
<title>{title}</title>
<style>
body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 40px; line-height: 1.5; color: #202124; }}
h1, h2, h3, h4 {{ color: #0b3d62; margin-top: 28px; }}
code {{ background: #f1f3f4; padding: 2px 4px; border-radius: 3px; }}
pre {{ background: #f1f3f4; padding: 12px; border-radius: 6px; overflow-x: auto; font-size: 0.9rem; }}
blockquote {{ border-left: 4px solid #89c2d9; padding-left: 12px; margin: 18px 0; color: #555; }}
table {{ border-collapse: collapse; width: 100%; margin: 16px 0; font-size: 0.92rem; }}
th, td {{ border: 1px solid #cfd8dc; padding: 8px 10px; text-align: left; }}
ul {{ margin-left: 1.2em; }}
ol {{ margin-left: 1.2em; }}
a {{ color: #0057b7; text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
hr {{ border: none; border-top: 1px solid #ddd; margin: 32px 0; }}
.page-break {{ page-break-after: always; }}
</style>
</head>
<body>
{body_html}
{annex_html}
</body>
</html>
"""


def convert_markdown(md_path: str, image_urls: list[str]):
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    body_html = markdown(md_content, extensions=['extra', 'toc'])
    title = os.path.basename(md_path)
    full_html = html_template(title, body_html, image_urls)

    base, _ = os.path.splitext(md_path)
    html_path = base + '.html'
    pdf_path = base + '.pdf'

    with open(html_path, 'w', encoding='utf-8') as html_file:
        html_file.write(full_html)

    with open(pdf_path, 'wb') as pdf_file:
        pisa_status = pisa.CreatePDF(full_html, dest=pdf_file, encoding='utf-8')
    if pisa_status.err:
        raise SystemExit(f'Error al generar PDF para {md_path}: {pisa_status.err}')
    print(f'Generado: {html_path}, {pdf_path}')


def main():
    image_urls = gather_image_urls()
    for md_path in TARGET_MARKDOWN:
        if os.path.exists(md_path):
            convert_markdown(md_path, image_urls)

if __name__ == '__main__':
    main()
