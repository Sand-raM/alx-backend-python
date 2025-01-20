from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to interact with it.
    """
    def has_permission(self, request, view):
        # Allow only authenticated users
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # Allow only participants to access the conversation
        if hasattr(obj, 'participants_id'):
            return request.user in obj.participants_id.all()
        # For messages, check if user is participant in the conversation
        if hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants_id.all()
        return False

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of a message to edit it.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the message
        return obj.sender_id == request.user 