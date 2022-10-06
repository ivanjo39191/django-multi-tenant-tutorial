from django.urls import path

from . import views

urlpatterns = [
    path('epaper/', views.EPaperView.as_view(), name='epaper'),
    path('thanks/', views.EPaperThanksView.as_view(), name='thanks'),
]