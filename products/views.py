from rest_framework import generics
from .serializers import ProductSerializer, AdminProductSerializer
from .models import Product
from rest_framework import filters
from rest_framework.permissions import IsAdminUser


# Create your views here.
class ViewProduct(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    model  = Product

class ProductList(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()  
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'price', 'product_category__name']  

class AdminCreateProduct(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = AdminProductSerializer
    queryset = Product.objects.all()     

class AdminManageProduct(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]    
    queryset = Product.objects.all()
    serializer_class = AdminProductSerializer    

