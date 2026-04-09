from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Foydalanuvchi, Oqituvchi, OtaOna

class RegistratsiyaSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = Foydalanuvchi
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name', 'telefon', 'roli')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'telefon': {'required': True},
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Parollar mos kelmadi"})
        
        # Telefon raqamni tekshirish
        telefon = attrs.get('telefon')
        if telefon and Foydalanuvchi.objects.filter(telefon=telefon).exists():
            raise serializers.ValidationError({"telefon": "Bu telefon raqam allaqachon ro'yxatdan o'tgan"})
        
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        
        user = Foydalanuvchi.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        
        # Agar o'qituvchi bo'lsa, Oqituvchi profilini yaratish
        if user.roli == 'OQITUVCHI':
            Oqituvchi.objects.create(
                foydalanuvchi=user,
                xodim_id=f"TCH{user.id:05d}",
                mutaxassislik="Umumiy"
            )
        
        # Agar ota-ona bo'lsa, OtaOna profilini yaratish
        elif user.roli == 'OTA_ONA':
            OtaOna.objects.create(
                foydalanuvchi=user,
                xabar_ushlubi='TELEGRAM'
            )
        
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        # Username yoki telefon orqali autentifikatsiya
        user = None
        if '@' in username:
            user = Foydalanuvchi.objects.filter(email=username).first()
        elif username.isdigit():
            user = Foydalanuvchi.objects.filter(telefon=username).first()
        else:
            user = Foydalanuvchi.objects.filter(username=username).first()
        
        if user and user.check_password(password):
            attrs['user'] = user
            return attrs
        
        raise serializers.ValidationError({"error": "Username yoki parol noto'g'ri"})

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Foydalanuvchi
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'telefon', 'roli', 'is_active')

class TokenSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UserSerializer()

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()