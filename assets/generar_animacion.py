"""Genera la animación SVG de "Cómo se compone el método" que muestra el README.

Usa los datos reales de la clase, tomados de la tabla de CACIC/README.md: la probabilidad de medir 1 en
cada qubit después de la rotación RY, después de las compuertas CRY, y el índice medido en ibm_fez.
No necesita ningún paquete. Uso: python3 generar_animacion.py como-se-compone-el-metodo.svg"""
import math, sys

T = 18.0                                   # segundos por ciclo
W, H = 1000, 440
TICKERS = ["AAPL", "MSFT", "AMZN", "NVDA", "TSLA", "MELI", "JPM", "BAC", "XOM", "CVX", "KO", "PEP"]
# Probabilidad de medir 1 después de cada etapa (tabla de CACIC/README.md): tras RY, tras CRY (ideal) y medida en ibm_fez
TRAS_RY = dict(AAPL=.292, MSFT=.236, AMZN=.359, NVDA=.692, TSLA=.950, MELI=.585, JPM=.000, BAC=.128, XOM=.314, CVX=.325, KO=.000, PEP=.142)
IDEAL   = dict(AAPL=.292, MSFT=.502, AMZN=.510, NVDA=.692, TSLA=.950, MELI=.585, JPM=.096, BAC=.128, XOM=.449, CVX=.529, KO=.095, PEP=.142)
MEDIDO  = dict(AAPL=.279, MSFT=.468, AMZN=.497, NVDA=.681, TSLA=.943, MELI=.567, JPM=.101, BAC=.143, XOM=.445, CVX=.513, KO=.108, PEP=.153)
PARES = [("MSFT", "AMZN"), ("JPM", "BAC"), ("XOM", "CVX"), ("KO", "PEP")]
ELEGIDOS = set(sorted(TICKERS, key=MEDIDO.get)[:6])

X0, X1, YQ, RB = 60, 940, 134, 31          # fila de qubits
BASE, ALTO = 372, 108                      # barras: línea de base y altura para índice 1
x = {t: X0 + k * (X1 - X0) / 11 for k, t in enumerate(TICKERS)}
angulo = lambda p: math.degrees(2 * math.asin(math.sqrt(p)))
AZUL, NARANJA = (127, 183, 230), (242, 166, 90)
color = lambda p: "#%02x%02x%02x" % tuple(round(a + (b - a) * p) for a, b in zip(AZUL, NARANJA))
n = lambda v: f"{v:.1f}".rstrip("0").rstrip(".")

def onda(xa, xb, sentido=1, puntos=70, amplitud=5.0, ciclos=4):
    """Camino ondulado entre dos qubits vecinos, por debajo de la fila. Devuelve el trazado y su largo."""
    p0, p1, p2 = (xa + 12 * sentido, YQ + 35), ((xa + xb) / 2, YQ + 82), (xb - 12 * sentido, YQ + 35)
    pts = []
    for i in range(puntos + 1):
        t = i / puntos
        bx = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
        by = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
        dx = 2 * (1 - t) * (p1[0] - p0[0]) + 2 * t * (p2[0] - p1[0]); dy = 2 * (1 - t) * (p1[1] - p0[1]) + 2 * t * (p2[1] - p1[1])
        largo = math.hypot(dx, dy) or 1
        a = amplitud * math.sin(2 * math.pi * ciclos * t) * math.sin(math.pi * t)
        pts.append((bx - dy / largo * a, by + dx / largo * a))
    total = sum(math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(puntos))
    return "M" + " L".join(f"{n(px)},{n(py)}" for px, py in pts), total

s = []
s.append(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d" font-family="-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif">
<title id="t">Cómo se compone el método</title>
<desc id="d">Doce qubits, uno por activo. Una rotación RY carga en cada qubit el riesgo propio del activo. Compuertas CRY agregan el contagio entre activos correlacionados. Al medir, la frecuencia de 1 de cada qubit es su índice de riesgo. La cartera toma los seis activos de menor índice.</desc>
<defs>
  <radialGradient id="fondo" cx="50%" cy="38%" r="75%"><stop offset="0" stop-color="#16304f"/><stop offset="1" stop-color="#0b1626"/></radialGradient>
  <linearGradient id="haz" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#F7F5EF" stop-opacity="0"/><stop offset=".5" stop-color="#F7F5EF" stop-opacity=".95"/><stop offset="1" stop-color="#F7F5EF" stop-opacity="0"/></linearGradient>
  <filter id="brillo" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="2.6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <clipPath id="marco"><rect width="{W}" height="{H}" rx="14"/></clipPath>
  <pattern id="trama" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".8" fill="#7FB7E6" opacity=".10"/></pattern>
</defs>
<style>
  .c {{ animation-duration: {T:g}s; animation-iteration-count: infinite; animation-fill-mode: both; animation-timing-function: ease-in-out; }}
  .qubit {{ animation-name: aparecer; }}
  .flecha {{ transform: rotate(var(--b)); animation-name: girar; }}
  .enlace {{ opacity: .42; animation-name: enlazar; }}
  .foton {{ opacity: 0; animation-name: viajar; animation-timing-function: linear; }}
  .barrido {{ opacity: 0; animation-name: barrer; animation-timing-function: linear; }}
  .barra {{ animation-name: crecer; }}
  .valor {{ animation-name: mostrar; }}
  .resto {{ opacity: .3; animation-name: atenuar; }}
  .marca {{ animation-name: elegir; }}
  .leyenda {{ opacity: 0; animation-name: none; }}
  .l1 {{ animation-name: leer1; }} .l2 {{ animation-name: leer2; }} .l3 {{ animation-name: leer3; }} .l4 {{ animation-name: leer4; }}
  .l5 {{ opacity: 1; animation-name: leer5; }}
  .mota {{ animation: titilar 5s ease-in-out infinite; }}
  .ondas {{ opacity: 0; animation-name: colapsar; }}
  .onda {{ animation: fluir 9s linear infinite; }}
  @keyframes aparecer {{ 0% {{ opacity: 0 }} 6%, 94% {{ opacity: 1 }} 100% {{ opacity: 0 }} }}
  @keyframes girar {{ 0%, 10% {{ transform: rotate(0deg) }} 26%, 36% {{ transform: rotate(var(--a)) }} 50%, 94% {{ transform: rotate(var(--b)) }} 100% {{ transform: rotate(0deg) }} }}
  @keyframes enlazar {{ 0%, 30% {{ opacity: 0 }} 33%, 93% {{ opacity: .42 }} 97%, 100% {{ opacity: 0 }} }}
  @keyframes viajar {{ 0%, 31.9% {{ opacity: 0; stroke-dashoffset: var(--s) }} 32% {{ opacity: 1; stroke-dashoffset: var(--s) }} 40% {{ opacity: 1; stroke-dashoffset: var(--f) }} 40.1% {{ opacity: 1; stroke-dashoffset: var(--s) }} 48% {{ opacity: 1; stroke-dashoffset: var(--f) }} 48.1%, 100% {{ opacity: 0; stroke-dashoffset: var(--f) }} }}
  @keyframes barrer {{ 0%, 53.9% {{ opacity: 0; transform: translateX(34px) }} 54% {{ opacity: 1; transform: translateX(34px) }} 66% {{ opacity: 1; transform: translateX(966px) }} 67%, 100% {{ opacity: 0; transform: translateX(966px) }} }}
  @keyframes crecer {{ 0%, 54% {{ transform: scaleY(0); opacity: 1 }} 58%, 85% {{ transform: scaleY(1); opacity: 1 }} 87%, 100% {{ transform: scaleY(1); opacity: 0 }} }}
  @keyframes mostrar {{ 0%, 58% {{ opacity: 0 }} 60%, 85% {{ opacity: 1 }} 87%, 100% {{ opacity: 0 }} }}
  @keyframes atenuar {{ 0%, 70% {{ opacity: 1 }} 74%, 92% {{ opacity: .3 }} 96%, 100% {{ opacity: 1 }} }}
  @keyframes elegir {{ 0%, 70% {{ opacity: 0 }} 74%, 92% {{ opacity: 1 }} 95%, 100% {{ opacity: 0 }} }}
  @keyframes leer1 {{ 0% {{ opacity: 0 }} 2%, 8% {{ opacity: 1 }} 10%, 100% {{ opacity: 0 }} }}
  @keyframes leer2 {{ 0%, 10% {{ opacity: 0 }} 12%, 29% {{ opacity: 1 }} 31%, 100% {{ opacity: 0 }} }}
  @keyframes leer3 {{ 0%, 31% {{ opacity: 0 }} 33%, 50% {{ opacity: 1 }} 52%, 100% {{ opacity: 0 }} }}
  @keyframes leer4 {{ 0%, 52% {{ opacity: 0 }} 54%, 68% {{ opacity: 1 }} 70%, 100% {{ opacity: 0 }} }}
  @keyframes leer5 {{ 0%, 70% {{ opacity: 0 }} 72%, 92% {{ opacity: 1 }} 94%, 100% {{ opacity: 0 }} }}
  @keyframes colapsar {{ 0% {{ opacity: 0 }} 6%, 54% {{ opacity: 1 }} 66%, 100% {{ opacity: 0 }} }}
  @keyframes fluir {{ from {{ transform: translateX(0) }} to {{ transform: translateX(-240px) }} }}
  @keyframes titilar {{ 0%, 100% {{ opacity: .15 }} 50% {{ opacity: .7 }} }}
  @media (prefers-reduced-motion: reduce) {{ .c, .mota, .onda {{ animation: none !important }} }}
</style>
<rect width="{W}" height="{H}" rx="14" fill="url(#fondo)"/>
<rect width="{W}" height="{H}" rx="14" fill="url(#trama)"/>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="14" fill="none" stroke="#28405f"/>
<text x="34" y="36" font-size="12.5" font-weight="600" letter-spacing="2.4" fill="#7FB7E6">CÓMO SE COMPONE EL MÉTODO</text>
<text x="{W - 34}" y="36" font-size="12.5" text-anchor="end" fill="#8FA5BD">12 activos reales · 12 qubits · resultado medido en ibm_fez</text>''')

# motas de fondo
import random
rnd = random.Random(7)
for i in range(18):
    s.append(f'<circle class="mota" cx="{rnd.uniform(20, W - 20):.0f}" cy="{rnd.uniform(52, H - 60):.0f}" r="{rnd.choice([.9, 1.1, 1.4])}" fill="#BFD9F2" style="animation-delay:-{rnd.uniform(0, 5):.1f}s;animation-duration:{rnd.uniform(3.5, 7):.1f}s"/>')

# ondas de fondo: la superposición antes de medir
def seno(y0, amp, fase, largo_onda=240):
    pts = [(xx, y0 + amp * math.sin(2 * math.pi * xx / largo_onda + fase)) for xx in range(-10, W + 260, 10)]
    return "M" + " L".join(f"{px},{py:.1f}" for px, py in pts)
s.append('<g class="c ondas" clip-path="url(#marco)">')
for y0, amp, fase, col_o, op, dur in ((262, 16, 0.0, "#7FB7E6", .20, 9), (292, 22, 1.7, "#7FB7E6", .13, 13), (322, 13, 3.1, "#F2A65A", .14, 11)):
    s.append(f'<path class="onda" d="{seno(y0, amp, fase)}" fill="none" stroke="{col_o}" stroke-width="1.6" opacity="{op}" style="animation-duration:{dur}s"/>')
s.append("</g>")

# referencia de lectura: arriba 0, abajo 1
s.append(f'<g font-size="10" fill="#8FA5BD" text-anchor="middle"><text x="16" y="{YQ - RB + 4}">0</text><text x="16" y="{YQ + RB + 3}">1</text>'
         f'<path d="M22,{YQ - RB} h5 M22,{YQ + RB} h5" stroke="#8FA5BD" stroke-width=".8"/></g>')

# enlaces y paquetes de onda (contagio)
for a, b in PARES:
    ida, largo = onda(x[a], x[b], 1)
    vuelta, _ = onda(x[b], x[a], -1)
    s.append(f'<path class="c enlace" d="M{n(x[a] + 12)},{YQ + 35} Q{n((x[a] + x[b]) / 2)},{YQ + 82} {n(x[b] - 12)},{YQ + 35}" fill="none" stroke="#F2A65A" stroke-width="1.2" stroke-dasharray="2 4"/>')
    tramo = 0.36 * largo
    for d, retraso in ((ida, 0), (vuelta, 0.55)):
        s.append(f'<path class="c foton" d="{d}" fill="none" stroke="#FFE2BD" stroke-width="2.5" stroke-linecap="round" filter="url(#brillo)" stroke-dasharray="{tramo:.1f} {largo + tramo:.1f}" style="--s:{tramo:.1f};--f:-{largo:.1f};animation-delay:{retraso}s"/>')

# qubits
for k, t in enumerate(TICKERS):
    xk, a, b = x[t], angulo(TRAS_RY[t]), angulo(IDEAL[t])
    col, elegido = color(MEDIDO[t]), t in ELEGIDOS
    abre = "" if elegido else '<g class="c resto">'
    cierra = "" if elegido else "</g>"
    dur, ini = 2.2 + 0.23 * ((k * 5) % 7), -0.37 * k
    orbita = f"M{n(xk - 37)},{YQ} a37,11 0 1,0 74,0 a37,11 0 1,0 -74,0"
    s.append(f'''{abre}<g class="c qubit" style="animation-delay:{0.07 * k:.2f}s">
  <text x="{n(xk)}" y="80" font-size="13" font-weight="600" text-anchor="middle" fill="#DCE6F0">{t}</text>
  <circle cx="{n(xk)}" cy="{YQ}" r="{RB}" fill="#0b1626" fill-opacity=".55" stroke="#7FB7E6" stroke-opacity=".28"/>
  <g transform="rotate(-18 {n(xk)} {YQ})"><path d="{orbita}" fill="none" stroke="#7FB7E6" stroke-opacity=".22" stroke-width=".8"/>
    <circle r="2.2" fill="#BFD9F2" filter="url(#brillo)"><animateMotion dur="{dur:.2f}s" begin="{ini:.2f}s" repeatCount="indefinite" path="{orbita}"/></circle></g>
  <g class="c flecha" style="transform-origin:{n(xk)}px {YQ}px;--a:{a:.1f}deg;--b:{b:.1f}deg">
    <path d="M{n(xk)},{YQ} V{YQ - 22}" stroke="{col}" stroke-width="2.6" stroke-linecap="round"/>
    <path d="M{n(xk - 5)},{YQ - 20.5} L{n(xk)},{YQ - 30} L{n(xk + 5)},{YQ - 20.5} Z" fill="{col}"/></g>
  <circle cx="{n(xk)}" cy="{YQ}" r="4.6" fill="#F7F5EF" filter="url(#brillo)"/>
</g>''')
    # barra con el índice medido
    h = ALTO * MEDIDO[t]
    retraso = 0.12 * T * (xk - 34) / 932
    s.append(f'''<rect class="c barra" x="{n(xk - 13)}" y="{BASE - h:.1f}" width="26" height="{h:.1f}" rx="3" fill="{col}" style="transform-origin:{n(xk)}px {BASE}px;animation-delay:{retraso:.2f}s"/>
<text class="c valor" x="{n(xk)}" y="{BASE - h - 7:.1f}" font-size="11.5" text-anchor="middle" fill="#DCE6F0" style="animation-delay:{retraso:.2f}s">{f"{MEDIDO[t]:.2f}".replace(".", ",")}</text>{cierra}''')
    if elegido:
        s.append(f'<g class="c marca"><rect x="{n(xk - 15.5)}" y="{BASE - h - 2.5:.1f}" width="31" height="{h + 2.5:.1f}" rx="4.5" fill="none" stroke="#F7F5EF" stroke-width="1.4"/>'
                 f'<circle cx="{n(xk)}" cy="{BASE + 13}" r="3.4" fill="#F7F5EF"/></g>')

s.append(f'<path d="M34,{BASE + .5} H{W - 34}" stroke="#3a5373" stroke-width="1"/>')
s.append(f'<g class="c barrido"><rect x="-16" y="90" width="32" height="{BASE - 86}" fill="url(#haz)" opacity=".13"/><rect x="-5" y="90" width="10" height="{BASE - 86}" fill="url(#haz)" opacity=".22"/><rect x="-1.1" y="90" width="2.2" height="{BASE - 86}" fill="url(#haz)"/></g>')

leyendas = ["Cada activo es un qubit",
            "RY carga el riesgo propio: a más riesgo, más gira la flecha hacia el 1",
            "CRY agrega el contagio entre los activos que se mueven juntos",
            "Se mide una sola vez: la frecuencia de 1 es el índice de riesgo",
            "La cartera toma los seis activos de menor índice"]
for i, txt in enumerate(leyendas, 1):
    s.append(f'<text class="c leyenda l{i}" x="{W / 2:g}" y="{H - 20}" font-size="18.5" text-anchor="middle" fill="#F7F5EF">'
             f'<tspan fill="#F2A65A" font-weight="700">{i}</tspan><tspan fill="#5d7696">  ·  </tspan>{txt}</text>')
s.append("</svg>")
open(sys.argv[1], "w", encoding="utf-8").write("\n".join(s) + "\n")
print("escrito", sys.argv[1], "|", sum(len(p) for p in s) // 1000, "KB | elegidos:", sorted(ELEGIDOS, key=MEDIDO.get))
