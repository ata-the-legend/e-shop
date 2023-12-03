from django.contrib import admin
from .models import Product, Category, Comment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    raw_id_fields = ('category',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user','content_object')