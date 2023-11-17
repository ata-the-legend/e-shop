from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator


class Order(models.Model):

    user = models.ForeignKey(get_user_model(), verbose_name=_("customer"), on_delete=models.CASCADE, related_name='orders')
    paid = models.BooleanField(_("paid"), default=False)    
    created_at = models.DateTimeField(_("created at"), auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True, auto_now_add=False)
    discount = models.IntegerField(_("discount"), blank=True, null=True, default=None)

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        ordering = ('paid', '-updated_at')

    def __str__(self):
        return f"{self.user} - {self.id}"
    
    def get_total_price(self):
        total = sum(item.get_cost() for item in self.items.all())
        if self.discount:
            discount = int(self.discount / 100 * total)
            total = total - discount
        return total

class OrderItem(models.Model):

    order = models.ForeignKey(Order, verbose_name=_("order"), on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey("home.product", verbose_name=_("product"), on_delete=models.CASCADE)
    price = models.IntegerField(_("price"))
    quantity = models.IntegerField(_("quantity"), default=1)
    

    class Meta:
        verbose_name = _("OrderItem")
        verbose_name_plural = _("OrderItems")

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity


class Coupon(models.Model):

    code = models.CharField(_("code"), max_length=30, unique=True)
    valid_from = models.DateTimeField(_("valid from"))
    valid_to = models.DateTimeField(_("valid to"))
    active = models.BooleanField(_("active"), default=False)
    discount = models.IntegerField(_("discount"), validators=[MinValueValidator(0), MaxValueValidator(90)])
    

    class Meta:
        verbose_name = _("Coupon")
        verbose_name_plural = _("Coupons")

    def __str__(self):
        return self.code

