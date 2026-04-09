from rest_framework import serializers
from .models import Talaba, Guruh, Kurs, Yonalish

class TalabaSerializer(serializers.ModelSerializer):
    toliq_ism = serializers.CharField(read_only=True)
    guruh_nomi = serializers.CharField(source='guruh.nomi', read_only=True)
    
    class Meta:
        model = Talaba
        fields = ('id', 'talaba_id', 'ism', 'familiya', 'toliq_ism', 'guruh', 'guruh_nomi', 'telefon', 'ota_ona_telefon', 'manzil', 'aktiv')

class GuruhSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guruh
        fields = ('id', 'nomi', 'yonalish', 'kurs', 'oquv_yili')

class KursSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kurs
        fields = ('id', 'nomi', 'tartib')

class YonalishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Yonalish
        fields = ('id', 'nomi', 'kodi')