from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

class Category(models.Model):
    parent = models.ForeignKey(
        "self", 
        verbose_name=_("Parent"), 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True,
        related_name='sub_category'
    )
    name = models.CharField(_("name"), max_length=200)
    slug = models.SlugField(_("slug"), unique=True)

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("home:category_filter", kwargs={"category": self.slug})

class Product(models.Model):
    
    category = models.ManyToManyField(Category, verbose_name=_("category"), related_name='products')
    name = models.CharField(_("name"), max_length=200)
    description = models.TextField(_("description"))
    image = models.ImageField(_("image"))#, upload_to='products-%Y-%m-%d')
    available = models.BooleanField(_("is available"), default=True)
    slug = models.SlugField(_("slug"), unique=True)
    price = models.IntegerField(_("price"))
    created_at = models.DateField(_("created at"), auto_now=False, auto_now_add=True)
    updated_at = models.DateField(_("updated at"), auto_now=True, auto_now_add=False)
    comment = GenericRelation('Comment')

    
    class Meta:
        ordering = ('name',)
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("home:product_detail", kwargs={"slug": self.slug})


class Comment(models.Model):
    user = models.ForeignKey(get_user_model(), verbose_name=_("user"), on_delete=models.CASCADE)
    body = models.TextField(_("body"))
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return self.user.email

    def get_absolute_url(self):
        return reverse("Comment_detail", kwargs={"pk": self.pk})
