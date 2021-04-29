from django.urls import path
from .views import some_view

app_name = 'mySignal'

urlpatterns = [
    path('', some_view, name='some_view'),
]
