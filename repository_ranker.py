def calculate_repository_score(repo):

    officiality = repo.get(
        "officiality_score",
        0
    )

    stars = repo.get(
        "stars",
        0
    )

    contributors = repo.get(
        "contributors",
        0
    )

    commits = repo.get(
        "commits",
        0
    )

    archived = repo.get(
        "archived",
        False
    )

    # ==============================
    # OFFICIALITY
    # MAX 40
    # ==============================

    officiality_score = min(
        officiality,
        40
    )

    # ==============================
    # ACTIVITY
    # MAX 25
    # ==============================

    activity_score = 0

    if commits >= 1000:
        activity_score = 25

    elif commits >= 500:
        activity_score = 20

    elif commits >= 100:
        activity_score = 15

    elif commits >= 50:
        activity_score = 10

    elif commits >= 10:
        activity_score = 5

    # ==============================
    # DEVELOPERS
    # MAX 15
    # ==============================

    developer_score = 0

    if contributors >= 100:
        developer_score = 15

    elif contributors >= 50:
        developer_score = 12

    elif contributors >= 20:
        developer_score = 9

    elif contributors >= 10:
        developer_score = 6

    elif contributors >= 5:
        developer_score = 3

    # ==============================
    # POPULARITY
    # MAX 10
    # ==============================

    popularity_score = 0

    if stars >= 10000:
        popularity_score = 10

    elif stars >= 5000:
        popularity_score = 8

    elif stars >= 1000:
        popularity_score = 6

    elif stars >= 500:
        popularity_score = 4

    elif stars >= 100:
        popularity_score = 2

    # ==============================
    # MAINTENANCE
    # MAX 10
    # ==============================

    maintenance_score = 0

    if not archived:
        maintenance_score = 10

    # ==============================
    # TOTAL
    # ==============================

    total = (
        officiality_score
        + activity_score
        + developer_score
        + popularity_score
        + maintenance_score
    )

    return {
        "officiality": officiality_score,
        "activity": activity_score,
        "developers": developer_score,
        "popularity": popularity_score,
        "maintenance": maintenance_score,
        "total": total
    }


def rank_repositories(repositories):

    ranked = []

    for repo in repositories:

        score = calculate_repository_score(
            repo
        )

        result = repo.copy()

        result[
            "repository_score"
        ] = score

        ranked.append(
            result
        )

    # Urutkan dari skor tertinggi
    ranked.sort(
        key=lambda x: x[
            "repository_score"
        ][
            "total"
        ],
        reverse=True
    )

    # Tambahkan ranking
    for index, repo in enumerate(
        ranked,
        start=1
    ):

        repo[
            "rank"
        ] = index

    return ranked