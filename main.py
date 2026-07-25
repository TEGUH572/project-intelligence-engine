from rich.console import Console
from rich.progress import Progress

from config import APP_NAME, APP_VERSION

from researcher.search import find_official_website
from researcher.website import get_website_info

from researcher.github import GitHubResearch
from repository_ranker import (
    rank_repositories
)
from analyzer.scorer import calculate_score
from analyzer.summary import generate_summary
from analyzer.intelligence import analyze_project
from analyzer.knowledge import get_project_knowledge
from reporter.exporter import export_json, export_markdown, export_batch_json, export_batch_markdown
from reporter.ranking import show_batch_ranking, show_batch_summary
from scanner.batch import get_projects

console = Console()

def show_header():

    console.rule(
        f"[bold blue]{APP_NAME} v{APP_VERSION}"
    )

def show_searching():

    console.print(
        "\n[yellow]🔍 Mencari website resmi...[/yellow]"
    )
def show_research_result(project, website, info):

    console.print()

    console.rule(
        "[bold green]HASIL RISET"
    )

    console.print(
        f"Project     : {project}"
    )

    console.print(
        f"Website     : {website}"
    )

    console.print(
        f"Title       : "
        f"{info.get('title', 'Not Found')}"
    )

    console.print(
        f"Description : "
        f"{info.get('description', 'Not Found')}"
    )
def show_social_links(socials):

    console.print()

    console.rule(
        "[bold cyan]SOCIAL LINKS"
    )

    for name, value in socials.items():

        console.print(
            f"{name.title():10}: "
            f"{value if value else 'Not Found'}"
        )

def show_project_analysis(analysis):

    console.print()

    console.rule(
        "[bold magenta]PROJECT ANALYSIS"
    )

    console.print(
        f"Category    : "
        f"{analysis.get('category', 'Unknown')}"
    )

    console.print(
        f"Blockchain  : "
        f"{analysis.get('blockchain', 'Unknown')}"
    )

    console.print(
        f"Token       : "
        f"{analysis.get('token', 'Not Found')}"
    )

    console.print(
        f"Testnet     : "
        f"{'Yes' if analysis.get('testnet') else 'No'}"
    )

    console.print(
        f"Mainnet     : "
        f"{'Yes' if analysis.get('mainnet') else 'No'}"
    )

    console.print(
        f"Bridge      : "
        f"{'Yes' if analysis.get('bridge') else 'No'}"
    )

    console.print(
        f"Explorer    : "
        f"{'Yes' if analysis.get('explorer') else 'No'}"
    )

def show_github_header():

    console.print()

    console.rule(
        "[bold cyan]GITHUB INTELLIGENCE"
    )

def show_ai_summary(summary):

    console.print()

    console.rule(
        "[bold green]EXECUTIVE SUMMARY"
    )

    console.print("[bold]Strengths[/bold]")

    if summary["strengths"]:

        for item in summary["strengths"]:

            console.print(f"✓ {item}")

    else:

        console.print("- None")

    console.print()

    console.print("[bold]Warnings[/bold]")

    if summary["warnings"]:

        for item in summary["warnings"]:

            console.print(f"• {item}")

    else:

        console.print("- None")

    console.print()

    console.print(
        f"[bold]Conclusion[/bold]\n"
        f"{summary['conclusion']}"
    )

def scan_project(project):

    show_header()    
    show_searching()

    website = find_official_website(
        project
    )

    if not website:

        console.print(
            "[red]❌ Website resmi tidak ditemukan.[/red]"
        )

        return

    console.print(
        f"[green]✅ Website ditemukan:[/green] "
        f"{website}"
    )

    # ==================================================
    # GET WEBSITE INFORMATION
    # ==================================================

    info = get_website_info(
        website
    )

    # ==================================================
    # PROJECT INTELLIGENCE
    # ==================================================

    analysis = analyze_project(
        info
    )

    # ==================================================
    # KNOWLEDGE
    # ==================================================

    knowledge = get_project_knowledge(
        project
    )

    # ==================================================
    # PROJECT INTELLIGENCE
    # ==================================================

    console.print()

    console.rule(
        "[bold yellow]PROJECT INTELLIGENCE"
    )

    # ==================================================
    # MERGE KNOWLEDGE BASE
    # ==================================================

    if knowledge:

        analysis["category"] = knowledge.get(
            "category",
            analysis["category"]
        )

        analysis["blockchain"] = knowledge.get(
            "blockchain",
            analysis["blockchain"]
        )

        analysis["token"] = knowledge.get(
            "token",
            analysis["token"]
        )

        analysis["testnet"] = knowledge.get(
            "testnet",
            analysis["testnet"]
        )

        analysis["mainnet"] = knowledge.get(
            "mainnet",
            analysis["mainnet"]
        )

        analysis["bridge"] = knowledge.get(
            "bridge",
            analysis["bridge"]
        )

        analysis["explorer"] = knowledge.get(
            "explorer",
            analysis["explorer"]
        )

    show_research_result(
        project,
        website,
        info
    )

    socials = info.get(
        "socials",
        {}
    )

    show_social_links(socials)

    show_project_analysis(analysis)

    show_github_header()

    github_research = GitHubResearch(
        project,
        website
    )

    github_info = github_research.analyze(
        socials.get("docs")
    )

    # ==================================================
    # OFFICIAL REPOSITORY RANKING
    # ==================================================

    repository_candidates = [
        {
           "name": github_info.get(
                "github_url",
                "Unknown"
            ),
            "officiality_score": (
                github_info.get(
                    "verification_score",
                    0
                ) * 40 / 100
            ),
            "stars": github_info.get(
                "stars",
                0
            ),
            "forks": github_info.get(
                "forks",
                0
            ),
            "contributors": github_info.get(
                "contributors",
                0
            ),
            "commits": github_info.get(
                "commits",
                0
            ),
            "archived": github_info.get(
                "archived",
                False
            )
        }
    ]

    ranked_repositories = rank_repositories(
        repository_candidates
)
    # ==================================================
    # REPOSITORY RANKING DISPLAY
    # ==================================================

    console.print()

    console.rule(
        "[bold blue]"
        "OFFICIAL REPOSITORY RANKING"
    )

    for repo in ranked_repositories:

        repo_score = repo[
            "repository_score"
        ]

        console.print()

        console.print(
            f"Rank         : "
            f"{repo['rank']}"
        )

        console.print(
            f"Repository   : "
            f"{repo['name']}"
        )

        console.print(
            f"Officiality  : "
            f"{repo_score['officiality']}/40"
        )

        console.print(
            f"Activity     : "
            f"{repo_score['activity']}/25"
        )

        console.print(
            f"Developers   : "
            f"{repo_score['developers']}/15"
        )

        console.print(
            f"Popularity   : "
            f"{repo_score['popularity']}/10"
        )

        console.print(
            f"Maintenance  : "
            f"{repo_score['maintenance']}/10"
        )

        console.print(
            f"Total Score  : "
            f"{repo_score['total']}/100"
        )
    # ==================================================
    # GITHUB BASIC INFORMATION
    # ==================================================

    console.print(
        f"GitHub URL   : "
        f"{github_info.get('github_url') or 'Not Found'}"
    )

    console.print(
        f"Discovery    : "
        f"{github_info.get('discovery_source', 'Not Found')}"
    )

    console.print(
        f"Organization : "
        f"{github_info.get('organization') or 'Not Found'}"
    )

    console.print(
        f"Verified     : "
        f"{github_info.get('verification_status', 'Unverified')}"
    )

    console.print(
        f"Verification : "
        f"{github_info.get('verification_score', 0)}/100"
    )

    console.print(
        f"Repositories : "
        f"{github_info.get('repositories', 0)}"
    )

    console.print(
        f"Stars        : "
        f"{github_info.get('stars', 0)}"
    )

    console.print(
        f"Forks        : "
        f"{github_info.get('forks', 0)}"
    )

    console.print(
        f"Watchers     : "
        f"{github_info.get('watchers', 0)}"
    )

    console.print(
        f"Issues       : "
        f"{github_info.get('issues', 0)}"
    )

    console.print(
        f"Pull Requests: "
        f"{github_info.get('pull_requests', 0)}"
    )

    console.print(
        f"Releases     : "
        f"{github_info.get('releases', 0)}"
    )

    console.print(
        f"Contributors : "
        f"{github_info.get('contributors', 0)}"
    )

    console.print(
        f"License      : "
        f"{github_info.get('license', 'Unknown')}"
    )

    languages = github_info.get(
        "languages",
        []
    )

    console.print(
        f"Languages    : "
        f"{', '.join(languages) if languages else 'Not Found'}"
    )

    console.print(
        f"Created At   : "
        f"{github_info.get('created_at', 'Not Found')}"
    )

    console.print(
        f"Updated At   : "
        f"{github_info.get('updated_at', 'Not Found')}"
    )

    console.print(
        f"Last Commit  : "
        f"{github_info.get('last_commit', 'Not Found')}"
    )

    console.print(
        f"GitHub Score : "
        f"{github_info.get('score', 0)}/25"
    )

    # ==================================================
    # KNOWLEDGE BASE DISPLAY
    # ==================================================

    console.print()

    console.rule(
        "[bold yellow]KNOWLEDGE BASE"
    )

    if knowledge:

        console.print(
            f"Funding     : "
            f"{knowledge.get('funding', 'Unknown')}"
        )

        console.print(
            f"Investors   : "
            f"{knowledge.get('investors', 'Unknown')}"
        )

        console.print(
            f"Ecosystem   : "
            f"{'Yes' if knowledge.get('ecosystem') else 'No'}"
        )

    else:

        console.print(
            "No Knowledge Base data found."
        )

    # ==================================================
    # AIRDROP SCORE
    # ==================================================

    score = calculate_score(
        info,
        analysis,
        github_info,
        knowledge
    )
    summary = generate_summary(
        analysis,
        github_info,
        knowledge,
        score
    )

    # ==================================================
    # PROJECT HEALTH SCORE
    # ==================================================

    console.print()

    console.rule(
        "[bold green]"
        "PROJECT HEALTH SCORE"
    )

    console.print(
        f"Total Score : "
        f"{score.get('total', 0)}/100"
    )

    console.print(
        f"Rating      : "
        f"{score.get('rating', 'Unknown')}"
    )

    # ==================================================
    # SCORE BREAKDOWN
    # ==================================================

    console.print()

    console.rule(
        "[bold cyan]"
        "SCORE BREAKDOWN"
    )

    breakdown = score.get(
        "breakdown",
        {}
    )

    for name, points in breakdown.items():

        console.print(
            f"{name.title():20}: "
            f"{points} points"
        )

    # ==================================================
    # FINAL RATING
    # ==================================================

    console.print()

    rating = score.get(
        "rating",
        "Unknown"
    )

    if rating == "Very High Potential":

        console.print(
            "[bold green]"
            "⭐⭐⭐⭐⭐ Very High Potential"
            "[/bold green]"
        )

    elif rating == "High Potential":

        console.print(
            "[bold cyan]"
            "⭐⭐⭐⭐ High Potential"
            "[/bold cyan]"
        )

    elif rating == "Medium Potential":

        console.print(
            "[bold yellow]"
            "⭐⭐⭐ Medium Potential"
            "[/bold yellow]"
        )

    else:

        console.print(
            "[bold red]"
            "⭐⭐ Low Potential"
            "[/bold red]"
        )

    show_ai_summary(summary)

    # ==================================================
    # EXPORT REPORT
    # ==================================================

    report = {
        "project": project,
        "website": website,
        "title": info.get("title"),
        "description": info.get("description"),
        "socials": socials,
        "analysis": analysis,
        "github": github_info,
        "knowledge": knowledge,
        "score": score
    }

    json_file = export_json(project, report)
    md_file = export_markdown(project, report)
    console.print()
    console.rule("[bold blue]REPORT EXPORT")
    console.print(f"[green]JSON Report : {json_file}[/green]")
    console.print(f"[green]Markdown Report : {md_file}[/green]")
    return report
def main():

    while True:

        console.rule(
            f"[bold blue]{APP_NAME} v{APP_VERSION}"
    )

        print("1. Single Scan")
        print("2. Batch Scan")
        print("3. Exit")

        choice = input("\nPilih menu : ").strip()

        if choice == "1":

            project = input(
                "\nNama Proyek : "
            ).strip()

            if project:

                scan_project(project)

        elif choice == "2":

            projects = get_projects()

            if not projects:

                continue

            total = len(projects)
            results = []

            with Progress() as progress:

                task = progress.add_task(
                    "[cyan]Scanning Projects...",
                    total=total
                )

            for project in projects:

                report = scan_project(project)

                if report:
                    results.append(report)

                progress.update(
                    task,
                    advance=1
                )
            show_batch_summary(results)
            batch_json = export_batch_json(results)
            batch_md = export_batch_markdown(results)

            console.print()
            console.rule("[bold green]BATCH REPORT EXPORT")
            console.print(f"Batch JSON Report     : {batch_json}")
            console.print(f"Batch Markdown Report : {batch_md}")
        elif choice == "3":

            console.print(
                "\n[green]Terima kasih.[/green]"
            )

            break

        else:

            console.print("[red]Pilihan tidak valid.[/red]"
            )
# ==================================================
# RUN PROGRAM
# ==================================================

if __name__ == "__main__":
    main()             