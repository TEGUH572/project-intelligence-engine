from time import sleep
from rich.progress import Progress

with Progress() as progress:

    task = progress.add_task(
        "[green]Scanning...",
        total=10
    )

    for i in range(10):
        sleep(0.5)
        progress.update(task, advance=1)