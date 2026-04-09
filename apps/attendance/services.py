from .models import Davomat
from datetime import date

class DavomatService:
    @staticmethod
    def get_today_attendance(guruh_id):
        return Davomat.objects.filter(talaba__guruh_id=guruh_id, sana=date.today())
    
    @staticmethod
    def get_student_nb(talaba_id):
        return Davomat.objects.filter(talaba_id=talaba_id, holat='KELMADI').count()