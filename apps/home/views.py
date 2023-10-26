from django import views
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render
from .models import Product
from .tasks import all_bucket_objects_task


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
        objects = all_bucket_objects_task()
        return render(request, self.template_name, {'objects': objects})