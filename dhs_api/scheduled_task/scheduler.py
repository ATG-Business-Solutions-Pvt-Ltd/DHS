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
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR,EVENT_JOB_MISSED


import time
# import environ
# from decouple import config
from dotenv import load_dotenv
logger = logging.getLogger(__name__)
logger_1 = logging.getLogger('apscheduler')
scheduler = None  # Initialize scheduler variable
# def send_weekly_mail():
#     try:
#             today = timezone.now()
#             last_week_start = today - timedelta(days=today.weekday() + 7)
#             last_week_end = last_week_start + timedelta(days=7)
            
#             current_time = timezone.now()
#             logger.info(f"Current time: {current_time} {current_time.weekday()}")
#             # Fetch feedback from the last week
#             feedbacks = FeedbackModel.objects.filter(created_at__range=[last_week_start, last_week_end])
#             conversation_history=ConversationHistoryModel.objects.filter(created_at__range=[last_week_start, last_week_end])
#             feedback_data = [{
#                 'id': feedback.id,
#                 'user_email': feedback.user_email,
#                 'ratings': feedback.ratings,
#                 'reviews':feedback.reviews,
#                 'created_at': feedback.created_at
#             } for feedback in feedbacks]
#             conversation_data=[{ 
#                 'id': conversation.id,
#                 'user_input': conversation.user_input,
#                 'bot_response':conversation.bot_response,
#                 'created_at': conversation.created_at
#             } for conversation in conversation_history]
            
            
#             body='Please find attached feedback summary and conversation history report of bot.'
#             email = EmailMessage(
#                 subject='Weekly feedback summary and conversation history ',
#                 body=body,
#                 from_email=settings.EMAIL_HOST_USER,
#                 #['sheetal.warbhuvan@aeriestechnology.com','shreeshalini.r@aeriestechnology.com',
#                             # 'asish.barik@aeriestechnology.com','nirmal.nathani@aeriestechnology.com','neha.patil@aeriestechnology.com'],
#                 to=['sheetal.warbhuvan@aeriestechnology.com']
#                 # to=['feedback.chatbot@deliverhealth.com','sairam.thummala@deliverhealth.com']# Replace with the recipient's email
#             )
#             logger.info(f"Feedback : {feedback_data}")
#             logger.info(f"conversation history: {conversation_data}")
#             if feedback_data:
#                 df = pd.DataFrame(feedback_data)
#                 df['created_at'] = df['created_at'].apply(lambda x: x.replace(tzinfo=None))
#                 buffer = BytesIO()
#                 df.to_excel(buffer, index=False, engine='openpyxl')
#                 buffer.seek(0)
#                 email.attach('feedback_summary.xlsx', buffer.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

#             if conversation_data:
#                 df_history = pd.DataFrame(conversation_data)
#                 df_history['created_at'] = df_history['created_at'].apply(lambda x: x.replace(tzinfo=None))
#                 history_buffer = BytesIO()
#                 df_history.to_excel(history_buffer, index=False, engine='openpyxl')
#                 history_buffer.seek(0)
#                 email.attach('conversation_history.xlsx', history_buffer.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

#             if not conversation_data and not feedback_data:
#                 email.body=f"No feedback and conversation history available to send."
#             # Create email
#             # Send the email
#             email.send()
#             logger.info(('Successfully sent feedback emails with attachment'))
#     except Exception as e:  
#             logger.info(f"Failed to send an email: {str(e)} ")
            
# def send_daily_mail():
#     try:
#             current_time = timezone.now()
#             start_time = current_time - timedelta(days=1)
#             end_time = current_time
            
#             logger.info(f"Current time: {current_time} {current_time.weekday()}")
#             # Fetch feedback from the last week
#             feedbacks = FeedbackModel.objects.filter(created_at__range=(start_time, end_time))
#             conversation_history=ConversationHistoryModel.objects.filter(created_at__range=(start_time, end_time))
            
#             feedback_data = [{
#                 'id': feedback.id,
#                 'user_email': feedback.user_email,
#                 'ratings': feedback.ratings,
#                 'reviews':feedback.reviews,
#                 'created_at': feedback.created_at
#             } for feedback in feedbacks]
#             conversation_data=[{ 
#                 'id': conversation.id,
#                 'user_input': conversation.user_input,
#                 'bot_response':conversation.bot_response,
#                 'created_at': conversation.created_at
#             } for conversation in conversation_history]
#             body='Please find attached feedback summary and conversation history report of bot.'
#             email = EmailMessage(
#                 subject='Daily feedback summary and conversation history ',
#                 body=body,
#                 from_email=settings.EMAIL_HOST_USER,
#                 #['sheetal.warbhuvan@aeriestechnology.com','shreeshalini.r@aeriestechnology.com',
#                             # 'asish.barik@aeriestechnology.com','nirmal.nathani@aeriestechnology.com','neha.patil@aeriestechnology.com'],
#                 to=['sheetal.warbhuvan@aeriestechnology.com']
#                 # to=['feedback.chatbot@deliverhealth.com','sairam.thummala@deliverhealth.com']# Replace with the recipient's email
#             )
#             logger.info(f"Feedback : {feedback_data}")
#             logger.info(f"conversation history: {conversation_data}")
#             if feedback_data:
#                 df = pd.DataFrame(feedback_data)
#                 df['created_at'] = df['created_at'].apply(lambda x: x.replace(tzinfo=None))
#                 buffer = BytesIO()
#                 df.to_excel(buffer, index=False, engine='openpyxl')
#                 buffer.seek(0)
#                 email.attach('feedback_summary.xlsx', buffer.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#             if conversation_data:
#                 df_history = pd.DataFrame(conversation_data)
#                 df_history['created_at'] = df_history['created_at'].apply(lambda x: x.replace(tzinfo=None))
#                 history_buffer = BytesIO()
#                 df_history.to_excel(history_buffer, index=False, engine='openpyxl')
#                 history_buffer.seek(0)
#                 email.attach('conversation_history.xlsx', history_buffer.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#             if not conversation_data and not feedback_data:
#                 email.body=f"No feedback and conversation history available to send."
#             # Send the email
#             email.send()
#             logger.info("Email sent successfully")
#             logger.info(('Successfully sent feedback emails with attachment'))
#     except Exception as e:  
#             logger.info(f"Failed to send an email: {str(e)} ")



def send_mail(start_time, end_time, period):
    retries = 3
    for attempt in range(retries):
        try:
            feedbacks = FeedbackModel.objects.filter(created_at__range=(start_time, end_time))
            conversation_history = ConversationHistoryModel.objects.filter(created_at__range=(start_time, end_time))
            feedback_data = [{
                'id': feedback.id,
                'user_email': feedback.user_email,
                'ratings': feedback.ratings,
                'reviews': feedback.reviews,
                'created_at': feedback.created_at
            } for feedback in feedbacks]
            conversation_data = [{
                'id': conversation.id,
                'user_input': conversation.user_input,
                'bot_response': conversation.bot_response,
                'created_at': conversation.created_at
            } for conversation in conversation_history]
            logger.info(f"Send {period.capitalize()} feedback  and conversation history")
            body = 'Please find attached feedback summary and conversation history report of bot.'
            email = EmailMessage(
                subject=f'{period.capitalize()} feedback summary and conversation history',
                body=body,
                from_email=settings.EMAIL_HOST_USER,
                to=['feedback.chatbot@deliverhealth.com','sairam.thummala@deliverhealth.com']
                # to=['sheetal.warbhuvan@aeriestechnology.com']
            )
            if feedback_data:
                logger.info(f"Sending feedback ")
                df = pd.DataFrame(feedback_data)
                df['created_at'] = df['created_at'].apply(lambda x: x.replace(tzinfo=None))
                buffer = BytesIO()
                df.to_excel(buffer, index=False, engine='openpyxl')
                buffer.seek(0)
                email.attach(f'{period}_feedback_summary.xlsx', buffer.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                logger.info(f"{period.capitalize()}-Feedback ---> {feedback_data} ")
            if conversation_data:
                logger.info(f"Sending Conversation History ")
                df_history = pd.DataFrame(conversation_data)
                df_history['created_at'] = df_history['created_at'].apply(lambda x: x.replace(tzinfo=None))
                history_buffer = BytesIO()
                df_history.to_excel(history_buffer, index=False, engine='openpyxl')
                history_buffer.seek(0)
                email.attach(f'{period}_conversation_history.xlsx', history_buffer.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                logger.info(f"{period.capitalize()}-Conversation History ---> {conversation_data} ")
            if not conversation_data and not feedback_data:
                    logger.info(f"No Conversation History and Feedback received from user ")
                    email.body=f"No feedback and conversation history available to send."
            logger.info(f"Sending an email")
            email.send()
            logger.info(f"{period.capitalize()} email sent successfully")
            break
        except Exception as e:
            logger.error(f"Failed to send {period} email: {str(e)}")
            if attempt < retries - 1:
                wait_time = 2 ** attempt
                logger.info(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                logger.error("All retry attempts failed.")
                
def send_daily_mail_new():
    current_time = timezone.now()
    start_time = current_time - timedelta(days=1)
    end_time = current_time
    logger.info(f"Scheduler -> {start_time} to {end_time}")
    send_mail(start_time, end_time, "daily")
    
def send_weekly_mail_new():
    today = timezone.now()
    last_week_start = today - timedelta(days=today.weekday() + 7)
    last_week_end = last_week_start + timedelta(days=7)
    logger.info(f"Scheduler -> {last_week_start} to {last_week_end}")
    send_mail(last_week_start, last_week_end, "weekly")

def job_listener(event):
    if event.code== EVENT_JOB_EXECUTED:
        logger_1.info(f'Scheduled Job {event.job_id} executed successfully at {event.scheduled_run_time}.')
    elif event.code == EVENT_JOB_ERROR:
        logger_1.error(f'Scheduled Job {event.job_id} failed with exception: {event.exception}  at {event.scheduled_run_time}. ')
    elif event.code == EVENT_JOB_MISSED:
        logger_1.info(f'Scheduled Job {event.job_id} was missed. Scheduled at {event.scheduled_run_time}.')
   
def start():
    global scheduler
    
    if scheduler and scheduler.running: 
        logger_1.info("Scheduler is already running.")  
        print("Scheduler is already running.")
        return

    scheduler = BackgroundScheduler()
    jobstores = {
        'default': SQLAlchemyJobStore(url= f"postgresql+psycopg2://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}@{os.getenv('DATABASE_HOST')}/{os.getenv('DATABASE_NAME')}"
    )
    }
    scheduler.configure(jobstores=jobstores)
    scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR | EVENT_JOB_MISSED)
    start_time = datetime.now() + timedelta(minutes=5)  
    # scheduler.add_job(send_daily_mail_new,'cron',hour=5, minute=0, max_instances=1, misfire_grace_time=300 ,replace_existing=True,id="send_daily_email_new") 
    # scheduler.add_job(send_weekly_mail_new, 'cron',day_of_week='mon',hour=6,minute = 0,max_instances=1, misfire_grace_time=300 ,replace_existing=True,id="send_weekly_email_new") 
    scheduler.add_job(send_daily_mail_new, 'interval',minutes = 30,misfire_grace_time=300 ,replace_existing=True,id="send_daily_email_new")
    scheduler.add_job(send_weekly_mail_new, 'interval',minutes = 30,misfire_grace_time=300 ,replace_existing=True,id="send_weekly_email_new")
    register_events(scheduler)
    scheduler.start()
    print("Scheduler started!") 
    time.sleep(2)
    
    jobs = scheduler.get_jobs()
    for job in jobs:
        logger_1.info(f"Jobs Job ID: {job.id}, Trigger: {job.trigger}")