from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model


class Order(models.Model):

    user = models.ForeignKey(get_user_model(), verbose_name=_("customer"), on_delete=models.CASCADE, related_name='orders')
    paid = models.BooleanField(_("paid"), default=False)    
    created_at = models.DateTimeField(_("created at"), auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        ordering = ('paid', '-updated_at')

    def __str__(self):
        return f"{self.user} - {self.id}"
    
    def get_total_price(self):
        return sum(item.get_cost() for item in self.items.all())

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
