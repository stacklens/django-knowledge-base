from django.dispatch import receiver
from mySignal.signals import view_done


@receiver(view_done, dispatch_uid="my_signal_receiver")
def my_signal_handler(sender, **kwargs):
    print(sender)
    print(kwargs.get('arg_1'), kwargs.get('arg_2'))