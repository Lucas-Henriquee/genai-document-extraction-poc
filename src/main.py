import argparse
import json
from pathlib import Path

from extractor import DocumentExtractor


def main():
    parser = argparse.ArgumentParser(
        description="POC de extração de dados de documentos com IA generativa multimodal."
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Caminho do documento PDF ou imagem."
    )

    parser.add_argument(
    "--case",
    default="generic",
    choices=["generic", "cnh", "invoice", "paper"],
    help="Tipo de documento a ser processado."
    )

    parser.add_argument(
        "--output",
        default="outputs/result.json",
        help="Caminho do arquivo JSON de saída."
    )

    args = parser.parse_args()

    extractor = DocumentExtractor()
    result = extractor.extract(args.input, case=args.case)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        if isinstance(result, str):
            file.write(result)
        else:
            json.dump(result.model_dump(), file, ensure_ascii=False, indent=2)

    print(f"Resultado salvo em: {output_path}")


if __name__ == "__main__":
    main()