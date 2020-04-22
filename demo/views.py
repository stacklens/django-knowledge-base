from django.shortcuts import render
from django.views.generic import View
from django.urls import reverse
from django.shortcuts import redirect

from .models import Post


# MARK: - reverse()

# 首页view
class HomePageView(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'home.html', context={'posts': posts})


# 重定向view
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


# 被重定向view
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


# MARK: - redirect()

# 跳转view
class RedirectView(View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        post = Post.objects.get(id=id)

        flag = id % 3
        if flag == 1:
            print('byModel')
            return redirect(post)
        elif flag == 2:
            print('byView')
            return redirect('demo:redirect_view', id=id)
        else:
            print('byURL')
            return redirect('/demo/post-detail/{}/'.format(post.id))


# model 跳转
class PostDetailView(View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        post = Post.objects.get(id=id)
        return render(request, 'post_detail.html', context={'post': post})


# view_name 跳转
def redirect_view(request, id):
    post = Post.objects.get(id=id)
    return render(request, 'post_detail.html', context={'post': post})
