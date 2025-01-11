from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Message
from django.views.decorators.cache import cache_page

@login_required
def inbox_view(request):
    # Use the custom manager to get unread messages for the logged-in user
    unread_messages = Message.unread_messages.unread_for_user(request.user)
    
    return render(request, 'messaging/inbox.html', {'unread_messages': unread_messages})


@cache_page(60)  # Cache timeout set to 60 seconds
def conversation_view(request, conversation_id):
    messages = Message.objects.filter(conversation_id=conversation_id).order_by('timestamp')
    return render(request, 'messaging/conversation.html', {'messages': messages})