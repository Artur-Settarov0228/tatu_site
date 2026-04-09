import logging
from django.utils import timezone
from .models import Xabarnoma, XabarnomaSozlamalari
from .tasks import telegram_xabar_yubor

logger = logging.getLogger(__name__)

def nb_chegarasini_tekshir(talaba):
    nb_soni = talaba.nb_soni
    ketma_ket = talaba.ketma_ket_nb_olish()
    
    if nb_soni == 3:
        xabarnoma_yarat(talaba, 'ALERT', f"⚠️ Diqqat! {talaba.toliq_ism} 3 marta dars qoldirdi!", nb_soni, ketma_ket)
    elif nb_soni == 5:
        xabarnoma_yarat(talaba, 'WARNING', f"⚠️ Ogohlantirish! {talaba.toliq_ism} 5 marta dars qoldirdi!", nb_soni, ketma_ket)
    
    if ketma_ket >= 3:
        xabarnoma_yarat(talaba, 'ALERT', f"⚠️ {talaba.toliq_ism} {ketma_ket} kun ketma-ket dars qoldirdi!", nb_soni, ketma_ket)

def xabarnoma_yarat(talaba, tur, sarlavha, nb_soni=0, ketma_ket_nb=0):
    for ota_ona in talaba.ota_onalar.all():
        xabarnoma = Xabarnoma.objects.create(
            talaba=talaba, ota_ona=ota_ona, tur=tur, sarlavha=sarlavha,
            matn=sarlavha, nb_soni=nb_soni, ketma_ket_nb=ketma_ket_nb
        )
        xabarni_yubor(xabarnoma)

def xabarni_yubor(xabarnoma):
    ota_ona = xabarnoma.ota_ona
    if not ota_ona:
        return
    
    try:
        sozlamalar = ota_ona.xabarnoma_sozlamalari
    except XabarnomaSozlamalari.DoesNotExist:
        sozlamalar = None
    
    if sozlamalar and sozlamalar.telegram_xabar:
        if ota_ona.foydalanuvchi.telegram_chat_id:
            telegram_xabar_yubor.delay(
                chat_id=ota_ona.foydalanuvchi.telegram_chat_id,
                matn=xabarnoma.matn,
                sarlavha=xabarnoma.sarlavha,
                tur=xabarnoma.tur
            )
            xabarnoma.yuborildi = True
            xabarnoma.yuborilgan_vaqt = timezone.now()
            xabarnoma.save()