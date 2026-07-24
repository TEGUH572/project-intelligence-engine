import json
from pathlib import Path
from datetime import datetime


REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(exist_ok=True)


def export_json(project_name, data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = REPORT_DIR / f"{project_name}_{timestamp}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return filename

def export_markdown(project_name, data):

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = REPORT_DIR / f"{project_name}_{timestamp}.md"

    with open(filename, "w", encoding="utf-8") as f:

        f.write(f"# {project_name}\n\n")

        for key, value in data.items():
            f.write(f"## {key}\n")
            f.write(f"{value}\n\n")

    return filename
def export_batch_json(results):

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = REPORT_DIR / f"batch_{timestamp}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    return filename
def export_batch_markdown(results):

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = REPORT_DIR / f"batch_{timestamp}.md"

    with open(filename, "w", encoding="utf-8") as f:

        f.write("# Batch Scan Report\n\n")

        for index, report in enumerate(results, start=1):

            f.write(f"## {index}. {report['project'].title()}\n\n")
            f.write(f"- Score : {report['score']['total']}/100\n")
            f.write(f"- Rating : {report['score']['rating']}\n")
            f.write(f"- Website : {report['website']}\n\n")

    return filename