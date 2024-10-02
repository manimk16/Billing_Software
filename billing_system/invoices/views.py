from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Client, Invoice, Payment
from django.contrib.auth import authenticate, login
from django.views import View
from google.oauth2 import id_token
from google.auth.transport import requests
from django.contrib.auth.models import User
from .serializers import ClientSerializer, InvoiceSerializer, PaymentSerializer
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Invoice
from .serializers import InvoiceSerializer



def queryset_to_json(queryset):
    # Convert queryset to a list of dictionaries
    return [obj_to_dict(obj) for obj in queryset]

def obj_to_dict(obj):
    # Convert a model instance to a dictionary
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
        data = queryset_to_json(invoices)
        return JsonResponse(data, safe=False)
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            data['client'] = Client.objects.get(id=data['client_id'])
            invoice = Invoice.objects.create(**data)
            return JsonResponse({'id': invoice.id}, status=201)
        except Client.DoesNotExist:
            return HttpResponse("Client not found", status=404)
        except Exception as e:
            return HttpResponse(f"Invalid data: {str(e)}", status=400)

@csrf_exempt
def payment_list(request):
    if request.method == 'GET':
        payments = Payment.objects.select_related('invoice').all()
        data = queryset_to_json(payments)
        return JsonResponse(data, safe=False)
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            data['invoice'] = Invoice.objects.get(id=data['invoice_id'])
            payment = Payment.objects.create(**data)
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
        # Get the token from the request body
        try:
            data = json.loads(request.body)
            token = data.get('token')
            if not token:
                return JsonResponse({'error': 'No token provided'}, status=400)

            # Verify the token
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), "484398151029-lf22i1853m8ne6pffc4g68mdvnne3mdr.apps.googleusercontent.com")

            # Extract user information
            user_email = idinfo['email']
            user_name = idinfo.get('name', '')

            # Check if the user exists, if not, create a new one
            user, created = User.objects.get_or_create(username=user_email, defaults={'email': user_email, 'first_name': user_name})

            # Log the user in
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
    
    
class InvoiceList(APIView):
    """
    Retrieve all invoices or create a new invoice.
    """
    def get(self, request):
        return Response({"message": "List of invoices"}, status=status.HTTP_200_OK)

    def post(self, request):
        return Response({"message": "Invoice created"}, status=status.HTTP_201_CREATED)
    
    

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
