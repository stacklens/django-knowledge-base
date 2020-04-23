from django.shortcuts import render
from django.views.generic import View
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404

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


# MARK: - redirect() && get_object_or_404()

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

        # post = Post.objects.get(id=id)
        post = get_object_or_404(Post, id=id)

        (post, owner) = detail_setup_helper(post)

        return render(request, 'post_detail.html', context={'post': post, 'owner': owner})


# view_name 跳转
def redirect_view(request, id):
    # post = Post.objects.get(id=id)
    queryset = Post.objects.filter(title__startswith='V')
    post = get_object_or_404(queryset, id=id)

    post, owner = detail_setup_helper(post)

    return render(request, 'post_detail.html', context={'post': post, 'owner': owner})


# MARK: - path()
def path_demo_view(request, count, salute):
    count = count
    salute = salute
    first_name = request.GET.get('first_name')
    last_name = request.GET.get('last_name')
    return render(request,
                  'path.html',
                  context={
                      'count': count,
                      'salute': salute,
                      'first_name': first_name,
                      'last_name': last_name}
                  )


def detail_setup_helper(obj):
    # MARK: - update()
    obj.increase_view()
    # 刷新数据
    obj.refresh_from_db()

    return obj, obj.owner.get_owner()
