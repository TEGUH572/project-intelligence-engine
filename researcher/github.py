import requests
import re
from urllib.parse import quote, urlparse, urljoin

from config import REQUEST_TIMEOUT, USER_AGENT, GITHUB_API, GITHUB_TOKEN

class GitHubResearch:

    def __init__(
        self,
        project_name,
        website_url=None
    ):
        self.project_name = project_name
        self.website_url = website_url

        self.headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": USER_AGENT
        }

        if GITHUB_TOKEN:
            self.headers["Authorization"] = (
                f"Bearer {GITHUB_TOKEN}"
            )

    # ==================================================
    # GENERIC REQUEST
    # ==================================================

    def request_url(
        self,
        url
    ):

        try:

            response = requests.get(
                url,
                timeout=REQUEST_TIMEOUT,
                headers={
                    "User-Agent": USER_AGENT
                }
            )

            if response.status_code == 200:

                return response.text

        except Exception:

            pass

        return ""

    # ==================================================
    # GITHUB API REQUEST
    # ==================================================

    def github_get(
        self,
        url,
        params=None
    ):

        try:

            response = requests.get(
                url,
                params=params,
                timeout=REQUEST_TIMEOUT,
                headers=self.headers
            )

            if response.status_code == 200:

                return response.json()

        except Exception as e:

            print(e)

        return None

    # ==================================================
    # GET WEBSITE HTML
    # ==================================================

    def get_website_html(
        self
    ):

        if not self.website_url:

            return ""

        return self.request_url(
            self.website_url
        ).lower()

    # ==================================================
    # EXTRACT GITHUB URLS
    # ==================================================

    def extract_github_urls(
        self,
        html
    ):

        if not html:

            return []

        pattern = (
            r'https?://(?:www\.)?'
            r'github\.com/'
            r'[A-Za-z0-9_.-]+'
            r'(?:/[A-Za-z0-9_.-]+)?'
        )

        urls = re.findall(
            pattern,
            html,
            flags=re.IGNORECASE
        )

        clean_urls = []

        for url in urls:

            url = url.rstrip(
                '"/\'<>.,);'
            )

            if url not in clean_urls:

                clean_urls.append(
                    url
                )

        return clean_urls

    # ==================================================
    # NORMALIZE GITHUB URL
    # ==================================================

    def normalize_github_url(
        self,
        url
    ):

        if not url:

            return None

        try:

            parsed = urlparse(
                url
            )

            parts = [
                part
                for part in parsed.path.split("/")
                if part
            ]

            if not parts:

                return None

            # Hanya ambil:
            # github.com/organization
            # github.com/organization/repository

            if len(parts) >= 2:

                return (
                    f"https://github.com/"
                    f"{parts[0]}/"
                    f"{parts[1]}"
                )

            return (
                f"https://github.com/"
                f"{parts[0]}"
            )

        except Exception:

            return None

    # ==================================================
    # DISCOVER GITHUB FROM OFFICIAL WEBSITE
    # ==================================================

    def discover_from_website(
        self
    ):

        html = self.get_website_html()

        if not html:

            return []

        urls = self.extract_github_urls(
            html
        )

        results = []

        for url in urls:

            normalized = (
                self.normalize_github_url(
                    url
                )
            )

            if normalized:

                results.append(
                    normalized
                )

        return list(
            dict.fromkeys(
                results
            )
        )

    # ==================================================
    # DISCOVER GITHUB FROM DOCS
    # ==================================================

    def discover_from_docs(
        self,
        docs_url
    ):

        if not docs_url:

            return []

        html = self.request_url(
            docs_url
        ).lower()

        if not html:

            return []

        urls = self.extract_github_urls(
            html
        )

        results = []

        for url in urls:

            normalized = (
                self.normalize_github_url(
                    url
                )
            )

            if normalized:

                results.append(
                    normalized
                )

        return list(
            dict.fromkeys(
                results
            )
        )

    # ==================================================
    # SEARCH GITHUB BY PROJECT NAME
    # ==================================================

    def search_organization(
        self
    ):

        url = (
            f"{GITHUB_API}/"
            f"search/users?q="
            f"{quote(self.project_name)}"
        )

        data = self.github_get(
            url
        )

        if not data:

            return None

        items = data.get(
            "items",
            []
        )

        if not items:

            return None

        project = (
            self.project_name
            .lower()
            .replace(
                " ",
                ""
            )
        )

        # Exact organization

        for item in items:

            login = item.get(
                "login",
                ""
            )

            if (
                item.get("type")
                == "Organization"
                and login.lower()
                == project
            ):

                return login

        # Organization contains name

        for item in items:

            login = item.get(
                "login",
                ""
            )

            if (
                item.get("type")
                == "Organization"
                and project
                in login.lower()
            ):

                return login

        # Exact user

        for item in items:

            login = item.get(
                "login",
                ""
            )

            if (
                item.get("type")
                == "User"
                and login.lower()
                == project
            ):

                return login

        return None

    # ==================================================
    # GET REPOSITORIES
    # ==================================================

    def get_repositories(
        self,
        organization
    ):

        url = (
            f"{GITHUB_API}/"
            f"orgs/{organization}/repos"
        )

        repos = self.github_get(
            url,
            params={
                "per_page": 100,
                "sort": "updated"
            }
        )

        if isinstance(
            repos,
            list
        ):

            return repos

        url = (
            f"{GITHUB_API}/"
            f"users/{organization}/repos"
        )

        repos = self.github_get(
            url,
            params={
                "per_page": 100,
                "sort": "updated"
            }
        )

        if isinstance(
            repos,
            list
        ):

            return repos

        return []

    # ==================================================
    # GET CONTRIBUTORS
    # ==================================================

    def get_contributors(
        self,
        organization,
        repos
    ):

        total_contributors = set()

        for repo in repos[:10]:

            repo_name = repo.get(
                "name"
            )

            if not repo_name:

                continue

            url = (
                f"{GITHUB_API}/"
                f"repos/{organization}/"
                f"{repo_name}/contributors"
            )

            contributors = self.github_get(
                url,
                params={
                    "per_page": 100
                }
            )

            if not isinstance(
                contributors,
                list
            ):

                continue

            for contributor in contributors:

                login = contributor.get(
                    "login"
                )

                if login:

                    total_contributors.add(
                        login
                    )

        return len(
            total_contributors
        )

    # ==================================================
    # GET PULL REQUESTS
    # ==================================================

    def get_pull_requests(
        self,
        organization,
        repos
    ):

        total = 0

        for repo in repos[:10]:

            repo_name = repo.get(
                "name"
            )

            if not repo_name:

                continue

            url = (
                f"{GITHUB_API}/"
                f"repos/{organization}/"
                f"{repo_name}/pulls"
            )

            data = self.github_get(
                url,
                params={
                    "state": "all",
                    "per_page": 1
                }
            )

            if isinstance(
                data,
                list
            ):

                total += len(
                    data
                )

        return total

    # ==================================================
    # GET RELEASES
    # ==================================================

    def get_releases(
        self,
        organization,
        repos
    ):

        total = 0

        for repo in repos[:10]:

            repo_name = repo.get(
                "name"
            )

            if not repo_name:

                continue

            url = (
                f"{GITHUB_API}/"
                f"repos/{organization}/"
                f"{repo_name}/releases"
            )

            releases = self.github_get(
                url,
                params={
                    "per_page": 100
                }
            )

            if isinstance(
                releases,
                list
            ):

                total += len(
                    releases
                )

        return total

    # ==================================================
    # CALCULATE SCORE
    # ==================================================

    def calculate_score(
        self,
        repositories,
        stars,
        forks,
        contributors,
        releases,
        pull_requests
    ):

        score = 0

        # Repositories

        if repositories >= 10:

            score += 5

        elif repositories >= 5:

            score += 4

        elif repositories >= 2:

            score += 3

        elif repositories >= 1:

            score += 2

        # Stars

        if stars >= 10000:

            score += 5

        elif stars >= 5000:

            score += 4

        elif stars >= 1000:

            score += 3

        elif stars >= 100:

            score += 2

        elif stars > 0:

            score += 1

        # Forks

        if forks >= 1000:

            score += 3

        elif forks >= 100:

            score += 2

        elif forks > 0:

            score += 1

        # Contributors

        if contributors >= 100:

            score += 5

        elif contributors >= 50:

            score += 4

        elif contributors >= 20:

            score += 3

        elif contributors >= 5:

            score += 2

        elif contributors > 0:

            score += 1

        # Releases

        if releases >= 10:

            score += 2

        elif releases > 0:

            score += 1

        # Pull Requests

        if pull_requests >= 50:

            score += 5

        elif pull_requests >= 20:

            score += 4

        elif pull_requests >= 10:

            score += 3

        elif pull_requests >= 5:

            score += 2

        elif pull_requests > 0:

            score += 1

        return min(
            score,
            25
        )

    # ==================================================
    # ANALYZE
    # ==================================================

    def analyze(
        self,
        docs_url=None
    ):

        # ==================================================
        # STEP 1
        # DISCOVER FROM WEBSITE
        # ==================================================

        website_candidates = (
            self.discover_from_website()
        )

        # ==================================================
        # STEP 2
        # DISCOVER FROM DOCS
        # ==================================================

        docs_candidates = (
            self.discover_from_docs(
                docs_url
            )
        )

        # ==================================================
        # COMBINE CANDIDATES
        # ==================================================

        candidates = []

        for url in website_candidates:

            candidates.append({
                "url": url,
                "source": "Official Website"
            })

        for url in docs_candidates:

            if url not in [
                item["url"]
                for item in candidates
            ]:

                candidates.append({
                    "url": url,
                    "source": "Official Docs"
                })

        # ==================================================
        # IF NO OFFICIAL SOURCE
        # SEARCH BY NAME
        # ==================================================

        if not candidates:

            organization = (
                self.search_organization()
            )

            if organization:

                candidates.append({
                    "url":
                        f"https://github.com/"
                        f"{organization}",

                    "source":
                        "GitHub Name Search"
                })

        # ==================================================
        # DEFAULT RESULT
        # ==================================================

        result = {

            "github_url":
                None,

            "organization":
                None,

            "discovery_source":
                "Not Found",

            "verified":
                False,

            "verification_status":
                "Unverified",

            "verification_score":
                0,

            "repositories":
                0,

            "stars":
                0,

            "forks":
                0,

            "contributors":
                0,

            "watchers":
                0,

            "issues":
                0,

            "pull_requests":
                0,

            "releases":
                0,

            "last_commit":
                "",

            "languages":
                [],

            "license":
                "Unknown",

            "created_at":
                "",

            "updated_at":
                "",

            "score":
                0
        }

        # ==================================================
        # SELECT BEST CANDIDATE
        # ==================================================

        if candidates:

            candidate = candidates[0]

            github_url = (
                candidate["url"]
            )

            discovery_source = (
                candidate["source"]
            )

            parsed = urlparse(
                github_url
            )

            parts = [
                part
                for part
                in parsed.path.split("/")
                if part
            ]

            if parts:

                organization = (
                    parts[0]
                )

                repos = (
                    self.get_repositories(
                        organization
                    )
                )

                print("Organization:", organization)
                print("Repos found:", len(repos))

                if repos:

                    result[
                        "github_url"
                    ] = github_url

                    result[
                        "organization"
                    ] = organization

                    result[
                        "discovery_source"
                    ] = discovery_source

                    # Official website/docs
                    # are stronger evidence

                    if discovery_source in [
                        "Official Website",
                        "Official Docs"
                    ]:

                        result[
                            "verified"
                        ] = True

                        result[
                            "verification_status"
                        ] = "Official"

                        result[
                            "verification_score"
                        ] = 100

                    else:

                        result[
                            "verification_status"
                        ] = "Unverified"

                        result[
                            "verification_score"
                        ] = 10

                    # ==================================================
                    # REPOSITORY METRICS
                    # ==================================================

                    result[
                        "repositories"
                    ] = len(
                        repos
                    )

                    total_stars = 0

                    total_forks = 0

                    total_watchers = 0

                    total_issues = 0

                    languages = set()

                    latest_repo = None

                    latest_update = ""

                    for repo in repos:

                        total_stars += repo.get(
                            "stargazers_count",
                            0
                        )

                        total_forks += repo.get(
                            "forks_count",
                            0
                        )

                        total_watchers += repo.get(
                            "watchers_count",
                            0
                        )

                        total_issues += repo.get(
                            "open_issues_count",
                            0
                        )

                        language = repo.get(
                            "language"
                        )

                        if language:

                            languages.add(
                                language
                            )

                        updated = repo.get(
                            "updated_at",
                            ""
                        )

                        if (
                            updated
                            and updated
                            > latest_update
                        ):

                            latest_update = (
                                updated
                            )

                            latest_repo = (
                                repo
                            )

                    result[
                        "stars"
                    ] = total_stars

                    result[
                        "forks"
                    ] = total_forks

                    result[
                        "watchers"
                    ] = total_watchers

                    result[
                        "issues"
                    ] = total_issues

                    result[
                        "languages"
                    ] = sorted(
                        languages
                    )

                    if latest_repo:

                        result[
                            "created_at"
                        ] = latest_repo.get(
                            "created_at",
                            ""
                        )

                        result[
                            "updated_at"
                        ] = latest_repo.get(
                            "updated_at",
                            ""
                        )

                        result[
                            "last_commit"
                        ] = latest_repo.get(
                            "pushed_at",
                            ""
                        )

                        result[
                            "license"
                        ] = (
                            latest_repo.get(
                                "license"
                            ) or {}
                        ).get(
                            "name",
                            "Unknown"
                        )

                    # ==================================================
                    # OTHER METRICS
                    # ==================================================

                    result[
                        "contributors"
                    ] = (
                        self.get_contributors(
                            organization,
                            repos
                        )
                    )

                    result[
                        "releases"
                    ] = (
                        self.get_releases(
                            organization,
                            repos
                        )
                    )

                    result[
                        "pull_requests"
                    ] = (
                        self.get_pull_requests(
                            organization,
                            repos
                        )
                    )

                    result[
                        "score"
                    ] = (
                        self.calculate_score(
                            result[
                                "repositories"
                            ],

                            result[
                                "stars"
                            ],

                            result[
                                "forks"
                            ],

                            result[
                                "contributors"
                            ],

                            result[
                                "releases"
                            ],

                            result[
                                "pull_requests"
                            ]
                        )
                    )

        return result