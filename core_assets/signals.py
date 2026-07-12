from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django_currentuser.middleware import get_current_user
from .models import (
    Department, Location, Employee, AssetCategory, AssetSubCategory, 
    Vendor, Asset, AssetAssignment, AssetTransfer, PurchaseOrder, 
    GoodsReceipt, SoftwareLicense, MaintenanceRequest, AssetAudit, 
    AssetDisposal, AssetDocument, ActivityLog
)

# মডেলের লিস্ট এখানে ডিফাইন করা হলো যাতে কোনো ইম্পোর্ট এরর না হয়
MODELS_TO_LOG = [
    Department, Location, Employee, AssetCategory, AssetSubCategory, 
    Vendor, Asset, AssetAssignment, AssetTransfer, PurchaseOrder, 
    GoodsReceipt, SoftwareLicense, MaintenanceRequest, AssetAudit, 
    AssetDisposal, AssetDocument
]

@receiver(post_save)
def log_all_changes(sender, instance, created, **kwargs):
    # যদি মডেলটি আমাদের লিস্টের হয়, তবেই লগ তৈরি হবে
    if sender in MODELS_TO_LOG:
        module_name = sender.__name__
        action = "Created" if created else "Updated"

        # বর্তমান ইউজারকে খুঁজে বের করা
        user = get_current_user()
        
        # ActivityLog তৈরি করা
        ActivityLog.objects.create(
            user=user if user and not user.is_anonymous else None,
            module_name=module_name,
            record_id=instance.id,
            action=action,
            new_value=f"{module_name} {action} with ID: {instance.id}"
        )

# ডিলিট অপারেশন ট্র্যাক করার জন্য সিগন্যাল
@receiver(post_delete)
def log_delete_action(sender, instance, **kwargs):
    if sender in MODELS_TO_LOG:
        user = get_current_user()
        ActivityLog.objects.create(
            user=user if user and not user.is_anonymous else None,
            module_name=sender.__name__,
            record_id=instance.id,
            action="Deleted",
            new_value=f"{sender.__name__} with ID {instance.id} was deleted"
        )