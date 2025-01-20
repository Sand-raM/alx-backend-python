from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

User = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom token view that returns user data along with tokens"""
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            user = User.objects.get(email=request.data['email'])
            user_data = UserSerializer(user).data
            response.data.update({
                'user': user_data,
                'status': 'success'
            })
        return response

class LogoutView(APIView):
    """Blacklist the refresh token to logout"""
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({
                    'status': 'success',
                    'message': 'Successfully logged out'
                }, status=status.HTTP_200_OK)
            return Response({
                'status': 'error',
                'message': 'Refresh token is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST) 