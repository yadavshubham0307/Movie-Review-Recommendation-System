from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny


class RegisterUserAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        # Check if username and password are provided
        if not username or not password:
            return Response(
                {'error': 'Username and password must be provided'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if the user already exists
        if User.objects.filter(username=username).exists():
            return Response(
                {'error': 'User already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create the user
        user = User.objects.create_user(username=username, password=password)
        return Response(
            {'message': 'User created successfully'},
            status=status.HTTP_201_CREATED
        )


class LoginUserAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'User logged in successfully',
            'token': {
            'refresh': str(refresh),
            'access': str(refresh.access_token)},}, 
                        status=status.HTTP_200_OK)
        
        
class LogoutUserAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # JWT authentication doesn't need server-side logout
        return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
