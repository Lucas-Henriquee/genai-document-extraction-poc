from typing import Any

from pydantic import BaseModel, Field


class GenericExtractionResult(BaseModel):
    document_type: str = Field(description="Tipo provável do documento")
    summary: str = Field(description="Resumo curto do conteúdo")
    extracted_fields: dict[str, Any] = Field(default_factory=dict)
    limitations: list[str] = Field(default_factory=list)