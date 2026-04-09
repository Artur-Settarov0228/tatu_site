from .models import Talaba

class TalabaXizmati:
    @staticmethod
    def nb_statistikasi(talaba_id):
        try:
            talaba = Talaba.objects.get(id=talaba_id)
            return {'talaba': talaba.toliq_ism, 'jami_nb': talaba.nb_soni, 'ketma_ket': talaba.ketma_ket_nb_olish()}
        except Talaba.DoesNotExist:
            return None