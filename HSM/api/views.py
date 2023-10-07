from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

class RegistrationView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response( {
                'error': 'Username and password are required.'
                })

        user = User.objects.create_user(username=username, password=password)
        refresh = RefreshToken.for_user(user)

        return Response({
            'message' : 'User created successfully.',
            'refresh': str(refresh), 
            'access': str(refresh.access_token)
            })


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({
                'message' : 'Login successful.',
                'refresh': str(refresh), 
                'access': str(refresh.access_token)
                })
        else:
            return Response({
                'error': 'Invalid credentials.'
                })


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh_token')  

        if not refresh_token:
            return Response({'error': 'Refresh token is required.'})

        try:
            RefreshToken(refresh_token).blacklist()
            logout(request)
            return Response({'message': 'Logout successful.'})
        
        except Exception as e:
            return Response({'error': 'Invalid refresh token.'})
