from apps.users.models import Foydalanuvchi, OtaOna
import random

class FoydalanuvchiXizmati:
    
    @staticmethod
    def telegram_bilan_boglash(telefon, chat_id):
        try:
            user = Foydalanuvchi.objects.get(telefon=telefon, roli='OTA_ONA')
            user.telegram_chat_id = chat_id
            user.tasdiqlangan = True
            user.save()
            return user
        except Foydalanuvchi.DoesNotExist:
            return None
    
    @staticmethod
    def tasdiqlash_kodi_yarat():
        return str(random.randint(100000, 999999))