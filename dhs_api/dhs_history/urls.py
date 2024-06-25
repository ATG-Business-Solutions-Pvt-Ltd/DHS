from django.urls import path
from .views import *
urlpatterns = [
     path('feedback',FeedbackView.as_view()),
      path('feedback/<str:email>',GetFeedback.as_view()),
        path('conversation-history',ConversationHistory.as_view()),
         
           path('feedback_history',GetConversationHistoryV2.as_view()),
]