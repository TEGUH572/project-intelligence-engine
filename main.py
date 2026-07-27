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
from analyzer.recommendation import generate_recommendation
from analyzer.recommendation import generate_integration_guide
from analyzer.code_generator import generate_code_examples
from analyzer.sdk import get_sdk
from analyzer.intelligence import analyze_project
from analyzer.knowledge import get_project_knowledge
from reporter.exporter import export_json, export_markdown, export_batch_json, export_batch_markdown
from reporter.ranking import show_batch_ranking, show_batch_summary
from scanner.batch import get_projects

console = Console()

def print_field(label, value):

    console.print(
        f"[cyan]{label:<15}[/cyan]: {value}"
    )

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

    knowledge = get_project_knowledge( project)

    sdk = get_sdk(project)


    if sdk:
        knowledge["sdk_info"] = sdk

    examples = generate_code_examples(
        knowledge,
        sdk
    )

    # ==================================================
    # PROJECT INTELLIGENCE
    # ==================================================

    console.print()

    console.rule(
        "[bold cyan]SUPERFLUID PROJECT INTELLIGENCE"
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
        "[bold yellow]SUPERFLUID KNOWLEDGE"
    )

    if knowledge:

        console.print(
            f"Funding      : {knowledge.get('funding', 'Unknown')}"
        )

        investors = knowledge.get("investors", [])

        console.print(
            f"Investors    : {', '.join(investors) if investors else 'Unknown'}"
        )

        console.print(
            f"Ecosystem    : {'Yes' if knowledge.get('ecosystem') else 'No'}"
        )

        console.print(
            f"SDK          : {'Available' if knowledge.get('sdk') else 'No'}"
        )

        console.print(
            f"Streaming    : {'Native' if knowledge.get('streaming') else 'No'}"
        )

        networks = knowledge.get("supported_networks", [])

        console.print(
            f"Networks     : {', '.join(networks) if networks else 'Unknown'}"
        )

        use_cases = knowledge.get("use_cases", [])

        console.print(
            f"Use Cases    : {', '.join(use_cases) if use_cases else 'None'}"
        )

    else:

        console.print(
            "No Knowledge Base data found."
        )

    # ==================================================
    # SDK INTELLIGENCE
    # ==================================================

    console.print()

    console.rule(
        "[bold cyan]SDK INTELLIGENCE"
    )

    sdk_info = knowledge.get("sdk_info", {})

    if sdk_info:

        console.print(
            f"SDK Available    : {'Yes' if sdk_info.get('available') else 'No'}"
        )

        console.print()

        console.print("[bold]Languages[/bold]")

        for lang in sdk_info.get("languages", []):
            console.print(f"✓ {lang}")

        console.print()

        console.print("[bold]Packages[/bold]")

        for package in sdk_info.get("packages", []):
            console.print(f"• {package}")

        console.print()

        console.print(
            f"Install Command  : {sdk_info.get('install', 'Unknown')}"
        )

        console.print(
            f"Package Manager  : {sdk_info.get('package_manager', 'Unknown')}"
        )

        console.print(
            f"Developer Docs   : {sdk_info.get('docs', 'Unknown')}"
        )

        console.print(
            f"Official Examples: {sdk_info.get('examples', 0)}"
        )

    else:

        console.print(
            "No SDK information available."
        )

    # ==================================================
    # CODE EXAMPLES
    # ==================================================

    console.print()

    console.rule(
        "[bold green]CODE EXAMPLES"
    )

    console.print(
        "[bold]Install Command[/bold]"
    )

    console.print(
        sdk_info.get(
            "install",
            "Unknown"
        )
    )

    console.print()

    console.print(
        "[bold]Documentation[/bold]"
    )

    console.print(
        sdk_info.get(
            "docs",
            "Unknown"
        )
    )

    console.print()

    if examples.get("javascript"):

        console.print("[bold cyan]JavaScript[/bold cyan]")

        console.print(
            examples["javascript"],
            markup=False
        )

    if examples.get("typescript"):

        console.print()

        console.print("[bold cyan]TypeScript[/bold cyan]")

        console.print(
            examples["typescript"],
            markup=False
        )

    if examples.get("python"):

        console.print()

        console.print("[bold cyan]Python[/bold cyan]")

        console.print(
            examples["python"],
            markup=False
        )

    if examples.get("solidity"):

        console.print()

        console.print("[bold cyan]Solidity[/bold cyan]")

        console.print(
            examples["solidity"],
            markup=False
        )

    # ==================================================
    # PROJECT INTELLIGENCE SCORE
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
        "[bold green]INTEGRATION READINESS"
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
        "[bold cyan]INTEGRATION BREAKDOWN"
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

    total_score = score.get("total", 0)

    if total_score >= 80:

        console.print(
            "[bold green]"
            "✅ Excellent Integration Candidate"
            "[/bold green]"
        )

    elif total_score >= 60:

        console.print(
            "[bold cyan]"
            "✅ Good Integration Candidate"
            "[/bold cyan]"
        )

    elif total_score >= 40:

        console.print(
            "[bold yellow]"
            "⚠ Needs Additional Review"
            "[/bold yellow]"
        )

    else:

        console.print(
            "[bold red]"
            "❌ Low Integration Readiness"
            "[/bold red]"
        )

    show_ai_summary(summary)

    # ==================================================
    # INTEGRATION RECOMMENDATION
    # ==================================================

    recommendation = generate_recommendation(
        knowledge,
        github_info
    )

    guide = generate_integration_guide(
        knowledge
    )

    console.print()

    console.rule(
        "[bold cyan]INTEGRATION RECOMMENDATION"
    )

    console.print(
        f"Overall Recommendation : {recommendation['overall']}"
    )

    console.print(
        f"Integration Difficulty : {recommendation['difficulty']}"
    )

    console.print(
        f"Estimated Time         : {recommendation['time']}"
    )

    console.print()

    console.print("[bold]Recommended Stack[/bold]")

    for item in recommendation["stack"]:
        console.print(f"• {item}")

    console.print()

    console.print("[bold]Supported Networks[/bold]")

    for network in recommendation["networks"]:
        console.print(f"• {network}")

    console.print()

    console.print("[bold]Best Use Cases[/bold]")

    for case in recommendation["use_cases"]:
        console.print(f"✓ {case}")

    console.print()

    console.print(
        f"Developer Experience : "
        f"{recommendation['developer_experience']}"
    )

    # ==================================================
    # INTEGRATION GUIDE
    # ==================================================

    console.print()

    console.rule(
        "[bold green]INTEGRATION GUIDE"
    )

    for i, step in enumerate(
        guide["steps"],
        start=1
    ):

        console.print(
            f"{i}. {step}"
        )

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
    console.rule("[bold blue]EXPORTED REPORTS")
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