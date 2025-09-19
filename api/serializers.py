from rest_framework  import serializers


class ChatBotSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=4000)