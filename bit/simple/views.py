from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from .models import Product, User
from .serializers import ProductSerializer, UserSerializer, RegisterSerializer
from rest_framework import generics
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.decorators import api_view
# Create your views here.


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return HttpResponseRedirect(reverse("products"))


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all().order_by("price")
    serializer_class = ProductSerializer


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
     
        })

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request=request, 
        username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("products"))
        return render(request, "login.html", {"message":"invalid inputs"})
    # return HttpResponse("POST  your credientials in JSON FORMAT to url '/login'", 200)
    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return render(request, "login.html", {"message":"logged out"})


@api_view(['GET'])
def get_products(request, user_id:int):
    products = Product.objects.filter(seller=user_id).order_by('price')
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)