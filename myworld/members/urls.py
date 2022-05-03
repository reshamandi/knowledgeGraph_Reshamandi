from django.urls import path
from . import views

# subrouting for particular path of an application
urlpatterns = [
    path('', views.index, name='index'),
]