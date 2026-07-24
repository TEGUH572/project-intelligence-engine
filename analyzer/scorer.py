def calculate_score(
    info,
    analysis,
    github_info=None,
    knowledge=None
):
    """
    Airdrop Intelligence Scoring Engine v2

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
        "Community": 0,
        "GitHub": 0,
        "Funding": 0,
        "Testnet": 0,
        "Mainnet": 0,
        "Ecosystem": 0,
        "Social Activity": 0,
        "Transparency": 0
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
    # COMMUNITY
    # MAX 15
    # ==================================================

    community_score = 0

    if twitter:
        community_score += 5

    if discord:
        community_score += 5

    if telegram:
        community_score += 5

    breakdown["Community"] = min(
        community_score,
        15
    )

    # ==================================================
    # GITHUB
    # MAX 15
    # ==================================================

    github_score = 0

    verification_status = github_info.get(
        "verification_status"
    )

    raw_github_score = github_info.get(
        "score",
        0
    )

    if verification_status == "Official":

        github_score = min(
            raw_github_score,
            15
        )

    else:

        github_score = min(
            raw_github_score,
            5
        )

    breakdown["GitHub"] = github_score

    # ==================================================
    # FUNDING
    # MAX 15
    # ==================================================

    funding_score = 0

    funding = knowledge.get(
        "funding"
    )

    if funding:

        import re

        funding_text = str(
            funding
        ).lower()

        match = re.search(
            r"\$?\s*([\d.]+)\s*m",
            funding_text
        )

        if match:

            try:

                funding_amount = float(
                    match.group(1)
                )

                if funding_amount >= 200:

                    funding_score = 15

                elif funding_amount >= 100:

                    funding_score = 12

                elif funding_amount >= 50:

                    funding_score = 9

                elif funding_amount >= 10:

                    funding_score = 6

                elif funding_amount > 0:

                    funding_score = 3

            except ValueError:

                funding_score = 0

    breakdown["Funding"] = funding_score

    # ==================================================
    # TESTNET
    # MAX 10
    # ==================================================

    if analysis.get(
        "testnet",
        False
    ):

        breakdown["Testnet"] = 10

    # ==================================================
    # MAINNET
    # MAX 10
    # ==================================================

    if analysis.get(
        "mainnet",
        False
    ):

        breakdown["Mainnet"] = 10

    # ==================================================
    # ECOSYSTEM
    # MAX 10
    # ==================================================

    if knowledge.get(
        "ecosystem",
        False
    ):

        breakdown["Ecosystem"] = 10

    # ==================================================
    # SOCIAL ACTIVITY
    # MAX 10
    # ==================================================

    social_activity = 0

    if twitter:
        social_activity += 4

    if discord:
        social_activity += 3

    if telegram:
        social_activity += 3

    breakdown["Social Activity"] = min(
        social_activity,
        10
    )

    # ==================================================
    # TRANSPARENCY
    # MAX 10
    # ==================================================

    transparency = 0

    if docs:
        transparency += 4

    if verification_status == "Official":
        transparency += 3

    if info.get(
        "description"
    ):
        transparency += 3

    breakdown["Transparency"] = min(
        transparency,
        10
    )

    # ==================================================
    # TOTAL SCORE
    # ==================================================

    raw_total = sum(
        breakdown.values()
    )

    # Maksimum raw score:
    #
    # Community       = 15
    # GitHub          = 15
    # Funding         = 15
    # Testnet         = 10
    # Mainnet         = 10
    # Ecosystem       = 10
    # Social Activity = 10
    # Transparency    = 10
    #
    # Total = 95

    total = round(
        (raw_total / 95) * 100
    )

    total = min(
        total,
        100
    )

    # ==================================================
    # RATING
    # ==================================================

    if total >= 80:

        rating = (
            "Very High Potential"
        )

    elif total >= 60:

        rating = (
            "High Potential"
        )

    elif total >= 40:

        rating = (
            "Medium Potential"
        )

    else:

        rating = (
            "Low Potential"
        )

    # ==================================================
    # RETURN
    # ==================================================

    return {
        "total": total,
        "rating": rating,
        "breakdown": breakdown
    }