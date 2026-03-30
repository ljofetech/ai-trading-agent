from django.conf import settings

from web3 import Web3
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .eip712 import build_eip712
from .signer import sign_trade
from .contract import send_trade


class ExecuteTradeView(APIView):

    def post(self, request):

        try:
            plan = request.data.get("plan")
            user_address = request.data.get("user_address")
            chain_id = int(request.data.get("chain_id"))

            if not Web3.is_address(user_address):
                return Response({"error": "user_address"}, status=400)

            if not plan:
                return Response({"error": "plan required"}, status=400)

            eip_data = build_eip712(plan, chain_id, settings.CONTRACT_ADDRESS)

            signature = sign_trade(eip_data)

            tx_hash = send_trade(user_address, plan, signature)

            return Response(
                {"status": "executed", "tx_hash": tx_hash, "signature": signature}
            )

        except Exception as e:
            return Response(
                {"status": "error", "message": str(e)},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        except Exception as e:
            return Response(
                {"status": "error", "message": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
