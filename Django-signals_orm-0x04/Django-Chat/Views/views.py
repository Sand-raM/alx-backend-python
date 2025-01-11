from django.contrib.auth.models import User
from django.http import HttpResponse

def delete_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return HttpResponse("User deleted successfully.")
    except User.DoesNotExist:
        return HttpResponse("User not found.", status=404)
