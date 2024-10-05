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
    username = serializers.CharField(source='user.username', read_only=True)
    phone_no = serializers.CharField(source='user.profile.phone_no', read_only=True)  # Assuming a Profile model
    email_id = serializers.EmailField(source='user.email', read_only=True)
    class Meta:
        model = Invoice
        fields = '__all__'  # Add 'client_id' if needed
