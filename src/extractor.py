import json

from gemini_client import GeminiClient
from schemas import (
    CNHExtractionResult,
    GenericExtractionResult,
    InvoiceExtractionResult,
    PaperExtractionResult,
)

class DocumentExtractor:
    def __init__(self):
        self.client = GeminiClient()

    @staticmethod
    def _build_prompt(case: str) -> str:
        prompts = {
            "generic": """
    Você é um sistema de extração de dados de documentos.

    Analise o documento enviado e retorne somente um JSON válido com esta estrutura:

    {
    "document_type": "tipo provável do documento",
    "summary": "resumo curto do conteúdo",
    "extracted_fields": {
        "campo": "valor"
    },
    "limitations": ["limitações ou campos incertos"]
    }

    Não inclua texto fora do JSON.
    """,
            "cnh": """
    Você é um sistema de extração de dados de documentos brasileiros.

    Analise a CNH enviada e retorne somente um JSON válido com esta estrutura:

    {
    "document_type": "CNH",
    "extracted_fields": {
        "nome": null,
        "cpf": null,
        "data_nascimento": null,
        "data_emissao": null,
        "data_validade": null,
        "categoria": null,
        "filiacao_pai": null,
        "filiacao_mae": null
    },
    "confidence_notes": ["campos incertos ou não encontrados"],
    "limitations": ["limitações da extração"]
    }

    Não inclua texto fora do JSON.
    """,
            "invoice": """
    Você é um sistema de extração de dados de faturas de energia elétrica.

    Analise a fatura enviada e retorne somente um JSON válido com esta estrutura:

    {
    "document_type": "Fatura de Energia",
    "extracted_fields": {
        "titular": null,
        "endereco": null,
        "numero_cliente": null,
        "mes_referencia": null,
        "data_vencimento": null,
        "valor_total": null,
        "consumo_kwh": null
    },
    "confidence_notes": ["campos incertos ou não encontrados"],
    "limitations": ["limitações da extração"]
    }

    Não inclua texto fora do JSON.
    """,
            "paper": """
    Você é um sistema de extração e estruturação de documentos técnicos extensos.

    Analise o documento enviado e retorne somente um JSON válido com esta estrutura:

    {
    "document_type": "Documento Técnico ou Artigo",
    "summary": "resumo objetivo do documento",
    "sections": [
        {
        "title": "nome da seção",
        "content_summary": "resumo da seção"
        }
    ],
    "tables_detected": ["descrição das tabelas identificadas"],
    "figures_or_charts_detected": ["descrição de figuras, gráficos ou imagens identificadas"],
    "limitations": ["limitações da extração"]
    }

    Não inclua texto fora do JSON.
    """,
            }

        return prompts[case]
    
    @staticmethod
    def _parse_result(case: str, data: dict):
        if case == "cnh":
            return CNHExtractionResult(**data)

        if case == "invoice":
            return InvoiceExtractionResult(**data)

        if case == "paper":
            return PaperExtractionResult(**data)

        return GenericExtractionResult(**data)

    @staticmethod
    def _clean_json_response(text: str) -> str:
        text = text.strip()

        if text.startswith("```json"):
            return text.replace("```json", "").replace("```", "").strip()

        if text.startswith("```"):
            return text.replace("```", "").strip()

        return text

    def extract(self, file_path: str, case: str = "generic"):
        prompt = self._build_prompt(case)
        raw_response = self.client.generate_from_document(file_path, prompt)
        cleaned_response = self._clean_json_response(raw_response)

        try:
            data = json.loads(cleaned_response)
            return self._parse_result(case, data)

        except Exception:
            return GenericExtractionResult(
                document_type="unknown",
                summary="Não foi possível estruturar a resposta automaticamente.",
                extracted_fields={"raw_response": raw_response},
                limitations=["A resposta do modelo não pôde ser convertida para o schema esperado."],
            )