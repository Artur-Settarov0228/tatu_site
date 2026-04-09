import logging
from celery import shared_task
from django.conf import settings
from telegram import Bot

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def telegram_xabar_yubor(self, chat_id, matn, sarlavha, tur):
    try:
        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        belgi = {'WARNING': '⚠️', 'ALERT': '🔴', 'REPORT': '📊'}.get(tur, '📢')
        toliq_matn = f"{belgi} *{sarlavha}*\n\n{matn}"
        bot.send_message(chat_id=chat_id, text=toliq_matn, parse_mode='Markdown')
        logger.info(f"Xabar yuborildi: {chat_id}")
        return {'status': 'success'}
    except Exception as e:
        logger.error(f"Xato: {e}")
        self.retry(exc=e, countdown=60)