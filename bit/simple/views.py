from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Product
from .serializers import ProductSerializer, UserSerializer, RegisterSerializer
from rest_framework import generics, permissions
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
    """Generic View to create and view all products """
    queryset = Product.objects.all().order_by("price") # get all products ordered by price
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # limit access to authorized users
    serializer_class = ProductSerializer # add queryset to a serializer


class RegisterAPI(generics.GenericAPIView):
    """ Generic view to register a new user"""
    serializer_class = RegisterSerializer 
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
     
        })

def login_view(request):
    """GET -> view login page , Post -> send required data to login"""
    if request.method == "POST": 
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request=request, 
        username=username, password=password) # check user credentials
        if user is not None: # if found a user with right data
            login(request, user) # login to the system
            return HttpResponseRedirect(reverse("products")) # redirect to product route
        return render(request, "login.html", {"message":"invalid inputs"}) 
    if not request.user.is_authenticated: # ask for data if not registered user
        return render(request, "login.html")
    return HttpResponseRedirect(reverse("products")) # in case of already logged user directed to login page


def logout_view(request):
    logout(request)
    return render(request, "login.html", {"message":"logged out"})


@api_view(['GET'])
def get_products(request, user_id:int):
    products = Product.objects.filter(seller=user_id).order_by('price') # filter products with the seller and order them by price
    serializer = ProductSerializer(products, many=True) # serialize the data and return it
    return Response(serializer.data)