from rest_framework import serializers

from .models import Conversation, Message


class ConversationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Conversation
        fields = "__all__"


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
