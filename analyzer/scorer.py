def calculate_score(
    info,
    analysis,
    github_info=None,
    knowledge=None
):
    """
    Project Intelligence Scoring Engine v3

    info:
        Data website dan social links

    analysis:
        Hasil Intelligence Engine

    github_info:
        Data GitHub Intelligence

    knowledge:
        Data Knowledge Base
    """

    # ==================================================
    # DEFAULT DATA
    # ==================================================

    if github_info is None:
        github_info = {}

    if knowledge is None:
        knowledge = {}

    if info is None:
        info = {}

    if analysis is None:
        analysis = {}

    # ==================================================
    # SCORE BREAKDOWN
    # ==================================================

    breakdown = {
        "Documentation": 0,
        "SDK": 0,
        "GitHub Health": 0,
        "Networks": 0,
        "Streaming": 0,
        "Developer Activity": 0,
        "Maintenance": 0,
        "Integration Examples": 0
    }

    # ==================================================
    # SOCIAL LINKS
    # ==================================================

    socials = info.get(
        "socials",
        {}
    )

    twitter = socials.get(
        "twitter"
    )

    discord = socials.get(
        "discord"
    )

    telegram = socials.get(
        "telegram"
    )

    docs = socials.get(
        "docs"
    )

   # ==================================================
    # DOCUMENTATION
    # ==================================================

    if docs:
        breakdown["Documentation"] = 20

    # ==================================================
    # SDK
    # ==================================================

    if knowledge.get("sdk"):
        breakdown["SDK"] = 15

    # ==================================================
    # GITHUB HEALTH
    # ==================================================

    github_score = github_info.get("score", 0)

    breakdown["GitHub Health"] = min(github_score, 20)

    # ==================================================
    # NETWORKS
    # ==================================================

    networks = knowledge.get(
        "supported_networks",
        []
    )

    breakdown["Networks"] = min(
        len(networks) * 3,
        15
    )

    # ==================================================
    # STREAMING
    # ==================================================

    if knowledge.get("streaming"):
        breakdown["Streaming"] = 10

    # ==================================================
    # DEVELOPER ACTIVITY
    # ==================================================

    contributors = github_info.get(
        "contributors",
        0
    )

    if contributors >= 50:

        breakdown["Developer Activity"] = 10

    elif contributors >= 20:

        breakdown["Developer Activity"] = 7

    elif contributors >= 5:

        breakdown["Developer Activity"] = 4

    # ==================================================
    # MAINTENANCE
    # ==================================================

    if github_info.get(
        "verification_status"
    ) == "Official":

        breakdown["Maintenance"] = 5

    # ==================================================
    # INTEGRATION EXAMPLES
    # ==================================================

    use_cases = knowledge.get(
        "use_cases",
        []
    )

    if len(use_cases) >= 5:

        breakdown["Integration Examples"] = 5

    elif len(use_cases) >= 3:

        breakdown["Integration Examples"] = 3

    # ==================================================
    # TOTAL SCORE
    # ==================================================

    raw_total = sum(
        breakdown.values()
    )

    total = min(
        raw_total,
        100
    )

    # ==================================================
    # RATING
    # ==================================================

    if total >= 80:

        rating = "Excellent Integration Candidate"

    elif total >= 60:

        rating = "Good Integration Candidate"

    elif total >= 40:

        rating = "Needs Additional Review"

    else:

        rating = "Low Integration Readiness"

    return {
        "total": total,
        "rating": rating,
        "breakdown": breakdown
    }