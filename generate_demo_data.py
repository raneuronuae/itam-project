import os
import django
import random
from datetime import datetime, timedelta

# জ্যাঙ্গো এনভায়রনমেন্ট সেটআপ
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'itam_core.settings')
django.setup()

from django.contrib.auth.models import User
from core_assets.models import (
    Department, Location, AssetCategory, AssetSubCategory, Vendor, Employee,
    Asset, AssetAssignment, AssetTransfer, PurchaseOrder, PurchaseOrderDetail,
    GoodsReceipt, GoodsReceiptDetail, SoftwareProduct, SoftwareLicense,
    SoftwareInstallation, MaintenanceRequest, MaintenanceHistory, AssetAudit,
    AssetAuditDetail, AssetDisposal, AssetDocument, ActivityLog
)

def create_demo_data():
    print("🚀 ডেমো ডেটা তৈরি হওয়া শুরু হয়েছে... দয়া করে অপেক্ষা করুন...")

    # ০. সুপারইউজার বা ডিফল্ট ইউজার চেক
    user = User.objects.first()
    if not user:
        user = User.objects.create_superuser('admin2', 'admin2@test.com', 'admin123')
        print("👤 একটি ডিফল্ট অ্যাডমিন ইউজার তৈরি করা হয়েছে (username: admin2, pass: admin123)")

    # ১. Locations (৫টি লোকেশন)
    locations_data = [
        {"name": "Dhaka HQ", "code": "LOC-DHAK-01", "city": "Dhaka", "country": "Bangladesh"},
        {"name": "Chittagong Branch", "code": "LOC-CHIT-02", "city": "Chittagong", "country": "Bangladesh"},
        {"name": "Sylhet IT Hub", "code": "LOC-SYLH-03", "city": "Sylhet", "country": "Bangladesh"},
        {"name": "Rajshahi Data Center", "code": "LOC-RAJS-04", "city": "Rajshahi", "country": "Bangladesh"},
        {"name": "Khulna Support Office", "code": "LOC-KHUL-05", "city": "Khulna", "country": "Bangladesh"},
    ]
    locations = []
    for loc in locations_data:
        obj, _ = Location.objects.get_or_create(
            location_code=loc["code"],
            defaults={"location_name": loc["name"], "address": f"Plot 12, Road 5, {loc['city']}", "city": loc["city"], "country": loc["country"]}
        )
        locations.append(obj)

    # ২. Departments (৫টি ডিপার্টমেন্ট)
    depts_data = [
        {"name": "Information Technology", "code": "DEPT-IT", "head": "Rahat Khan"},
        {"name": "Human Resources", "code": "DEPT-HR", "head": "Sadia Afrin"},
        {"name": "Finance & Accounts", "code": "DEPT-FIN", "head": "Anisur Rahman"},
        {"name": "Marketing & Sales", "code": "DEPT-MKT", "head": "Tanvir Ahmed"},
        {"name": "Operations", "code": "DEPT-OPS", "head": "Farhana Yasmin"},
    ]
    departments = []
    for dept in depts_data:
        obj, _ = Department.objects.get_or_create(
            department_code=dept["code"],
            defaults={"department_name": dept["name"], "head_of_department": dept["head"]}
        )
        departments.append(obj)

    # ৩. Asset Categories (৫টি ক্যাটাগরি)
    cats_data = ["Computing Devices", "Network Equipment", "Office Furniture", "Software & Licenses", "Mobile Devices"]
    categories = []
    for cat_name in cats_data:
        obj, _ = AssetCategory.objects.get_or_create(category_name=cat_name, defaults={"description": f"All kinds of {cat_name}"})
        categories.append(obj)

    # ৪. Asset Sub Categories (১০টি সাব-ক্যাটাগরি)
    sub_cats_data = [
        (categories[0], "Laptops"), (categories[0], "Desktops"),
        (categories[1], "Routers"), (categories[1], "Switches"),
        (categories[2], "Ergonomic Chairs"), (categories[2], "Conference Tables"),
        (categories[3], "Operating Systems"), (categories[3], "Design Tools"),
        (categories[4], "Smartphones"), (categories[4], "Tablets")
    ]
    sub_categories = []
    for cat, sub_name in sub_cats_data:
        obj, _ = AssetSubCategory.objects.get_or_create(category=cat, sub_category_name=sub_name, defaults={"description": f"Standard {sub_name}"})
        sub_categories.append(obj)

    # ৫. Vendors (৫টি ভেন্ডর)
    vendors_data = [
        {"name": "Dell Bangladesh", "email": "info@dellbd.com", "phone": "01711111111"},
        {"name": "Star Tech & Engineering", "email": "sales@startech.com", "phone": "01722222222"},
        {"name": "Ryans Computers", "email": "support@ryans.com", "phone": "01733333333"},
        {"name": "Microsoft BD Partner", "email": "license@msbd.com", "phone": "01744444444"},
        {"name": "Flora Telecom", "email": "contact@flora.com", "phone": "01755555555"},
    ]
    vendors = []
    for v in vendors_data:
        obj, _ = Vendor.objects.get_or_create(vendor_name=v["name"], defaults={"email": v["email"], "phone": v["phone"], "address": "Dhaka, Bangladesh"})
        vendors.append(obj)

    # ৬. Employees (৫০টি র্যান্ডম এমপ্লয়ি তৈরি)
    first_names = ["Arif", "Sultana", "Imran", "Nusrat", "Rakib", "Fariha", "Sajid", "Mitu", "Tamim", "Tasnim"]
    last_names = ["Hassan", "Ahmed", "Islam", "Rahman", "Khan", "Ali", "Chowdhury", "Sarker", "Hossain", "Begum"]
    designations = ["Software Engineer", "HR Executive", "Financial Analyst", "Marketing Manager", "IT Support Specialist"]
    
    employees = []
    for i in range(1, 51):
        emp_code = f"EMP-{1000 + i}"
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        email = f"employee{i}@itamproject.com"
        obj, _ = Employee.objects.get_or_create(
            employee_code=emp_code,
            defaults={
                "employee_name": name,
                "email": email,
                "designation": random.choice(designations),
                "department": random.choice(departments),
                "location": random.choice(locations)
            }
        )
        employees.append(obj)

    # ৭. Assets (৫০টি র্যান্ডম অ্যাসেট বা সম্পদ তৈরি)
    brands = ["Dell", "HP", "Lenovo", "Cisco", "Apple", "Samsung", "Otobi"]
    models_pool = ["Latitude 5420", "ThinkPad E14", "ProBook 450", "Catalyst 2960", "MacBook Pro", "Galaxy Tab S8", "Executive Chair"]
    
    assets = []
    for i in range(1, 51):
        tag = f"AST-TAG-{2000 + i}"
        brand = random.choice(brands)
        model = random.choice(models_pool)
        sub_cat = random.choice(sub_categories)
        
        obj, _ = Asset.objects.get_or_create(
            asset_tag=tag,
            defaults={
                "asset_name": f"{brand} {model}",
                "category": sub_cat.category,
                "sub_category": sub_cat,
                "vendor": random.choice(vendors),
                "brand": brand,
                "model": model,
                "serial_number": f"SN-{random.randint(100000, 999999)}-XYZ{i}",
                "purchase_date": datetime.today().date() - timedelta(days=random.randint(30, 730)),
                "purchase_cost": random.randint(5000, 120000),
                "location": random.choice(locations),
                "current_status": "Available",
                "condition_status": "Excellent" if i % 3 == 0 else "Good"
            }
        )
        assets.append(obj)

    # ৮. Asset Assignments (আদান-প্রদান - ২৫টি)
    for i in range(25):
        asset = assets[i]
        employee = employees[i]
        
        # অ্যাসেট স্ট্যাটাস 'Assigned' করা
        asset.current_status = 'Assigned'
        asset.save()
        
        AssetAssignment.objects.get_or_create(
            asset=asset,
            employee=employee,
            assigned_date=datetime.today().date() - timedelta(days=10),
            defaults={
                "assigned_by": user,
                "status": "Assigned",
                "assignment_note": "Assigned for official remote work."
            }
        )

    # ৯. Asset Transfers (স্থানান্তর - ১০টি)
    for i in range(10):
        AssetTransfer.objects.get_or_create(
            asset=random.choice(assets),
            from_location=random.choice(locations),
            to_location=random.choice(locations),
            transfer_date=datetime.today().date(),
            defaults={
                "approved_by": "Admin Approved",
                "status": "Completed",
                "transfer_reason": "Inter-branch office reallocation."
            }
        )

    # ১০. Procurement (ক্রয় আদেশ বা Purchase Orders - ১০টি)
    for i in range(1, 11):
        po, _ = PurchaseOrder.objects.get_or_create(
            po_number=f"PO-2026-{500 + i}",
            defaults={
                "vendor": random.choice(vendors),
                "po_date": datetime.today().date() - timedelta(days=15),
                "approval_status": "Approved",
                "created_by": "Admin User",
                "total_amount": 150000.00
            }
        )
        PurchaseOrderDetail.objects.get_or_create(
            purchase_order=po,
            category=random.choice(categories),
            defaults={"quantity": 5, "unit_price": 30000.00, "total_price": 150000.00}
        )

    # ১১. Maintenance (রক্ষণাবেক্ষণ - ১০টি টিকিট)
    for i in range(10):
        req, _ = MaintenanceRequest.objects.get_or_create(
            ticket_no=f"TKT-{8000 + i}",
            defaults={
                "asset": random.choice(assets),
                "reported_by": "IT Desk",
                "issue_description": "Display flickering issue or OS crash.",
                "priority": "High",
                "status": "Open"
            }
        )

    # ১২. Software Products & Licenses (সফটওয়্যার - ৫টি)
    softwares = ["Windows 11 Pro", "Microsoft Office 365", "Adobe Photoshop", "Kaspersky Antivirus", "Slack Premium"]
    for sw_name in softwares:
        sw, _ = SoftwareProduct.objects.get_or_create(
            software_name=sw_name,
            defaults={"version": "2026.1", "vendor": "Global Distribution", "license_type": "Subscription"}
        )
        SoftwareLicense.objects.get_or_create(
            software_product=sw,
            defaults={"license_key": f"XXXX-XXXX-XXXX-KEY-{random.randint(10,99)}", "quantity": 50, "cost": 15000.00, "status": "Active"}
        )

    print("✅ অভিনন্দন! ৫০টি করে ডেমো ডেটা আপনার সিস্টেমে সফলভাবে ইনপুট হয়ে গেছে।")

if __name__ == "__main__":
    create_demo_data()