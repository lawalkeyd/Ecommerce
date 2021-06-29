from rest_framework import generics, status
from rest_framework.views import APIView
from .serializers import UserSerializer, ViewCustomersSerializer
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from .models import CustomUser


class RegisterCustomer(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer


class LoginView(APIView):
    permission_classes = ()
    def post(self, request,):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return Response({"token": user.auth_token.key})
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)

class ViewCustomerView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = ViewCustomersSerializer