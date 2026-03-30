from eth_account.messages import encode_typed_data
from .web3_client import account


class EIP712SigningError(Exception):
    """Error sign EIP-712"""

    pass


def sign_trade(eip712_data: dict) -> str:
    try:
        # 1. Валидация структуры
        required_fields = ["types", "domain", "primaryType", "message"]
        for field in required_fields:
            if field not in eip712_data:
                raise EIP712SigningError(f"Missing field: {field}")

        # 2. Кодирование EIP-712
        message = encode_typed_data(full_message=eip712_data)

        # 3. Подпись
        signed_message = account.sign_message(message)

        # 4. Возврат hex-подписи
        return signed_message.signature.hex()

    except ValueError as e:
        raise EIP712SigningError(f"Encoding error: {str(e)}")

    except Exception as e:
        raise EIP712SigningError(f"Unexpected signing error: {str(e)}")
