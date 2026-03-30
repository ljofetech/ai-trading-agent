from django.conf import settings

from web3 import Web3
from eth_account import Account

w3 = Web3(Web3.HTTPProvider(settings.RPC_URL))
account = Account.from_key(settings.PRIVATE_KEY)
balance = w3.eth.get_balance(account.address)

if not w3.is_connected():
    raise Exception("RPC unavailable")

if balance < w3.to_wei(0.01, "ether"):
    raise Exception("Insufficient gas balance")
