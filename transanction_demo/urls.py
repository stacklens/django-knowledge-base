from django.urls import path
from .views import create_student

app_name = 'transanction_demo'

urlpatterns = [
    path('create/', create_student, name='create')
]
