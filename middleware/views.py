from django.shortcuts import render
from django.http import HttpResponse
from django.template.response import TemplateResponse

# Create your views here.

def mid_test(request):
    print('--- 视图执行中...')
    # raise None
    # return HttpResponse('中间件测试..')
    return TemplateResponse(request, 'midware_demo.html', context={})

