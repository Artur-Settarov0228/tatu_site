from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Foydalanuvchi, Oqituvchi, OtaOna

class RegistratsiyaSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = Foydalanuvchi
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name', 'telefon', 'roli')
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Parollar mos kelmadi"})
        if data.get('telefon') and Foydalanuvchi.objects.filter(telefon=data['telefon']).exists():
            raise serializers.ValidationError({"telefon": "Bu telefon ro'yxatdan o'tgan"})
        return data
    
    def create(self, data):
        data.pop('password2')
        password = data.pop('password')
        user = Foydalanuvchi.objects.create_user(**data)
        user.set_password(password)
        user.save()
        
        if user.roli == 'OQITUVCHI':
            Oqituvchi.objects.create(foydalanuvchi=user, xodim_id=f"TCH{user.id:05d}", mutaxassislik="Umumiy")
        elif user.roli == 'OTA_ONA':
            OtaOna.objects.create(foydalanuvchi=user)
        
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Username yoki parol noto'g'ri")
        if not user.is_active:
            raise serializers.ValidationError("Foydalanuvchi faol emas")
        data['user'] = user
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Foydalanuvchi
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'telefon', 'roli')