
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from chatbot import chatboot
import logging
from drf_spectacular.utils import extend_schema
from .serializers import ChatBotSerializer


@extend_schema(
    tags=["Chatbot"],
    summary="Chatbot endpoint summary",
    description="Chatbot Detailed description of what this API does.",
)
class ChatBotView(APIView):
    serializer_class = ChatBotSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user_message = serializer.validated_data.get("message")
        else:
            return Response({"error": "Message is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            bot_response = chatboot(user_message)
            return Response({"response": bot_response}, status=status.HTTP_200_OK)
        except Exception as e:
            logging.error(f"Chatbot error: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

