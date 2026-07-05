from django.db import models
from django.contrib.auth.models import User

# ১.১ Departments Table
class Department(models.Model):
    department_name = models.CharField(max_length=100)
    department_code = models.CharField(max_length=20, unique=True)
    head_of_department = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, default='Active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.department_name


# ১.২ Locations Table
class Location(models.Model):
    location_name = models.CharField(max_length=100)
    location_code = models.CharField(max_length=20, unique=True)
    address = models.TextField()
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default='Active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.location_name


# ২.১ Asset Categories Table
class AssetCategory(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, default='Active')

    class Meta:
        verbose_name = "Asset Category"
        verbose_name_plural = "Asset Categories"

    def __str__(self):
        return self.category_name


# ২.২ Asset Sub Categories Table
class AssetSubCategory(models.Model):
    category = models.ForeignKey(AssetCategory, on_delete=models.CASCADE)
    sub_category_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, default='Active')

    class Meta:
        verbose_name = "Asset Sub Category"
        verbose_name_plural = "Asset Sub Categories"

    def __str__(self):
        return f"{self.category.category_name} - {self.sub_category_name}"


# ৩.১ Vendors Table
class Vendor(models.Model):
    vendor_name = models.CharField(max_length=150)
    contact_person = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, default='Active')

    def __str__(self):
        return self.vendor_name


# ১.৩ Employees Table
class Employee(models.Model):
    employee_code = models.CharField(max_length=20, unique=True)
    employee_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    designation = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, default='Active')

    def __str__(self):
        return f"{self.employee_code} - {self.employee_name}"


# ৪.১ Assets Master Table
class Asset(models.Model):
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Assigned', 'Assigned'),
        ('In Repair', 'In Repair'),
        ('Disposed', 'Disposed'),
    ]

    CONDITION_CHOICES = [
        ('Excellent', 'Excellent'),
        ('Good', 'Good'),
        ('Fair', 'Fair'),
        ('Poor', 'Poor'),
    ]

    asset_tag = models.CharField(max_length=50, unique=True)
    asset_name = models.CharField(max_length=150)

    category = models.ForeignKey(AssetCategory, on_delete=models.PROTECT, null=True, blank=True)
    sub_category = models.ForeignKey(AssetSubCategory, on_delete=models.PROTECT, null=True, blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT, null=True, blank=True)

    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    serial_number = models.CharField(max_length=100, unique=True)
    purchase_date = models.DateField()
    purchase_cost = models.DecimalField(max_digits=10, decimal_places=2)

    location = models.ForeignKey(Location, on_delete=models.PROTECT)

    current_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Available'
    )

    condition_status = models.CharField(
        max_length=20,
        choices=CONDITION_CHOICES,
        default='Good'
    )

    remarks = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.asset_tag} - {self.asset_name}"


# ৫.১ Asset Assignments Table
class AssetAssignment(models.Model):
    ASSIGNMENT_STATUS = [
        ('Assigned', 'Assigned'),
        ('Returned', 'Returned'),
        ('Lost', 'Lost'),
        ('Transferred', 'Transferred'),
    ]

    asset = models.ForeignKey(Asset, on_delete=models.PROTECT)
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
    assigned_date = models.DateField()
    expected_return_date = models.DateField(blank=True, null=True)
    returned_date = models.DateField(blank=True, null=True)
    
    assigned_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='assignments_made')
    received_by = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name='assets_received', blank=True, null=True)
    
    assignment_note = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=ASSIGNMENT_STATUS, default='Assigned')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.asset.asset_tag} assigned to {self.employee.employee_name}"


# ==========================================
# 6. Asset Transfer Module
# ==========================================
class AssetTransfer(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Rejected', 'Rejected'),
    ]
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='transfers')
    from_location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='transfers_from')
    to_location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='transfers_to')
    transfer_date = models.DateField()
    approved_by = models.CharField(max_length=100, blank=True, null=True)
    received_by = models.CharField(max_length=100, blank=True, null=True)
    transfer_reason = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Transfer of {self.asset.asset_tag} to {self.to_location.location_name}"


# ==========================================
# 7. Procurement Module
# ==========================================
class PurchaseOrder(models.Model):
    APPROVAL_CHOICES = [
        ('Draft', 'Draft'),
        ('Pending Approval', 'Pending Approval'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT, related_name='purchase_orders')
    po_date = models.DateField()
    expected_delivery_date = models.DateField(blank=True, null=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    approval_status = models.CharField(max_length=20, choices=APPROVAL_CHOICES, default='Draft')
    created_by = models.CharField(max_length=100)
    approved_by = models.CharField(max_length=100, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.po_number

class PurchaseOrderDetail(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='details')
    category = models.ForeignKey(AssetCategory, on_delete=models.PROTECT)
    description = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)


# ==========================================
# 8. Asset Receiving Module
# ==========================================
class GoodsReceipt(models.Model):
    grn_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.SET_NULL, blank=True, null=True)
    received_date = models.DateField()
    received_by = models.CharField(max_length=100)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.grn_number

class GoodsReceiptDetail(models.Model):
    goods_receipt = models.ForeignKey(GoodsReceipt, on_delete=models.CASCADE, related_name='details')
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    serial_number = models.CharField(max_length=100, blank=True, null=True)


# ==========================================
# 9. Software License Management
# ==========================================
class SoftwareProduct(models.Model):
    software_name = models.CharField(max_length=150)
    version = models.CharField(max_length=50, blank=True, null=True)
    vendor = models.CharField(max_length=100, blank=True, null=True)
    license_type = models.CharField(max_length=50, blank=True, null=True) # e.g., Subscription, OEM, Retail
    status = models.CharField(max_length=20, default='Active')

    def __str__(self):
        return f"{self.software_name} ({self.version})"

class SoftwareLicense(models.Model):
    software_product = models.ForeignKey(SoftwareProduct, on_delete=models.CASCADE, related_name='licenses')
    license_key = models.TextField()
    purchase_date = models.DateField(blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT, blank=True, null=True)
    status = models.CharField(max_length=20, default='Active')

    def __str__(self):
        return f"License for {self.software_product.software_name}"

class SoftwareInstallation(models.Model):
    license = models.ForeignKey(SoftwareLicense, on_delete=models.CASCADE, related_name='installations')
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='software_installed')
    installed_date = models.DateField()
    installed_by = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, default='Installed')


# ==========================================
# 10. Maintenance Management
# ==========================================
class MaintenanceRequest(models.Model):
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
    ]
    ticket_no = models.CharField(max_length=50, unique=True)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='maintenance_requests')
    reported_by = models.CharField(max_length=100)
    issue_description = models.TextField()
    priority = models.CharField(max_length=15, choices=PRIORITY_CHOICES, default='Medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ticket_no

class MaintenanceHistory(models.Model):
    maintenance_request = models.OneToOneField(MaintenanceRequest, on_delete=models.CASCADE, related_name='history')
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, blank=True, null=True)
    repair_date = models.DateField()
    repair_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    resolution = models.TextField()
    downtime_hours = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    completed_by = models.CharField(max_length=100)


# ==========================================
# 11. Asset Audit Module
# ==========================================
class AssetAudit(models.Model):
    audit_date = models.DateField()
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    auditor_name = models.CharField(max_length=100)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Audit at {self.location.location_name} on {self.audit_date}"

class AssetAuditDetail(models.Model):
    STATUS_CHOICES = [
        ('Found', 'Found'),
        ('Missing', 'Missing'),
        ('Damaged', 'Damaged'),
        ('Replaced', 'Replaced'),
    ]
    audit = models.ForeignKey(AssetAudit, on_delete=models.CASCADE, related_name='details')
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    physical_status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    remarks = models.TextField(blank=True, null=True)


# ==========================================
# 12. Asset Disposal Module
# ==========================================
class AssetDisposal(models.Model):
    REASON_CHOICES = [
        ('Obsolete', 'Obsolete'),
        ('Damaged', 'Damaged'),
        ('Lost', 'Lost'),
        ('Sold', 'Sold'),
        ('Scrapped', 'Scrapped'),
    ]
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE, related_name='disposal')
    disposal_date = models.DateField()
    book_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    sale_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    disposal_reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    approved_by = models.CharField(max_length=100)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Disposal of {self.asset.asset_tag}"


# ==========================================
# 13. Document Management
# ==========================================
class AssetDocument(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=50) 
    file_name = models.CharField(max_length=255)
    file_path = models.FileField(upload_to='asset_documents/')
    uploaded_by = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)


# ==========================================
# 15. Activity Log
# ==========================================
class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    module_name = models.CharField(max_length=100)
    record_id = models.IntegerField()
    action = models.CharField(max_length=50) 
    old_value = models.TextField(blank=True, null=True)
    new_value = models.TextField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} on {self.module_name}"