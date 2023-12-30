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
from .forms import SearchForm
from .documents import ProductDocument
from elasticsearch_dsl import MultiSearch
from django_elasticsearch_dsl.search import Search


class HomeView(views.View):
    template_name = "home/home.html"
    form_class = SearchForm

    def get(self, request, category=None):
        products = Product.objects.filter(available=True)
        categories = Category.objects.filter(parent=None)
        if category:
            products = products.filter(category__slug= category)
        return render(request, self.template_name, {'products': products, 'categories': categories})
    

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            search_results = ProductDocument.search().query(
                "multi_match", 
                query=cd['search'], 
                fields=['name', 'description', 'category.name']
            )
            response = search_results.execute()
            product_ids = [hit.meta.id for hit in response.hits]
            products = Product.objects.filter(available=True, id__in=product_ids)
            categories = Category.objects.filter(parent=None)
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
    

class SearchView(views.View):
    form_class = SearchForm
    template_name = 'home/search.html'

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            search_results = ProductDocument.search().query(
                "multi_match", 
                query=cd['search'], 
                fields=['name', 'description', 'category.name']
            )
            return render(request, self.template_name, {'search_results': search_results})