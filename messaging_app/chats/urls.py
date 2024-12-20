from django.urls import path, include
from rest_framework_nested import routers  # Import the nested router
from .views import ConversationViewSet, MessageViewSet

# Main router
router = routers.DefaultRouter()  # Create a default router
router.register(r'conversations', ConversationViewSet, basename='conversation')

# Nested router for messages under conversations
nested_router = routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
nested_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)), # Include the main router
    path('', include(nested_router.urls)), # Include the nested router
]
