from django.urls import path

from .views import ChatView, PredictView

urlpatterns = [
    path("chat/", ChatView.as_view(), name="chat"),
    path("predict/", PredictView.as_view(), name="predict"),
]
