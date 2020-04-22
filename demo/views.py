from django.shortcuts import render
from django.views.generic import View
from django.urls import reverse
from django.shortcuts import redirect

from .models import Post

# MARK: - reverse()
# MARK: - redirect()

class HomePageView(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'home.html', context={'posts': posts})


class ReverseView(View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')

        if id == None:
            # 不带参数
            url = reverse('demo:home_with_context')
        else:
            # 带有参数
            url = reverse('demo:home_with_context', args=(id,))
        return redirect(url)


class HomePageWithContextView(View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')

        if id == 0:
            context = {'content': '我从 Url 模板语法解析回来，并带有参数 id - {} 哦'.format(id)}
        elif id == 1:
            context = {'content': '我从 Reverse() 回来，并带有参数 id - {} 哦'.format(id)}
        else:
            context = {'content': '我从 Reverse() 回来'}

        posts = Post.objects.all()
        context.update({'posts': posts})
        return render(request, 'home.html', context=context)
