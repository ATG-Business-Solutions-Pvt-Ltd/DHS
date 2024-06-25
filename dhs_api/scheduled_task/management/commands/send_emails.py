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
import logging
logger = logging.getLogger(__name__)
class Command(BaseCommand):
    help = 'Send feedback emails with Excel attachment'

    def handle(self, *args, **kwargs):
        try:
            today = timezone.now()
            last_week_start = today - timedelta(days=today.weekday() + 7)
            last_week_end = last_week_start + timedelta(days=7)
            current_time = timezone.now()
            logger.info(f"Current time: {current_time} {current_time.weekday()}")
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
                'user_input': conversation.user_input,
                'bot_response':conversation.bot_response,
                'created_at': conversation.created_at
            } for conversation in conversation_history]
            body='Please find attached feedback summary and conversation history report of bot.'
            email = EmailMessage(
                subject='Weekly feedback summary and conversation history ',
                body=body,
                from_email=settings.EMAIL_HOST_USER,
                #['sheetal.warbhuvan@aeriestechnology.com','shreeshalini.r@aeriestechnology.com',
                            # 'asish.barik@aeriestechnology.com','nirmal.nathani@aeriestechnology.com','neha.patil@aeriestechnology.com'],
                to=['sheetal.warbhuvan@aeriestechnology.com','shreeshalini.r@aeriestechnology.com',
                            'asish.barik@aeriestechnology.com','nirmal.nathani@aeriestechnology.com','neha.patil@aeriestechnology.com','feedback.chatbot@deliverhealth.com']
                # to=['sheetal.warbhuvan@aeriestechnology.com']# Replace with the recipient's email
            )
            logger.info(f"Feedback of last week : {feedback_data}")
            logger.info(f"conversation history: {conversation_data}")
            if not feedback_data:
                email.body='No feedback available to send. \n'
            else:  
                email.body='Please find Feedback summary of the bot.\n'  
                df = pd.DataFrame(list(feedback_data))
                df['created_at'] = df['created_at'].apply(lambda x: x.replace(tzinfo=None))
                # Save the dataframe to a BytesIO buffer
                buffer = BytesIO()
                df.to_excel(buffer, index=False, engine='openpyxl')
                buffer.seek(0)
                email.attach('feedback_summary.xlsx', buffer.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            if not conversation_data:
                email.body+='No conversation history available to send. \n'
            else:
                email.body+='Please find conversation history of the bot.' 
                df_history=pd.DataFrame(list(conversation_data))
                df_history['created_at'] = df_history['created_at'].apply(lambda x: x.replace(tzinfo=None))
                # Save the dataframe to a BytesIO buffer
                history_buffer = BytesIO()
                df_history.to_excel(history_buffer, index=False, engine='openpyxl')
                history_buffer.seek(0)
                email.attach('conversation_history.xlsx', history_buffer.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            if not feedback_data and conversation_data:
                email.body=f"No feedback available to send. \n However, please find attached the conversation history. "
            elif not conversation_data and feedback_data:
                email.body=f"No conversation history available to send. \n However, please find attached the feedback summary. "
            elif conversation_data and feedback_data:
                 email.body=f" please find attached the feedback summary and conversation history. "
            else:
                email.body=f"No feedback and conversation history available to send."
            # Create email
            # Send the email
            email.send()
            logger.info("Email sent successfully")
            self.stdout.write(self.style.SUCCESS('Successfully sent feedback emails with attachment'))
        except Exception as e:  
            logger.info(f"Failed to send an email: {str(e)} ")