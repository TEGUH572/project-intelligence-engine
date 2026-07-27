def generate_code_examples(knowledge, sdk):

    examples = {}

    if not sdk:
        return examples

    packages = sdk.get(
        "packages",
        []
    )

    package = (
        packages[0]
        if packages
        else ""
    )

    # ==================================================
    # JAVASCRIPT
    # ==================================================

    examples["javascript"] = f"""
import {{ Framework }} from "{package}";

const sf = await Framework.create({{
    chainId: 1,
    provider
}});
""".strip()

    # ==================================================
    # TYPESCRIPT
    # ==================================================

    examples["typescript"] = f"""
import {{ Framework }} from "{package}";

const sf = await Framework.create({{
    chainId: 1,
    provider
}});
""".strip()

    # ==================================================
    # PYTHON
    # ==================================================

    examples["python"] = """
from web3 import Web3

w3 = Web3(
    Web3.HTTPProvider(RPC_URL)
)
""".strip()

    # ==================================================
    # SOLIDITY
    # ==================================================

    examples["solidity"] = """
// SPDX-License-Identifier: MIT

pragma solidity ^0.8.20;

interface ISuperToken {

    function transfer(
        address to,
        uint256 amount
    ) external returns (bool);

}
""".strip()

    return examples