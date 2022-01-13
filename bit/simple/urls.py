from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path("", views.index, name="index"), # go to products if logged in
    path("products", views.ProductList.as_view(), name="products"), # GET ALL PRODUCTS AND if logged in -> ADD NEW ONE
    path("products/<int:user_id>", views.get_products, name="get_product"), # RETRIVE PRODUCT BY USER ID
    path("register", views.RegisterAPI.as_view(), name="register"), # register new user
    path("login", views.login_view, name="login"), # login 
    path("logout", views.logout_view, name="logout") # logout
    
]