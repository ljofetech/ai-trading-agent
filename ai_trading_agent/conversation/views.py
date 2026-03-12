from rest_framework.views import APIView
from rest_framework.response import Response

from .services import ConversationService


class ChatView(APIView):

    def post(self, request):

        conversation_id = request.data.get("conversation_id")
        message = request.data.get("message")

        result = ConversationService.process_message(conversation_id, message)

        return Response(result)


class ApproveTradeView(APIView):

    def post(self, request):

        plan = request.data.get("plan")
        user_address = request.data.get("user_address")
        chain_id = request.data.get("chain_id")

        result = ConversationService.approve_trade(plan, user_address, chain_id)

        return Response(result)
