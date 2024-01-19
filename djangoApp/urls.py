from django.urls import path
from . import views


app_name = 'djangoApp'

urlpatterns = [
    path('', views.index, name='index'),
]


