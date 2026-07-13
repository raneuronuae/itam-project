from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.urls import reverse
from datetime import date

# আপনার মডেলগুলো এখানে ইমপোর্ট করা আছে
from .models import (
    Department, Location, AssetCategory, AssetSubCategory, Vendor, 
    Employee, Asset, AssetAssignment, AssetTransfer, PurchaseOrder, 
    PurchaseOrderDetail, GoodsReceipt, GoodsReceiptDetail,
    SoftwareProduct, SoftwareLicense, SoftwareInstallation, MaintenanceRequest, 
    MaintenanceHistory, AssetAudit, AssetAuditDetail, AssetDisposal, 
    AssetDocument, ActivityLog
)

# --- Unregistering default User to avoid conflict ---
admin.site.unregister(User)

# --- Inlines ---
class GoodsReceiptDetailInline(admin.TabularInline):
    model = GoodsReceiptDetail
    extra = 1
    fields = ('asset', 'serial_number')

# --- User Admin ---
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    exclude = ('password',) 
    
    fieldsets = (
        (None, {'fields': ('username', 'first_name', 'last_name', 'email')}),
        ('Security & Status', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
        ('Password Management', {'fields': ('password_change_link',)}),
    )
    
    readonly_fields = ('password_change_link',)

    def password_change_link(self, obj):
        if obj.pk:
            change_password_url = reverse('admin:auth_user_password_change', args=[obj.pk])
            # বাটনটিকে সরাসরি একটি লিঙ্কের ক্লাসে রূপান্তর করা হলো যা Jazzmin থিমের সাথে ভালো মানাবে
            return mark_safe(
                f'<a href="{change_password_url}" class="btn btn-info" style="color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">'
                f'<i class="fa fa-key"></i> Change User Password'
                f'</a>'
            )
        return "Save the user first to set a password."
    
    password_change_link.short_description = "Security Action"

# --- Master Data Admin ---
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('department_name', 'department_code', 'head_of_department', 'status_badge')
    list_filter = ('status',)
    
    def status_badge(self, obj):
        color = '#28a745' if obj.status == 'Active' else '#dc3545'
        return format_html('<span style="padding: 4px 10px; border-radius: 12px; background-color: {}; color: white; font-size: 11px; font-weight: bold;">{}</span>', color, obj.status)
    status_badge.short_description = 'Status'

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('location_name', 'location_code', 'city', 'country', 'status')
    list_filter = ('status', 'country')

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('vendor_name', 'email', 'phone', 'status')
    list_filter = ('status',)

# --- Asset Management Admin ---
@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('asset_tag', 'asset_name', 'category', 'brand', 'model', 'purchase_cost', 'current_status', 'condition_status')
    list_editable = ('current_status', 'condition_status')
    list_filter = ('current_status', 'condition_status', 'category', 'location', 'brand')
    search_fields = ('asset_tag', 'asset_name', 'serial_number')
    fieldsets = (
        ('Basic Information', {'fields': ('asset_name', 'asset_tag', 'category', 'brand', 'model', 'serial_number', 'service_tag')}),
        ('Financial & Lifecycle', {'fields': ('purchase_cost', 'purchase_date', 'vendor'), 'classes': ('collapse',)}),
        ('Status & Location', {'fields': ('current_status', 'condition_status', 'location', 'employee')}),
    )

@admin.register(AssetCategory)
class AssetCategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'description', 'status')

@admin.register(AssetSubCategory)
class AssetSubCategoryAdmin(admin.ModelAdmin):
    list_display = ('sub_category_name', 'category', 'status')

@admin.register(AssetAssignment)
class AssetAssignmentAdmin(admin.ModelAdmin):
    list_display = ('asset', 'employee', 'assigned_date', 'status')

@admin.register(AssetTransfer)
class AssetTransferAdmin(admin.ModelAdmin):
    list_display = ('asset', 'from_location', 'to_location', 'transfer_date', 'status')

# --- Procurement Admin ---
@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('po_number', 'vendor', 'po_date', 'total_amount', 'approval_status')

@admin.register(GoodsReceipt)
class GoodsReceiptAdmin(admin.ModelAdmin):
    list_display = ('grn_number', 'vendor', 'purchase_order', 'received_date', 'received_by')
    inlines = [GoodsReceiptDetailInline]

# --- Software Admin ---
@admin.register(SoftwareProduct)
class SoftwareProductAdmin(admin.ModelAdmin):
    list_display = ('software_name', 'version', 'license_type', 'status')

@admin.register(SoftwareLicense)
class SoftwareLicenseAdmin(admin.ModelAdmin):
    list_display = ('software_product', 'license_key', 'expiry_date_colored', 'status')
    
    def expiry_date_colored(self, obj):
        color = "#dc3545" if obj.expiry_date and obj.expiry_date < date.today() else "#27ae60"
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', color, obj.expiry_date)
    expiry_date_colored.short_description = 'Expiry Date'

# --- Maintenance & Audit ---
@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ('ticket_no', 'asset', 'priority', 'status', 'created_at')
    list_editable = ('status', 'priority')

@admin.register(MaintenanceHistory)
class MaintenanceHistoryAdmin(admin.ModelAdmin):
    list_display = ('maintenance_request', 'repair_cost_formatted', 'repair_date')
    
    def repair_cost_formatted(self, obj):
        return f"৳ {obj.repair_cost:,.2f}"
    repair_cost_formatted.short_description = 'Repair Cost'

@admin.register(AssetDisposal)
class AssetDisposalAdmin(admin.ModelAdmin):
    list_display = ('asset', 'disposal_date', 'profit_or_loss_display')
    
    def profit_or_loss_display(self, obj):
        val = obj.profit_or_loss or 0
        color = 'green' if val >= 0 else 'red'
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', color, val)

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'module_name', 'created_at')

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_code', 'employee_name', 'department', 'status')

@admin.register(AssetAudit)
class AssetAuditAdmin(admin.ModelAdmin):
    list_display = ('id', 'audit_date', 'location', 'auditor_name')

@admin.register(AssetDocument)
class AssetDocumentAdmin(admin.ModelAdmin):
    list_display = ('asset', 'document_type', 'uploaded_at')