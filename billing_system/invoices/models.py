from django.db import models
from django.core.exceptions import ValidationError

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

    def __str__(self):
        return self.invoice_number

    def clean(self):
        # Ensure that the due date is after the issued date
        if self.due_date < self.issued_date:
            raise ValidationError("Due date cannot be before the issued date.")

class Payment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=50, blank=True)  # Optional field for payment method

    def __str__(self):
        return f"Payment {self.id} for Invoice {self.invoice.invoice_number}"
