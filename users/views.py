from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework.decorators import action
from django.shortcuts import render

class UserViews(APIView):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def list_users(self, request):
        users = User.objects.all()
        user_data = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]
        return Response({'users': user_data})

    @action(detail=True, methods=['get'])
    def get_user(self, request, pk=None):
        try:
            user = User.objects.get(id=pk)
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
            return Response({'user': user_data})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)
    

class LoginView(APIView):
    permission_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=400)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=401)

class RegisterView(APIView):
    permission_classes = []

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not username or not email or not password:
            return Response({'error': 'Username, email, and password are required'}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=400)

        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists'}, status=400)

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return Response({'message': 'User registered successfully'}, status=201)
    
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'date_joined': user.date_joined,
            'profile_picture': user.profile_picture.url if getattr(user, 'profile_picture', None) else None,
            'bio': getattr(user, 'bio', ''),
            'location': getattr(user, 'location', ''),
            'date_of_birth': getattr(user, 'date_of_birth', None),
            'phone_number': getattr(user, 'phone_number', ''),
        }

        return Response(user_data, status=200)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({'message': 'Logged out successfully'}, status=205)
            else:
                return Response({'error': 'Refresh token is required'}, status=400)
        except Exception as e:
            return Response({'error': str(e)}, status=400)