from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords

# ==========================================
# Base Abstract Model (শুধু ইতিহাস ট্র্যাক করার জন্য)
# ==========================================
class BaseModel(models.Model):
    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True

# ==========================================
# ১. অর্গানাইজেশন ও ইউজার কোর মডিউল
# ==========================================

class Department(BaseModel):
    department_name = models.CharField(max_length=100)
    department_code = models.CharField(max_length=50, unique=True)
    head_of_department = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, default='Active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.department_name

class Location(BaseModel):
    location_name = models.CharField(max_length=100)
    location_code = models.CharField(max_length=50, unique=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, default='Active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.location_name

class Employee(BaseModel):
    employee_code = models.CharField(max_length=50, unique=True)
    employee_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    joining_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, default='Active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.employee_code} - {self.employee_name}"

# ==========================================
# ২. অ্যাসেট ক্যাটাগরি মডিউল
# ==========================================

class AssetCategory(BaseModel):
    category_name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, default='Active')

    class Meta:
        verbose_name = "Asset Category"
        verbose_name_plural = "Asset Categories"

    def __str__(self):
        return self.category_name

class AssetSubCategory(BaseModel):
    category = models.ForeignKey(AssetCategory, on_delete=models.CASCADE)
    sub_category_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, default='Active')

    class Meta:
        verbose_name = "Asset Sub Category"
        verbose_name_plural = "Asset Sub Categories"

    def __str__(self):
        return f"{self.category.category_name} - {self.sub_category_name}"

# ==========================================
# ৩. ভেন্ডর মডিউল
# ==========================================

class Vendor(BaseModel):
    vendor_name = models.CharField(max_length=150)
    contact_person = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=20, default='Active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name

# ==========================================
# ৪. অ্যাসেট মাস্টার মডিউল
# ==========================================

class Asset(BaseModel):
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Assigned', 'Assigned'),
        ('In Repair', 'In Repair'),
        ('In Transit', 'In Transit'),
        ('Disposed', 'Disposed'),
        ('Lost', 'Lost'),
        ('Damaged', 'Damaged'),
        ('Reserved', 'Reserved'),
    ]
    CONDITION_CHOICES = [
        ('Excellent', 'Excellent'),
        ('Good', 'Good'),
        ('Fair', 'Fair'),
        ('Poor', 'Poor'),
        ('Damaged', 'Damaged'),
    ]

    asset_tag = models.CharField(max_length=100, unique=True)
    asset_name = models.CharField(max_length=150)
    category = models.ForeignKey(AssetCategory, on_delete=models.PROTECT)
    sub_category = models.ForeignKey(AssetSubCategory, on_delete=models.SET_NULL, null=True, blank=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)
    serial_number = models.CharField(max_length=100, unique=True, blank=True, null=True)
    service_tag = models.CharField(max_length=100, blank=True, null=True)
    purchase_date = models.DateField(blank=True, null=True)
    purchase_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True)
    warranty_start = models.DateField(blank=True, null=True)
    warranty_end = models.DateField(blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    current_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')
    condition_status = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='Good')
    depreciation_years = models.IntegerField(default=0)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.asset_tag} - {self.asset_name}"

# ==========================================
# ৫. অ্যাসেট অপারেশনস
# ==========================================

class AssetAssignment(BaseModel):
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
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assignments_made')
    received_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='assets_received', blank=True)
    assignment_note = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=ASSIGNMENT_STATUS, default='Assigned')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.asset.asset_tag} assigned to {self.employee.employee_name}"

class AssetTransfer(BaseModel):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Rejected', 'Rejected'),
    ]
    asset = models.ForeignKey(Asset, on_delete=models.PROTECT, related_name='transfers')
    from_location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='transfers_from')
    to_location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='transfers_to')
    transfer_date = models.DateField()
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='transfer_approved_by')
    received_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='transfer_received_by')
    transfer_reason = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Transfer of {self.asset.asset_tag} to {self.to_location.location_name}"

# ==========================================
# ৬. প্রকিউরমেন্ট ও রিসিভিং মডিউল
# ==========================================

class PurchaseOrder(BaseModel):
    APPROVAL_CHOICES = [
        ('Draft', 'Draft'),
        ('Pending Approval', 'Pending Approval'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    po_number = models.CharField(max_length=100, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT, related_name='purchase_orders')
    po_date = models.DateField()
    expected_delivery_date = models.DateField(blank=True, null=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    approval_status = models.CharField(max_length=20, choices=APPROVAL_CHOICES, default='Draft')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='po_created_by')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='po_approved_by')
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.po_number

class PurchaseOrderDetail(BaseModel):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='details')
    category = models.ForeignKey(AssetCategory, on_delete=models.PROTECT)
    description = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

class GoodsReceipt(BaseModel):
    grn_number = models.CharField(max_length=100, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.SET_NULL, blank=True, null=True)
    received_date = models.DateField()
    received_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.grn_number

class GoodsReceiptDetail(BaseModel):
    goods_receipt = models.ForeignKey(GoodsReceipt, on_delete=models.CASCADE, related_name='details')
    asset = models.ForeignKey(Asset, on_delete=models.SET_NULL, null=True, blank=True)
    serial_number = models.CharField(max_length=100, blank=True, null=True)

# ==========================================
# ৭. সফটওয়্যার লাইসেন্স ম্যানেজমেন্ট
# ==========================================

class SoftwareProduct(BaseModel):
    software_name = models.CharField(max_length=150)
    version = models.CharField(max_length=50, blank=True, null=True)
    vendor = models.CharField(max_length=100, blank=True, null=True)
    license_type = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=20, default='Active')

    def __str__(self):
        return f"{self.software_name} ({self.version})"

class SoftwareLicense(BaseModel):
    software_product = models.ForeignKey(SoftwareProduct, on_delete=models.CASCADE, related_name='licenses')
    license_key = models.TextField()
    purchase_date = models.DateField(blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    cost = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, default='Active')

    def __str__(self):
        return f"License for {self.software_product.software_name}"

class SoftwareInstallation(BaseModel):
    license = models.ForeignKey(SoftwareLicense, on_delete=models.CASCADE, related_name='installations')
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='software_installed')
    installed_date = models.DateField()
    installed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, default='Installed')
    def __str__(self):
        return f"{self.license} - {self.asset}"

# ==========================================
# ৮. মেইনটেন্যান্স ম্যানেজমেন্ট
# ==========================================

class MaintenanceRequest(BaseModel):
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
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    issue_description = models.TextField()
    priority = models.CharField(max_length=15, choices=PRIORITY_CHOICES, default='Medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ticket_no

class MaintenanceHistory(BaseModel):
    maintenance_request = models.OneToOneField(MaintenanceRequest, on_delete=models.CASCADE, related_name='history_data')
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, blank=True, null=True)
    repair_date = models.DateField(blank=True, null=True)
    repair_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    resolution = models.TextField(blank=True, null=True)
    downtime_hours = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    completed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

# ==========================================
# ৯. অডিট, ডিসপোজাল ও ডকুমেন্ট মডিউল
# ==========================================

class AssetAudit(BaseModel):
    audit_date = models.DateField()
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    auditor_name = models.CharField(max_length=100)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Audit at {self.location.location_name} on {self.audit_date}"

class AssetAuditDetail(BaseModel):
    STATUS_CHOICES = [
        ('Found', 'Found'),
        ('Missing', 'Missing'),
        ('Damaged', 'Damaged'),
        ('Replaced', 'Replaced'),
    ]
    audit = models.ForeignKey(AssetAudit, on_delete=models.CASCADE, related_name='details')
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    physical_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Found')
    remarks = models.TextField(blank=True, null=True)

class AssetDisposal(BaseModel):
    REASON_CHOICES = [
        ('Obsolete', 'Obsolete'),
        ('Damaged', 'Damaged'),
        ('Lost', 'Lost'),
        ('Sold', 'Sold'),
        ('Scrapped', 'Scrapped'),
    ]
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE, related_name='disposal')
    disposal_date = models.DateField()
    book_value = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    sale_value = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    disposal_reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    remarks = models.TextField(blank=True, null=True)

    @property
    def profit_or_loss(self):
        return self.sale_value - self.book_value

    def __str__(self):
        return f"Disposal of {self.asset.asset_tag}"

class AssetDocument(BaseModel):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=50) 
    file_name = models.CharField(max_length=255)
    file_path = models.FileField(upload_to='asset_documents/')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.document_type} - {self.asset.asset_tag}"

# ==========================================
# ১০. সিস্টেম সিকিউরিটি (অ্যাক্টিভিটি লগ)
# ==========================================

class ActivityLog(models.Model): # BaseModel থেকে উত্তরাধিকার না নিয়ে সরাসরি models.Model ব্যবহার করা নিরাপদ
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    module_name = models.CharField(max_length=100)
    record_id = models.IntegerField()
    action = models.CharField(max_length=50) 
    old_value = models.TextField(blank=True, null=True)
    new_value = models.TextField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # যদি ইউজার থাকে তবে নাম দেখাবে, না থাকলে 'System' দেখাবে
        username = self.user.username if self.user else "System"
        return f"{self.action} on {self.module_name} by {self.user}"
    
class Meta:
        ordering = ['-created_at'] # নতুন লগ সবার উপরে দেখাবে