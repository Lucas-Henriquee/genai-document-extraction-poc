import csv
from collections import defaultdict
from pathlib import Path


INPUT_FILE = Path("reports/experiment_results.csv")
OUTPUT_FILE = Path("reports/latency_summary.csv")


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {INPUT_FILE}")

    times_by_case = defaultdict(list)

    with INPUT_FILE.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["status"] != "success":
                continue

            case = row["case"]
            elapsed = float(row["total_time_seconds"])
            times_by_case[case].append(elapsed)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "case",
                "count",
                "mean_seconds",
                "min_seconds",
                "max_seconds",
            ]
        )

        for case, times in times_by_case.items():
            mean = sum(times) / len(times)

            writer.writerow(
                [
                    case,
                    len(times),
                    round(mean, 2),
                    round(min(times), 2),
                    round(max(times), 2),
                ]
            )

    print(f"Resumo salvo em: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()