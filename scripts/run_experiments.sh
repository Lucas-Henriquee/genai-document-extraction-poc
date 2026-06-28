#!/usr/bin/env bash

set +e

export LC_ALL=C
export LC_NUMERIC=C

RUNS=2
SLEEP_SECONDS=60

mkdir -p outputs/experiments
mkdir -p reports

SUMMARY_FILE="reports/experiment_results.csv"

echo "case,run,input_file,file_size_mb,output_file,total_time_seconds,status" > "$SUMMARY_FILE"

declare -A FILES
FILES["cnh"]="data/samples/cnh_sample.jpeg"
FILES["invoice"]="data/samples/energy_invoice.jpg"
FILES["paper"]="data/samples/claude_paper.pdf"

for CASE in cnh invoice paper; do
  INPUT_FILE="${FILES[$CASE]}"

  if [ ! -f "$INPUT_FILE" ]; then
    echo "Arquivo não encontrado: $INPUT_FILE"
    echo "$CASE,0,$INPUT_FILE,,,""file_not_found" >> "$SUMMARY_FILE"
    continue
  fi

  FILE_SIZE_BYTES=$(stat -c%s "$INPUT_FILE")
  FILE_SIZE_MB=$(awk "BEGIN {printf \"%.2f\", $FILE_SIZE_BYTES / 1024 / 1024}")

  for RUN in $(seq 1 $RUNS); do
    if [ "$CASE" = "paper" ]; then
      OUTPUT_FILE="outputs/experiments/${CASE}_run_${RUN}.md"
    else
      OUTPUT_FILE="outputs/experiments/${CASE}_run_${RUN}.json"
    fi

    TIME_FILE="outputs/experiments/${CASE}_run_${RUN}_time.txt"

    echo "======================================"
    echo "Caso: $CASE | Execução: $RUN"
    echo "Entrada: $INPUT_FILE"
    echo "Tamanho: ${FILE_SIZE_MB} MB"
    echo "Saída: $OUTPUT_FILE"

    /usr/bin/time -f "%e" -o "$TIME_FILE" \
      python src/main.py --input "$INPUT_FILE" --case "$CASE" --output "$OUTPUT_FILE"

    EXIT_CODE=$?
    ELAPSED=$(cat "$TIME_FILE")

    if [ $EXIT_CODE -eq 0 ]; then
      STATUS="success"
      echo "Execução concluída com sucesso em ${ELAPSED}s"
    else
      STATUS="error"
      echo "Erro detectado na execução do modelo em ${ELAPSED}s. Exit Code: $EXIT_CODE"
    fi

    echo "$CASE,$RUN,$INPUT_FILE,$FILE_SIZE_MB,$OUTPUT_FILE,$ELAPSED,$STATUS" >> "$SUMMARY_FILE"

    if [ $RUN -lt $RUNS ] || [ "$CASE" != "paper" ]; then
      echo "Aguardando ${SLEEP_SECONDS}s antes da próxima chamada..."
      sleep "$SLEEP_SECONDS"
    fi
  done
done

python scripts/summarize_results.py

echo "======================================"
echo "Resultados brutos: $SUMMARY_FILE"
echo "Resumo de latência: reports/latency_summary.csv"