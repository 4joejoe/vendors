from django.urls import path
from .views import (
    VendorView,
    PurchaseOrderView,
    PurchaseOrderAcknowledgement,
    VendorPerformance,
)

urlpatterns = [
    path("vendors/", VendorView.as_view()),
    path("vendors/<int:vendor_id>/", VendorView.as_view()),
    path("purchase-order/", PurchaseOrderView.as_view()),
    path("purchase-order/<int:po_id>/", PurchaseOrderView.as_view()),
    path("purchase-order/vendor/<int:vendor_id>/", PurchaseOrderView.as_view()),
    path(
        "purchase-order/<int:po_id>/acknowledge/",
        PurchaseOrderAcknowledgement.as_view(),
    ),
    path("vendors/<int:vendor_id>/performance/", VendorPerformance.as_view()),
]
