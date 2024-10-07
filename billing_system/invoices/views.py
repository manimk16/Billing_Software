from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Client, Invoice, Payment, Product  # Ensure Product model is imported
from django.contrib.auth import authenticate, login
from django.views import View
from google.oauth2 import id_token
from google.auth.transport import requests
from django.contrib.auth.models import User
from .serializers import ClientSerializer, InvoiceSerializer, PaymentSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from reportlab.pdfgen import canvas
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .forms import InvoiceForm  # Assuming you have an InvoiceForm for the Invoice model
from io import BytesIO
from reportlab.pdfgen import canvas

# Helper functions for JSON conversion
def queryset_to_json(queryset):
    return [obj_to_dict(obj) for obj in queryset]

def obj_to_dict(obj):
    return {
        'id': obj.id,
        'name': obj.name if hasattr(obj, 'name') else None,
        'email': obj.email if hasattr(obj, 'email') else None,
        'address': obj.address if hasattr(obj, 'address') else None,
        # Add other fields as necessary
    }

@csrf_exempt
def client_list(request):
    if request.method == 'GET':
        clients = Client.objects.all()
        data = queryset_to_json(clients)
        return JsonResponse(data, safe=False)
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            client = Client.objects.create(**data)
            return JsonResponse({'id': client.id}, status=201)
        except Exception as e:
            return HttpResponse(f"Invalid data: {str(e)}", status=400)

@csrf_exempt
def client_detail(request, id):
    try:
        client = Client.objects.get(id=id)
    except Client.DoesNotExist:
        return HttpResponse("Client not found.", status=404)

    if request.method in ['PUT', 'PATCH']:
        data = json.loads(request.body)
        for key, value in data.items():
            setattr(client, key, value)
        client.save()
        return JsonResponse({'id': client.id}, status=200)

    if request.method == 'DELETE':
        client.delete()
        return HttpResponse(status=204)

    return JsonResponse(obj_to_dict(client))

@csrf_exempt
def invoice_list(request):
    if request.method == 'GET':
        invoices = Invoice.objects.select_related('client').all()
        data = InvoiceSerializer(invoices, many=True).data  # Use serializer for consistency
        return JsonResponse(data, safe=False)
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            client = Client.objects.get(id=data['client_id'])
            invoice = Invoice.objects.create(client=client, total_amount=data['total_amount'])
            return JsonResponse({'id': invoice.id}, status=201)
        except Client.DoesNotExist:
            return HttpResponse("Client not found", status=404)
        except Exception as e:
            return HttpResponse(f"Invalid data: {str(e)}", status=400)

@csrf_exempt
def payment_list(request):
    if request.method == 'GET':
        payments = Payment.objects.select_related('invoice').all()
        data = PaymentSerializer(payments, many=True).data  # Use serializer for consistency
        return JsonResponse(data, safe=False)
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            invoice = Invoice.objects.get(id=data['invoice_id'])
            payment = Payment.objects.create(
                amount=data['amount'],
                payment_date=data['payment_date'],
                invoice=invoice,
                username=data['username'],
                phone_no=data['phone_no'],
                email_id=data['email_id'],
                payment_method=data['payment_method']
            )
            return JsonResponse({'id': payment.id}, status=201)
        except Invoice.DoesNotExist:
            return HttpResponse("Invoice not found", status=404)
        except Exception as e:
            return HttpResponse(f"Invalid data: {str(e)}", status=400)

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'failed'}, status=401)

# Google login callback class
class GoogleLoginCallback(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            token = data.get('token')
            if not token:
                return JsonResponse({'error': 'No token provided'}, status=400)

            idinfo = id_token.verify_oauth2_token(token, requests.Request(), "YOUR_GOOGLE_CLIENT_ID")

            user_email = idinfo['email']
            user_name = idinfo.get('name', '')

            user, created = User.objects.get_or_create(username=user_email, defaults={'email': user_email, 'first_name': user_name})

            login(request, user)

            return JsonResponse({'status': 'success', 'user_id': user.id})
        except ValueError:
            return JsonResponse({'error': 'Invalid token'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def create(self, request, *args, **kwargs):
        try:
            data = request.data.copy()  # Make a mutable copy of the request data
            payment = Payment.objects.create(
                amount=data['amount'],
                payment_date=data['payment_date'],
                invoice_id=data['invoice'],  # Use invoice_id for ForeignKey
                username=data['username'],
                phone_no=data['phone_no'],
                email_id=data['email_id'],
                payment_method=data['payment_method']
            )
            return Response({'id': payment.id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

from django.views.generic import ListView, DetailView

class InvoiceListView(ListView):
    model = Invoice
    template_name = 'invoices/invoice_list.html'  # Create this template

class InvoiceDetailView(DetailView):
    model = Invoice
    template_name = 'invoices/invoice_detail.html'  # Create this template

@api_view(['GET'])
def fetch_invoice(request, invoice_id):
    try:
        invoice = Invoice.objects.get(id=invoice_id)
        serializer = InvoiceSerializer(invoice)
        return Response(serializer.data)
    except Invoice.DoesNotExist:
        return Response({"error": "Invoice not found"}, status=404)

@api_view(['GET'])
def download_invoice(request, invoice_id):
    try:
        invoice = Invoice.objects.get(id=invoice_id)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="invoice_{invoice_id}.pdf"'
        
        # Create a PDF
        p = canvas.Canvas(response)
        p.drawString(100, 750, f"Invoice ID: {invoice_id}")
        
        # Assuming Invoice has a related Product model and Quantity field
        for product in invoice.product_set.all():  # Use related name if different
            p.drawString(100, 725, f"Product: {product.name}")
            p.drawString(100, 700, f"Quantity: {product.quantity}")  # If quantity is a field in Product
            p.drawString(100, 675, f"Price: {product.price}")
            p.drawString(100, 650, f"Total: {product.price * product.quantity}")

        p.showPage()
        p.save()

        # Send email to the customer after downloading the PDF
        send_email_to_customer(invoice)

        return response
    except Invoice.DoesNotExist:
        return Response({"error": "Invoice not found"}, status=404)

def send_email_to_customer(invoice):
    subject = f'Your Invoice #{invoice.id}'
    message = f'Dear {invoice.client.name},\n\nThank you for your business! Your invoice is attached.\n\nBest regards,\nYour Company'
    recipient_list = [invoice.client.email]  # Assuming you have the client's email in the invoice

    send_mail(
        subject,
        message,
        'your-email@example.com',  # From email
        recipient_list,
        fail_silently=False,
    )

def invoice_create(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new invoice to the database
            return redirect('/invoices/')  # Redirect after saving
    else:
        form = InvoiceForm()  # Display an empty form for GET request
    
    return render(request, 'invoices/invoice_form.html', {'form': form})


def generate_invoice_pdf(invoice):
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    # Create your PDF content here
    p.drawString(100, 750, f'Invoice #{invoice.id}')
    # Add more content based on the invoice details
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer.getvalue()
