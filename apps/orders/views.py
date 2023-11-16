from django.shortcuts import render
from django import views

class CartView(views.View):
    template_name = 'orders/cart.html'

    def get(self, request):
        return render(request, self.template_name,)
