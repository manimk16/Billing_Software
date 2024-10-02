from django.shortcuts import render
from django.http import JsonResponse
from paypalrestsdk import Payment
import paypalrestsdk

def create_payment(request):
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": "http://127.0.0.1:8000/payment/success/",
            "cancel_url": "http://127.0.0.1:8000/payment/cancel/"
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "Invoice Item",
                    "sku": "item",
                    "price": "100.00",  # Replace with your item price
                    "currency": "USD",
                    "quantity": 1
                }]
            },
            "amount": {
                "total": "100.00",  # Total amount
                "currency": "USD"
            },
            "description": "This is the payment description."
        }]
    })

    if payment.create():
        print("Payment created successfully")
        for link in payment.links:
            if link.rel == "approval_url":
                approval_url = str(link.href)
                return JsonResponse({'approval_url': approval_url})

    return JsonResponse({'error': 'Payment creation failed'})

def payment_success(request):
    return render(request, 'payment_success.html')

def payment_cancel(request):
    return render(request, 'payment_cancel.html')

def execute_payment(request):
    # Logic to execute the payment goes here
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        return JsonResponse({'status': 'Payment executed successfully!'})
    else:
        return JsonResponse({'error': payment.error}, status=400)