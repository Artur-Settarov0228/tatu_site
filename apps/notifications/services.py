import logging
from django.conf import settings
from .tasks import send_telegram_message

logger = logging.getLogger(__name__)

def check_nb_and_notify(talaba, nb_count):
    """
    NB soni 5 dan oshganda ota-onaga xabar yuborish
    """
    # Faqat 5 va undan ko'p bo'lganda xabar yuboramiz
    if nb_count >= 5:
        # Talabaning barcha ota-onalariga xabar yuborish
        for ota_ona in talaba.ota_onalar.all():
            if ota_ona.foydalanuvchi.telegram_chat_id:
                # Xabar matnini tayyorlash
                message = f"""
⚠️ *DIQQAT!* ⚠️

Farzandingiz *{talaba.toliq_ism}* 
🎓 Guruh: {talaba.guruh.nomi}

❌ *{nb_count}* marta dars qoldirgan!

Bu jiddiy muammo bo'lishi mumkin.
Iltimos, farzandingiz bilan suhbatlashing va sababini bilib oling.

📊 /stats - Statistika ko'rish
📅 /davomat - Davomat tarixi

--- 
Davomat Tizimi
"""
                # Xabarni yuborish
                send_telegram_message.delay(
                    ota_ona.foydalanuvchi.telegram_chat_id,
                    message
                )
                logger.info(f"Xabar yuborildi: {ota_ona.foydalanuvchi.telefon}")