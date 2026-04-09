from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Xabarnoma
from .serializers import XabarnomaSerializer

class XabarnomaListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = XabarnomaSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.roli == 'OTA_ONA':
            return Xabarnoma.objects.filter(ota_ona=user.ota_ona_profili)
        return Xabarnoma.objects.none()