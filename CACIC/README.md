# Aplicaciones Financieras en la Computación Cuántica

Material de la clase de Juan Pablo Braña (CAETI, Universidad Abierta Interamericana) en la XXX Escuela Internacional
de Informática del CACIC 2026, UTN Facultad Regional Concepción del Uruguay, 5 al 9 de octubre de 2026. Forma parte
del Curso 3: "Fundamentos e Intuición del Cómputo Cuántico – De los Principios a sus Aplicaciones".

Es de nivel introductorio. Se arman carteras con precios reales de 12 empresas conocidas y se recorre el camino
completo, de la teoría clásica de Markowitz a un circuito que corre en una computadora cuántica de IBM.

El notebook también se puede leer en línea, ya ejecutado, en el
[sitio del proyecto](https://314-ia.github.io/quantum-portfolio-risk/notebook.html).

## Contenido

| Carpeta o archivo | Qué es |
|---|---|
| `presentacion/Aplicaciones_Financieras_Computacion_Cuantica_CACIC2026.pdf` | Las 26 diapositivas de la clase: 17 de la exposición y un anexo de 9 que explica el notebook sección por sección |
| `notebook/Finanzas_Cuanticas_CACIC2026.ipynb` | El notebook de la clase, ya ejecutado, con salidas y figuras |
| `notebook/datos/resultado_hardware.json` | Resultado real del circuito de 12 qubits en `ibm_fez`: número de trabajo y las 4.000 mediciones |
| `notebook/datos/experimento_110_qubits_ibm_fez.csv` | Índices de riesgo de la corrida de 110 qubits en `ibm_fez` del 27 de junio de 2026 |
| `notebook/requirements.txt` | Paquetes necesarios, en las versiones con que se construyó y probó el notebook |
| `notebook/.env.example` | Plantilla para las credenciales de IBM Quantum |
| `material_extra/figuras/` | Las figuras de las diapositivas en PNG |

## Qué recorre el notebook

| Sección | Tema | Dónde corre |
|---|---|---|
| 1 | Precios reales de 12 acciones | Yahoo Finance |
| 2 | Teoría moderna de carteras: la frontera eficiente | Computadora clásica |
| 3 | Circuitos paramétricos: una perilla que cambia probabilidades | Simulador cuántico |
| 4 | Un optimizador cuántico, VQE, elige una cartera | Simulador cuántico |
| 5 | Un circuito que estima el riesgo de cada activo | Simulador cuántico |
| 6 | Por qué ese circuito no arranca con Hadamard | Simulador cuántico |
| 7 | El mismo circuito con ruido y en una computadora cuántica | Simulador con ruido e IBM Quantum |
| 8 | Evaluación con datos que el modelo nunca vio | Computadora clásica |

## Cómo correrlo

```bash
git clone https://github.com/314-ia/quantum-portfolio-risk.git
cd quantum-portfolio-risk/CACIC
python3 -m venv .venv
.venv/bin/pip install -r notebook/requirements.txt
.venv/bin/jupyter lab notebook/Finanzas_Cuanticas_CACIC2026.ipynb
```

- Las versiones fijadas en `notebook/requirements.txt` exigen Python 3.12 como mínimo. Se probó con Python 3.13.
- En Windows los ejecutables están en `.venv\Scripts\`.
- En Google Colab alcanza con descomentar la línea `%pip` de la primera celda de código.
- El notebook corre de arriba hacia abajo en alrededor de un minuto. Todo lo cuántico se ejecuta en simuladores,
  salvo la sección 7.2.
- Los dos gráficos de curvas, en las secciones 1 y 8, son interactivos en JupyterLab: se arrastra el mouse para
  agrandar una zona, al pasarlo se ven los valores y la leyenda funciona como filtro de curvas. En GitHub y en
  cualquier visor sin JavaScript se ven como imagen fija.
- Los precios se bajan de Yahoo Finance al ejecutar. El notebook guarda una copia en `notebook/datos/` para poder
  trabajar después sin conexión. Esa copia no se sube al repositorio.

## Cómo correrlo en una computadora cuántica real

Tal como está publicado, el notebook muestra el resultado guardado de la corrida del 4 de octubre de 2026 y no
envía nada. Para enviar una corrida propia:

1. Crear una cuenta gratuita en [IBM Quantum](https://quantum.cloud.ibm.com) y obtener la API key y la instancia.
2. Copiar `notebook/.env.example` con el nombre `.env` y completar los valores. El notebook lo busca junto a él,
   en la carpeta `CACIC/` o en la raíz del repositorio. Ese archivo es personal: no se comparte ni se sube.
3. Borrar o renombrar `notebook/datos/resultado_hardware.json`.
4. En la sección 7.2, poner `EJECUTAR_EN_HARDWARE = True` y ejecutar la celda.

El notebook guarda el número de trabajo antes de esperar. Si la cola es larga se puede interrumpir y volver a
ejecutar la celda más tarde con el valor en `False`: va a buscar el resultado por su número de trabajo.
El plan gratuito de IBM da 10 minutos de procesador por mes y este circuito usa unos pocos segundos.

## Resultado en hardware real

El circuito de 12 qubits se ejecutó en el procesador `ibm_fez` de IBM el 4 de octubre de 2026.
Trabajo `db1djj3id5ic73er0ceg`: 4.000 mediciones, 3 segundos de procesador. Circuito traducido al chip: profundidad
15, con 8 compuertas de dos qubits.

| Activo | Riesgo propio R | Ideal | Simulador con ruido | Hardware real |
|---|---|---|---|---|
| KO | 0,000 | 0,095 | 0,090 | 0,108 |
| JPM | 0,000 | 0,096 | 0,108 | 0,101 |
| BAC | 0,128 | 0,128 | 0,134 | 0,143 |
| PEP | 0,142 | 0,142 | 0,139 | 0,153 |
| AAPL | 0,292 | 0,292 | 0,290 | 0,279 |
| XOM | 0,314 | 0,449 | 0,424 | 0,445 |
| MSFT | 0,236 | 0,502 | 0,497 | 0,468 |
| AMZN | 0,359 | 0,510 | 0,509 | 0,497 |
| CVX | 0,325 | 0,529 | 0,514 | 0,513 |
| MELI | 0,585 | 0,585 | 0,580 | 0,567 |
| NVDA | 0,692 | 0,692 | 0,695 | 0,681 |
| TSLA | 1,000 | 0,950 | 0,941 | 0,943 |

- La diferencia promedio con el ideal fue 0,015 en hardware y 0,010 en el simulador con ruido. El error de muestreo
  esperable con 4.000 mediciones llega a 0,008. La mayor diferencia es la de MSFT: 0,034.
- El orden de riesgo coincide con el ideal. Solo se invierten KO y JPM, que en el ideal están empatados.
- La cartera elige los mismos seis activos que el ideal, con pesos casi iguales. En los 12 meses de prueba tuvo una
  volatilidad de 11,9 %. El mercado tuvo 12,5 % y la cartera de mínimo riesgo de Markowitz, 9,6 %.
- En el experimento de 110 qubits la diferencia promedio con el ideal fue 0,10: el ruido crece con el tamaño del
  circuito.

No hay ventaja cuántica: este circuito se puede simular en una laptop y el método clásico logra menos riesgo.

## Diapositivas y notebook

| Diapositivas | Sección del notebook |
|---|---|
| Teoría moderna de carteras y frontera eficiente, 2 a 4 | 2 |
| Circuitos paramétricos, 5 y 6 | 3 |
| VQE y QAOA, 7 | 4 |
| Nuestra aproximación, 8 | 5 |
| Optimizadores cuánticos y nuestra aproximación, 9 | 4, 5 y 8 |
| Por qué no arrancamos con Hadamard, 10 | 6 |
| Nuestro código en seis pasos, 11 | 1, 5, 7 y 8 |
| Quantum Portfolio Optimizer y nuestra propuesta, 12 | No está en el notebook |
| Del pizarrón al notebook, 13 | Acá se pasa a la demostración |
| Cómo leer los resultados, 14 | 7 y 8 |

## Fuentes de la comparación con IBM

La diapositiva 12 compara esta propuesta con el Quantum Portfolio Optimizer, una Qiskit Function de Global Data
Quantum disponible en el catálogo de IBM. La comparación se hizo leyendo su documentación: la función no se ejecutó,
porque exige un plan Premium, Flex u On-Prem.

- Guía: https://quantum.cloud.ibm.com/docs/en/guides/global-data-quantum-optimizer
- Manuscrito asociado: arXiv:2412.19150
- 7 activos x 4 períodos x 4 qubits de resolución = 112 qubits.
- Circuitos = (num_generations + 1) x population_size = 21 x 90 = 1.890 en el ejemplo de 112 qubits.
- Uso de procesador de ese ejemplo: 12.735 segundos, unas 3,5 horas.
- En sus cuatro pruebas publicadas, el optimizador clásico Gurobi obtiene menor costo objetivo.

Las dos soluciones resuelven problemas distintos. La función de IBM busca la cartera óptima y la rebalancea en
varios períodos. Esta propuesta estima un índice de riesgo por activo y no rebalancea.

## Aviso y licencia

Es material educativo. Nada de lo que hay acá es una recomendación de inversión. Licencia [MIT](../LICENSE).
