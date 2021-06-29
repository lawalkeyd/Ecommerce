from django.db import models
from django.db.models.query import ModelIterable

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=80, verbose_name='Product Category')


    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(verbose_name='Product Name', max_length=140)
    price = models.DecimalField(verbose_name='Product Price', max_digits=5, decimal_places=2)
    product_category = models.ManyToManyField(Category, null=True)
    inventory = models.PositiveIntegerField(verbose_name='Product Inventory')

    def __str__(self):
        return self.name
