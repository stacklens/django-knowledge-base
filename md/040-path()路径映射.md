网站地址是由**统一资源定位符**表示的，也是就我们常说的 `url`。`Django` 中有非常强大的 `path()` 方法，可以动态构造出你想要的各种不同形态的 `url` 。

基本写法如下：

```python
from django.urls import path

urlpatterns = [
    # 固定地址
    path('articles/2003/', ...),
    # 可传入 int 参数
    path('articles/<int:year>/', ...),
    # 可传入 int、str 等多个参数
    path('articles/<int:year>/<str:title>/', ...),
]
```

可以看出 `path()` 中是可以传入动态参数的，比如上面的第三个 `path()` 可以匹配下面的 `url`：

```python
'/articles/2020/awesome/'
```

并且这些参数可以在**视图**中取得：

```python
def some_view(request, year, title):
    date = year
    name = title
    ...
```

你可以给这些参数指定默认值：

```python
def some_view(request, year=2020, title='Django'):
    ...
```

但是需要注意的是，`GET` 请求中**附带的参数**是不能够直接通过**视图函数的参数**取得的，比如下面这个地址：

```python
'/articles/2020/awesome/?month=4&day=22'
```

问号后面的参数不能作为**视图函数**的参数，否则你会得到无情的报错。

获取它们的方法是这样：

```python
def some_view(request, ...):
    ...
    # month = 4
    month = request.GET.get('month')
    # day = 22
    day = request.GET.get('day')
    ...
```

接下来就可以愉快的使用了，很简单吧。

最后总结一下，`path()` 能接受的参数一共有**四种**：

- `str` ：匹配除路径分隔符 `'/'` 之外的非空字符串。
- `int` ：匹配零或正整数。
- `slug` ：匹配由ASCII字母、数字、连字符、下划线字符组成的字符串。例如， `building-your-1st-django-site`。
- `uuid` ：匹配格式化的UUID，如 `075194d3-6885-417e-a8a8-6c931e272f00` 。

合理运用吧。