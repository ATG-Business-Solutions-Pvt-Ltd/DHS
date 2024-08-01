from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django.core.mail import send_mail
from django.conf import settings
from dhs_history.models import FeedbackModel,ConversationHistoryModel
from datetime import datetime
from datetime import timedelta
import logging
from io import BytesIO
from django.utils import timezone
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.triggers.interval import IntervalTrigger
from django.core.mail import EmailMessage
import pandas as pd
import pytz
from django.conf import settings
import os
import logging.config
import time
# import environ
# from decouple import config
from dotenv import load_dotenv
logger = logging.getLogger(__name__)

def send_mail():
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
                # to=['sheetal.warbhuvan@aeriestechnology.com','shreeshalini.r@aeriestechnology.com',
                #             'asish.barik@aeriestechnology.com','nirmal.nathani@aeriestechnology.com','neha.patil@aeriestechnology.com','feedback.chatbot@deliverhealth.com']
                to=['feedback.chatbot@deliverhealth.com','sairam.thummala@deliverhealth.com']# Replace with the recipient's email
            )
            logger.info(f"Feedback : {feedback_data}")
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
            logger.info(('Successfully sent feedback emails with attachment'))
    except Exception as e:  
            logger.info(f"Failed to send an email: {str(e)} ")
            
def send__daily_mail():
    try:
            today = timezone.now()
            last_week_start = today - timedelta(days=today.weekday() + 7)
            last_week_end = last_week_start + timedelta(days=7)
            current_time = timezone.now()
            start_time = current_time - timedelta(days=1)
            end_time = current_time
            
            logger.info(f"Current time: {current_time} {current_time.weekday()}")
            # Fetch feedback from the last week
            feedbacks = FeedbackModel.objects.filter(created_at__range=(start_time, end_time))
            conversation_history=ConversationHistoryModel.objects.filter(created_at__range=(start_time, end_time))
            
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
                subject='Daily feedback summary and conversation history ',
                body=body,
                from_email=settings.EMAIL_HOST_USER,
                #['sheetal.warbhuvan@aeriestechnology.com','shreeshalini.r@aeriestechnology.com',
                            # 'asish.barik@aeriestechnology.com','nirmal.nathani@aeriestechnology.com','neha.patil@aeriestechnology.com'],
                # to=['sheetal.warbhuvan@aeriestechnology.com','shreeshalini.r@aeriestechnology.com',
                #             'asish.barik@aeriestechnology.com','nirmal.nathani@aeriestechnology.com','neha.patil@aeriestechnology.com','feedback.chatbot@deliverhealth.com']
                to=['feedback.chatbot@deliverhealth.com','sairam.thummala@deliverhealth.com']# Replace with the recipient's email
            )
            logger.info(f"Feedback : {feedback_data}")
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
            logger.info(('Successfully sent feedback emails with attachment'))
    except Exception as e:  
            logger.info(f"Failed to send an email: {str(e)} ")

def start():
    scheduler = BackgroundScheduler()
    jobstores = {
        'default': SQLAlchemyJobStore(url= f'postgresql+psycopg2://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}@{os.getenv('DATABASE_HOST')}/{os.getenv('DATABASE_NAME')}'
)
    }
    scheduler.configure(jobstores=jobstores)
    start_time = datetime.now() + timedelta(minutes=5)
    scheduler.add_job(
    send__daily_mail,
    trigger=IntervalTrigger(hours=24, start_date=start_time),  # Run every 3 hours
    id="send_interval_email",
    max_instances=1,
    replace_existing=True,
)
    
    # Schedule the weekly email job
    scheduler.add_job(
        send_mail,
        trigger=CronTrigger(day_of_week='sun', hour='10', minute='0'),  # Every Sunday at 10:00 AM
        id='weekly_email',  # Unique ID
        max_instances=1,
        replace_existing=True,
    )
    register_events(scheduler)
    scheduler.start()
    print("Scheduler started!")  
    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
         scheduler.shutdown()