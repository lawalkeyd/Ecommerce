from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.LoginView.as_view(), name='create_order'),
    path('register/', views.RegisterCustomer.as_view(), name='list_order'),
]
