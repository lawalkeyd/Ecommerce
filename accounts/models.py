from typing import Text
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
from products.models import Product
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    USERNAME_FIELD = 'email'
    username = None
    email = models.EmailField(unique=True) # changes email to unique and blank to false
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class CustomerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=45)
    wishlist = models.ManyToManyField(Product, blank=True)
    first_order = models.DateField(default=timezone.now)
    last_order = models.DateField(default=timezone.now)

    def average_order_value(self):
        order_list = [order.get_total_cost() for order in self.orders.all if order.paid]
        return sum(order_list) / len(order_list)

    def get_first_order(self):
        return self.orders.filter(paid = False).first().values_only('created')    

    def get_last_order(self):
        return self.orders.filter(paid = False).last().values_only('created')   

    def __str__(self):
        return self.name