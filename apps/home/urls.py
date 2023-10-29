from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'home'

bucket_urls = [
    path("", views.BucketHome.as_view(), name="bucket"),
    path("download_obj/<str:key>", views.DownloadBucketObjectView.as_view(), name="download_obj_bucket"),
    path("delete_obj/<str:key>", views.DeleteBucketObjectView.as_view(), name="delete_obj_bucket"),
]

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("bucket/", include(bucket_urls)),
    path("<slug:slug>/", views.ProductDetailView.as_view(), name="product_detail"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)