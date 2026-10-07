from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .chatbot_logic import process_question


class ChatbotView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        question = request.data.get("question")

        if not question:
            return Response(
                {
                    "error": "Please provide a question."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            result = process_question(question)

            return Response(
                result,
                status=status.HTTP_200_OK
            )

        except Exception as e:

            return Response(
                {
                    "error": "Something went wrong while processing your question.",
                    "details": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )