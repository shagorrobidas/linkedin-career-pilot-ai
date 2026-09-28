from django.urls import path, include
from rest_framework.routers import DefaultRouter
from billing.api.views import PaymentViewSet, InvoiceViewSet, WebhookPaymentView

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'invoices', InvoiceViewSet, basename='invoice')

urlpatterns = [
    path('webhook/', WebhookPaymentView.as_view(), name='billing-webhook'),
    path('', include(router.urls)),
]
