from .models import Student, Info, Address
from django.http import HttpResponse
from django.views import View

from django.db import transaction


class CreateStudent(View):
    @transaction.atomic
    def get(self, request):
        student = Student.objects.create(name='张三')

        info = Info.objects.create(age=19)
        # 引发错误
        oh_my_god = int('abc')
        address = Address.objects.create(home='北京')

        return HttpResponse('Create success...')


@transaction.atomic
def create_student(request):
    student = Student.objects.create(name='张三')
    info = Info.objects.create(age=19)
    oh_my_god = int('abc')
    address = Address.objects.create(home='北京')

    return HttpResponse('Create success...')

# @transaction.atomic
# def create_student(request):
#     student = Student.objects.create(name='张三')
#
#     # 回滚保存点
#     save_tag = transaction.savepoint()
#
#     try:
#         info = Info.objects.create(age=19)
#         # 引发错误
#         oh_my_god = int('abc')
#         address = Address.objects.create(home='北京')
#     except:
#         # 回滚到 save_tag 的位置
#         transaction.savepoint_rollback(save_tag)
#
#     return HttpResponse('Create success...')


# def create_student(request):
#     student = Student.objects.create(name='张三')
#
#     with transaction.atomic:
#         info = Info.objects.create(age=19)
#         # 引发错误
#         oh_my_god = int('abc')
#         address = Address.objects.create(home='北京')
#
#     return HttpResponse('Create success...')

# @transaction.non_atomic_requests
# def create_student(request):
#     student = Student.objects.create(name='张三')
#
#     info = Info.objects.create(age=19)
#     # 引发错误
#     oh_my_god = int('abc')
#     address = Address.objects.create(home='北京')
#
#     return HttpResponse('Create success...')
