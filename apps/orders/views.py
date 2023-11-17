from django.shortcuts import render, get_object_or_404, redirect
from django import views
from .cart import Cart
from .forms import CartAddForm
from apps.home.models import Product

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

