from django.urls import path
from . import views

app_name = 'djangoApp'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/filter', views.request_table, name='api_table_full'),
    path('api/default', views.default_table, name='api_default')
]
