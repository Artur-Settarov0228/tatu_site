from .models import Talaba

class TalabaService:
    @staticmethod
    def get_talaba_by_id(talaba_id):
        try:
            return Talaba.objects.get(id=talaba_id)
        except Talaba.DoesNotExist:
            return None