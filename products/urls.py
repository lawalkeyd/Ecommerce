from django.urls import path
from . import views


urlpatterns = [
    path('', views.ProductList.as_view(), name='create_order'),
    path('<pk>', views.ViewProduct.as_view(), name='list_order'),
    path('admin/', views.AdminCreateProduct.as_view()),
    path('admin/<int:pk>/', views.AdminManageProduct.as_view()),    
]
