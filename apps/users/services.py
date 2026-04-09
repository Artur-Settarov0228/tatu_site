from .models import Foydalanuvchi

class UserService:
    @staticmethod
    def get_user_by_telefon(telefon):
        try:
            return Foydalanuvchi.objects.get(telefon=telefon)
        except Foydalanuvchi.DoesNotExist:
            return None