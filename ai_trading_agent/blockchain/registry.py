from django.conf import settings
from .web3_client import Web3Client


class ERC8004Registry:

    @staticmethod
    def submit(intent: dict, signature: str):

        client = Web3Client()
        account = client.get_account()

        contract = client.w3.eth.contract(
            address=settings.REGISTRY_ADDRESS,
            abi=settings.REGISTRY_ABI,
        )

        nonce = client.get_nonce(account.address)

        tx = contract.functions.submitIntent(intent, signature).build_transaction(
            {
                "from": account.address,
                "nonce": nonce,
                "chainId": client.chain_id,
                "gasPrice": client.w3.eth.gas_price,
            }
        )

        tx["gas"] = client.w3.eth.estimate_gas(tx)

        signed_tx = account.sign_transaction(tx)

        tx_hash = client.w3.eth.send_raw_transaction(signed_tx.rawTransaction)

        return client.w3.to_hex(tx_hash)
