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
    
    # জ্যাঙ্গোর বিল্ট-ইন ইউজার টেবিলের সাথে লিংক (কারা আদান-প্রদান করছে)
    assigned_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='assignments_made')
    received_by = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name='assets_received', blank=True, null=True)
    
    assignment_note = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=ASSIGNMENT_STATUS, default='Assigned')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.asset.asset_tag} assigned to {self.employee.employee_name}"
