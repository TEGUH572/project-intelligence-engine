def generate_recommendation(knowledge, github):

    recommendation = {}

    score = 0

    if knowledge.get("sdk"):
        score += 25

    if knowledge.get("streaming"):
        score += 20

    if knowledge.get("supported_networks"):
        score += 20

    if github.get("verification_status") == "Official":
        score += 20

    if github.get("contributors", 0) >= 50:
        score += 15

    if score >= 90:
        overall = "★★★★★ Excellent"

    elif score >= 75:
        overall = "★★★★ Very Good"

    elif score >= 60:
        overall = "★★★ Good"

    else:
        overall = "★★ Fair"

    recommendation["overall"] = overall

    if score >= 90:
        recommendation["difficulty"] = "Easy"

    elif score >= 70:
        recommendation["difficulty"] = "Medium"

    else:
        recommendation["difficulty"] = "Hard"

    if score >= 90:
        recommendation["time"] = "2–4 Hours"

    elif score >= 70:
        recommendation["time"] = "1–2 Days"

    else:
        recommendation["time"] = "Several Days"

    recommendation["stack"] = [
        "Superfluid SDK",
        "Super Tokens",
        "Constant Flow Agreement (CFA)",
        "Instant Distribution Agreement (IDA)"
    ]

    recommendation["networks"] = knowledge.get(
        "supported_networks",
        []
    )

    recommendation["use_cases"] = knowledge.get(
        "use_cases",
        []
    )

    recommendation["developer_experience"] = overall

    return recommendation

# ==================================================
# INTEGRATION GUIDE
# ==================================================

def generate_integration_guide(knowledge):

    guide = {}

    guide["steps"] = [

        "Read the official documentation",

        "Install the SDK",

        "Configure RPC and wallet",

        "Deploy or connect Super Tokens",

        "Create Constant Flow Agreement (CFA)",

        "Test real-time token streaming",

        "Implement Instant Distribution Agreement (IDA)",

        "Run end-to-end integration tests",

        "Deploy to supported mainnet",

        "Monitor streaming performance"
    ]

    return guide