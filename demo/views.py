from django.shortcuts import render
from django.views.generic import View
from django.urls import reverse
from django.shortcuts import redirect

# MARK: - Reverse()
class HomePageView(View):
    def get(self, request):
        return render(request, 'home.html', context={})


class ReverseToSomePageView(View):
    def get(self, request):
        url = reverse('demo:home_with_context')
        return redirect(url)


class HomePageWithContextView(View):
    def get(self, request):
        context = {'content': '我从 Reverse() 回来'}
        return render(request, 'home.html', context=context)


class HomePageWithContextAndParamsView(View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        if id == 0:
            context = {'content': '我从 Url 模板语法解析回来，并带有参数 id - {} 哦'.format(id)}
        else:
            context = {'content': '我从 Reverse() 回来，并带有参数 id - {} 哦'.format(id)}

        return render(request, 'home.html', context=context)
