from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def mid_test(request):
    print('--- 视图执行中...')
    return HttpResponse('中间件测试..')
