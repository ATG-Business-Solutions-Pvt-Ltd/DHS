import pandas as pd
from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage
from django.conf import settings
from dhs_history.models import FeedbackModel,ConversationHistoryModel
from io import BytesIO
import pytz
from datetime import datetime

class Command(BaseCommand):
    help = 'Send feedback emails with Excel attachment'

    def handle(self, *args, **kwargs):
        feedbacks = FeedbackModel.objects.all().values('id','user_email','ratings', 'reviews', 'created_at')
        chat_history=ConversationHistoryModel.objects.all().values('id','user_email','user_input','bot_response','created_at')
        if not feedbacks:
            self.stdout.write('No feedback available to send.')
            return

        df = pd.DataFrame(list(feedbacks))
        df['created_at'] = df['created_at'].apply(lambda x: x.replace(tzinfo=None))

        # Save the dataframe to a BytesIO buffer
        buffer = BytesIO()
        df.to_excel(buffer, index=False, engine='openpyxl')
        buffer.seek(0)
        
        df_history=pd.DataFrame(list(chat_history))
        df_history['created_at'] = df_history['created_at'].apply(lambda x: x.replace(tzinfo=None))
        # Save the dataframe to a BytesIO buffer
        history_buffer = BytesIO()
        df_history.to_excel(history_buffer, index=False, engine='openpyxl')
        history_buffer.seek(0)
        # Create email
        email = EmailMessage(
            subject='Feedback Summary with Attachment',
            body='Please find attached the feedback summary.',
            from_email=settings.EMAIL_HOST_USER,
            to=['sheetal.warbhuvan@aeriestechnology.com'],  # Replace with the recipient's email
        )

        # Attach the Excel file
        email.attach('feedback_summary.xlsx', buffer.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        email.attach('conversation_history.xlsx', history_buffer.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        # Send the email
        email.send()

        self.stdout.write(self.style.SUCCESS('Successfully sent feedback emails with attachment'))