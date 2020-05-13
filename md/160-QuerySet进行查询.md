以博客文章模型为例：

```python
# models.py

class Post(models.Model):
    owner = models.ForeignKey(User, ..., related_name='posts')
    title = models.CharField(...)
    body = models.TextField(...)
    created = models.DateTimeField(...)
```

要从模型中检索对象，首先要构建一个管理器。默认情况下的管理器是这个：

```python
>>> Post.objects
<django.db.models.manager.Manager object at ...>

>>> p = Post(title='...')
>>> p.objects
Traceback:
    ...
AttributeError: "Manager isn't accessible via Post instances."
```

管理器只能通过模型类获得，而不能通过实例获得。

最常用的检索就是获取所有对象了：

```python
>>> all_posts = Post.objects.all()
>>> all_posts
<QuerySet [<Post: ...>, <Post: ...>, <Post: ...>]>
```

得到的结果是满足检索要求的集合，这就是通常说的 `QuerySet`。

检索特定对象用 `filter()`：

```python
# 获取 2019 年发布的文章
Post.objects.filter(created__year=2019)
```

如果你要排除某些特定对象，可以用 `exclude()`：

```python
# 获取 2019 年以外时间发布的文章
Post.objects.exclude(created__year=2019)
```

也可以做链式查询：

```python
Post.objects.filter(created__year=2019).exclude(title__startswith='Foo')
```

链多少层都可以，只要你喜欢。

此外，查询集在执行时不会原地修改，每次都会返回一个全新的子集：

```python
a = Post.objects.all()
b = a.exclude(created__year=2019)
```

上面代码中的 `a`  、 `b` 都是独立分开的查询集，互不影响。

`QuerySet` 在创建时是懒惰的，即并不会涉及数据库的操作：

```python
>>> a = Post.objects.all()
>>> b = a.exclude(created__year=2019)
>>> c = b.filter(title__startswith='Foo')
>>> print(c)
```

上面的代码看起来像是对数据库查询了三次，但实际上只是在 `print(c)` 时才会真正执行查询。

稍有不同的是切片：

```python
>>> d = Post.objects.all()[1:10]
```

上面这句不会执行查询，道理相同。

下面这句就不一样了：

```python
>>> e = Post.objects.all()[:10:2]
```

这句是会执行查询的，Django 需要查询数据库以便返回带有间隔的列表。换句话说，带有步长的切片就会触发查询。

有一些管理器方法并不返回 `QuerySet` ，而是返回一个模型对象或者变量。比如 `get()` 方法可以取得单个确定的对象：

```python
>>> Post.objects.get(id=1)
```

`.create()`、`.first()`、`last()`、`count()`、`exists()`都属于这一类。

跨关系的查找也可以：

```python
>>> Post.objects.get(owner__username='dusai')
```

如果 `get()` 返回了多个或者零个结果会报错。

我们已经多次用到如 `owner__username` 这种参数形式了。其实这里的 `__` 你理解成 `.` 就好了，因为语法规则里关键字不能用 `.` ，所以就用 `__` 来代替了。

还有 `title__startswith='Foo'` 这类用法，`startswith` 显然不是模型字段，而是指查找以 `Foo` 打头的 `title` 字段的相关数据。类似的查询方法还有：

```python
exact # 完全匹配
iexact # 不区分大小写的完全匹配
contains # 包含
icontains # 不区分大小写的包含
in # 被包含在给定的集合中，如 Post.objects.filter(id__in=[2, 3, 4])
gt # 大于，如 Post.objects.filter(id__gt=3)
gte # 大于或等于
lt # 小于
lte # 小于或等于
startswith # 以 xx 开头
istartswith # 不区分大小写的以 xx 开头
endswith
iendswith
range # 在范围内
date # 日期字段使用，如 Post.objects.filter(created__date=datetime.date(2020, 1, 1))
year, month, day...
isnull
regex # 匹配正则
iregex
```

有这么多，够你折腾了。