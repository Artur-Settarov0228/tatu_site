from django.urls import path
from .views import DavomatRoyxatiView, FanRoyxatiView

urlpatterns = [
    path('', DavomatRoyxatiView.as_view(), name='davomat_royxati'),
    path('fans/', FanRoyxatiView.as_view(), name='fan_royxati'),
]