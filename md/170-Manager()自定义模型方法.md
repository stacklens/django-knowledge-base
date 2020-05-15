如果你需要在保存数据前先进行一些操作，那么需要覆写 `save()` 实例方法：

```python
class Book(models.Model):
    title = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        # 在这里执行自定义逻辑
        ...
        
        super().save(*args, **kwargs)
```

使用时就像 Python 那样，正常 `book.save()` 调用，很简单。

如果需要在创建新模型时塞点私货就有点点不同，因为创建这个动作由类本身来执行，而不是实例。

所以要这么写：

```python
class Book(models.Model):
    title = models.CharField(max_length=100)

    @classmethod
    def create(cls, title):
        book = cls(title=title)
        # do something with the book
        return book
```

这样子调用：

```python
book = Book.create('Foo')
book.save()
```

还有一种更加推荐的方式：

```python
class BookManager(models.Manager):
    def create_book(self, title):
        book = self.create(title=title)
        # do something with the book
        book.save()
        return book


class Book(models.Model):
    title = models.CharField(max_length=100)

    objects = models.Manager() # 默认管理器
    custom = BookManager() # 自定义管理器
```

这种方式就用到了**模型管理器**这个神奇的玩意了。

虽说神奇，但是你随时都在用到：

```python
Obj.objects.create()  # 中间那个 objects 就是友情赠送的默认管理器
```

除了默认管理器，还自定义了一个新管理器 `custom`，它里面有一个 `create_book` 方法，是这样子使用的：

```python
book = Book.custom.create_book('Bar')
```

除此之外，你还可以修改管理器的初始查询集：

```python
class BookManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(title__contains='money')


class Book(models.Model):
    title = models.CharField(max_length=100)

    objects = models.Manager()
    custom = BookManager()
```

上面这坨代码，`Book.objects.all()` 返回所有的书籍，而 `Book.custom.all()` 仅返回标题里包含 `money` 的书籍。

你甚至可以在管理器里定义新方法：

```python
class PollManager(models.Manager):
    def with_counts(self):
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT p.id, p.question, p.poll_date, COUNT(*)
                FROM polls_opinionpoll p, polls_response r
                WHERE p.id = r.poll_id
                GROUP BY p.id, p.question, p.poll_date
                ORDER BY p.poll_date DESC""")
            result_list = []
            for row in cursor.fetchall():
                p = self.model(id=row[0], question=row[1], poll_date=row[2])
                p.num_responses = row[3]
                result_list.append(p)
        return result_list

class OpinionPoll(models.Model):
    question = models.CharField(max_length=200)
    poll_date = models.DateField()
    objects = PollManager()

class Response(models.Model):
    poll = models.ForeignKey(OpinionPoll, on_delete=models.CASCADE)
    person_name = models.CharField(max_length=50)
    response = models.TextField()
```

`with_counts()` 方法返回所有 `OpinionPoll` 对象，并且每个对象附带一个 `num_responses` 聚合查询属性。