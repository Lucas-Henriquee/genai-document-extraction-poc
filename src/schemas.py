from typing import Any

from pydantic import BaseModel, Field


class GenericExtractionResult(BaseModel):
    document_type: str = Field(description="Tipo provável do documento")
    summary: str = Field(description="Resumo curto do conteúdo")
    extracted_fields: dict[str, Any] = Field(default_factory=dict)
    limitations: list[str] = Field(default_factory=list)

class CNHExtractionResult(BaseModel):
    document_type: str = "CNH"
    extracted_fields: dict[str, Any] = Field(default_factory=dict)
    confidence_notes: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)

class InvoiceExtractionResult(BaseModel):
    document_type: str = "Fatura de Energia"
    extracted_fields: dict[str, Any] = Field(default_factory=dict)
    layout_sections: list[dict[str, Any]] = Field(default_factory=list)
    tables_detected: list[str] = Field(default_factory=list)
    confidence_notes: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)