from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class FeedbackModel(models.Model):
    user_email = models.CharField(max_length=100)
    ratings=models.IntegerField(null=True,default=0,validators=[MinValueValidator(0),MaxValueValidator(5)])
    reviews = models.TextField()
    created_at= models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_feedback'

    def __str__(self):
        return self.user_email
    
class ConversationHistoryModel(models.Model):
    user_email = models.CharField(max_length=100)
    user_input=models.TextField()
    bot_response=models.TextField()
    created_at= models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'conversation_history'

    def __str__(self):
        return self.user_email