浏览器和 Django 服务之间的通信采用 HTTP 协议，该协议是无状态的。也就是说，即使是同一个浏览器的请求也是完全独立的，服务器并不知道两次请求是否来自同一个用户。

会话（Session）就是来解决这类问题的。Session 为每个浏览器存储任意数据，并在浏览器连接时，将该数据提供给站点。Session 依赖 Cookie ，但 Cookie 中仅保存一个识别值，真正的数据是保存在数据库中的。

Django 在创建时默认开启了 Session 功能：

```python
# settings.py

INSTALLED_APPS = [
    ...
    'django.contrib.sessions',
    ...
]

MIDDLEWARE = [
    ...
    'django.contrib.sessions.middleware.SessionMiddleware',
    ...
]
```

操作起来也很友好，跟 Python 的字典有点类似。

比如利用 Session 记录匿名用户的登录次数。写视图函数：

```python
# views.py

def session_visits_count(request):
    # 获取 visits_count 数据，若不存在则设置为 0
    count = request.session.get('visits_count', 0)
    count += 1
    # 保存 visits_count 进 session
    request.session['visits_count'] = count
    return  render(request, 'visits_count.html', context={'count': count })
```

路由：

```python
# urls.py

...
urlpatterns = [
    path('visits-count/', session_visits_count, name='visits_count'),
]
```

模板：

```html
# visits_count.html

...
{% block content %}
    <h4 class="col mt-4">
        您已经访问本页面：{{ count }} 次.
    </h4>
{% endblock %}
```

Session 的默认保存时间为 2 周，如果你想手动删除也可以：

```python
del request.session['xxx']
```

通常情况下对 session 的修改会自动保存。但如果你存的是某种嵌套结构（比如字典），那么需要手动保存：

```python
def some_view(request):
    ...
    # session 保存字典数据
    if request.session.get('deeper_count'):
        num = request.session['deeper_count']['num']
        # 此时 session 并未更新，因为更新的仅仅是字典中的数据
        request.session['deeper_count']['num'] = num + 1
        # 通知会话已修改
        request.session.modified = True
    else:
        num = 1
        request.session['deeper_count'] = {'num': num}
    return  ...
```

> 关联文档：[How to use sessions](https://docs.djangoproject.com/en/3.0/topics/http/sessions/)