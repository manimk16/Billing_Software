from django.contrib import admin
from .models import Client, Invoice, Payment

admin.site.register(Client)
admin.site.register(Invoice)
admin.site.register(Payment)
