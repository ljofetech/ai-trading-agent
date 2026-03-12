from eth_account.messages import encode_defunct
from .web3_client import Web3Client
import json


class EIP712Signer:

    @staticmethod
    def sign(intent: dict):

        client = Web3Client()
        account = client.get_account()

        # Преобразуем intent в JSON-строку
        message_text = json.dumps(intent, separators=(",", ":"), sort_keys=True)

        # Кодируем сообщение для подписи
        message = encode_defunct(text=message_text)

        # Подписываем сообщение
        signed = account.sign_message(message)

        return signed.signature.hex()
