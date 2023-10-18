from django import views
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render
from .models import Product


class HomeView(ListView):
    model = Product
    queryset = Product.objects.filter(available=True)
    template_name = "home/home.html"

class ProductDetailView(DetailView):
    model = Product
    template_name = "home/detail.html"
    

