import pandas as pd
from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage
from django.conf import settings
from dhs_history.models import FeedbackModel,ConversationHistoryModel
from io import BytesIO
from django.utils import timezone
import pytz
from datetime import datetime
from datetime import timedelta

class Command(BaseCommand):
    help = 'Send feedback emails with Excel attachment'

    def handle(self, *args, **kwargs):
        today = timezone.now()
        last_week_start = today - timedelta(days=today.weekday() + 7)
        last_week_end = last_week_start + timedelta(days=7)
        
        # Fetch feedback from the last week
        feedbacks = FeedbackModel.objects.filter(created_at__range=[last_week_start, last_week_end])
        conversation_history=ConversationHistoryModel.objects.filter(created_at__range=[last_week_start, last_week_end])
       
        feedback_data = [{
            'id': feedback.id,
            'user_email': feedback.user_email,
            'ratings': feedback.ratings,
            'reviews':feedback.reviews,
            'created_at': feedback.created_at
        } for feedback in feedbacks]
        conversation_data=[{
            'id': conversation.id,
            'user_email': conversation.user_email,
            'user_input': conversation.user_input,
            'bot_response':conversation.bot_response,
            'created_at': conversation.created_at
        } for conversation in conversation_history]
        body='Please find attached the feedbackn and summary of bot.'
        email = EmailMessage(
            subject='DHS-bot feedback and Summary ',
            body=body,
            from_email=settings.EMAIL_HOST_USER,
            #['sheetal.warbhuvan@aeriestechnology.com','shreeshalini.r@aeriestechnology.com',
                         # 'asish.barik@aeriestechnology.com','nirmal.nathani@aeriestechnology.com','neha.patil@aeriestechnology.com'],
            to=['sheetal.warbhuvan@aeriestechnology.com','shreeshalini.r@aeriestechnology.com',
                          'asish.barik@aeriestechnology.com','nirmal.nathani@aeriestechnology.com',], 
            # to=['sheetal.warbhuvan@aeriestechnology.com']# Replace with the recipient's email
        )
        if not feedback_data:
            email.body='No feedback available to send. \n'
        else:    
            df = pd.DataFrame(list(feedback_data))
            df['created_at'] = df['created_at'].apply(lambda x: x.replace(tzinfo=None))
            # Save the dataframe to a BytesIO buffer
            buffer = BytesIO()
            df.to_excel(buffer, index=False, engine='openpyxl')
            buffer.seek(0)
            email.attach('feedback_summary.xlsx', buffer.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        if not conversation_data:
            email.body='No conversation history available to send. \n'
        else:
            df_history=pd.DataFrame(list(conversation_data))
            df_history['created_at'] = df_history['created_at'].apply(lambda x: x.replace(tzinfo=None))
            # Save the dataframe to a BytesIO buffer
            history_buffer = BytesIO()
            df_history.to_excel(history_buffer, index=False, engine='openpyxl')
            history_buffer.seek(0)
            email.attach('conversation_history.xlsx', history_buffer.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        # Create email
            
           
        # Send the email
        email.send()

        self.stdout.write(self.style.SUCCESS('Successfully sent feedback emails with attachment'))