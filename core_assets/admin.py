from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from django.urls import reverse

from .models import (
    Department, Location, AssetCategory, AssetSubCategory, Vendor, 
    Employee, Asset, AssetAssignment, AssetTransfer, PurchaseOrder, 
    PurchaseOrderDetail, GoodsReceipt, GoodsReceiptDetail, SoftwareProduct, 
    SoftwareLicense, SoftwareInstallation, MaintenanceRequest, 
    MaintenanceHistory, AssetAudit, AssetAuditDetail, AssetDisposal, 
    AssetDocument, ActivityLog
)

# ==========================================
# পাসওয়ার্ড ফিল্ড প্রফেশনাল করার জন্য কাস্টম ইউজার অ্যাডমিন
# ==========================================
class CustomUserAdmin(UserAdmin):
    # নতুন ক্লিন পাসওয়ার্ড ডিসপ্লে ফিল্ডটি রিড-অনলি হিসেবে যুক্ত করা
    readonly_fields = ('clean_password_display',)

    def clean_password_display(self, obj):
        if obj.pk:
            # পাসওয়ার্ড চেঞ্জ করার ইন্টারনাল অ্যাডমিন ইউআরএল
            change_password_url = reverse('admin:auth_user_password_change', args=[obj.pk])
            return mark_safe(
                f'<div style="margin: 0; padding: 4px 0; font-size: 13px; color: #6c757d; display: flex; align-items: center;">'
                f'<span>Raw passwords are encrypted for security.</span>'
                f'<a href="{change_password_url}" class="btn btn-sm btn-info" '
                f'style="color: #fff; background-color: #17a2b8; border-color: #17a2b8; padding: 4px 10px; border-radius: 4px; margin-left: 15px; font-weight: 500; text-decoration: none;">'
                f'Change Password</a>'
                f'</div>'
            )
        return "Raw passwords are not stored."
    
    clean_password_display.short_description = "Password"

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj:
            # ডিফল্ট ভাঙা পাসওয়ার্ড ফিল্ডটি বাদ দিয়ে আমাদের ক্লিন ফিল্ডটি বসানো
            new_fieldsets = []
            for name, options in fieldsets:
                fields = list(options.get('fields', []))
                if 'password' in fields:
                    fields[fields.index('password')] = 'clean_password_display'
                new_options = dict(options)
                new_options['fields'] = tuple(fields)
                new_fieldsets.append((name, new_options))
            return tuple(new_fieldsets)
        return fieldsets

# ডিফল্ট ইউজার অ্যাডমিন আন-রেজিস্টার করে নতুনটি রেজিস্টার করা
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


# ==========================================
# ১. বেসিক মডিউল সমূহ
# ==========================================
admin.site.register(Department)
admin.site.register(Location)
admin.site.register(Employee)
admin.site.register(Vendor)

# ==========================================
# ২. অ্যাসেট ক্যাটাগরি ও মাস্টার মডিউল
# ==========================================
admin.site.register(AssetCategory)
admin.site.register(AssetSubCategory)
admin.site.register(Asset)
admin.site.register(AssetAssignment)
admin.site.register(AssetTransfer)

# ==========================================
# ৩. প্রকিউরমেন্ট ও রিসিভিং মডিউল
# ==========================================
admin.site.register(PurchaseOrder)
admin.site.register(PurchaseOrderDetail)
admin.site.register(GoodsReceipt)
admin.site.register(GoodsReceiptDetail)

# ==========================================
# ৪. সফটওয়্যার লাইসেন্স মডিউল
# ==========================================
admin.site.register(SoftwareProduct)
admin.site.register(SoftwareLicense)
admin.site.register(SoftwareInstallation)

# ==========================================
# ৫. মেইনটেইন্যান্স, অডিট ও ডিসপোজাল মডিউল
# ==========================================
admin.site.register(MaintenanceRequest)
admin.site.register(MaintenanceHistory)
admin.site.register(AssetAudit)
admin.site.register(AssetAuditDetail)
admin.site.register(AssetDisposal)

# ==========================================
# ৬. ডকুমেন্ট ও লগ মডিউল
# ==========================================
admin.site.register(AssetDocument)
admin.site.register(ActivityLog)