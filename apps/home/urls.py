from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'home'
urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("bucket/", views.BucketHome.as_view(), name="bucket"),
    path("<slug:slug>/", views.ProductDetailView.as_view(), name="product_detail"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)