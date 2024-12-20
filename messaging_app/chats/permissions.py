from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwner(BasePermission):
    """
    Custom permission to check if the user is the owner of the object.
    """
    def has_object_permission(self, request, view, obj):
        # Check if the user is the owner of the conversation or message
        return obj.owner == request.user

class IsAuthenticatedAndParticipant(BasePermission):
    """
    Custom permission to ensure the user is authenticated and is a participant
    of the conversation.
    """
    def has_object_permission(self, request, view, obj):
        # Ensure user is authenticated
        if not request.user.is_authenticated:
            return False

        # Check if user is a participant of the conversation
        if hasattr(obj, 'participants'):  # For conversation objects
            return request.user in obj.participants.all()

        if hasattr(obj, 'conversation'):  # For message objects
            return request.user in obj.conversation.participants.all()

        return False

