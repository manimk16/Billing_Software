from rest_framework import serializers
from .models import Client, Invoice, Payment, Product  # Ensure all models are imported


# Client Serializer
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


# Invoice Serializer with Product and Client details
class InvoiceSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)  # Serialize client data
    products = serializers.SerializerMethodField()  # Use SerializerMethodField for custom product serialization

    class Meta:
        model = Invoice
        fields = ['id', 'client', 'total_amount', 'issue_date', 'due_date', 'products']  # Add 'due_date' if applicable

    # Custom method to serialize products (if invoice has related products)
    def get_products(self, obj):
        products = obj.product_set.all()  # Assuming an Invoice has a relationship with Product
        return ProductSerializer(products, many=True).data  # Serialize multiple products


# Payment Serializer
class PaymentSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='invoice.client.name', read_only=True)  # Add client name from invoice
    email_id = serializers.EmailField(source='invoice.client.email', read_only=True)  # Add client email from invoice

    class Meta:
        model = Payment
        fields = ['id', 'amount', 'payment_date', 'invoice', 'username', 'phone_no', 'email_id', 'payment_method', 'client_name']


# Product Serializer (assuming it's a model related to Invoice)
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price']
