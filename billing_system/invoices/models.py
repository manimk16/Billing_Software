from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Client(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    address = models.TextField()
    phone_number = models.CharField(max_length=15, blank=True)  # Optional field for phone number

    def __str__(self):
        return self.name


class Invoice(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='invoices')
    invoice_number = models.CharField(max_length=50, unique=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    issued_date = models.DateField()
    due_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.invoice_number

    def clean(self):
        # Ensure that the due date is after the issued date
        if self.due_date < self.issued_date:
            raise ValidationError("Due date cannot be before the issued date.")

    def is_paid(self):
        # Check if total payments match the total amount
        total_paid = sum(payment.amount for payment in self.payment_set.all())
        return total_paid >= self.total_amount


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
        ('cash', 'Cash'),
    ]

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(default=timezone.now)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES)

    def __str__(self):
        return f"Payment of {self.amount} for Invoice {self.invoice.invoice_number}"

    def clean(self):
        # Ensure the payment amount does not exceed the invoice total
        if self.amount <= 0:
            raise ValidationError("Payment amount must be greater than zero.")
        if self.amount + sum(p.amount for p in self.invoice.payment_set.all()) > self.invoice.total_amount:
            raise ValidationError("Payment exceeds the total invoice amount.")
