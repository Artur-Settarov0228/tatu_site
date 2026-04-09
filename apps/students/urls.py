from django.urls import path
from .views import TalabaRoyxatiView, TalabaTafsilotView, GuruhRoyxatiView

urlpatterns = [
    path('', TalabaRoyxatiView.as_view(), name='talaba_royxati'),
    path('groups/', GuruhRoyxatiView.as_view(), name='guruh_royxati'),
    path('<int:pk>/', TalabaTafsilotView.as_view(), name='talaba_tafsilot'),
]