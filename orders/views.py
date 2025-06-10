import razorpay
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem
from apps.cart.cart import Cart
import json

# Initialize Razorpay client
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        order = Order.objects.create(user=request.user)
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
            )
        cart.clear()
        return redirect('orders:order_confirmation', order_id=order.id)
    return render(request, 'orders/order_create.html', {'cart': cart})

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_confirmation.html', {'order': order})

def create_payment(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        
        # Create Razorpay order
        razorpay_order = client.order.create({
            'amount': int(order.get_total_cost() * 100),  # Amount in paise
            'currency': 'INR',
            'payment_capture': 1
        })
        
        return JsonResponse({
            'order_id': razorpay_order['id'],
            'amount': razorpay_order['amount'],
            'currency': razorpay_order['currency'],
            'key': settings.RAZORPAY_KEY_ID
        })
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def payment_webhook(request):
    if request.method == 'POST':
        try:
            # Verify the payment signature
            params_dict = {
                'razorpay_payment_id': request.POST.get('razorpay_payment_id'),
                'razorpay_order_id': request.POST.get('razorpay_order_id'),
                'razorpay_signature': request.POST.get('razorpay_signature')
            }
            
            client.utility.verify_payment_signature(params_dict)
            
            # Update order status
            order_id = request.POST.get('razorpay_order_id')
            order = Order.objects.get(id=order_id)
            order.paid = True
            order.save()
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400) 