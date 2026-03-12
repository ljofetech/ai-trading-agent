from django.urls import path

from .views import ChatView, ApproveTradeView

urlpatterns = [
    path("chat/", ChatView.as_view(), name="chat"),
    path("trade/approve/", ApproveTradeView.as_view(), name="approve-trade"),
]
