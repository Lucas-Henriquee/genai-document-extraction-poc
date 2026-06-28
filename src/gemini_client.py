import mimetypes
from pathlib import Path

from google import genai
from google.genai import types, errors
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
        max_attempts = 3

        for attempt in range(1, max_attempts + 1):
            try:
                attempt_start = time.perf_counter()

                response = self.client.models.generate_content(
                    model=self.model,
                    contents=[file_part, prompt],
                )

                attempt_time = time.perf_counter() - attempt_start
                total_time = time.perf_counter() - total_start

                print(f"Resposta recebida em {attempt_time:.2f} segundos")
                print(f"Tempo total: {total_time:.2f} segundos")

                return response.text.strip()

            except errors.ServerError as error:
                if attempt == max_attempts:
                    raise error

                wait_seconds = 10 * attempt
                print(
                    f"Tentativa {attempt}/{max_attempts} falhou por indisponibilidade do servidor "
                    f"Aguardando {wait_seconds}s antes de tentar novamente..."
                )
                time.sleep(wait_seconds)

            except errors.ClientError as error:
                status_code = getattr(error, "status_code", None)

                if status_code != 429 or attempt == max_attempts:
                    raise error

                wait_seconds = 20 * attempt
                print(
                    f"Tentativa {attempt}/{max_attempts} falhou por rate limit "
                    f"Aguardando {wait_seconds}s antes de tentar novamente..."
                )
                time.sleep(wait_seconds)

        raise RuntimeError("Falha inesperada ao chamar o modelo")