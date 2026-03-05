from web3 import Web3
from django.conf import settings
from eth_account import Account


class Web3Client:

    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(settings.RPC_URL))

        if not self.w3.is_connected():
            raise Exception("Web3 connection failed")

        self.chain_id = self.w3.eth.chain_id

    def get_account(self):
        if not settings.PRIVATE_KEY:
            return None

        return Account.from_key(settings.PRIVATE_KEY)

    def get_nonce(self, address):
        return self.w3.eth.get_transaction_count(address)
