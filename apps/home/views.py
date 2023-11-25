from typing import Any
from django import http, views
from django.http.response import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect
from .models import Product, Category
from . import tasks
from django.contrib import messages
from utils import IsAdminUserMixin
from apps.orders.forms import CartAddForm
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import PermissionRequiredMixin


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

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['form'] = CartAddForm()
        return context
    

class BucketHome(IsAdminUserMixin, views.View):
    template_name = "home/bucket.html"

    def get(self, request):
        objects = tasks.all_bucket_objects_task()
        return render(request, self.template_name, {'objects': objects})
    

class DeleteBucketObjectView(PermissionRequiredMixin, IsAdminUserMixin, views.View):
    permission_required = 'accounts.delete_user'

    # def dispatch(self, request, *args: Any, **kwargs: Any) -> HttpResponse:
    #     if not request.user.has_perm('accounts.delete_user'):
    #         raise PermissionDenied()
    #     return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, key):
        tasks.delete_object_task.delay(key)
        messages.info(request, 'Object will delete soon...', 'info')
        return redirect('home:bucket')
    
class DownloadBucketObjectView(IsAdminUserMixin, views.View):
    def get(self, request, key):
        tasks.download_object_task.delay(key)
        messages.info(request, 'Object is downloading...', 'info')
        return redirect('home:bucket')