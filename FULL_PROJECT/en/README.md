# Financial Applications of Quantum Computing

**English** · [Español](../README.md)

Material of the class given by Juan Pablo Braña (CAETI, Universidad Abierta Interamericana) at the XXX International
School of Informatics of CACIC 2026, UTN Facultad Regional Concepción del Uruguay, Argentina, October 5 to 9, 2026. It is
part of Course 3: "Foundations and Intuition of Quantum Computing – From Principles to Applications".

It is introductory. Portfolios are built from the real prices of 12 well-known companies, and the class walks the whole
path, from Markowitz's classical theory to a circuit that runs on an IBM quantum computer.

The class was taught in Spanish. This folder is the complete English version: the notebook with its code and outputs
translated, the slides and the figures. The data and the results are the same as in the Spanish version.

The notebook can also be read online, already executed, on the
[project website](https://314-ia.github.io/quantum-portfolio-risk/en/notebook.html).

## Contents

| Folder or file | What it is |
|---|---|
| `slides/Financial_Applications_of_Quantum_Computing_CACIC2026.pdf` | The 30 slides of the class: 18 for the talk and a 12-slide appendix that explains the notebook section by section |
| `notebook/Quantum_Finance_CACIC2026.ipynb` | The class notebook, already executed, with outputs and figures |
| `notebook/data/hardware_result.json` | Real result of the 12-qubit circuit on `ibm_fez`: job id and the 4,000 shots |
| `notebook/data/110_qubit_experiment_ibm_fez.csv` | Risk indices from the 110-qubit run on `ibm_fez` of June 27, 2026 |
| `notebook/requirements.txt` | Required packages, in the versions the notebook was built and tested with |
| `notebook/.env.example` | Template for the IBM Quantum credentials |
| `extras/figures/` | The figures of the slides, as PNG |

## What the notebook covers

| Section | Topic | Where it runs |
|---|---|---|
| 1 | Real prices of 12 stocks | Yahoo Finance |
| 2 | Modern portfolio theory: the efficient frontier | Classical computer |
| 3 | Parametric circuits: a knob that changes probabilities | Quantum simulator |
| 4 | A quantum optimizer, VQE, picks a portfolio | Quantum simulator |
| 5 | A circuit that estimates the risk of each asset | Quantum simulator |
| 6 | Why that circuit does not start with Hadamard | Quantum simulator |
| 7 | The same circuit with noise and on a quantum computer | Noisy simulator and IBM Quantum |
| 8 | Evaluation on the following 12 months and a new out-of-sample test | Classical computer |

## How to run it

```bash
git clone https://github.com/314-ia/quantum-portfolio-risk.git
cd quantum-portfolio-risk/FULL_PROJECT/en
python3 -m venv .venv
.venv/bin/pip install -r notebook/requirements.txt
.venv/bin/jupyter lab notebook/Quantum_Finance_CACIC2026.ipynb
```

- The versions pinned in `notebook/requirements.txt` require Python 3.12 or newer. Tested with Python 3.13.
- On Windows the executables are in `.venv\Scripts\`.
- On Google Colab it is enough to uncomment the `%pip` line in the first code cell.
- The notebook runs top to bottom in about a minute. Everything quantum runs on simulators, except section 7.2.
- The two line charts, in sections 1 and 8, are interactive in JupyterLab: drag the mouse to zoom into an area, hover to
  see the values, and use the legend as a filter for the curves. On GitHub, and in any viewer without JavaScript, they
  show as a static image.
- Prices are downloaded from Yahoo Finance at run time. The notebook saves a copy in `notebook/data/` so you can work
  offline afterwards. That copy is not uploaded to the repository.

## How to run it on a real quantum computer

As published, the notebook shows the saved result of the run of October 4, 2026 and sends nothing. To send a run of
your own:

1. Create a free account at [IBM Quantum](https://quantum.cloud.ibm.com) and get the API key and the instance.
2. Copy `notebook/.env.example` as `.env` and fill in the values. The notebook looks for it next to itself, in
   `FULL_PROJECT/en/`, in `FULL_PROJECT/` or at the repository root. That file is personal: do not share it or upload it.
3. Delete or rename `notebook/data/hardware_result.json`.
4. In section 7.2, set `RUN_ON_HARDWARE = True` and run the cell.

The notebook saves the job id before waiting. If the queue is long you can interrupt it and run the cell again later
with the value set to `False`: it will fetch the result by its job id.
IBM's free plan gives 10 minutes of processor time per month, and this circuit uses a few seconds.

## Result on real hardware

The 12-qubit circuit was executed on IBM's `ibm_fez` processor on October 4, 2026.
Job `db1djj3id5ic73er0ceg`: 4,000 shots, 3 seconds of processor time. Circuit translated to the chip: depth 15, with
8 two-qubit gates.

| Asset | Own risk R | Ideal | Noisy simulator | Real hardware |
|---|---|---|---|---|
| KO | 0.000 | 0.095 | 0.090 | 0.108 |
| JPM | 0.000 | 0.096 | 0.108 | 0.101 |
| BAC | 0.128 | 0.128 | 0.134 | 0.143 |
| PEP | 0.142 | 0.142 | 0.139 | 0.153 |
| AAPL | 0.292 | 0.292 | 0.290 | 0.279 |
| XOM | 0.314 | 0.449 | 0.424 | 0.445 |
| MSFT | 0.236 | 0.502 | 0.497 | 0.468 |
| AMZN | 0.359 | 0.510 | 0.509 | 0.497 |
| CVX | 0.325 | 0.529 | 0.514 | 0.513 |
| MELI | 0.585 | 0.585 | 0.580 | 0.567 |
| NVDA | 0.692 | 0.692 | 0.695 | 0.681 |
| TSLA | 1.000 | 0.950 | 0.941 | 0.943 |

- The average gap to the ideal was 0.015 on hardware and 0.010 on the noisy simulator. The sampling error to be expected
  with 4,000 shots reaches 0.008. The largest gap is MSFT's: 0.034.
- The risk ordering matches the ideal. Only KO and JPM swap places, and they are tied in the ideal.
- The portfolio weights the 12 assets by 1 / index, with no cut-off: with the hardware index, KO 20%, JPM 20%, BAC 15%,
  PEP 14%, AAPL 7% and between 2 and 4% for the rest; with the ideal index, almost the same. On FUTURE, the following
  12 months, it had 11.0% volatility; the market, 12.5%; Markowitz, 9.6%; the classical analogue, all 12 weighted by
  1 / historical volatility, 10.3%. On the five months after that, May to September 2026: circuit 10.5%, analogue 10.0%,
  market 12.4%, Markowitz 13.6%.
- In the 110-qubit experiment the average gap to the ideal was 0.10: noise grows with the size of the circuit.

There is no quantum advantage: this circuit can be simulated on a laptop, and the classical method achieves less risk.
The control test in section 8 of the notebook is harsher: with the same portfolio rule, weighting the 12 by
1 / historical volatility does better than weighting them by the circuit's index. The portfolio rule was changed twice
after seeing the first evaluation, the last time by design, so that no number would be a decision of ours; that is why
the figures are exploratory.

## Slides and notebook

| Slides | Notebook section |
|---|---|
| Map of the territory, 2 | Not in the notebook |
| Modern portfolio theory and the efficient frontier, 3 to 5 | 2 |
| Parametric circuits, 6 to 9 | 3 and 5 |
| VQE and QAOA, 10 | 4 |
| Our approach, 11 | 5 |
| Quantum optimizers and our approach, 12 | 4, 5 and 8 |
| Why we do not start with Hadamard, 13 | 6 |
| Our code in six steps, 14 | 1, 5, 7 and 8 |
| From 4,000 shots to the portfolio, 15 | 7 and 8 |
| Quantum Portfolio Optimizer and our proposal, 16 | Not in the notebook |
| How to read the results, 17 | 7 and 8 |
| Appendix, 19 to 30 | The whole notebook, section by section, with the code cells of each part |

## Sources of the comparison with IBM

Slide 16 compares this proposal with the Quantum Portfolio Optimizer, a Qiskit Function by Global Data Quantum available
in IBM's catalog. The comparison was made by reading its documentation: the function was not executed, because it
requires a Premium, Flex or On-Prem plan.

- Guide: https://quantum.cloud.ibm.com/docs/en/guides/global-data-quantum-optimizer
- Associated manuscript: arXiv:2412.19150
- 7 assets x 4 periods x 4 resolution qubits = 112 qubits.
- Circuits = (num_generations + 1) x population_size = 21 x 90 = 1,890 in the 112-qubit example.
- Processor usage of that example: 12,735 seconds, about 3.5 hours.
- In its four published tests, the classical optimizer Gurobi obtains a lower objective cost.

The two solutions solve different problems. IBM's function searches for the optimal portfolio and rebalances it over
several periods. This proposal estimates a risk index per asset and does not rebalance.

## Disclaimer and license

This is educational material. Nothing here is investment advice. [MIT](../../LICENSE) license.
