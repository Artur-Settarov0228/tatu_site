from .models import Davomat
from datetime import date

class DavomatXizmati:
    @staticmethod
    def bugungi_davomat(guruh_id):
        return Davomat.objects.filter(talaba__guruh_id=guruh_id, sana=date.today())
    
    @staticmethod
    def talaba_davomati(talaba_id, oy, yil):
        return Davomat.objects.filter(talaba_id=talaba_id, sana__year=yil, sana__month=oy)