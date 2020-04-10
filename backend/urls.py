from django.urls import path
from . import views

urlpatterns = [
    path('get_predictions', views.get_pred, name='get_pred'),
]
