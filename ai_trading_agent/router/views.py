import os

from rest_framework.views import APIView
from rest_framework.response import Response
from dotenv import load_dotenv

from .services import ConversationService
from Kronos.examples.test import KronosForecaster

load_dotenv()


# This Python class `ChatView` defines a POST method that processes a message in a conversation using
# a `ConversationService` and returns the result.
class ChatView(APIView):
    def post(self, request):
        conversation_id = request.data.get("conversation_id")
        message = request.data.get("message")
        result = ConversationService.process_message(conversation_id, message)
        return Response(result)


# The `PredictView` class uses the `KronosForecaster` to predict future values for a given symbol with
# specified parameters.
class PredictView(APIView):
    def get(self, request):
        forecaster = KronosForecaster(
            symbol=os.getenv("symbol"),
            interval=os.getenv("interval"),
            limit=500,
            pred_len=50,
            lookback=400,
            forecast_hours=int(os.getenv("forecast_hours")),
        )
        df, pred_df = forecaster.predict()
        print("\nForecast:")
        print(df)
        print(pred_df)
        return Response(pred_df)
