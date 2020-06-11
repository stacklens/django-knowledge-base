from django.urls import path
from .views import create_student, CreateStudent

app_name = 'transanction_demo'

urlpatterns = [
    path('create/', create_student, name='create'),
    path('createbv/', CreateStudent.as_view(), name='createBV')
]
