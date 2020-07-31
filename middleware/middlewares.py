# Django 1.11 以前的中间件 Mixin
# 以后可能会废弃
from django.utils.deprecation import MiddlewareMixin

from django.http import HttpResponseForbidden
import sys
from django.views.debug import technical_500_response
from datetime import datetime


class ResponseTimer:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request._request_time = datetime.now()
        response = self.get_response(request)
        return response

    def process_template_response(self, request, response):
        response_time = request._request_time - datetime.now()
        response.context_data['response_time'] = abs(response_time)
        return response


class NormalUserBlock:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (request.user.is_superuser != True) and (request.path == '/middleware/'):
            return HttpResponseForbidden('<h3>超级用户方可访问此页面！</h3>')

        response = self.get_response(request)

        return response


class DebugOnlySuperUser:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if request.user.is_superuser:
            return technical_500_response(request, *sys.exc_info())


class Md1:
    def __init__(self, get_response):
        self.get_response = get_response
        # (0) 在这里进行某些自定义参数的初始化

    def __call__(self, request):
        # (1) 这里写实际视图执行之前的逻辑
        print('Md1 视图执行前..')

        # (2) response 是下一个中间件或视图函数的返回值
        response = self.get_response(request)

        # (3) 这里写实际视图执行之后的逻辑
        print('Md1 视图执行后..')

        return response


class Md2:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print('Md2 视图执行前..')

        # if True:
        #     print('Md2 引发短路')
        #     return HttpResponse('Md2 引发短路')

        response = self.get_response(request)

        print('Md2 视图执行后..')

        return response


class Md3:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print('Md3 视图执行前..')

        response = self.get_response(request)

        print('Md3 视图执行后..')

        return response
