"""
Rol asosida ruxsat berish tizimi
"""

from rest_framework import permissions

class RolAsosidaRuxsat(permissions.BasePermission):
    """
    Rol asosida ruxsat:
    - ADMIN: To'liq kirish
    - OQITUVCHI: Talabalar va davomatni boshqarish
    - OTA_ONA: Faqat o'z farzandlarini ko'rish
    """
    
    def has_permission(self, request, view):
        # Foydalanuvchi tizimga kirmagan bo'lsa
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Admin hamma narsaga ruxsat
        if request.user.roli == 'ADMIN':
            return True
        
        # Har bir rol uchun ruxsat etilgan sahifalar
        rol_ruxsatlari = {
            'OQITUVCHI': [
                'talaba_royxati', 'talaba_yaratish', 'talaba_tahrirlash',
                'talaba_tafsilotlari', 'davomat_royxati', 'davomat_yaratish',
                'kop_davomat', 'davomat_tarixi', 'oqituvchi_bosh_sahifa'
            ],
            'OTA_ONA': [
                'ota_ona_bosh_sahifa', 'farzand_tafsilotlari',
                'farzand_davomati', 'farzand_statistikasi',
                'farzand_xabarnomalari'
            ]
        }
        
        # Hozirgi sahifa nomini olish
        korinish_nomi = getattr(view, 'ruxsat_nomi', view.__class__.__name__)
        
        # Foydalanuvchi rolida ruxsat bormi?
        if request.user.roli in rol_ruxsatlari:
            return korinish_nomi in rol_ruxsatlari[request.user.roli]
        
        return False
    
    def has_object_permission(self, request, view, obj):
        """Ob'ektga ruxsat"""
        # Admin hamma ob'ektga ruxsat
        if request.user.roli == 'ADMIN':
            return True
        
        # Ota-ona faqat o'z farzandlariga ruxsat
        if request.user.roli == 'OTA_ONA':
            from apps.talabalar.models import Talaba
            from apps.foydalanuvchilar.models import OtaOna
            
            try:
                ota_ona = request.user.ota_ona_profili
                # Ob'ekt Talaba bo'lsa
                if isinstance(obj, Talaba):
                    return ota_ona.talabalar.filter(id=obj.id).exists()
                # Ob'ekt Davomat bo'lsa
                elif hasattr(obj, 'talaba'):
                    return ota_ona.talabalar.filter(id=obj.talaba.id).exists()
            except:
                pass
        
        return False


class AdminRuxsati(permissions.BasePermission):
    """Faqat adminlar uchun ruxsat"""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.roli == 'ADMIN'


class OqituvchiRuxsati(permissions.BasePermission):
    """Faqat o'qituvchilar uchun ruxsat"""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.roli == 'OQITUVCHI'


class OtaOnaRuxsati(permissions.BasePermission):
    """Faqat ota-onalar uchun ruxsat"""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.roli == 'OTA_ONA'