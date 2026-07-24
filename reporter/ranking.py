from rich.console import Console
from rich.table import Table

console = Console()


def show_batch_ranking(results):
    results = sorted(
        results,
        key=lambda report: report["score"]["total"],
        reverse=True
    )
    table = Table(title="Batch Ranking")

    table.add_column("Rank", justify="center", style="cyan")
    table.add_column("Project", style="green")
    table.add_column("Score", justify="center", style="yellow")
    table.add_column("Rating", style="magenta")

    for index, report in enumerate(results, start=1):

        table.add_row(
            str(index),
            report["project"].title(),
            f'{report["score"]["total"]}/100',
            report["score"]["rating"]
        )

    console.print(table)
def show_batch_summary(results):

    total_projects = len(results)

    console.print()
    console.rule("[bold cyan]SUMMARY")

    console.print(f"Projects Scanned : {total_projects}")
    highest = max(
        results,
        key=lambda report: report["score"]["total"]
    )

    console.print(
        f'Highest Score : {highest["project"].title()} ({highest["score"]["total"]}/100)'
    )
    total_score = sum(
        report["score"]["total"]
        for report in results
    )

    average_score = total_score / total_projects

    console.print(
        f"Average Score : {average_score:.1f}/100"
    )
    high = 0
    medium = 0
    low = 0

    for report in results:

        rating = report["score"]["rating"]

        if rating == "Very High Potential":
            high += 1

        elif rating == "High Potential":
            high += 1

        elif rating == "Medium Potential":
            medium += 1

        else:
            low += 1
    console.print()
    console.print(f"High Potential   : {high}")
    console.print(f"Medium Potential : {medium}")
    console.print(f"Low Potential    : {low}")