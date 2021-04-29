from django.http.response import HttpResponse
from django.core.signals import request_finished, request_started
from django.dispatch import receiver

# @receiver([request_finished, request_started])
# def signal_callback(sender, **kwargs):
#     print('信号已接收..')
#
#
# @receiver(request_finished)
# def signal_callback_2(sender, **kwargs):
#     print('信号已接收2..')

from mySignal.signals import view_done


def some_view(request):

    view_done.send(
        sender='View function...',
        arg_1='My signal...',
        arg_2='received...'
    )

    return HttpResponse('响应完毕..')
