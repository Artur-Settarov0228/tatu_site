from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import logout
from .serializers import (
    RegistratsiyaSerializer, LoginSerializer, 
    UserSerializer, TokenSerializer, LogoutSerializer
)
from .models import Foydalanuvchi

class RegistratsiyaView(generics.CreateAPIView):
    """Yangi foydalanuvchi ro'yxatdan o'tkazish"""
    permission_classes = [AllowAny]
    serializer_class = RegistratsiyaSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Token yaratish
            refresh = RefreshToken.for_user(user)
            return Response({
                'status': 'success',
                'message': 'Foydalanuvchi muvaffaqiyatli ro\'yxatdan o\'tdi',
                'data': {
                    'user': UserSerializer(user).data,
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                }
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class LoginView(generics.GenericAPIView):
    """Foydalanuvchi tizimga kirish"""
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'status': 'success',
                'message': 'Tizimga muvaffaqiyatli kirdingiz',
                'data': {
                    'user': UserSerializer(user).data,
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                }
            })
        return Response({
            'status': 'error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(generics.GenericAPIView):
    """Tizimdan chiqish - Refresh tokenni blacklist qilish"""
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return Response({
                'status': 'success',
                'message': 'Tizimdan chiqdingiz'
            })
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(generics.RetrieveUpdateAPIView):
    """Foydalanuvchi profilini ko'rish va tahrirlash"""
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user
    
    def put(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Profil yangilandi',
                'data': serializer.data
            })
        return Response({
            'status': 'error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class UserListView(generics.ListAPIView):
    """Barcha foydalanuvchilar ro'yxati (faqat admin uchun)"""
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.roli == 'ADMIN':
            return Foydalanuvchi.objects.all()
        return Foydalanuvchi.objects.none()