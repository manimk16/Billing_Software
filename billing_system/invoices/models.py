from django.db import models

# Client model for storing client details
class Client(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)  # Added unique constraint for email

    def __str__(self):
        return self.name

# Invoice model for storing invoices linked to a client
class Invoice(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='invoices')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    issue_date = models.DateField(auto_now_add=True)  # Automatically set the issue date when created
    due_date = models.DateField(null=True, blank=True)  # Optional field for due date

    def __str__(self):
        return f"Invoice {self.id} - {self.client.name}"

# Payment model for storing payment details
class Payment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)  # Automatically set payment date when created
    username = models.CharField(max_length=255)
    phone_no = models.CharField(max_length=20)
    email_id = models.EmailField(max_length=255)
    payment_method = models.CharField(max_length=50, choices=[
        ('Credit Card', 'Credit Card'),
        ('PayPal', 'PayPal'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Cash', 'Cash')
    ])  # Optional: Add more choices

    def __str__(self):
        return f"Payment by {self.username} - {self.amount}"

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    # other fields as needed
