def generate_summary(
    analysis,
    github,
    knowledge,
    score
):
    """
    Generate Superfluid integration summary.
    """

    strengths = []
    warnings = []

    if github.get("verification_score", 0) >= 80:
        strengths.append("Official verified GitHub")

    if github.get("contributors", 0) >= 10:
        strengths.append("Active open-source contributors")

    if github.get("releases", 0) > 0:
        strengths.append("Regular project releases")

    if analysis.get("mainnet"):
        strengths.append("Mainnet available")

    if analysis.get("testnet"):
        strengths.append("Public testnet available")

    if github.get("verification_score", 0) < 80:
        warnings.append("GitHub repository is not officially verified")

    if github.get("contributors", 0) < 5:
        warnings.append("Limited contributor activity")

    total = score.get("total", 0)

    if total >= 80:
        conclusion = (
            "This project appears to be an excellent candidate "
            "for Superfluid integration."
        )

    elif total >= 60:
        conclusion = (
            "This project appears suitable for Superfluid "
            "integration with minor additional review."
        )

    elif total >= 40:
        conclusion = (
            "This project requires additional technical review "
            "before considering Superfluid integration."
        )

    else:
        conclusion = (
            "This project is currently not recommended "
            "for Superfluid integration."
        )

    return {
        "strengths": strengths,
        "warnings": warnings,
        "conclusion": conclusion
    }