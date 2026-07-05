from django.urls import path
from . import views

urlpatterns = [ 
    path('purchase-order/<int:po_id>/invoice/', views.purchase_order_invoice, name='po_invoice'),
]