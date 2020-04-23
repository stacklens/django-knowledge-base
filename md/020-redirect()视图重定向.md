上一节我们已经领教到 `redirect()` 和 `reverse()` 配合使用的强大威力了。

但 `redirect()` 的能力并不止于此。它可以接受 3 中不同的参数：

### Model 作为参数

`redirect()` 可以接收模型作为第一个参数，像这样：

```python
def redirect_view(request, id):
    ...
    obj = SomeModel.objects.get(id=id)
    return redirect(obj)
```

此时 `redirect()` 会调用**模型**实例中的 `get_absolute_url()` 方法，所以你必须在模型中加上它：

```python
class SomeModel(...)
    ...
    def get_absolute_url(self):
        return reverse('some_url', args=(self.id,))
```

> `reverse()` 的用法上一节讲过了。

**路由**部分的写法像这样：

```python
...
path('...', redirect_view, name='...'),
path('...', destination_view, name='some_url')
```

所以当你请求 `redirect_view()` 时，`redirect()` 就帮你跳转到 `destination_view()` 视图中去了。

### View 作为参数

如果你在 `url` 中有如下需要跳转的地址：

```python
path('...', another_view, name='another_url'),
```

你还可以通过**视图的命名**作为参数：

```python
return redirect('another_url', id=id)
```

依然可以用关键字参数传递变量到被跳转的视图中。

> 在 `reverse()` 的章节中我们是这样写的：`return redirect(reverse('foo_name'))`。两种写法本质上是一样的，路由都是由 `reverse()` 解析的，只不过 `Django` 隐式帮你处理了。

### URL 作为参数

第三种方式就更加粗暴了，把 `url` 字符串作为参数：

```python
return redirect('/your_url/{}/'.format(post.id))
```

参数也可以通过字符串格式化传递进去，不过这种方式属于硬编码，还是少用为好。

导入路径在这里：

```python
from django.urls import reverse
from django.shortcuts import redirect
```

