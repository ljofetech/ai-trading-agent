from eth_account.messages import encode_structured_data
from django.conf import settings
from .web3_client import Web3Client


class EIP712Signer:

    @staticmethod
    def sign(intent: dict):

        client = Web3Client()
        account = client.get_account()

        domain = {
            "name": "AITradingAgent",
            "version": "1",
            "chainId": intent["chain_id"],
            "verifyingContract": settings.REGISTRY_ADDRESS,
        }

        types = {
            "Intent": [
                {"name": "user", "type": "address"},
                {"name": "asset_in", "type": "address"},
                {"name": "asset_out", "type": "address"},
                {"name": "amount", "type": "uint256"},
                {"name": "max_slippage", "type": "uint256"},
                {"name": "deadline", "type": "uint256"},
                {"name": "nonce", "type": "uint256"},
            ]
        }

        structured_data = {
            "types": types,
            "domain": domain,
            "primaryType": "Intent",
            "message": intent,
        }

        message = encode_structured_data(structured_data)

        signed = account.sign_message(message)

        return signed.signature.hex()
