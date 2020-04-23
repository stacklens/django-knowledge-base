从模型中取出某个特定内容，最简单的方式就是用模型管理器的 `get()` 方法了：

```python
obj = SomeModel.objects.get(id=1)
```

像上面的代码，如果数据库中没有 `id=1` 的数据条目时，`Django` 会抛出 `Error 500` 错误。但问题是大部分时候，没有相关条目仅仅是因为**资源不存在**，应该抛出万恶的 `Error 404` 才对。

因此就有了 `get_object_or_404()` ：

```python
obj = get_object_or_404(SomeModel, id=1)
```

它其实就是下面这种写法的快捷方式：

```python
try:
    obj = SomeModel.objects.get(id=1)
except SomeModel.DoesNotExist:
    raise Http404("No SomeModel matches the given query.")
```

除了上面这种最常用的写法， `get_object_or_404()` 还可以接受 `queryset` 作为第一个参数：

```python
queryset = Post.objects.filter(title__startswith='V')
post = get_object_or_404(queryset, id=id)
```

当你需要把查询集反复筛选、传递时，这种写法还是很有用的。

最后还要注意， `get_object_or_404()` 和 `get()` 一样，只能返回单个结果，否则服务器将抛出错误。

> `get_object_or_404()` 还可以接受管理器作为参数，有兴趣请去官方文档了解。

那要是我想获取多个结果呢？请用`get_list_or_404()`：

```python
objs = get_list_or_404(SomeModel, isMale=True)
```

它类似于如下代码：

```python
objs = list(SomeModel.objects.filter(isMale=True))
if not objs:
    raise Http404("No SomeModel matches the given query.")
```

用之前别忘了导入它们：

```python
from django.shortcuts import get_object_or_404
from django.shortcuts import get_list_or_404
```

