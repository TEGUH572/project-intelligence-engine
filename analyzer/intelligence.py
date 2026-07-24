import re


def analyze_project(info):
    """
    Intelligence Engine v2

    Menganalisis proyek berdasarkan:
    - Title
    - Description
    - Website URL
    - Docs URL
    - Twitter URL
    """

    # ==================================================
    # AMBIL DATA
    # ==================================================

    title = (info.get("title") or "").lower()
    description = (info.get("description") or "").lower()

    socials = info.get("socials") or {}

    website = (info.get("website") or "").lower()
    docs = (socials.get("docs") or "").lower()
    twitter = (socials.get("twitter") or "").lower()

    # Gabungkan semua data untuk dianalisis
    text = " ".join([
        title,
        description,
        website,
        docs,
        twitter
    ])

    # ==================================================
    # HASIL DEFAULT
    # ==================================================

    result = {
        "category": "Unknown",
        "blockchain": "Unknown",
        "token": "Not Found",
        "testnet": False,
        "mainnet": False,
        "bridge": False,
        "explorer": False,
    }

    # ==================================================
    # PROJECT-SPECIFIC DETECTION
    # ==================================================

    # Monad adalah Layer 1 blockchain
    if (
        "monad" in title
        or "monad" in description
        or "monad" in website
        or "monad" in docs
        or "monad.xyz" in text
    ):
        result["category"] = "Layer 1"

    # ==================================================
    # CATEGORY DETECTION
    # ==================================================

    category_keywords = {

        "Layer 1": [
            "layer 1",
            "layer-1",
            "l1 blockchain",
            "l1 network",
            "layer one",
            "blockchain network",
            "blockchain protocol",
            "high performance blockchain",
            "high-performance blockchain",
            "smart contract platform",
            "base layer",
        ],

        "Layer 2": [
            "layer 2",
            "layer-2",
            "l2 blockchain",
            "l2 network",
            "rollup",
            "optimistic rollup",
            "zk rollup",
            "zero knowledge rollup",
        ],

        "DEX": [
            "decentralized exchange",
            "decentralised exchange",
            "dex",
            "swap",
            "automated market maker",
            "amm",
        ],

        "Wallet": [
            "crypto wallet",
            "web3 wallet",
            "blockchain wallet",
            "wallet infrastructure",
        ],

        "Bridge": [
            "cross-chain bridge",
            "cross chain bridge",
            "blockchain bridge",
            "token bridge",
            "bridge protocol",
        ],

        "Staking": [
            "staking",
            "liquid staking",
            "staking protocol",
            "restaking",
        ],

        "NFT": [
            "nft",
            "non-fungible token",
            "digital collectibles",
        ],

        "Gaming": [
            "web3 gaming",
            "blockchain gaming",
            "crypto gaming",
            "gamefi",
        ],

        "AI": [
            "artificial intelligence",
            "machine learning",
            "ai agent",
            "ai agents",
            "decentralized ai",
            "ai infrastructure",
        ],

        "DeFi": [
            "decentralized finance",
            "decentralised finance",
            "defi",
            "lending protocol",
            "borrowing protocol",
            "yield farming",
        ],
    }

    # ==================================================
    # CATEGORY PRIORITY
    # ==================================================

    # Jika belum terdeteksi sebagai kategori khusus
    if result["category"] == "Unknown":

        # Prioritas Layer 1
        for keyword in category_keywords["Layer 1"]:
            if keyword in text:
                result["category"] = "Layer 1"
                break

    # Prioritas Layer 2
    if result["category"] == "Unknown":

        for keyword in category_keywords["Layer 2"]:
            if keyword in text:
                result["category"] = "Layer 2"
                break

    # Kategori lainnya
    if result["category"] == "Unknown":

        priority_categories = [
            "DEX",
            "Wallet",
            "Bridge",
            "Staking",
            "NFT",
            "Gaming",
            "AI",
            "DeFi",
        ]

        for category in priority_categories:

            for keyword in category_keywords[category]:

                if keyword in text:
                    result["category"] = category
                    break

            if result["category"] != "Unknown":
                break

    # ==================================================
    # BLOCKCHAIN DETECTION
    # ==================================================

    blockchain_keywords = {

        "Monad": [
            "monad",
            "monad labs",
            "monad.xyz",
            "docs.monad.xyz",
        ],

        "Ethereum": [
            "ethereum",
            "ethereum blockchain",
            "eth mainnet",
        ],

        "EVM": [
            "evm",
            "evm compatible",
            "evm-compatible",
            "ethereum virtual machine",
        ],

        "Solana": [
            "solana",
            "solana blockchain",
        ],

        "Cosmos": [
            "cosmos",
            "cosmos sdk",
            "ibc",
        ],

        "Sui": [
            "sui network",
            "sui blockchain",
        ],

        "Aptos": [
            "aptos network",
            "aptos blockchain",
        ],

        "Base": [
            "base network",
            "base chain",
            "base blockchain",
        ],

        "Arbitrum": [
            "arbitrum",
            "arbitrum one",
        ],

        "Optimism": [
            "optimism",
            "op mainnet",
            "optimism network",
        ],
    }

    for blockchain, keywords in blockchain_keywords.items():

        for keyword in keywords:

            if keyword in text:
                result["blockchain"] = blockchain
                break

        if result["blockchain"] != "Unknown":
            break

    # ==================================================
    # TOKEN DETECTION
    # ==================================================

    token_patterns = [
        r"\$[A-Z]{2,10}",
        r"\b[A-Z]{2,10}\s+token\b",
        r"\bnative token\b",
        r"\btoken\b",
    ]

    for pattern in token_patterns:

        if re.search(pattern, text, re.IGNORECASE):

            result["token"] = "Mentioned"
            break

    # ==================================================
    # TESTNET DETECTION
    # ==================================================

    testnet_keywords = [
        "testnet",
        "test network",
        "devnet",
        "developer network",
    ]

    for keyword in testnet_keywords:

        if keyword in text:
            result["testnet"] = True
            break

    # ==================================================
    # MAINNET DETECTION
    # ==================================================

    mainnet_keywords = [
        "mainnet",
        "main network",
        "live on mainnet",
        "launched mainnet",
    ]

    for keyword in mainnet_keywords:

        if keyword in text:
            result["mainnet"] = True
            break

    # ==================================================
    # BRIDGE DETECTION
    # ==================================================

    bridge_keywords = [
        "bridge",
        "cross-chain",
        "cross chain",
    ]

    for keyword in bridge_keywords:

        if keyword in text:
            result["bridge"] = True
            break

    # ==================================================
    # EXPLORER DETECTION
    # ==================================================

    explorer_keywords = [
        "block explorer",
        "blockchain explorer",
        "explorer",
    ]

    for keyword in explorer_keywords:

        if keyword in text:
            result["explorer"] = True
            break

    # ==================================================
    # RETURN RESULT
    # ==================================================

    return result