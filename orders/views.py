from orders.serializers import OrderItemSerializer
from rest_framework.permissions import IsAuthenticated
from .models import OrderItem, Order
from products.models import Product
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from decimal import InvalidOperation


class ViewOrder(APIView):
    '''
    View to list User's order
    '''
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        order = Order.objects.get(customer=request.user, paid=False)
        serial = OrderItemSerializer(order.items.all(), many=True)
        return Response({"items": serial.data})

class addOrder(APIView):
    '''
    View to add Order Items
    '''
    permission_classes = [IsAuthenticated]    
    def post(self, request):
        id = request.data.get('id')
        quantity = request.data.get('quantity')
        item = get_object_or_404(Product, id=id)
        if item.inventory < 1:
            return Response({"error": "This item is not currently available"})
        try:
            order, createn = Order.objects.get_or_create(customer=request.user, paid=False)
            order_item, created = OrderItem.objects.get_or_create(
                product=item,
                order=order,
            )
            if not created:
                # check if the order item is in the order
                order_item.quantity += quantity
                order_item.save()
            else:
                order_item.quantity = quantity    
            order.updated = timezone.now()
            serial = OrderItemSerializer(order.items.all(), many=True)
            return Response({"item": serial.data})    
        except (ValueError, InvalidOperation):
            return Response({"error": "You have a maximum order value of a $1000"})


class RemoveOrder(APIView):
    '''
    View to remove Order Items
    '''
    permission_classes = [IsAuthenticated]    
    def post(self, request):
        id = request.data.get('id')
        order_item= get_object_or_404(OrderItem, id=id)
        order_item.delete()
        return Response({"deleted": True})                
  
        