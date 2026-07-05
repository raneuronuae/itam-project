from django.contrib import admin
from .models import Department, Location, Asset

admin.site.register(Department)
admin.site.register(Location)
admin.site.register(Asset)


from .models import Department, Location, Asset, AssetCategory, AssetSubCategory, Vendor, Employee

admin.site.register(AssetCategory)
admin.site.register(AssetSubCategory)
admin.site.register(Vendor)
admin.site.register(Employee)


from .models import (
    Department, Location, Asset, AssetCategory, 
    AssetSubCategory, Vendor, Employee, AssetAssignment # এটি যোগ করুন
)