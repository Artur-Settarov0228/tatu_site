from rest_framework import serializers
from .models import Xabarnoma

class XabarnomaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Xabarnoma
        fields = ('id', 'talaba', 'tur', 'sarlavha', 'matn', 'yuborildi', 'yaratilgan_vaqt')