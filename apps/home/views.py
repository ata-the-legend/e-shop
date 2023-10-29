from django import views
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect
from .models import Product
from . import tasks
from django.contrib import messages


class HomeView(ListView):
    model = Product
    queryset = Product.objects.filter(available=True)
    template_name = "home/home.html"

class ProductDetailView(DetailView):
    model = Product
    template_name = "home/detail.html"
    

class BucketHome(views.View):
    template_name = "home/bucket.html"

    def get(self, request):
        objects = tasks.all_bucket_objects_task()
        return render(request, self.template_name, {'objects': objects})
    

class DeleteBucketObjectView(views.View):
    def get(self, request, key):
        tasks.delete_object_task.delay(key)
        messages.info(request, 'Object will delete soon...', 'info')
        return redirect('home:bucket')