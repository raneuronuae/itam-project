"""
URL configuration for itam_core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# অ্যাপ্লিকেশনের ইউআরএলগুলো এখানে গুছিয়ে রাখা হয়েছে
urlpatterns = [
    # অ্যাডমিন প্যানেল
    path('admin/', admin.site.urls),

    # কোর এসেট মডিউল (ITAM Core Assets)
    path('core/', include('core_assets.urls')),

    # অথেন্টিকেশন সিস্টেম (Allauth)
    # জ্যাঙ্গো টেমপ্লেট থেকে রিডাইরেক্ট এবং পাসওয়ার্ড রিসেট এরর ফিক্স করতে এটি জরুরি
    path('accounts/', include('allauth.urls')),
]

# লোকাল ডেভেলপমেন্টে (DEBUG=True) কাস্টম CSS, জ্যাজমিন থিম এবং মিডিয়া ফাইল জোরপূর্বক সার্ভ করার ফিক্স
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)