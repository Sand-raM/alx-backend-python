from django.shortcuts import render
from .models import Message

def unread_messages_view(request):
    user = request.user  # Assuming user is logged in
    unread_messages = Message.unread_messages.unread_for_user(user)  # Use the custom manager
    
    return render(request, 'messaging/unread_messages.html', {'unread_messages': unread_messages})
