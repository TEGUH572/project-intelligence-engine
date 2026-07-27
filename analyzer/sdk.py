SDK_DATABASE = {

    "superfluid": {

        "available": True,

        "languages": [
            "TypeScript",
            "JavaScript",
            "Solidity"
        ],

        "packages": [
            "@superfluid-finance/sdk-core",
            "@superfluid-finance/sdk-redux"
        ],

        "install": (
            "npm install "
            "@superfluid-finance/sdk-core"
        ),

        "package_manager": "npm",

        "docs": (
            "https://docs.superfluid.org/sdk"
        ),

        "examples": 15

    }

}


def get_sdk(project):

    return SDK_DATABASE.get(
        project.lower(),
        {}
    )