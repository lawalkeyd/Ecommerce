from accounts.models import CustomUser
from django.db import models
from django.conf import settings
from products.models import Product


# Create your models here.

class Order(models.Model):
    customer = models.ForeignKey(
       CustomUser,
        on_delete=models.CASCADE,
        related_name='orders', null=True, blank=True
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    total_value = models.DecimalField(max_digits=5, decimal_places=2, default=0, blank=True)


    def set_total_value(self):
        self.total_value = sum([item.get_cost() for item in self.items.all()])
        self.save()

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    order_info = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.product.price * self.quantity

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(OrderItem, self).save()
        self.order.set_total_value()