import json

from gemini_client import GeminiClient
from prompts import PROMPTS
from schemas import (
    CNHExtractionResult,
    GenericExtractionResult,
    InvoiceExtractionResult,
)

class DocumentExtractor:
    def __init__(self):
        self.client = GeminiClient()

    @staticmethod
    def _clean_json_response(text: str) -> str:
        text = text.strip()

        if text.startswith("```json"):
            return text.replace("```json", "").replace("```", "").strip()

        if text.startswith("```"):
            return text.replace("```", "").strip()

        return text

    @staticmethod
    def _build_prompt(case: str) -> str:
        if case not in PROMPTS:
            raise ValueError(f"Tipo de documento não suportado: {case}")

        return PROMPTS[case]

    @staticmethod
    def _parse_result(case: str, data: dict):
        if case == "cnh":
            return CNHExtractionResult(**data)

        if case == "invoice":
            return InvoiceExtractionResult(**data)

        return GenericExtractionResult(**data)

    def extract(self, file_path: str, case: str = "generic"):
        prompt = self._build_prompt(case)
        raw_response = self.client.generate_from_document(file_path, prompt)

        if case == "paper":
            return raw_response

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