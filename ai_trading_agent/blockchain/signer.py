import json
from eth_account.messages import encode_defunct
from .web3_client import Web3Client


class IntentSigner:

    @staticmethod
    def sign(intent: dict) -> str:
        """
        Подписывает intent.
        """

        client = Web3Client()
        account = client.get_account()

        message_text = json.dumps(
            intent,
            separators=(",", ":"),
            sort_keys=True,
        )

        message = encode_defunct(text=message_text)

        signed = account.sign_message(message)

        return signed.signature.hex()

    @staticmethod
    def recover(intent: dict, signature: str):
        """
        Проверка подписи.
        """

        from eth_account import Account

        message_text = json.dumps(
            intent,
            separators=(",", ":"),
            sort_keys=True,
        )

        message = encode_defunct(text=message_text)

        return Account.recover_message(message, signature=signature)
