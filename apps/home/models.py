from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

class Category(models.Model):
    name = models.CharField(_("name"), max_length=200)
    slug = models.SlugField(_("slug"), unique=True)

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.name

class Product(models.Model):
    
    category = models.ForeignKey(Category, verbose_name=_("category"), on_delete=models.CASCADE, related_name='products')
    name = models.CharField(_("name"), max_length=200)
    description = models.TextField(_("description"))
    image = models.ImageField(_("image"), upload_to='products/%Y/%m/%d')
    available = models.BooleanField(_("is available"), default=True)
    slug = models.SlugField(_("slug"), unique=True)
    price = models.IntegerField(_("price"))
    created_at = models.DateField(_("created at"), auto_now=False, auto_now_add=True)
    updated_at = models.DateField(_("updated at"), auto_now=True, auto_now_add=False)

    
    class Meta:
        ordering = ('name',)
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("home:product_detail", kwargs={"slug": self.slug})

