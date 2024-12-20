from rest_framework.permissions import  BasePermission

class IsOwner(BasePermission):
    """
       Custom permission to check if the user is the owner of the object.
       """
    def has_object_permission(self, request, view, obj):
        # Check if the user is the owner of the conversation or message
        return obj.owner == request.user