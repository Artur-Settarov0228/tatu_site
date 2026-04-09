from rest_framework import serializers
from apps.students.models import Kurs, Yonalish, Guruh, Talaba, OtaOnaTalaba

class KursSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kurs
        fields = '__all__'


class YonalishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Yonalish
        fields = '__all__'


class GuruhSerializer(serializers.ModelSerializer):
    yonalish_nomi = serializers.CharField(source='yonalish.nomi', read_only=True)
    kurs_nomi = serializers.CharField(source='kurs.nomi', read_only=True)
    
    class Meta:
        model = Guruh
        fields = ['id', 'nomi', 'yonalish', 'yonalish_nomi', 'kurs', 'kurs_nomi', 'oquv_yili', 'rahbar', 'aktiv']


class TalabaSerializer(serializers.ModelSerializer):
    toliq_ism = serializers.CharField(read_only=True)
    nb_soni = serializers.IntegerField(read_only=True)
    guruh_nomi = serializers.CharField(source='guruh.nomi', read_only=True)
    yonalish_nomi = serializers.CharField(source='guruh.yonalish.nomi', read_only=True)
    kurs_nomi = serializers.CharField(source='guruh.kurs.nomi', read_only=True)
    
    class Meta:
        model = Talaba
        fields = [
            'id', 'talaba_id', 'ism', 'familiya', 'toliq_ism',
            'guruh', 'guruh_nomi', 'yonalish_nomi', 'kurs_nomi',
            'telefon', 'ota_ona_telefon', 'manzil', 'qabul_sana',
            'aktiv', 'nb_soni', 'yaratilgan_vaqt'
        ]
        read_only_fields = ['id', 'talaba_id', 'qabul_sana', 'yaratilgan_vaqt']


class TalabaYaratishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Talaba
        fields = ['ism', 'familiya', 'guruh', 'telefon', 'ota_ona_telefon', 'manzil']
    
    def create(self, validated_data):
        # Unikal talaba_id yaratish
        import random
        import string
        talaba_id = ''.join(random.choices(string.digits, k=8))
        validated_data['talaba_id'] = talaba_id
        return super().create(validated_data)