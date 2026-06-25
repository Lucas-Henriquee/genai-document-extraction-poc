import mimetypes
from pathlib import Path

from google import genai
from google.genai import types
import time

from config import settings


class GeminiClient:
    def __init__(self):
        if not settings.GEMINI_API_KEY:
            raise RuntimeError("GEMINI_API_KEY não encontrada no arquivo .env")

        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model = settings.GEMINI_MODEL

    @staticmethod
    def _detect_mime_type(file_path: Path) -> str:
        mime_type, _ = mimetypes.guess_type(file_path)

        if mime_type:
            return mime_type

        if file_path.suffix.lower() == ".pdf":
            return "application/pdf"

        raise ValueError(f"Tipo de arquivo não suportado: {file_path.suffix}")

    def generate_from_document(self, file_path: str, prompt: str) -> str:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

        total_start = time.perf_counter()
        file_size_mb = path.stat().st_size / 1024 / 1024
        mime_type = self._detect_mime_type(path)

        print(f"Arquivo: {path}")
        print(f"Tamanho: {file_size_mb:.2f} MB")
        print(f"MIME type: {mime_type}")
        print("Lendo arquivo e preparando envio...")

        file_part = types.Part.from_bytes(
            data=path.read_bytes(),
            mime_type=mime_type,
        )

        print("Chamando modelo Gemini...")

        response = self.client.models.generate_content(
            model=self.model,
            contents=[file_part, prompt],
        )

        total_end = time.perf_counter()
        print(f"Tempo total: {total_end - total_start:.2f} segundos")

        return response.text.strip()