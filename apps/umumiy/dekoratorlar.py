from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseForbidden

def rol_talab_qilinadi(ruxsat_etilgan_rollar):
    """
    Faqat belgilangan rollarga ruxsat berish uchun dekorator
    
    Ishlatish:
    @rol_talab_qilinadi(['ADMIN', 'OQITUVCHI'])
    def my_view(request):
        ...
    """
    def dekorator(korinish):
        @wraps(korinish)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('kirish')
            
            if request.user.roli not in ruxsat_etilgan_rollar:
                messages.error(request, 'Sizga bu sahifaga kirish ruxsati berilmagan!')
                return HttpResponseForbidden("Ruxsat yo'q")
            
            return korinish(request, *args, **kwargs)
        return wrapper
    return dekorator


def log_qil(fayl_nomi='harakatlar.log'):
    """
    Funksiya chaqirilganini log faylga yozish uchun dekorator
    """
    def dekorator(funksiya):
        @wraps(funksiya)
        def wrapper(*args, **kwargs):
            import logging
            logger = logging.getLogger('ilovalar')
            
            # Qaysi funksiya chaqirilganini log qilish
            logger.info(f"Funksiya chaqirildi: {funksiya.__name__}")
            
            # Funksiyani bajarish
            natija = funksiya(*args, **kwargs)
            
            logger.info(f"Funksiya tugadi: {funksiya.__name__}")
            return natija
        return wrapper
    return dekorator