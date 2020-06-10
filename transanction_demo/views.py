from .models import Student, Info, Address
from django.http import HttpResponse
from django.db import transaction

@transaction.atomic
def create_student(request):
    student = Student.objects.create(name='张三')

    save_tag = transaction.savepoint()

    try:
        info = Info.objects.create(age=19)

        oh_my_god = int('abc')

        address = Address.objects.create(home='北京')
    except:
        transaction.savepoint_rollback(save_tag)

    return HttpResponse('Create success...')
