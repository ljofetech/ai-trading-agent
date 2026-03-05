import time
import uuid


class IntentBuilder:

    @staticmethod
    def build(plan, user_address: str, chain_id: int) -> dict:
        """
        Формирует стандартизированный intent.
        """

        return {
            "intent_id": str(uuid.uuid4()),
            "user": user_address,
            "chain_id": chain_id,
            "asset_in": plan.asset_in,
            "asset_out": plan.asset_out,
            "amount": int(plan.amount * 10**6),  # пример для USDC (6 decimals)
            "max_slippage": int(plan.max_slippage * 10_000),
            "deadline": int(time.time()) + 300,
            "nonce": IntentBuilder.generate_nonce(),
            "confidence": plan.confidence,
        }

    @staticmethod
    def generate_nonce():
        return int(time.time() * 1000)
