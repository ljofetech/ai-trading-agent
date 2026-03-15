import time
import uuid
import hashlib

from typing import Dict


class IntentBuilder:

    DEFAULT_TTL = 300

    @staticmethod
    def build(plan, user_address: str, chain_id: int, token_decimals: int) -> Dict:
        """
        Создаёт стандартизированный intent.
        """

        IntentBuilder._validate_plan(plan)

        amount = int(plan.amount * 10**token_decimals)

        intent = {
            "version": 1,
            "intent_id": str(uuid.uuid4()),
            "user": user_address,
            "chain_id": chain_id,
            "asset_in": plan.asset_in,
            "asset_out": plan.asset_out,
            "amount": amount,
            "max_slippage": int(plan.max_slippage * 10_000),
            "deadline": int(time.time()) + IntentBuilder.DEFAULT_TTL,
            "nonce": IntentBuilder.generate_nonce(),
            "confidence": float(plan.confidence),
        }

        intent["intent_hash"] = IntentBuilder.hash_intent(intent)

        return intent

    @staticmethod
    def generate_nonce() -> int:
        """
        Безопасный nonce.
        """
        return uuid.uuid4().int >> 64

    @staticmethod
    def hash_intent(intent: Dict) -> str:
        """
        Детерминированный hash intent.
        """
        payload = str(sorted(intent.items())).encode()
        return hashlib.sha256(payload).hexdigest()

    @staticmethod
    def _validate_plan(plan):
        if plan.amount <= 0:
            raise ValueError("Amount must be positive")

        if not (0 < plan.max_slippage < 1):
            raise ValueError("Invalid slippage")

        if not (0 <= plan.confidence <= 1):
            raise ValueError("Invalid confidence")

        if plan.asset_in == plan.asset_out:
            raise ValueError("Assets must differ")
