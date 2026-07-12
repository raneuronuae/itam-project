from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.urls import reverse
from datetime import date
from django.utils import timezone

from .models import (
    Department, Location, AssetCategory, AssetSubCategory, Vendor, 
    Employee, Asset, AssetAssignment, AssetTransfer, PurchaseOrder, 
    PurchaseOrderDetail, GoodsReceipt, GoodsReceiptDetail,
    SoftwareProduct, SoftwareLicense, SoftwareInstallation, MaintenanceRequest, 
    MaintenanceHistory, AssetAudit, AssetAuditDetail, AssetDisposal, 
    AssetDocument, ActivityLog
)

# Custom User Admin
class CustomUserAdmin(UserAdmin):
    readonly_fields = ('clean_password_display',)
    def clean_password_display(self, obj):
        if obj.pk:
            change_password_url = reverse('admin:auth_user_password_change', args=[obj.pk])
            return mark_safe(f'<div style="margin: 0; padding: 4px 0; font-size: 13px; color: #6c757d; display: flex; align-items: center;"><span>Raw passwords are encrypted for security.</span><a href="{change_password_url}" class="btn btn-sm btn-info" style="color: #fff; background-color: #17a2b8; border-color: #17a2b8; padding: 4px 10px; border-radius: 4px; margin-left: 15px; font-weight: 500; text-decoration: none;">Change Password</a></div>')
        return "Raw passwords are not stored."
    clean_password_display.short_description = "Password"

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('department_name', 'department_code', 'head_of_department', 'status')
    search_fields = ('department_name', 'department_code', 'head_of_department')
    list_filter = ('status',)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('location_name', 'location_code', 'city', 'country', 'status')
    search_fields = ('location_name', 'location_code', 'city', 'country')
    list_filter = ('status', 'country')

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_code', 'employee_name', 'email', 'department', 'location', 'status')
    search_fields = ('employee_code', 'employee_name', 'email')
    list_filter = ('status', 'department', 'location')

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('vendor_name', 'email', 'phone', 'status')
    search_fields = ('vendor_name', 'email', 'phone')
    list_filter = ('status',)

@admin.register(AssetCategory)
class AssetCategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'description', 'status')
    search_fields = ('category_name',)
    list_filter = ('status',)

@admin.register(AssetSubCategory)
class AssetSubCategoryAdmin(admin.ModelAdmin):
    list_display = ('sub_category_name', 'category', 'status')
    search_fields = ('sub_category_name', 'category__category_name')
    list_filter = ('status', 'category')

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('asset_tag', 'asset_name', 'category', 'brand', 'model', 'purchase_cost', 'current_status', 'condition_status')
    search_fields = ('asset_tag', 'asset_name', 'serial_number', 'service_tag', 'brand', 'model')
    list_filter = ('current_status', 'condition_status', 'category', 'location', 'brand')
    list_editable = ('current_status', 'condition_status')
    list_per_page = 20

@admin.register(AssetAssignment)
class AssetAssignmentAdmin(admin.ModelAdmin):
    list_display = ('asset', 'employee', 'assigned_date', 'expected_return_date', 'returned_date', 'status')
    search_fields = ('asset__asset_tag', 'asset__asset_name', 'employee__employee_name', 'employee__employee_code')
    list_filter = ('status', 'assigned_date')

@admin.register(AssetTransfer)
class AssetTransferAdmin(admin.ModelAdmin):
    list_display = ('asset', 'from_location', 'to_location', 'transfer_date', 'status')
    search_fields = ('asset__asset_tag', 'transfer_reason')
    list_filter = ('status', 'transfer_date')

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('po_number', 'vendor', 'po_date', 'total_amount', 'approval_status', 'created_by')
    list_filter = ('approval_status', 'po_date', 'vendor')
    search_fields = ('po_number', 'vendor__name', 'remarks')
    ordering = ('-po_date',)
    list_display_links = ('po_number',)

@admin.register(PurchaseOrderDetail)
class PurchaseOrderDetailAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'purchase_order', 
        'category', 
        'quantity', 
        'unit_price', 
        'total_price'
    )
    search_fields = ('purchase_order__id', 'category__name')
    list_filter = ('category', 'purchase_order')

@admin.register(GoodsReceipt)
class GoodsReceiptAdmin(admin.ModelAdmin):
    list_display = ('grn_number', 'vendor', 'purchase_order', 'received_date', 'received_by')
    list_filter = ('received_date', 'vendor')
    search_fields = ('grn_number', 'vendor__name') # আপনার Vendor মডেলে name ফিল্ড থাকলে এটি কাজ করবে
    list_display_links = ('grn_number',)
    ordering = ('-received_date',)

@admin.register(GoodsReceiptDetail)
class GoodsReceiptDetailAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'goods_receipt', 
        'asset', 
        'serial_number',
    )
    list_filter = ('goods_receipt', 'asset')
    search_fields = ('serial_number', 'goods_receipt__id', 'asset__name')
    list_display_links = ('id', 'serial_number')
    list_per_page = 20

@admin.register(SoftwareProduct)
class SoftwareProductAdmin(admin.ModelAdmin):
    # status_badge এবং license_type_badge এখানে রাখা হয়েছে
    list_display = ('software_name', 'version', 'vendor', 'license_type_badge', 'status_badge')
    list_filter = ('license_type', 'status', 'vendor')
    search_fields = ('software_name', 'vendor')
    
    def status_badge(self, obj):
        color = '#28a745' if obj.status == 'Active' else '#dc3545'
        return format_html(
            '<span style="padding: 4px 10px; border-radius: 12px; background-color: {}; color: white; font-size: 11px; font-weight: bold;">{}</span>',
            color, obj.status
        )
    status_badge.short_description = 'Status'

    def license_type_badge(self, obj):
        return format_html(
            '<span style="padding: 4px 10px; border-radius: 12px; background-color: #007bff; color: white; font-size: 11px; font-weight: bold;">{}</span>',
            obj.license_type
        )
    license_type_badge.short_description = 'License Type'

@admin.register(SoftwareLicense)
class SoftwareLicenseAdmin(admin.ModelAdmin):
    list_display = ('get_software_name', 'license_key', 'expiry_date_colored', 'status_badge')
    
    # Software নাম দেখানোর জন্য
    def get_software_name(self, obj):
        return obj.software_product.software_name
    get_software_name.short_description = 'Software'

    # স্ট্যাটাস ব্যাজ (ইনলাইন স্টাইল)
    def status_badge(self, obj):
        status_val = str(obj.status).strip() if obj.status else 'Inactive'
        
        if status_val.lower() == 'active':
            return mark_safe('<span style="background-color: #28a745; color: white; padding: 4px 8px; border-radius: 4px; font-size: 0.85em;">Active</span>')
        else:
            return mark_safe('<span style="background-color: #dc3545; color: white; padding: 4px 8px; border-radius: 4px; font-size: 0.85em;">Inactive</span>')
    status_badge.short_description = 'Status'

    # এক্সপায়ারি ডেট (কালারসহ)
    def expiry_date_colored(self, obj):
        if not obj.expiry_date:
            return "No Date"
        
        # যদি তারিখ পার হয়ে যায় (লাল রঙ), অন্যথায় সবুজ
        color = "#dc3545" if obj.expiry_date < date.today() else "#27ae60"
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', color, obj.expiry_date)
    expiry_date_colored.short_description = 'Expiry Date'

@admin.register(SoftwareInstallation)
class SoftwareInstallationAdmin(admin.ModelAdmin):
    list_display = ('license', 'asset', 'installed_date', 'installed_by', 'status')
    
    list_filter = ('status', 'installed_date', 'installed_by')
    
    search_fields = ('license__software_name', 'asset__name') # আপনার মডেলের ফিল্ড অনুযায়ী এটি পরিবর্তন করতে হতে পারে

    def __str__(self):
        return f"{self.license} on {self.asset}"

@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = (
        'ticket_no', 
        'asset', 
        'reported_by', 
        'priority', 
        'status', 
        'created_at'
    )
    list_display_links = ('ticket_no', 'asset')
    list_editable = ('status', 'priority')
    list_filter = ('status', 'priority', 'created_at')
    search_fields = ('ticket_no', 'asset__name', 'issue_description')
    date_hierarchy = 'created_at'
    list_per_page = 20
    def get_list_display(self, request):
        return self.list_display

@admin.register(MaintenanceHistory)
class MaintenanceHistoryAdmin(admin.ModelAdmin):
    list_display = ('maintenance_request', 'vendor', 'repair_date', 'repair_cost_formatted', 'status', 'downtime_hours')
    list_display_links = ('maintenance_request',)
    list_editable = ('status',)
    list_filter = ('status', 'repair_date', 'vendor')
    search_fields = ('maintenance_request__id', 'vendor__name', 'status')
    date_hierarchy = 'repair_date'
    readonly_fields = ('maintenance_request',)
    list_per_page = 20

    def repair_cost_formatted(self, obj):
        return f"৳ {obj.repair_cost:,.2f}"
    repair_cost_formatted.short_description = 'Repair Cost'

    class Media:
        css = {'all': ('css/admin_custom.css',)}

@admin.register(AssetAudit)
class AssetAuditAdmin(admin.ModelAdmin):
    list_display = ('id', 'audit_date', 'location', 'auditor_name')
    list_filter = ('audit_date', 'location')
    search_fields = ('auditor_name', 'location__location_name', 'remarks')
    date_hierarchy = 'audit_date'
    list_display_links = ('id', 'audit_date')
    list_per_page = 20

@admin.register(AssetAuditDetail)
class AssetAuditDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'audit', 'asset', 'physical_status', 'remarks')
    list_filter = ('physical_status', 'audit')
    search_fields = ('asset__name', 'audit__id', 'remarks')
    list_editable = ('physical_status',)
    list_per_page = 20
    autocomplete_fields = ['audit', 'asset']

@admin.register(AssetDisposal)
class AssetDisposalAdmin(admin.ModelAdmin):
    # টেবিলে প্রদর্শিত কলামসমূহ
    list_display = (
        'asset', 
        'disposal_date', 
        'disposal_reason', 
        'book_value', 
        'sale_value', 
        'profit_or_loss_display', 
        'approved_by'
    )
    
    # সাইডবার ফিল্টার
    list_filter = ('disposal_reason', 'disposal_date', 'approved_by')
    
    # সার্চ বার
    search_fields = ('asset__asset_tag', 'remarks')

    # প্রফিট বা লস দেখানোর জন্য কাস্টম মেথড
    def profit_or_loss_display(self, obj):
        val = obj.profit_or_loss
        # নিশ্চিত করুন val একটি সংখ্যা, প্রয়োজনে ০ ধরুন
        if val is None:
            val = 0
        color = 'green' if val >= 0 else 'red'
        # format_html এর সিনট্যাক্স ঠিক করা হলো
        return format_html(
            '<span style="color: {color}; font-weight: bold;">{val}</span>',
            color=color,
            val=val
        )
    
    profit_or_loss_display.short_description = 'Profit/Loss'

@admin.register(AssetDocument)
class AssetDocumentAdmin(admin.ModelAdmin):
    list_display = ('asset', 'document_type', 'file_path', 'uploaded_at')
    list_filter = ('document_type', 'uploaded_at')
    search_fields = ('asset__asset_tag', 'asset__asset_name')
    readonly_fields = ('uploaded_at',)

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'action', 'module_name', 'record_id', 'created_at')
    list_filter = ('action', 'created_at')
    search_fields = ('user__username', 'module_name', 'action')
    readonly_fields = ('created_at',)
    def get_username(self, obj):
        return obj.user.username if obj.user else "System"
    get_username.short_description = 'User'