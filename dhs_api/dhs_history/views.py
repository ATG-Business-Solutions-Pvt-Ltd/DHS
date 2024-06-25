from io import BytesIO
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializer import *
import pandas as pd
from django.core.mail import EmailMessage
from django.conf import settings
import json
import logging
# Create your views here.
logger = logging.getLogger(__name__)
class FeedbackView(APIView):
    def post(self,request):
        serializer=FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.info(f'Failed to save feedback {serializer.errors}')
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
        try:
            if isinstance(request.data, list):
                serializer = ChatHistorySerializer(data=request.data, many=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                logger.info(f'Failed to save conversation history{serializer.errors}')
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("Please provide valid input",status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
    def get(self,request):
        chat_history=ConversationHistoryModel.objects.all()
        serializer=ChatHistorySerializer(chat_history,many=True)
        return Response(serializer.data)
    
class GetConversationHistoryV2(APIView):
    def get(self,request):
        chat_history=ConversationHistoryModel.objects.all()
        serializer_1=ChatHistorySerializer(chat_history,many=True)
        feedback=FeedbackModel.objects.all()
        serializer=FeedbackSerializer(feedback,many=True)
        send_email(serializer_1.data,serializer.data)
        return Response(data={'message':'Email sent successfully'})
    
    
def send_email(feedback_data,history_data):
    df_feedback = pd.json_normalize(feedback_data)
    df_history=pd.json_normalize(history_data)
    print(df_feedback)
    print(df_history)
    
    buffer_feedback = BytesIO()
    df_feedback.to_excel(buffer_feedback, index=False)
    buffer_feedback.seek(0)
    
    buffer_history= BytesIO()
    df_history.to_excel(buffer_history, index=False)
    buffer_history.seek(0)
     # Create email
    email = EmailMessage(
        subject='Feedback Report',
        body='Please find attached the feedback report .',
        from_email=settings.EMAIL_HOST_USER,
        to=['sheetal.warbhuvan@aeriestechnology.com','shreeshalini.r@aeriestechnology.com',
                          'asish.barik@aeriestechnology.com','nirmal.nathani@aeriestechnology.com','neha.patil@aeriestechnology.com']
        #  to=['sheetal.warbhuvan@aeriestechnology.com']
    )
    
    email.attach('feedback_report.xlsx', buffer_feedback.read(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    email.attach('conversation_history_report.xlsx', buffer_history.read(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    email.send()
    
def modify_data(data):
    reslst=[]
    history={
        "user_email":"",
        "user_input":"",
        "bot_response":"",
        "created_at":""
    }
    for conversation in data.get('conversation_history'):
        history=conversation
        history["user_email"]=data.get('user_email')
        reslst.append(history)
        
    return reslst
    