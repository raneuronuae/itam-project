"""
URL configuration for itam_core project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

# অ্যাপ্লিকেশনের ইউআরএলগুলো এখানে গুছিয়ে রাখা হয়েছে
urlpatterns = [
    # মূল লিংকে প্রবেশ করলে সরাসরি অ্যাডমিনে রিডাইরেক্ট করবে
    path('', lambda request: redirect('admin/')),

    # অ্যাডমিন প্যানেল
    path('admin/', admin.site.urls),

    # কোর এসেট মডিউল (ITAM Core Assets)
    path('core/', include('core_assets.urls')),

    # অথেন্টিকেশন সিস্টেম (Allauth)
    path('accounts/', include('allauth.urls')),
]

# মিডিয়া এবং স্ট্যাটিক ফাইল হ্যান্ডলিং
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)