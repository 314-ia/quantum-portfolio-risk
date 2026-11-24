"""Genera las páginas del notebook de la clase, ya ejecutado, para el sitio web: docs/notebook.html en
español y docs/en/notebook.html en inglés.

Hay que volver a correrlo cada vez que cambia un notebook. Usa nbconvert, que se instala junto con
JupyterLab, así que alcanza con el entorno del notebook. Uso: python assets/generar_pagina_notebook.py
Para un solo idioma: python assets/generar_pagina_notebook.py es   (o en)

La exportación se hace por programa y no con el comando "jupyter nbconvert": el comando incrusta en
la página la hoja de estilos personal de Jupyter de quien lo ejecuta, si tiene una.

English: builds the website pages of the executed class notebook: docs/notebook.html in Spanish and
docs/en/notebook.html in English. Run it again whenever a notebook changes. It uses nbconvert, which
comes with JupyterLab, so the notebook's environment is enough. Usage:
python assets/generar_pagina_notebook.py, or with a single language: es or en.
The export is done from Python and not with the "jupyter nbconvert" command: the command embeds the
personal Jupyter style sheet of whoever runs it, if they have one."""
import html, json, re, sys
from pathlib import Path

from nbconvert import HTMLExporter

RAIZ = Path(__file__).resolve().parent.parent
SITIO = "https://314-ia.github.io/quantum-portfolio-risk/"
REPO = "https://github.com/314-ia/quantum-portfolio-risk"
AUTORES = [("Juan Pablo Braña", "CAETI, Universidad Abierta Interamericana"),
           ("Alejandro Fernández", "LIFIA, Universidad Nacional de La Plata"),
           ("Alejandra M. J. Litterio", "CAETI, Universidad Abierta Interamericana")]
PAGINAS = {"es": "notebook.html", "en": "en/notebook.html"}        # dirección de cada idioma dentro del sitio

IDIOMAS = {
    "es": dict(
        notebook="FULL_PROJECT/notebook/Finanzas_Cuanticas_CACIC2026.ipynb", region="es_AR", recursos="assets/",
        tarjeta="assets/social-card.png",
        titulo="Notebook: finanzas con computación cuántica en Qiskit, paso a paso",
        descripcion=("Notebook de Qiskit ya ejecutado: precios reales de Yahoo Finance, frontera eficiente de Markowitz, "
                     "circuitos paramétricos, VQE, un circuito de riesgo de 12 qubits, simulación con ruido y resultado "
                     "en una computadora cuántica de IBM."),
        og_titulo="Notebook: finanzas con computación cuántica en Qiskit",
        og_descripcion=("De la frontera eficiente de Markowitz a un circuito cuántico de 12 qubits ejecutado en IBM Quantum, "
                        "con precios reales."),
        barra="Notebook de la clase, ya ejecutado", codigo="Código en GitHub", descargar="Descargar el notebook",
        otro="en", otro_nombre="English", figura="Figura {n} del notebook, sección {seccion}"),
    "en": dict(
        notebook="FULL_PROJECT/en/notebook/Quantum_Finance_CACIC2026.ipynb", region="en_US", recursos="../assets/",
        tarjeta="assets/social-card-en.png",
        titulo="Notebook: quantum computing for finance in Qiskit, step by step",
        descripcion=("An executed Qiskit notebook: real prices from Yahoo Finance, the Markowitz efficient frontier, "
                     "parametric circuits, VQE, a 12-qubit risk circuit, noisy simulation and the result on an IBM "
                     "quantum computer."),
        og_titulo="Notebook: quantum computing for finance in Qiskit",
        og_descripcion=("From the Markowitz efficient frontier to a 12-qubit quantum circuit run on IBM Quantum, "
                        "with real prices."),
        barra="Class notebook, already executed", codigo="Code on GitHub", descargar="Download the notebook",
        otro="es", otro_nombre="Español", figura="Figure {n} of the notebook, section {seccion}"),
}

SIN_TEXTO = 'alt="No description has been provided for this image"'


def cambiar(texto, patron, nuevo):
    """Reemplaza un patrón que tiene que aparecer exactamente una vez."""
    texto, n = re.subn(patron, lambda _: nuevo, texto)
    assert n == 1, f"se esperaba una aparición de {patron!r} y hay {n}"
    return texto


def describir_figuras(pagina, plantilla):
    """Pone como texto alternativo de cada figura el título de la sección en la que está."""
    titulos = [(m.start(), html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).replace("¶", "").strip())
               for m in re.finditer(r"<h[23][^>]*>(.*?)</h[23]>", pagina, flags=re.S)]
    partes, n = pagina.split(SIN_TEXTO), 0
    salida, pos = [partes[0]], len(partes[0])
    for parte in partes[1:]:
        n += 1
        seccion = [t for p, t in titulos if p < pos][-1]
        salida.append(f'alt="{html.escape(plantilla.format(n=n, seccion=seccion), quote=True)}"' + parte)
        pos += len(SIN_TEXTO) + len(parte)
    return "".join(salida), n


def generar(idioma):
    """Exporta el notebook de un idioma y le agrega la cabecera, la barra superior y los textos alternativos."""
    tx = IDIOMAS[idioma]
    notebook, salida, url = RAIZ / tx["notebook"], RAIZ / "docs" / PAGINAS[idioma], SITIO + PAGINAS[idioma]
    datos = {"@context": "https://schema.org", "@type": "TechArticle", "headline": tx["titulo"],
             "description": tx["descripcion"], "url": url, "inLanguage": idioma, "datePublished": "2026-10-04",
             "isAccessibleForFree": True, "license": "https://opensource.org/licenses/MIT",
             "image": SITIO + tx["tarjeta"], "isPartOf": {"@id": SITIO + "#material"},
             "author": [{"@type": "Person", "name": n, "affiliation": {"@type": "Organization", "name": a}} for n, a in AUTORES]}
    alternos = "\n".join(f'<link rel="alternate" hreflang="{i}" href="{SITIO}{p}">' for i, p in PAGINAS.items())
    cabecera = f"""<title>{tx["titulo"]}</title>
<meta name="description" content="{tx["descripcion"]}">
<meta name="author" content="{', '.join(n for n, _ in AUTORES)}">
<link rel="canonical" href="{url}">
{alternos}
<link rel="alternate" hreflang="x-default" href="{SITIO}{PAGINAS["es"]}">
<link rel="icon" type="image/svg+xml" href="{tx["recursos"]}favicon.svg">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Quantum Portfolio Risk">
<meta property="og:locale" content="{tx["region"]}">
<meta property="og:title" content="{tx["og_titulo"]}">
<meta property="og:description" content="{tx["og_descripcion"]}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITIO}{tx["tarjeta"]}">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{json.dumps(datos, ensure_ascii=False)}</script>"""
    barra = f"""<div style="font:16px/1.4 system-ui,-apple-system,'Segoe UI',Helvetica,Arial,sans-serif;background:#0E1B2C;color:#F7F5EF;padding:12px 20px;display:flex;flex-wrap:wrap;gap:8px 22px;align-items:center">
<a href="./" style="color:#F7F5EF;font-weight:700;text-decoration:none">Quantum Portfolio Risk</a>
<span style="color:#9FB3C8">{tx["barra"]}</span>
<a href="{REPO}" style="color:#7FB7E6;margin-left:auto">{tx["codigo"]}</a>
<a href="{REPO}/blob/main/{tx["notebook"]}" style="color:#7FB7E6">{tx["descargar"]}</a>
<a href="{SITIO}{PAGINAS[tx["otro"]]}" hreflang="{tx["otro"]}" lang="{tx["otro"]}" style="color:#7FB7E6">{tx["otro_nombre"]}</a>
</div>"""
    pagina, _ = HTMLExporter().from_filename(str(notebook))
    pagina = cambiar(pagina, r'<html lang="en">', f'<html lang="{idioma}">')
    pagina = cambiar(pagina, r"<title>[^<]*</title>", cabecera)
    pagina = cambiar(pagina, r"<body[^>]*>", re.search(r"<body[^>]*>", pagina).group() + "\n" + barra)
    pagina, figuras = describir_figuras(pagina, tx["figura"])
    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.write_text(pagina, encoding="utf-8")
    print("escrito", salida.relative_to(RAIZ), "|", len(pagina.encode()) // 1000, "KB |", figuras, "figuras con texto alternativo")


for idioma in (sys.argv[1:] or list(IDIOMAS)):
    generar(idioma)
