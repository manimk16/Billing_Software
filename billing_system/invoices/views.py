from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Client, Invoice, Payment
from django.contrib.auth import authenticate, login
from django.core import serializers

# Helper function to convert querysets to JSON
def queryset_to_json(queryset):
    return json.loads(serializers.serialize('json', queryset))


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
        except:
            return HttpResponse("Invalid data", status=400)
    else:
        return HttpResponse("Unsupported HTTP method.", status=405)

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
        except:
            return HttpResponse("Invalid data", status=400)
    else:
        return HttpResponse("Unsupported HTTP method.", status=405)

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
        except:
            return HttpResponse("Invalid data", status=400)
    else:
        return HttpResponse("Unsupported HTTP method.", status=405)

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
    
@csrf_exempt
def client_detail(request, id):
    try:
        client = Client.objects.get(id=id)
    except Client.DoesNotExist:
        return HttpResponse("Client not found.", status=404)

    if request.method == 'PUT' or request.method == 'PATCH':
        data = json.loads(request.body)
        for key, value in data.items():
            setattr(client, key, value)
        client.save()
        return JsonResponse({'id': client.id}, status=200)

    if request.method == 'DELETE':
        client.delete()
        return HttpResponse(status=204)

    # Optional: Handle GET request to return client data
    return JsonResponse({
        'id': client.id,
        'name': client.name,
        'email': client.email,
        'address': client.address,
    })

