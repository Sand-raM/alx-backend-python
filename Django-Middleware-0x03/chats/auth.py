from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom Token View to add extra information like user details in response.
    """

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token_data = response.data

        # Include user-specific details
        user = self.request.user
        token_data.update({
            'user_id': user.id,
            'email': user.email,
        })
        return Response(token_data, status=status.HTTP_200_OK)
