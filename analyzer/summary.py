def generate_summary(
    analysis,
    github,
    knowledge,
    score
):
    """
    Generate research summary
    """

    strengths = []

    if knowledge and knowledge.get("funding"):
        strengths.append(
            f"Strong funding ({knowledge['funding']})"
        )

    if github.get("verification_score", 0) >= 80:
        strengths.append(
            "Official verified GitHub"
        )

    if analysis.get("testnet"):
        strengths.append(
            "Public testnet available"
        )

    if analysis.get("mainnet"):
        strengths.append(
            "Mainnet already launched"
        )

    rating = score.get("rating", "Unknown")
    total = score.get("total", 0)

    conclusion = (
        f"This project has a {rating} rating "
        f"with a total score of {total}/100."
    )

    return {
        "strengths": strengths,
        "warnings": [],
        "conclusion": conclusion
    }