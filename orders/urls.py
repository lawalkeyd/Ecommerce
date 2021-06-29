from django.urls import path
from . import views


urlpatterns = [
    path('', views.ViewOrder.as_view(), name='customer_orders'),
    path('add_item/', views.addOrder.as_view(), name='add_order'),
    path('delte_item/', views.RemoveOrder.as_view(), name='add_order'),
]
