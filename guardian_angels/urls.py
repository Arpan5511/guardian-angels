"""
URL configuration for guardian_angels project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .auth_views import login_view, logout_view

def home_view(request):
    from django.shortcuts import render
    from doctors.models import Doctor
    featured_doctors = Doctor.objects.filter(is_available=True)[:3]
    return render(request, 'index.html', {'featured_doctors': featured_doctors})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('doctors/', include('doctors.urls')),
    path('patients/', include('patients.urls')),
    path('appointments/', include('appointments.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
