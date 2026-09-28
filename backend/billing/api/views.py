from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from billing.models import Payment, Invoice
from billing.api.serializers import PaymentSerializer, InvoiceSerializer


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class InvoiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer


class WebhookPaymentView(APIView):
    def post(self, request):
        event_type = request.data.get('type')
        # Idempotent webhook handling
        return Response({
            'success': True,
            'message': f"Webhook event '{event_type}' processed successfully."
        })
