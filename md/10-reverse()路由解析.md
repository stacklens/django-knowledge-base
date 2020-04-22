假设已经有了这么一个路由：

```python
path('foo/', some_view, name='foo_name'),
```

想从**页面模板**某处链接跳转到**视图函数**中就非常容易了，用如下模板语法：

```html
<a href="{% url 'foo' %}">Jump</a>
```

现在问题来了，如果我想从**视图函数**中跳转到**另一个视图函数**该怎么办呢？这种情况是有可能发生的，比如某个视图会根据条件的不同而转换到不同的视图中去。

很简单，有现成的 `redirect()` 函数可使用：

```python
return redirect('/foo/')
```

但是这样把 `url` 硬编码到代码里了，不美。更好的写法就要用到主角 `reverse()` 了：

```python
return redirect(reverse('foo_name'))
```

这样写的好处是你可以任意更改 `url` 实际地址，只要路由的 `name` 不变，都是可以解析到正确的地址中去的。

带有参数的写法如下：

```python
reverse('another_name', args=(id,))
```

因此带有参数的路由也可以正确解析了。简单又好用吧。