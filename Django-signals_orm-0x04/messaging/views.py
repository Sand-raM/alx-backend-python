from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from .models import Message

@cache_page(60)  # Cache this view for 60 seconds
def conversation_list(request, user_id):
    user = get_object_or_404(User, id=user_id)
    messages = Message.objects.filter(receiver=user).select_related('sender', 'parent_message').prefetch_related('replies')
    return render(request, 'messaging/conversation_list.html', {'messages': messages})

def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
    return render(request, 'messaging/user_deleted.html')
