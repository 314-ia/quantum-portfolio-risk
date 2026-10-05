"""Genera docs/notebook.html: el notebook de la clase, ya ejecutado, como página del sitio web.

Hay que volver a correrlo cada vez que cambia el notebook. Usa nbconvert, que se instala junto con
JupyterLab, así que alcanza con el entorno del notebook. Uso: python assets/generar_pagina_notebook.py

La exportación se hace por programa y no con el comando "jupyter nbconvert": el comando incrusta en
la página la hoja de estilos personal de Jupyter de quien lo ejecuta, si tiene una."""
import html, json, re
from pathlib import Path

from nbconvert import HTMLExporter

RAIZ = Path(__file__).resolve().parent.parent
NOTEBOOK = RAIZ / "CACIC" / "notebook" / "Finanzas_Cuanticas_CACIC2026.ipynb"
SALIDA = RAIZ / "docs" / "notebook.html"
SITIO = "https://314-ia.github.io/quantum-portfolio-risk/"
REPO = "https://github.com/314-ia/quantum-portfolio-risk"

TITULO = "Notebook: finanzas con computación cuántica en Qiskit, paso a paso"
DESCRIPCION = ("Notebook de Qiskit ya ejecutado: precios reales de Yahoo Finance, frontera eficiente de Markowitz, "
               "circuitos paramétricos, VQE, un circuito de riesgo de 12 qubits, simulación con ruido y resultado "
               "en una computadora cuántica de IBM.")
AUTORES = [("Juan Pablo Braña", "CAETI, Universidad Abierta Interamericana"),
           ("Alejandro Fernández", "LIFIA, Universidad Nacional de La Plata"),
           ("Alejandra M. J. Litterio", "CAETI, Universidad Abierta Interamericana")]

DATOS = {"@context": "https://schema.org", "@type": "TechArticle", "headline": TITULO, "description": DESCRIPCION,
         "url": SITIO + "notebook.html", "inLanguage": "es", "datePublished": "2026-10-04", "isAccessibleForFree": True,
         "license": "https://opensource.org/licenses/MIT", "image": SITIO + "assets/social-card.png",
         "isPartOf": {"@id": SITIO + "#material"},
         "author": [{"@type": "Person", "name": n, "affiliation": {"@type": "Organization", "name": a}} for n, a in AUTORES]}

CABECERA = f"""<title>{TITULO}</title>
<meta name="description" content="{DESCRIPCION}">
<meta name="author" content="{', '.join(n for n, _ in AUTORES)}">
<link rel="canonical" href="{SITIO}notebook.html">
<link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Quantum Portfolio Risk">
<meta property="og:locale" content="es_AR">
<meta property="og:title" content="Notebook: finanzas con computación cuántica en Qiskit">
<meta property="og:description" content="De la frontera eficiente de Markowitz a un circuito cuántico de 12 qubits ejecutado en IBM Quantum, con precios reales.">
<meta property="og:url" content="{SITIO}notebook.html">
<meta property="og:image" content="{SITIO}assets/social-card.png">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{json.dumps(DATOS, ensure_ascii=False)}</script>"""

BARRA = f"""<div style="font:16px/1.4 system-ui,-apple-system,'Segoe UI',Helvetica,Arial,sans-serif;background:#0E1B2C;color:#F7F5EF;padding:12px 20px;display:flex;flex-wrap:wrap;gap:8px 22px;align-items:center">
<a href="./" style="color:#F7F5EF;font-weight:700;text-decoration:none">Quantum Portfolio Risk</a>
<span style="color:#9FB3C8">Notebook de la clase, ya ejecutado</span>
<a href="{REPO}" style="color:#7FB7E6;margin-left:auto">Código en GitHub</a>
<a href="{REPO}/blob/main/CACIC/notebook/{NOTEBOOK.name}" style="color:#7FB7E6">Descargar el notebook</a>
</div>"""

SIN_TEXTO = 'alt="No description has been provided for this image"'


def cambiar(texto, patron, nuevo):
    """Reemplaza un patrón que tiene que aparecer exactamente una vez."""
    texto, n = re.subn(patron, lambda _: nuevo, texto)
    assert n == 1, f"se esperaba una aparición de {patron!r} y hay {n}"
    return texto


def describir_figuras(pagina):
    """Pone como texto alternativo de cada figura el título de la sección en la que está."""
    titulos = [(m.start(), html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).replace("¶", "").strip())
               for m in re.finditer(r"<h[23][^>]*>(.*?)</h[23]>", pagina, flags=re.S)]
    partes, n = pagina.split(SIN_TEXTO), 0
    salida, pos = [partes[0]], len(partes[0])
    for parte in partes[1:]:
        n += 1
        seccion = [t for p, t in titulos if p < pos][-1]
        salida.append(f'alt="{html.escape(f"Figura {n} del notebook, sección {seccion}", quote=True)}"' + parte)
        pos += len(SIN_TEXTO) + len(parte)
    return "".join(salida), n


pagina, _ = HTMLExporter().from_filename(str(NOTEBOOK))
pagina = cambiar(pagina, r'<html lang="en">', '<html lang="es">')
pagina = cambiar(pagina, r"<title>[^<]*</title>", CABECERA)
pagina = cambiar(pagina, r"<body[^>]*>", re.search(r"<body[^>]*>", pagina).group() + "\n" + BARRA)
pagina, figuras = describir_figuras(pagina)
SALIDA.write_text(pagina, encoding="utf-8")
print("escrito", SALIDA.relative_to(RAIZ), "|", len(pagina.encode()) // 1000, "KB |", figuras, "figuras con texto alternativo")
