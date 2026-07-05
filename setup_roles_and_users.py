import os
import django

# জ্যাঙ্গো এনভায়রনমেন্ট সেটআপ
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'itam_core.settings')
django.setup()

from django.contrib.auth.models import User, Group, Permission

def setup_roles_and_users():
    print("🚀 রোল, গ্রুপ এবং মাল্টিইউজার তৈরি হওয়া শুরু হয়েছে...")

    # ৩টি গ্রুপ বা রোল তৈরি
    admin_group, _ = Group.objects.get_or_create(name='ITAM_Admin')
    manager_group, _ = Group.objects.get_or_create(name='ITAM_Manager')
    viewer_group, _ = Group.objects.get_or_create(name='ITAM_Viewer')

    # core_assets অ্যাপের সব পারমিশন নেওয়া
    all_permissions = Permission.objects.filter(content_type__app_label='core_assets')

    # গ্রুপভিত্তিক পারমিশন অ্যাসাইন করা
    admin_group.permissions.set(all_permissions)
    
    manager_perms = all_permissions.exclude(codename__startswith='delete_')
    manager_group.permissions.set(manager_perms)

    viewer_perms = all_permissions.filter(codename__startswith='view_')
    viewer_group.permissions.set(viewer_perms)

    # ৩টি রোল-ভিত্তিক ইউজার ডাটা
    users_data = [
        {'username': 'asset_admin', 'email': 'admin@itam.com', 'pass': 'admin123', 'group': admin_group},
        {'username': 'asset_manager', 'email': 'manager@itam.com', 'pass': 'manager123', 'group': manager_group},
        {'username': 'asset_viewer', 'email': 'viewer@itam.com', 'pass': 'viewer123', 'group': viewer_group},
    ]

    for u in users_data:
        if not User.objects.filter(username=u['username']).exists():
            user = User.objects.create_user(
                username=u['username'], email=u['email'], password=u['pass'], is_staff=True
            )
            user.groups.add(u['group'])
            print(f"✅ ইউজার রেডি: {u['username']} | পাসওয়ার্ড: {u['pass']} -> রোল: {u['group'].name}")
        else:
            print(f"⚠️ ইউজার '{u['username']}' অলরেডি আছে।")

    print("🎉 রোল পারমিশন এবং মাল্টিইউজার সেটআপ সফল!")

if __name__ == "__main__":
    setup_roles_and_users()