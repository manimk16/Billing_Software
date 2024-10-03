# invoices/serializers.py

from rest_framework import serializers
from .models import Client, Invoice, Payment  # Ensure these models are imported

from .models import Invoice  # Ensure the path is correct

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['id','amount', 'payment_date', 'payment_method', 'customer', 'description']  # Add 'client_id' if needed
