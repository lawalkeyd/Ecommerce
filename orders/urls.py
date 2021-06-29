from django.urls import path
from . import views


urlpatterns = [
    path('', views.ViewOrder.as_view(), name='customer_orders'),
    path('add_item/', views.addOrder.as_view(), name='add_order'),
    path('add_wish/', views.addWishlist.as_view(), name='add_wish'),
    path('remove_wish/', views.RemoveWishlist.as_view(), name='remove_wish'),
    path('delete_item/', views.RemoveOrder.as_view(), name='delete_order'),
]
