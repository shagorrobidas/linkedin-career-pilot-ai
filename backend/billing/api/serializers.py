from rest_framework import serializers
from billing.models import Payment, Invoice


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'amount', 'currency', 'provider', 'external_payment_id', 'status', 'created_at']
        read_only_fields = ['id', 'created_at']


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['id', 'invoice_number', 'amount', 'currency', 'status', 'invoice_pdf_url', 'issued_at']
        read_only_fields = ['id', 'issued_at']
