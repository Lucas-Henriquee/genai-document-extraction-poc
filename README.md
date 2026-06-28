# genai-document-extraction-poc

POC de extração de dados de documentos com modelo multimodal Gemini em chamada única.

## Requisitos

- Python 3.12+
- API key do [Google AI Studio](https://aistudio.google.com/app/apikey)

## Instalação

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

```bash
cp .env.example .env
# edite o .env com sua GEMINI_API_KEY
```

## Uso

```bash
# CNH — saída JSON com campos predeterminados
python src/main.py --input data/samples/cnh_sample.jpeg --case cnh --output outputs/cnh_result.json

# Fatura de energia — saída JSON com campos e seções de layout
python src/main.py --input data/samples/energy_invoice.jpg --case invoice --output outputs/invoice_result.json

# Documento técnico extenso — saída Markdown preservando tabelas e figuras
python src/main.py --input data/samples/claude_paper.pdf --case paper --output outputs/paper_result.md
```

## Experimentos

```bash
chmod +x scripts/run_experiments.sh
./scripts/run_experiments.sh
```

Gera `reports/experiment_results.csv` com latência por execução e `reports/latency_summary.csv` com média, mínimo e máximo por caso.