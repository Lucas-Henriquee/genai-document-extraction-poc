import json

from gemini_client import GeminiClient
from schemas import GenericExtractionResult

class DocumentExtractor:
    def __init__(self):
        self.client = GeminiClient()

    @staticmethod
    def _build_generic_prompt() -> str:
        return """
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
    """

    @staticmethod
    def _clean_json_response(text: str) -> str:
        text = text.strip()

        if text.startswith("```json"):
            return text.replace("```json", "").replace("```", "").strip()

        if text.startswith("```"):
            return text.replace("```", "").strip()

        return text

    def extract_generic(self, file_path: str) -> GenericExtractionResult:
        prompt = self._build_generic_prompt()
        raw_response = self.client.generate_from_document(file_path, prompt)
        cleaned_response = self._clean_json_response(raw_response)

        try:
            data = json.loads(cleaned_response)
            return GenericExtractionResult(**data)

        except Exception:
            return GenericExtractionResult(
                document_type="unknown",
                summary="Não foi possível estruturar a resposta automaticamente.",
                extracted_fields={"raw_response": raw_response},
                limitations=["A resposta do modelo não pôde ser convertida para o schema esperado."],
            )