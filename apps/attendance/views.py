from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Davomat, Fan, Jadval
from .serializers import DavomatSerializer, FanSerializer, JadvalSerializer

class DavomatListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DavomatSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['talaba', 'fan', 'sana', 'holat']
    search_fields = ['talaba__ism', 'talaba__familiya']
    ordering_fields = ['sana']
    
    def get_queryset(self):
        user = self.request.user
        if user.roli == 'ADMIN':
            return Davomat.objects.all()
        elif user.roli == 'OQITUVCHI':
            return Davomat.objects.filter(talaba__guruh__rahbar=user.oqituvchi_profili)
        elif user.roli == 'OTA_ONA':
            return Davomat.objects.filter(talaba__in=user.ota_ona_profili.talabalar.all())
        return Davomat.objects.none()

class FanListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FanSerializer
    queryset = Fan.objects.all()

class JadvalListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = JadvalSerializer
    queryset = Jadval.objects.all()