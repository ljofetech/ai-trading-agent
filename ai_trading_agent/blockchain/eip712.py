from decimal import Decimal


def build_eip712(plan, chain_id, contract):
    return {
        "types": {
            "EIP712Domain": [
                {"name": "name", "type": "string"},
                {"name": "version", "type": "string"},
                {"name": "chainId", "type": "uint256"},
                {"name": "verifyingContract", "type": "address"},
            ],
            "Trade": [
                {"name": "asset_in", "type": "string"},
                {"name": "asset_out", "type": "string"},
                {"name": "amount", "type": "uint256"},
                {"name": "max_slippage", "type": "uint256"},
            ],
        },
        "primaryType": "Trade",
        "domain": {
            "name": "TrustlessAgent",
            "version": "1",
            "chainId": chain_id,
            "verifyingContract": contract,
        },
        "message": {
            "asset_in": plan["asset_in"],
            "asset_out": plan["asset_out"],
            "amount": int(Decimal(plan["amount"]) * Decimal("1e8")),
            "max_slippage": int(float(plan["max_slippage"]) * 1e6),
        },
    }
