from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializer import *
# Create your views here.
class FeedbackView(APIView):
    def post(self,request):
        serializer=FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetFeedback(APIView):
    def get(self,request,email):
        try:
            feedback=FeedbackModel.objects.filter(user_email=email)
            if feedback.exists():
                serializer=FeedbackSerializer(feedback,many=True)
                return Response(serializer.data)
            return Response({'error': 'No feedback found for this email'}, status=status.HTTP_404_NOT_FOUND)
        except FeedbackModel.DoesNotExist:
            return Response({'error': 'FeedbackModel not found'}, status=404)
    def delete(self,request,email):
        feedback=FeedbackModel.objects.filter(user_email=email)
        if feedback.exists():
            count, _ = feedback.delete()  # delete() returns a tuple (number of deletions, dict of deletions)
            return Response({'message': f'{count} feedback(s) deleted.'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'No feedback found for this email'}, status=status.HTTP_404_NOT_FOUND)
    
class ConversationHistory(APIView):
    def post(self,request):
        if isinstance(request.data, list):
            serializer = ChatHistorySerializer(data=request.data, many=True)
        else:
            return Response({'error': 'Expected a list of chat history '}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self,request):
        chat_history=ConversationHistoryModel.objects.all()
        serializer=ChatHistorySerializer(chat_history,many=True)
        return Response(serializer.data)
class GetConversationHistory(APIView):
    def get(self,request,email):
        try:
            chat_history=ConversationHistoryModel.objects.filter(user_email=email)
            if chat_history.exists():
                serializer=ChatHistorySerializer(chat_history,many=True)
                return Response(serializer.data)
            return Response({'error': 'No Conversation history found for this email'}, status=status.HTTP_404_NOT_FOUND)
        except ConversationHistoryModel.DoesNotExist:
            return Response({'error': 'ConversationHistoryModel not found'}, status=404)
 