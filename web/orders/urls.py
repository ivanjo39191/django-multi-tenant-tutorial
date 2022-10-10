from django.urls import path

from . import views

urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cart'),
    path('addcart/<int:product_id>/', views.AddCartView.as_view(), name='add_cart'),
    path('deletecart/<int:product_id>/', views.DeleteCartView.as_view(), name='delete_cart'),
]