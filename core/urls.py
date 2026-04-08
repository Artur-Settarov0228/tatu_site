"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/talabalar/', include('apps.talabalar.urls')),
    path('api/davomat/', include('apps.davomat.urls')),
    path('api/tahlillar/', include('apps.tahlillar.urls')),
    path('api/foydalanuvchilar/', include('apps.foydalanuvchilar.urls')),
    path('api/umumiy/', include('apps.umumiy.urls')),
    path('api/xabarnomalar/', include('apps.xabarnomalar.urls')),
]
# Media va statik fayllar uchun (faqat development muhitida)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)