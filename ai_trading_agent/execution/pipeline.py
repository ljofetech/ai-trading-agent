import logging

from typing import Dict, Optional

from .intents import IntentBuilder
from blockchain.signer import IntentSigner
from blockchain.registry import ERC8004Registry
from risk.router import RiskRouter, RiskException

logger = logging.getLogger(__name__)


class ExecutionPipeline:

    @staticmethod
    def execute(
        plan_data,
        user_address: str,
        chain_id: int,
        token_decimals: int,
        portfolio: Optional[Dict] = None,
    ) -> str:
        """
        Полный pipeline исполнения intent.
        """

        try:

            # 1. Build intent
            intent = IntentBuilder.build(
                plan=plan_data,
                user_address=user_address,
                chain_id=chain_id,
                token_decimals=token_decimals,
            )

            # 2. Risk validation
            RiskRouter.route(intent, portfolio)

            # 3. Sign intent
            signature = IntentSigner.sign(intent)

            # 4. Submit to registry
            tx_hash = ERC8004Registry.submit(intent, signature)

            logger.info(
                "Intent submitted",
                extra={
                    "intent_id": intent["intent_id"],
                    "tx_hash": tx_hash,
                },
            )

            return tx_hash

        except RiskException as risk_error:

            logger.warning(
                "Risk policy blocked execution",
                extra={
                    "reason": str(risk_error),
                    "user": user_address,
                },
            )

            raise

        except Exception as exc:

            logger.exception(
                "Execution pipeline failed",
                extra={"user": user_address},
            )

            raise RuntimeError("Execution pipeline error") from exc
