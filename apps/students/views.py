from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from .models import Talaba, Guruh, Kurs, Yonalish
from .serializers import TalabaSerializer, GuruhSerializer, KursSerializer, YonalishSerializer

class TalabaListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TalabaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['ism', 'familiya', 'talaba_id']
    ordering_fields = ['ism', 'familiya']
    
    def get_queryset(self):
        user = self.request.user
        if user.roli == 'ADMIN':
            return Talaba.objects.filter(aktiv=True)
        elif user.roli == 'OQITUVCHI':
            return Talaba.objects.filter(guruh__rahbar=user.oqituvchi_profili, aktiv=True)
        elif user.roli == 'OTA_ONA':
            return user.ota_ona_profili.talabalar.filter(aktiv=True)
        return Talaba.objects.none()

class TalabaDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TalabaSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.roli == 'ADMIN':
            return Talaba.objects.all()
        elif user.roli == 'OQITUVCHI':
            return Talaba.objects.filter(guruh__rahbar=user.oqituvchi_profili)
        elif user.roli == 'OTA_ONA':
            return user.ota_ona_profili.talabalar.all()
        return Talaba.objects.none()

class GuruhListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GuruhSerializer
    queryset = Guruh.objects.filter(aktiv=True)

class KursListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = KursSerializer
    queryset = Kurs.objects.all()

class YonalishListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = YonalishSerializer
    queryset = Yonalish.objects.all()