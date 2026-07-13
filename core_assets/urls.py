from django.urls import path
from . import views

urlpatterns = [
    # PO Invoice URL 
    path('purchase-order/<int:po_id>/invoice/', views.purchase_order_invoice, name='purchase_order_invoice'),
    
    # Delivery Challan URL 
    path('asset-assignment/<int:assignment_id>/challan/', views.asset_assignment_challan, name='asset_assignment_challan'),

    # Admin Creation URL (Temporary)
    path('create-me/', views.force_create_admin, name='force_create_admin'),
]