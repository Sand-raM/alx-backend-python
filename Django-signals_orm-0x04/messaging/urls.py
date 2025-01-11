from django.urls import path
from . import views

urlpatterns = [
    path('message/<int:message_id>/history/', views.message_edit_history, name='message_edit_history'),
    path('delete_account/', views.delete_user, name='delete_user'),
    path('conversation/', views.conversation_view, name='conversation_view'),
    path('inbox/', views.inbox_view, name='inbox_view'),
    path('conversation/<int:conversation_id>/', views.conversation_view, name='conversation_view'),
]
