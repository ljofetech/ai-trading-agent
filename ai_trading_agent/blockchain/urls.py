from django.urls import path

from .views import ExecuteTradeView

urlpatterns = [
    path("exe/trade/", ExecuteTradeView.as_view(), name="execute-trade"),
]
