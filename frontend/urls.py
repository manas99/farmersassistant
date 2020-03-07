from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/get_predictions', views.get_pred, name='get_pred'),
]
