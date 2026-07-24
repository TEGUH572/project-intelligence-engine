from ddgs import DDGS


def find_official_website(project_name):
    """
    Mencari website resmi proyek menggunakan DDGS.
    """

    query = f"{project_name} official website crypto"

    blacklist = [
        "coingecko.com",
        "coinmarketcap.com",
        "cryptorank.io",
        "defillama.com",
        "rootdata.com",
        "medium.com",
        "mirror.xyz",
        "github.com",
        "linkedin.com",
        "facebook.com",
        "instagram.com",
        "youtube.com",
        "reddit.com",
        "wikipedia.org",
    ]

    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=10)

            for result in results:
                url = result.get("href")

                if not url:
                    continue

                url_lower = url.lower()

                if any(site in url_lower for site in blacklist):
                    continue

                return url

    except Exception as e:
        print(f"Search Error: {e}")

    return None