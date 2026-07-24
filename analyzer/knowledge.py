# ==================================================
# PROJECT KNOWLEDGE BASE
# ==================================================

PROJECT_KNOWLEDGE = {

    # ==================================================
    # MONAD
    # ==================================================

    "monad": {
        "name": "Monad",
        "category": "Layer 1",
        "blockchain": "EVM",
        "token": "MON",

        "website": "https://www.monad.xyz/",
        "docs": "https://docs.monad.xyz/",

        "testnet": True,
        "mainnet": True,

        "bridge": True,
        "explorer": True,

        "funding": "$225M",

        "investors": [
            "Paradigm",
            "Coinbase Ventures",
            "DragonFly",
        ],

        "ecosystem": True,

        "description": (
            "Monad is a high-performance Layer 1 blockchain "
            "compatible with the Ethereum Virtual Machine (EVM)."
        ),
    },


    # ==================================================
    # ETHEREUM
    # ==================================================

    "ethereum": {
        "name": "Ethereum",
        "category": "Layer 1",
        "blockchain": "Ethereum",
        "token": "ETH",

        "website": "https://ethereum.org/",
        "docs": "https://ethereum.org/en/developers/docs/",

        "testnet": True,
        "mainnet": True,

        "bridge": True,
        "explorer": True,

        "funding": "N/A",

        "investors": [],

        "ecosystem": True,

        "description": (
            "Ethereum is a decentralized Layer 1 blockchain "
            "for smart contracts and decentralized applications."
        ),
    },


    # ==================================================
    # BASE
    # ==================================================

    "base": {
        "name": "Base",
        "category": "Layer 2",
        "blockchain": "Ethereum",
        "token": "Not Found",

        "website": "https://base.org/",
        "docs": "https://docs.base.org/",

        "testnet": True,
        "mainnet": True,

        "bridge": True,
        "explorer": True,

        "funding": "Coinbase-backed",

        "investors": [
            "Coinbase",
        ],

        "ecosystem": True,

        "description": (
            "Base is an Ethereum Layer 2 network "
            "incubated by Coinbase."
        ),
    },


    # ==================================================
    # ARBITRUM
    # ==================================================

    "arbitrum": {
        "name": "Arbitrum",
        "category": "Layer 2",
        "blockchain": "Ethereum",
        "token": "ARB",

        "website": "https://arbitrum.io/",
        "docs": "https://docs.arbitrum.io/",

        "testnet": True,
        "mainnet": True,

        "bridge": True,
        "explorer": True,

        "funding": "N/A",

        "investors": [],

        "ecosystem": True,

        "description": (
            "Arbitrum is an Ethereum Layer 2 scaling ecosystem "
            "using optimistic rollup technology."
        ),
    },


    # ==================================================
    # OPTIMISM
    # ==================================================

    "optimism": {
        "name": "Optimism",
        "category": "Layer 2",
        "blockchain": "Ethereum",
        "token": "OP",

        "website": "https://www.optimism.io/",
        "docs": "https://docs.optimism.io/",

        "testnet": True,
        "mainnet": True,

        "bridge": True,
        "explorer": True,

        "funding": "N/A",

        "investors": [],

        "ecosystem": True,

        "description": (
            "Optimism is an Ethereum Layer 2 blockchain "
            "designed to provide scalable and low-cost transactions."
        ),
    },


    # ==================================================
    # SOLANA
    # ==================================================

    "solana": {
        "name": "Solana",
        "category": "Layer 1",
        "blockchain": "Solana",
        "token": "SOL",

        "website": "https://solana.com/",
        "docs": "https://solana.com/docs",

        "testnet": True,
        "mainnet": True,

        "bridge": True,
        "explorer": True,

        "funding": "N/A",

        "investors": [],

        "ecosystem": True,

        "description": (
            "Solana is a high-performance Layer 1 blockchain "
            "designed for fast and scalable decentralized applications."
        ),
    },
}


# ==================================================
# FIND PROJECT KNOWLEDGE
# ==================================================

def get_project_knowledge(project_name):
    """
    Mencari project berdasarkan nama.
    """

    if not project_name:
        return None

    project_name = project_name.lower().strip()

    return PROJECT_KNOWLEDGE.get(project_name)


# ==================================================
# SEARCH PROJECT IN TEXT
# ==================================================

def detect_known_project(text):
    """
    Mencari apakah teks mengandung proyek
    yang sudah ada di Knowledge Base.
    """

    if not text:
        return None

    text = text.lower()

    for project_name in PROJECT_KNOWLEDGE:

        if project_name in text:

            return PROJECT_KNOWLEDGE[project_name]

    return None