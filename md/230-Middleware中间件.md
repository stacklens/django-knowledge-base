**中间件**是 Django 处理请求和响应的**钩子框架**。它是一个轻量级的、低层级的“插件”系统，用于**全局**改变 Django 的输入或输出。如果你需要在响应请求时插入一个自定义功能、参数的时候特别有用。

### 自定义中间件

假设你有一个叫 `middleware` 的 app 。在 app 中创建文件 `middlewares.py`，一会儿在这里面自定义中间件。

来看一下 Django 官方推荐的中间件写法是什么样子的：

```python
# middleware/middlewares.py

class Md1:
    def __init__(self, get_response):
        self.get_response = get_response
        # (0) 参数的配置与初始化。初始化只执行一次。

    def __call__(self, request):

        # (1) 这里写实际视图执行之前的逻辑
        print('Md1 视图执行前..')

        # (2) get_response 是下一个中间件或视图函数的处理程序
        response = self.get_response(request)

        # (3) 这里写实际视图执行之后的逻辑
        print('Md1 视图执行后..')

        return response
```

这个类 `Md1` 就是一个最简单的中间件了，它最核心的部分就是实现了 `__call__` 方法，使得类变成可调用对象：

-  方法里的 `request` 就是视图函数中传入的那个 `request` 。
- `get_response` 是可调用对象，它处理的内容可以是下一个中间件，也可以是实际的视图函数，当前中间件并不关心。`request` 通过它传递到下一级，也就是说 `get_response` 到达的最底层就是视图函数了。
- 因此，**序号(1)** 则是**请求到达视图前**需要自定义的逻辑，**序号(3)** 是**请求从视图出来后**需要自定义的逻辑。

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

    # 刚才自定义的中间件，注册规则：appName.fileName.className
    'middleware.middlewares.Md1',
]
```

在 app 中编写测试视图：

```python
# middleware/views.py

from django.http import HttpResponse

def mid_test(request):
    print('--- 视图执行中...')
    return HttpResponse('中间件测试..')
```

最后在项目根 `urls.py` 中添加路由：

```python
# your_project/urls.py

...

from middleware.views import mid_test

urlpatterns = [
    ...
    path('middleware/', mid_test),
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

为了直观表现调用次序，再添加两个自定义中间件：

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
    

class Md3:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        print('Md3 视图执行前..')
        response = self.get_response(request)
        print('Md3 视图执行后..')

        return response
```

注册到配置中：

```python
# your_project/settings.py

MIDDLEWARE = [
    ...
    'middleware.middlewares.Md1',
    'middleware.middlewares.Md2',
    'middleware.middlewares.Md3',
]
```

刷新页面后，命令行打印如下：

```python
Md1 视图执行前..
Md2 视图执行前..
Md3 视图执行前..
--- 视图执行中...
Md3 视图执行后..
Md2 视图执行后..
Md1 视图执行后..
```

非常神奇的是，中间件调用的 `get_response()` 方法**之前**的逻辑是按照注册列表**顺序**执行，而**之后**的逻辑是**逆序**执行的。

> 也就是说，中间件在传递请求的阶段顺序执行，在返回响应的阶段逆序执行。

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

视图函数返回了响应体 `response` 后，整个中间件的调用从 `get_response(request)` 的位置一层层的往回翻，直到回到最初始的位置，整个调用才宣告结束。

所以中间件的执行顺序，**就像洋葱一样，请求通过洋葱的每一层直到核心的视图函数，再带着响应从里面反着出来**。

### 短路

中间件有种比较常用的用法，即不调用 `get_response()` 方法，手动返回一个 http 响应体，像这样：

```python
# middleware/middlewares.py

from django.http import HttpResponse


class Md1:
    ...
    

class Md2:
    ...
    
    def __call__(self, request):
        print('Md2 视图执行前..')
        
        # 新增代码
        if True:
            print('Md2 引发短路')
            return HttpResponse('Md2 引发短路')

        response = self.get_response(request)
        print('Md2 视图执行后..')
        return response


class Md3:
    ...
```

刷新页面，命令行打印如下：

```python
Md1 视图执行前..
Md2 视图执行前..
Md2 引发短路
Md1 视图执行后..
```

`if` 语句中直接返回了 `HttpResponse`响应体，从而中断了中间件向下一级传播，直接从 `return` 位置返回了，甚至请求也不会进入视图函数。这就是中间件的**短路**，比较常用在权限控制等功能中。

### 更多钩子

除了上述最基础的模式之外，中间件类还提供了另外三种钩子方法。

#### process_view()

- `process_view(request, view_func, view_args, view_kwargs)`

`request` 是一个 `HttpRequest` 对象。`view_func` 是实际要执行的视图函数。 `view_args` 是传递给视图的位置参数列表，`view_kwargs` 是传递给视图的关键字参数字典。

`process_view()` 在**所有中间件的基础模式后、视图执行前**被调用。它返回 `None` 或 `HttpResponse`对象：

- 返回 `None` ，Django 将按照规则处理这个请求并顺序执行接下来的中间件。
- 返回 `HttpResponse` 对象，则 Django 不调用实际的视图，而是从已经调用的中间件开始逐层返回。

#### process_exception()

- `process_exception(request, exception)`

 `exception` 是视图函数引发的 `Exception` 对象。

当视图引发异常时，Django 会调用 `process_exception()`。它返回 `None` 或 `HttpResponse` 对象：

- 如果返回 `HttpResponse`对象，中间件会直接将结果响应返回浏览器。
- 否则就开始默认的异常处理。

也就是说，如果异常中间件返回一个响应，那么其他之后的中间件的 `process_exception` 方法将不会被调用。

#### process_template_response()

- `process_template_response(request, response)`

`response` 是 `TemplateResponse` 对象。

它在视图被执行后调用，必须返回一个实现了 `render` 方法的响应对象。此钩子方法会在响应阶段按照相反的顺序运行。**也就是说，此方法仅当视图返回 `TemplateResponse` 对象才会被调用，通常用的 `render` 快捷方式不会触发它。**

> 所有这些钩子方法组合到一起可以形成复杂的短路规则。推荐读者自行测试一下，印象会比较深刻。

### 案例

#### 用户拦截

假设你有一个敏感路径，要求必须超级用户才能访问：

```python
from django.http import HttpResponseForbidden

class NormalUserBlock:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if (request.user.is_superuser != True) and (request.path == '/secret-url/'):
            return HttpResponseForbidden('<h1>超级用户方可访问此页面！</h1>')

        response = self.get_response(request)

        return response
```

此功能可以非常容易扩展为 IP 拦截：通过 `request.META['REMOTE_ADDR'] ` 获取请求的 IP 地址，比对数据库中的黑名单进行拦截。

#### Debug 页面优化

假设你的博客部署到线上了，并且理所当然的配置了 `DEBUG = False` 。当引发 500 错误后，你想让超级用户仍然看到 DEBUG 页面，而普通用户看不到，可以这样：

```python
import sys
from django.views.debug import technical_500_response

class DebugOnlySuperUser():
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if request.user.is_superuser:
            return technical_500_response(request, *sys.exc_info())
```

这样调试起来就方便了不少。

#### CSRF 验证

`process_view()` 方法和基础用法的主要区别之一，就是它带有与请求相关的视图的信息。

Django 自带的 CSRF 中间件就是很好的例子：

```python
...

def process_view(self, request, callback, callback_args, callback_kwargs):
    ...

    if getattr(callback, 'csrf_exempt', False):
        return None
    
    ...
```

如果请求的视图上存在 `csrf_exempt` 装饰器，则本次请求不会实施 CSRF 保护。

#### 响应计时器

自定义中间件，记录从收到请求到完成响应所花费的时间：

```python
from datetime import datetime

class ResponseTimer:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request._request_time = datetime.now()
        response = self.get_response(request)
        return response

    def process_template_response(self, request, response):
        response_time = request._request_time - datetime.now()
        response.context_data['response_time'] = abs(response_time)
        return response
```

有了这个中间件，所有的模板都可以获取到 `{{ response_time }}` 这个变量了。

**再重复一次**，此方法仅当视图返回 `TemplateResponse` 对象才会被调用，通常用的 `render` 快捷方式不会触发它。它两的区别是，`TemplateResponse` 会延迟渲染，它包含了呈现模板之前的上下文数据，因此让中间件有机会去修改里面的变量。而 `render` 会立即呈现模板并返回 `HttpResponse` ，无法唤起此钩子方法：

```python
from django.shortcuts import render
from django.template.response import TemplateResponse

# 无法调用 process_template_response()
def mid_test(request):
    return render(request, '....html', context={})

# 返回 TemplateResponse 才可调用
def mid_test(request):
    return TemplateResponse(request, '....html', context={})
```

