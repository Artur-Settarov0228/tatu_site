from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def rol_talab(ruxsat_etilgan_rollar):
    def dekorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if request.user.roli not in ruxsat_etilgan_rollar:
                messages.error(request, 'Ruxsat etilmagan!')
                return redirect('dashboard')
            return view_func(request, *args, **kwargs)
        return wrapper
    return dekorator