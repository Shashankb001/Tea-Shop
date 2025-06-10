from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from apps.products.models import Product
from .cart import Cart
from .forms import CartAddProductForm

def get_cart(request):
    return Cart(request)

def cart_detail(request):
    cart = get_cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': int(item['quantity']), 'override': True})
    return render(request, 'cart/cart_detail.html', {'cart': cart})

@require_POST
def cart_add(request, product_id):
    cart = get_cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])
        messages.success(request, f'{product.name} added/updated in your cart.')
    return redirect('cart:cart_detail')

@require_POST
def cart_remove(request, product_id):
    cart = get_cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.success(request, f'{product.name} removed from your cart.')
    return redirect('cart:cart_detail')
