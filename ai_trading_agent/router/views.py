from rest_framework.views import APIView
from rest_framework.response import Response

from .services import ConversationService
from Kronos.examples.test import KronosForecaster


class ChatView(APIView):
    def post(self, request):
        conversation_id = request.data.get("conversation_id")
        message = request.data.get("message")
        result = ConversationService.process_message(conversation_id, message)
        return Response(result)


class PredictView(APIView):
    def get(self, request):
        forecaster = KronosForecaster()
        df, pred_df = forecaster.predict()
        print("\n📊 Forecast:")
        print(pred_df.head())
        forecaster.plot(df, pred_df)
        return Response(pred_df.head())
