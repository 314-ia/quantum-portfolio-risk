# quantum-portfolio-risk

Circuitos cuánticos paramétricos para evaluar el riesgo de carteras de inversión, con datos reales de mercado y
ejecución en computadoras cuánticas de IBM.

> **In English.** Parametric quantum circuits for portfolio risk assessment, built from real market data and run on
> IBM Quantum hardware. This repository starts with the material of a class given at the CACIC 2026 school, in
> Spanish: slides and a Qiskit notebook that runs on simulators and on a real quantum processor.

## Contenido

| Carpeta | Qué es |
|---|---|
| [`CACIC/`](CACIC/) | Material de la clase "Aplicaciones Financieras en la Computación Cuántica", Escuela Internacional de Informática del CACIC 2026: diapositivas y un notebook de Qiskit listo para correr |

Está previsto sumar más adelante el código del trabajo de investigación en el que se basa la clase.

## La idea en pocas líneas

- Cada activo de la cartera es un qubit.
- Una rotación RY carga en el qubit el riesgo propio del activo. Compuertas RY controladas entre activos muy
  correlacionados agregan el contagio.
- Los ángulos se calculan directamente de los datos históricos. No hay un bucle de optimización como en VQE o QAOA.
- Al medir, la frecuencia de 1 de cada qubit es su índice de riesgo. La cartera se arma con los activos de menor índice.

## Qué se puede afirmar y qué no

- El circuito corre en hardware actual. Con 12 qubits el resultado real casi coincide con el ideal. Con 110 qubits
  el ruido crece y el orden general de riesgo se mantiene.
- No hay ventaja cuántica. Estos circuitos se pueden simular en una laptop, y un método clásico como el de Markowitz
  logra carteras de menor riesgo.
- El valor está en el método para validar un circuito contra su versión ideal y contra un modelo clásico, y en el
  paso siguiente: usar el circuito dentro de la estimación de amplitud cuántica.

## Trabajo de referencia

J. P. Braña, A. M. J. Litterio, A. Fernández y S. E. Sepúlveda Cuevas, "A Parametric Quantum Circuit for Portfolio
Risk Assessment at 110 Qubits: Three-Way Validation and a Demonstrator of the Path to Advantage via Amplitude
Estimation", aceptado en el Workshop Chileno de Computación Cuántica e Ingeniería de Software Cuántico
(QCQSE-Chile), JCC 2026.

## Aviso

Es material educativo y de investigación. Nada de lo que hay acá es una recomendación de inversión.

## Licencia

[MIT](LICENSE). Los precios de mercado provienen de Yahoo Finance y no se redistribuyen en este repositorio: el
notebook los descarga al ejecutarse.
