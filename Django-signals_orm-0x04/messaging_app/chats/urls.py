from django.urls import path
from . import views

urlpatterns = [
    path('unread/', views.unread_messages_view, name='unread_messages'),  # Add this path
]
