from rest_framework import serializers
from .models import *

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model=FeedbackModel
        fields = ['id', 'user_email','ratings', 'reviews', 'created_at']
        read_only_fields = ['created_at']
        
class ChatHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model=ConversationHistoryModel
        fields = ['id','user_input', 'bot_response', 'created_at']
        read_only_fields = ['created_at']