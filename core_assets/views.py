from django.shortcuts import render, get_object_or_404
from .models import PurchaseOrder

def purchase_order_invoice(request, po_id):
    # ডেটাবেস থেকে নির্দিষ্ট Purchase Order এবং তার ডিটেইলস নিয়ে আসা
    po = get_object_or_404(PurchaseOrder, id=po_id)
    po_details = po.details.all()  # মডেলে দেওয়া related_name='details'
    
    # ব্যাকএন্ডেই প্রতিটি আইটেমের সাবটোটাল এবং গ্র্যান্ড টোটাল ডাইনামিকালি হিসাব করা
    calculated_total = 0
    for detail in po_details:
        detail.subtotal = detail.quantity * detail.unit_price
        calculated_total += detail.subtotal

    context = {
        'po': po,
        'po_details': po_details,
        'calculated_total': calculated_total,  # সঠিক গ্র্যান্ড টোটাল পাঠানো হলো
    }
    return render(request, 'core_assets/invoice.html', context)