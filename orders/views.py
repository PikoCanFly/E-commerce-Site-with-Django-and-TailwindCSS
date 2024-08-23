from django.shortcuts import render, redirect, get_object_or_404
from cart.models import Cart
from .forms import OrderCreateForm
from .models import OrderItem, Order



def order_create(request):
    cart=None
    cart_id = request.session.get('cart_id')
    
    if cart_id:
        cart = Cart.objects.get(id=cart_id)
        
        if not cart or not cart.items.exists():
            return redirect("cart:cart_detail")
    
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            
            for item in cart.items.all():
                OrderItem.objects.create(
                    order = order,
                    product = item.product,
                    price = item.product.price,
                    quantity = item.quantity
                )
            cart.delete()
            del request.session["cart_id"]
            return redirect("orders:order_confirmation", order.id)
        else:
            form = OrderCreateForm()
            
        return render(request, "orders/order_create.html", {
            "cart":cart, "form":form
        })

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "orders/order_confirmation.html", {"order":order})