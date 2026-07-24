import requests
from bs4 import BeautifulSoup


def get_website_info(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Ambil title
        title = soup.title.string.strip() if soup.title else "Tidak ada title"

        # Ambil meta description
        description = "Tidak ada deskripsi"

        meta = soup.find("meta", attrs={"name": "description"})
        if meta and meta.get("content"):
            description = meta["content"]

        # Menyimpan link penting
        socials = {
            "twitter": None,
            "discord": None,
            "github": None,
            "docs": None,
            "telegram": None
        }

        # Scan semua link
        for a in soup.find_all("a", href=True):
            href = a["href"]

            href_lower = href.lower()

            # Twitter / X
            if "x.com/" in href_lower and "/i/" not in href_lower:
                socials["twitter"] = href

            elif "twitter.com/" in href_lower:
                socials["twitter"] = href

            # Discord
            elif "discord.gg" in href_lower or "discord.com" in href_lower:
                socials["discord"] = href

            # GitHub
            elif "github.com" in href_lower:
                socials["github"] = href

            # Documentation
            elif "docs" in href_lower:
                socials["docs"] = href

            # Telegram
            elif "t.me/" in href_lower or "telegram" in href_lower:
                socials["telegram"] = href

        return {
            "title": title,
            "description": description,
            "socials": socials
        }

    except Exception as e:
        return {
            "title": "Error",
            "description": str(e),
            "socials": {}
        }