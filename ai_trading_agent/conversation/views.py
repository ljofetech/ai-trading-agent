from rest_framework.views import APIView
from rest_framework.response import Response

from .services import ConversationService


class ChatView(APIView):

    def post(self, request):

        conversation_id = request.data.get("conversation_id")
        message = request.data.get("message")

        result = ConversationService.process_message(conversation_id, message)

        return Response(result)
