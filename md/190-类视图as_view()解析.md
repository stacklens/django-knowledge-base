`Django` 有**函数视图**和**类视图**，分别是这样用的：

```python
# 函数视图
path(..., function_view, ...)
# 类视图
path(..., ClassView.as_view(), ...)
```

这个 `as_view()` 很有意思，我们通过源码来看看它是如何把类转化成函数的。

源码不是很长，全贴出来如下所示：

```python
class View:
    ...
    
    @classonlymethod
    def as_view(cls, **initkwargs):
        """Main entry point for a request-response process."""
        for key in initkwargs:
            if key in cls.http_method_names:
                raise TypeError("You tried to pass in the %s method name as a "
                                "keyword argument to %s(). Don't do that."
                                % (key, cls.__name__))
            if not hasattr(cls, key):
                raise TypeError("%s() received an invalid keyword %r. as_view "
                                "only accepts arguments that are already "
                                "attributes of the class." % (cls.__name__, key))

        def view(request, *args, **kwargs):
            self = cls(**initkwargs)
            if hasattr(self, 'get') and not hasattr(self, 'head'):
                self.head = self.get
            self.setup(request, *args, **kwargs)
            if not hasattr(self, 'request'):
                raise AttributeError(
                    "%s instance has no 'request' attribute. Did you override "
                    "setup() and forget to call super()?" % cls.__name__
                )
            return self.dispatch(request, *args, **kwargs)
        view.view_class = cls
        view.view_initkwargs = initkwargs

        # take name and docstring from class
        update_wrapper(view, cls, updated=())

        # and possible attributes set by decorators
        # like csrf_exempt from dispatch
        update_wrapper(view, cls.dispatch, assigned=())
        return view
```

来一步步分解。

`as_view()` 是个类方法，它的第一个参数 `cls` 表示类本身，跟实例方法的 `self` 差不多，都是自动传入的。

进入 `as_view()` 后首先对传入的参数做简单的校验，避免传入的参数将类自己的关键函数名覆盖掉，或者传入类中没定义的属性。开头这个 `for` 循环就是干这个用的。

接着 `as_view()` 内部又定义了一个 `view()` 函数，它接收的参数和普通的**函数视图**是相同的： `request` 对象以及从 `url` 获取的 `args` 和 `kwargs` 参数。我们挑重点看它在干什么：

```python
def view(request, *args, **kwargs):
    self = cls(**initkwargs)
    ...
    self.setup(request, *args, **kwargs)
    ...
    return self.dispatch(request, *args, **kwargs)
```

首先实例化了类自己 `cls()`，并赋值给 `self` ，也就是你编写的类视图的实例。

接着调用 `self.setup()`  对实例的属性进行了初始化。`setup()` 方法非常简单：

```python
def setup(self, request, *args, **kwargs):
    """Initialize attributes shared by all view methods."""
    self.request = request
    self.args = args
    self.kwargs = kwargs
```

把接收的参数原封不动的赋值到类实例中。

> 这几个属性经常能用到，比如 `self.kwargs.get('id')` 获取 `url` 中传递的 `id` 值。

`view()` 函数最后返回了 `dispatch()` ，它的源码是这样的：

```python
class View:
    # dispatch 用到的http请求方法名 -- 杜赛注
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']
    ...
    
    def dispatch(self, request, *args, **kwargs):
        # Try to dispatch to the right method; if a method doesn't exist,
        # defer to the error handler. Also defer to the error handler if the
        # request method isn't on the approved list.
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)
```

`dispatch()` 非常简短，功能却非常重要：如果 `request.method` 是一个 `GET` 请求，则调用类视图 `self.get()` 方法，如果是 `POST` 请求，那就调用 `self.post()` 方法。这就起到根据 http 请求类型派发到不同函数的功能，这是类视图的核心了。

回到 `as_view()` 来，它最后做了属性赋值、修改函数签名等收尾工作后，返回了 `view` 函数闭包：

```python
def as_view(cls, **initkwargs):
    ...

    view.view_class = cls
    view.view_initkwargs = initkwargs

    # take name and docstring from class
    update_wrapper(view, cls, updated=())

    # and possible attributes set by decorators
    # like csrf_exempt from dispatch
    update_wrapper(view, cls.dispatch, assigned=())
    
    return view
```

`as_view()` 方法就完成了，来总结一下它的核心流程：

- `as_view()` 内部定义了 `view()` 函数。`view()` 函数对类视图进行初始化，返回并调用了 `dispatch()` 方法。
- `dispatch()` 根据请求类型的不同，调用不同的函数（如 `get()` 、 `post()`），并将这些函数的 `response` 响应结果返回。
- `as_view()` 返回了这个 `view` 函数闭包，供 `path()` 路由调用。

把核心部分拿出来就这样：

```python
class View:
    ...
    @classonlymethod
    def as_view(cls, **initkwargs):
        ...
        def view(request, *args, **kwargs):
            self = cls(**initkwargs)
            ...
            self.setup(request, *args, **kwargs)
            ...
            return self.dispatch(request, *args, **kwargs)
        ...
        return view

    def setup(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs

    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), ...)
        ...
        return handler(request, *args, **kwargs)
```

结果就是 `as_view()` 返回了一个函数（携带着必要的参数），和你用视图函数时直接传递给路由一个函数的效果是相同的。

相当的神奇吧。