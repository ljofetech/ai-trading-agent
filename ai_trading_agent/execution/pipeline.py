from blockchain.signer import EIP712Signer
from blockchain.registry import ERC8004Registry
from risk.router import RiskRouter
from .intents import IntentBuilder


class ExecutionPipeline:

    @staticmethod
    def execute(plan_data, user_address, chain_id):

        intent = IntentBuilder.build(plan_data, user_address, chain_id)

        signature = EIP712Signer.sign(intent)

        tx_hash = ERC8004Registry.submit(intent, signature)

        RiskRouter.route(intent)

        return tx_hash
