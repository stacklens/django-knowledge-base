路由中的 `include()` 方法非常的常用。它的作用是把 `url` 的剩余部分发配到另一个 `URLconfs` 处理，以免单个路由文件过于庞大和凌乱。

通常我们在**根路由**中使用它：

```python
# root/urls.py

from django.urls import path, include

path('post/', include('post.urls', namespace='post')),
```

后端在匹配到 `post/` 后，继续在 `post` 模块的 `urls.py` 中处理剩下的部分：

```python
# post/urls.py
...

path('john/', some_view, name='user')
```

它两配合起来就可以匹配类似这样的地址：

```python
'/post/john/'
```

另外，你可能注意到了参数 `namespace`  （应用程序命名空间）和 `name`  （实例命名空间）这两兄弟了，他们是地址反向解析用的，比如在**模板**中：

```html
{% url 'post:user' %}
```

或者在**视图**中：

```python
reverse('post:user')
```

这样多级命名的好处是你可以在不同的 app 中重复的命名，它们是互不影响的。

