from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
from types import SimpleNamespace
from weasyprint import HTML
from .models import AssetAssignment
from django.contrib.auth.models import User

# --- সেন্ট্রাল পিডিএফ জেনারেশন ইঞ্জিন ---
def generate_pdf_response(template_path, context, filename):
    html_string = render_to_string(template_path, context)
    html = HTML(string=html_string, base_url=str(settings.BASE_DIR))
    pdf_file = html.write_pdf()
    
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}.pdf"'
    return response

# --- ১) Real DB-based Asset Assignment Challan ---
@login_required
def asset_assignment_challan(request, assignment_id):
    challan = get_object_or_404(
        AssetAssignment.objects.select_related('asset', 'employee', 'employee__department'), 
        id=assignment_id
    )
    
    context = {
        'challan': challan,
        'page_title': f"Challan DC-2026-{challan.id:04d}",
    }
    
    if request.GET.get('format') == 'pdf':
        return generate_pdf_response('core_assets/delivery_challan.html', context, f"Challan_{challan.id}")
        
    return render(request, 'core_assets/delivery_challan.html', context)

# --- ২) Purchase Order (PO) Invoice (Mock Data) ---
@login_required
def purchase_order_invoice(request, po_id):
    po = SimpleNamespace(
        id=po_id,
        po_number=f"PO-2026-{po_id:04d}",
        created_at="2026-07-10",
        due_date="2026-08-10",
        status="Approved",
        vendor_name="Nexus IT Distribution Enterprise",
        vendor_address="Business Bay, Downtown, Dubai, UAE",
        company_name="Enterprise ITAM Solutions",
        sub_total=15450.00,
        tax_amount=772.50,
        grand_total=15772.50,
        items_all=[
            SimpleNamespace(name="Dell XPS 15 9530 Laptop", sku="LAP-DELL-XPS15", qty=5, price=2500.00, total=12500.00),
            SimpleNamespace(name="Asus ProArt 27\" 4K Monitor", sku="MON-ASUS-PA27", qty=3, price=953.33, total=2860.00)
        ]
    )

    context = {'po': po, 'page_title': f"Invoice {po.po_number}"}

    if request.GET.get('format') == 'pdf':
        return generate_pdf_response('core_assets/invoice.html', context, f"Invoice_{po.po_number}")

    return render(request, 'core_assets/invoice.html', context)

# --- ৩) Asset Assignment Delivery Challan (Mock Data) ---
@login_required
def mock_asset_assignment_challan(request, assignment_id):
    challan = SimpleNamespace(
        id=assignment_id,
        challan_no=f"DC-2026-{assignment_id:04d}",
        issue_date="2026-07-10",
        employee_name="Abir Hasan",
        department="Software Engineering",
        items_all=[
            SimpleNamespace(asset_name="Dell XPS 15 9530 Laptop", serial_no="CN-0XPS15-74123-XYZ", condition="Brand New", qty=1),
            SimpleNamespace(asset_name="Asus ProArt 27\" 4K Monitor", serial_no="ASUS-PA27-99812-ABC", condition="Refurbished", qty=1)
        ]
    )

    context = {'challan': challan, 'page_title': f"Challan {challan.challan_no}"}

    if request.GET.get('format') == 'pdf':
        return generate_pdf_response('core_assets/delivery_challan.html', context, f"Challan_{challan.challan_no}")

    return render(request, 'core_assets/delivery_challan.html', context)

# --- Force Create Admin User (Temporary Fix) ---
def force_create_admin(request):
    if not User.objects.filter(username='Ruhul_Amin').exists():
        User.objects.create_superuser('Ruhul_Amin', 'ruhulaminn@gmail.com', 'adminuae')
        return HttpResponse("সফলভাবে ইউজার তৈরি হয়েছে! এখন লগইন করুন।")
    return HttpResponse("ইউজার আগেই তৈরি করা আছে।")