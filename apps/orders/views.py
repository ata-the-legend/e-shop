from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django import views
from .cart import Cart
from .forms import CartAddForm
from apps.home.models import Product
from .models import Order, OrderItem
from django.contrib import messages

class CartView(views.View):
    template_name = 'orders/cart.html'

    def get(self, request):
        cart = Cart(request)
        return render(request, self.template_name, {'cart': cart})


class CartAddView(views.View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id) 
        form = CartAddForm(request.POST)
        if form.is_valid():
            cart.add(product, form.cleaned_data['quantity'])
        return redirect("orders:cart")
    
class CartRemoveView(views.View):
    def get(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id= product_id)
        cart.remove(product)
        return redirect("orders:cart")

class OrderCreateView(LoginRequiredMixin, views.View):
    def get(self, request):
        cart = Cart(request)
        if not cart:
            messages.info(request, 'Cart is empty', 'info')
            return redirect("orders:cart",)
        order = Order.objects.create(user= request.user,)
        for item in cart:
            OrderItem.objects.create(
                order = order,
                product = item['product'],
                price = item['price'],
                quantity = item['quantity']
            )
        cart.clear()
        return redirect("orders:order_detail", order.id)

class OrderDetailView(LoginRequiredMixin, views.View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id= order_id)
        if request.user == order.user:
            return render(request, 'orders/order.html', {'order': order})
        messages.warning(request, 'Permission denied', 'danger')
        return redirect('orders:cart')