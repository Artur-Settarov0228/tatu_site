from rest_framework import serializers
from .models import Davomat, Fan, Jadval

class DavomatSerializer(serializers.ModelSerializer):
    talaba_nomi = serializers.CharField(source='talaba.toliq_ism', read_only=True)
    
    class Meta:
        model = Davomat
        fields = ('id', 'talaba', 'talaba_nomi', 'fan', 'sana', 'holat', 'sabab', 'izoh')

class FanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fan
        fields = ('id', 'nomi', 'kodi')

class JadvalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jadval
        fields = ('id', 'guruh', 'fan', 'oqituvchi', 'hafta_kuni', 'boshlanish_vaqti', 'tugash_vaqti', 'xona')