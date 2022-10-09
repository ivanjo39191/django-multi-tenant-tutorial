from django.urls import path
from django.urls.conf import include

from . import views

urlpatterns = [
    path('form/', views.CustomersFormView.as_view(), name='customers_form'),
]