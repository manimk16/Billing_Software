from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Invoice(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Invoice {self.id} - {self.client.name}"

class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    username = models.CharField(max_length=255)  
    phone_no = models.CharField(max_length=20)  
    email_id = models.EmailField(max_length=255) 
    payment_method = models.CharField(max_length=50) 

    def __str__(self):
        return f"{self.username} - {self.amount}"
