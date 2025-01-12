from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.cache import cache_page
from .models import Message, Notification

@login_required
@cache_page(60)
def unread_messages(request):
    """
    View to display unread messages for the logged-in user.
    """
    unread_msgs = Message.unread.unread_for_user(request.user).only('content', 'timestamp', 'sender')
    return render(request, 'messaging/unread_messages.html', {'unread_msgs': unread_msgs})

@login_required
@cache_page(60)
def delete_user(request):
    """
    View to delete a user account and all related data.
    """
    user = request.user
    user.delete()
    return HttpResponseRedirect(reverse('homepage'))

@login_required
@cache_page(60)
def message_list(request):
    """
    View to display all messages sent by the logged-in user.
    """
    messages = Message.objects.filter(sender=request.user).select_related('receiver').prefetch_related('replies')
    return render(request, 'messaging/message_list.html', {'messages': messages})

@login_required
@cache_page(60)
def message_thread(request, message_id):
    """
    View to display a message and its threaded replies.
    """
    message = get_object_or_404(Message, id=message_id)
    thread = message.replies.all().select_related('sender', 'receiver')
    return render(request, 'messaging/message_thread.html', {'message': message, 'thread': thread})
