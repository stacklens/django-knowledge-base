**中间件**是 Django 处理请求和响应的**钩子框架**。它是一个轻量级的、低层级的“插件”系统，用于**全局**改变 Django 的输入或输出。如果你需要在响应所有请求时插入一个自定义功能、参数的时候特别有用。

### 自定义中间件

假设你有一个叫 `middleware` 的 app 。在 app 中创建文件 `middlewares.py`，一会儿在这里面自定义中间件。

来看一下 Django 官方推荐的中间件写法是什么样子的：

```python
# middleware/middlewares.py

class Md1:
    def __init__(self, get_response):
        self.get_response = get_response
        # (0) 在这里进行某些自定义参数的初始化。初始化只执行一次。

    def __call__(self, request):

        # (1) 这里写实际视图执行之前的逻辑
        print('Md1 视图执行前..')

        # (2) response 是下一个中间件或视图函数的返回值
        response = self.get_response(request)

        # (3) 这里写实际视图执行之后的逻辑
        print('Md1 视图执行后..')

        return response
```

这个类 `Md1` 就是一个最简单的中间件了，它最核心的部分就是实现了 `__call__` 方法，使得类变成可调用对象：

-  方法里的 `request` 就是视图函数中传入的那个 `request` 。
- `get_response` 也是一个可调用对象，可以是下一个中间件，也可以是实际的视图函数。`request` 通过它传递到下一级，也就是说 `get_response` 到达的最底层就是视图函数了。
- 因此，**序号(1)** 则是**请求到达视图前**需要自定义的逻辑，**序号(2)** 是**请求从视图出来后**需要自定义的逻辑。

来实际测试一下。

首先注册 app 和中间件：

```python
# your_project/settings.py

INSTALLED_APPS = [
    ...
    'middleware',
]

MIDDLEWARE = [
    # 这里是 Django 默认注册的中间件
    ...

    # 刚才自定义的中间件，注册规则：'appName.fileName.className'
    'middleware.middlewares.Md1',
]
```

在 app 中编写测试视图：

```python
# middleware/views.py

from django.http import HttpResponse

def mid_test(request):
    print('Md1 视图执行中...')
    return HttpResponse('中间件测试..')
```

最后在项目根 `urls.py` 中添加路由：

```python
# your_project/urls.py

...

from middleware.views import mid_test

urlpatterns = [
    ...
    path('middleware/',mid_test),
]
```

访问此路由，命令行打印结果如下：

```python
Md1 视图执行前..
--- 视图执行中...
Md1 视图执行后..
```

不仅视图 `mid_test`，项目中所有的请求都会执行中间件的代码，也就是说是**影响全局**的。

### 执行顺序

Django 收到请求后，会根据配置文件中 `MIDDLEWARE` 列表挨个执行中间件，所以列表里中间件的**顺序就很重要**，有些是互相依赖的，比如 Django 默认开启的 `SessionMiddleware` 和 `AuthenticationMiddleware` ，调换执行顺序后功能就会不正常。

为了直观看看中间件的调用次序，再添加一个中间件：

```python
# middleware/middlewares.py

class Md1:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print('Md1 视图执行前..')
        response = self.get_response(request)
        print('Md1 视图执行后..')
        return response


class Md2:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print('Md2 视图执行前..')
        response = self.get_response(request)
        print('Md2 视图执行后..')
        return response
```

别忘了将 `Md2` 也注册到配置中：

```python
# your_project/settings.py

MIDDLEWARE = [
    ...
    'middleware.middlewares.Md1',
    'middleware.middlewares.Md2',
]
```

刷新页面后，命令行打印如下：

```python
Md1 视图执行前..
Md2 视图执行前..
--- 视图执行中...
Md2 视图执行后..
Md1 视图执行后..
```

非常神奇的是，中间件调用的 `get_response()` 方法**之前**的逻辑是按照注册列表**顺序**执行，而**之后**的逻辑是**逆序**执行的。

为什么会这样？让我们再看一眼 `__call__` 方法：

```python
def __call__(self, request):
    
    # (1) 这里的逻辑按中间件注册列表顺序执行
    
    # (2) 下一个中间件或视图
    response = self.get_response(request)
    
    # (3) 这里逆序执行
    
    return response
```

请求通过 `__call__` 方法，首先执行了 **序号(1) ** 位置的代码后，通过 `get_response(request)` 传递到下一个中间件里后，又执行下一个 **序号(1)** 位置的代码并继续传递，直到到达了视图函数。

视图函数返回了响应体 `response` 后，整个中间件的调用从 `get_response(request)` 的位置一层层的往回翻，直到回到最初始的中间件，整个调用才宣告结束。

所以中间件的执行顺序，**就像洋葱一样，请求通过洋葱的每一层直到核心的视图函数，再带着响应从里面反着走出来**。

### 传递中断

