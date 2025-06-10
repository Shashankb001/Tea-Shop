import razorpay
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from apps.cart.views import get_cart
from .models import Order, OrderItem
from .forms import OrderCreateForm

# Initialize Razorpay client
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@login_required
def order_create(request):
    cart = get_cart(request)
    if not cart:
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart:cart_detail')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            # Create order items
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )

            # Clear the cart
            cart.clear()

            # For now, redirect to confirmation. Payment integration will go here.
            return JsonResponse({'order_id': order.id}) # Return JSON for fetch API
        else:
             return JsonResponse({'error': form.errors}, status=400)

    else:
        form = OrderCreateForm(initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        })
        if hasattr(request.user, 'userprofile'):
            form.initial.update({
                'address': request.user.userprofile.address,
                'postal_code': request.user.userprofile.postal_code,
                'city': request.user.userprofile.city,
                #'phone': request.user.userprofile.phone,
            })

    return render(request, 'orders/order_create.html', {
        'cart': cart,
        'form': form
    })

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_confirmation.html', {'order': order})

@login_required
def create_payment(request, order_id):
    try:
        order = get_object_or_404(Order, id=order_id, user=request.user)
        
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
            order = get_object_or_404(Order, id=order_id)
            order.paid = True
            order.save()
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})
