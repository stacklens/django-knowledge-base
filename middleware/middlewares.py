# Django 1.11 以前的中间件 Mixin
# 以后可能会废弃
from django.utils.deprecation import MiddlewareMixin


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

        response = self.get_response(request)

        print('Md2 视图执行后..')

        return response