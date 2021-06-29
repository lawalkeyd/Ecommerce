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
    """
    Custom User Model where email is used as the username field
    """
    USERNAME_FIELD = 'email'
    username = None
    REQUIRED_FIELDS = []
    email = models.EmailField(unique=True) # changes email to unique and blank to false
    wishlist = models.ManyToManyField(Product, blank=True, null=True)
    first_order = models.DateField(default=timezone.now)
    last_order = models.DateField(default=timezone.now)

    def average_order_value(self):
        order_list = [order.total_value() for order in self.orders.all if order.paid]
        return sum(order_list) / len(order_list)

    def first_order_date(self):
        return self.orders.filter(paid = True).first().values_only('created')    

    def last_order_date(self):
        return self.orders.filter(paid = True).last().values_only('created')     

    objects = CustomUserManager()


    def __str__(self):
        return self.email

