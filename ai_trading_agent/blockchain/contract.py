import logging

from decimal import Decimal

from django.conf import settings

from web3 import Web3
from web3.exceptions import TransactionNotFound

from .web3_client import w3, account

logger = logging.getLogger(__name__)

ABI = [
    {
        "name": "executeTrade",
        "type": "function",
        "inputs": [
            {"name": "user", "type": "address"},
            {"name": "assetIn", "type": "string"},
            {"name": "assetOut", "type": "string"},
            {"name": "amount", "type": "uint256"},
            {"name": "maxSlippage", "type": "uint256"},
            {"name": "signature", "type": "bytes"},
        ],
        "outputs": [],
    }
]

contract = w3.eth.contract(
    address=Web3.to_checksum_address(settings.CONTRACT_ADDRESS), abi=ABI
)


class TradeSendError(Exception):
    pass


def send_trade(user_address, plan, signature):
    try:
        sig = signature[2:] if signature.startswith("0x") else signature

        tx = contract.functions.executeTrade(
            user_address,
            plan["asset_in"],
            plan["asset_out"],
            int(Decimal(plan["amount"]) * Decimal("1e8")),
            int(float(plan["max_slippage"]) * 1e6),
            bytes.fromhex(sig),
        ).build_transaction(
            {
                "from": account.address,
                "nonce": w3.eth.get_transaction_count(account.address),
                "gas": 300000,
                "gasPrice": w3.eth.gas_price,
            }
        )

        signed_tx = account.sign_transaction(tx)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

        return tx_hash.hex()

    except ValueError as e:
        logger.exception("Invalid transaction params")
        raise TradeSendError(f"Invalid transaction: {str(e)}")

    except TransactionNotFound as e:
        logger.exception("Transaction not found after send")
        raise TradeSendError("Transaction broadcast failed")

    except Exception as e:
        logger.exception("Unexpected Web3 error")
        raise TradeSendError(f"Web3 error: {str(e)}")
