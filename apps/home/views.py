from django import views
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect
from .models import Product, Category
from . import tasks
from django.contrib import messages
from utils import IsAdminUserMixin


class HomeView(views.View):
    template_name = "home/home.html"

    def get(self, request, category=None):
        products = Product.objects.filter(available=True)
        categories = Category.objects.filter(parent=None)
        if category:
            products = products.filter(category__slug= category)
        return render(request, self.template_name, {'products': products, 'categories': categories})

class ProductDetailView(DetailView):
    model = Product
    template_name = "home/detail.html"
    

class BucketHome(IsAdminUserMixin, views.View):
    template_name = "home/bucket.html"

    def get(self, request):
        objects = tasks.all_bucket_objects_task()
        return render(request, self.template_name, {'objects': objects})
    

class DeleteBucketObjectView(IsAdminUserMixin, views.View):
    def get(self, request, key):
        tasks.delete_object_task.delay(key)
        messages.info(request, 'Object will delete soon...', 'info')
        return redirect('home:bucket')
    
class DownloadBucketObjectView(IsAdminUserMixin, views.View):
    def get(self, request, key):
        tasks.download_object_task.delay(key)
        messages.info(request, 'Object is downloading...', 'info')
        return redirect('home:bucket')