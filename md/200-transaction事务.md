有些时候我们需要**对数据库进行一连串的操作**，如果其中某一个操作失败，那么其他的操作也要跟着回滚到操作以前的状态。

举个例子。某天你到银行存了 100 块钱，所以你的账户的数据库表就应该减去 100 块，而银行的账户上增加 100 块。但如果数据库在执行银行账户增加 100 块时操作失败了，岂不是平白无故损失掉 100 块钱，那你不得把银行屋顶给拆了。

这种情况下就需要用到**事务**这个概念了，即把一组操作捆绑到一起，大家生死与共，要么都成功，要么都失败，结成人民统一战线。

Django 里如何实现事务？看下面的例子：

```python
# models.py
from django.db import models


class Student(models.Model):
    """学生"""
    name = models.CharField(max_length=20)

    
class Info(models.Model):
    """学生的基本情况"""
    age = models.IntegerField()

    
class Address(models.Model):
    """学生的家庭住址"""
    home = models.CharField(max_length=100)
```

有三个模型，`Student` 为学生、`Info` 为学生的基本情况、`Address` 为学生的住址。**假设这三个模型必须同时创建，否则数据就是不完整的。**

我们可以这样写视图：

```python
def create_student(request):
    student = Student.objects.create(name='张三')
    info = Info.objects.create(age=19)
    address = Address.objects.create(home='北京')

    return HttpResponse('Create success...')
```

很正常对吧。接下来让程序故意引发错误：

```python
def create_student(request):
    student = Student.objects.create(name='张三')
    info = Info.objects.create(age=19)
    
    # 引发错误
    oh_my_god = int('abc')
    
    address = Address.objects.create(home='北京')

    return HttpResponse('Create success...')
```

这就有问题了，前面的 `Student` 和 `Info` 都正常保存进数据库了，但是 `Address` 却由于前一句报错而没有执行创建，因此学生信息就变成了不完整的垃圾数据了。

解决办法就是把视图函数中的数据操作转化为**事务**：

```python
from django.db import transaction

# 注意这个装饰器
@transaction.atomic
def create_student(request):
    student = Student.objects.create(name='张三')
    info = Info.objects.create(age=19)
    
    oh_my_god = int('abc')
    
    address = Address.objects.create(home='北京')

    return HttpResponse('Create success...')

```

这就非常不同了。无论视图里哪一个数据库操作失败或是没有执行，那么其他的操作也都会回滚到操作前的状态。也就是说上面这段代码中的三个模型，都没有保存成功。

有的时候视图里有很多的数据操作，如果我只想回滚其中一部分为事务也是有办法的：

```python
from django.db import transaction

@transaction.atomic
def create_student(request):
    student = Student.objects.create(name='张三')
    
    # 回滚保存点
    save_tag = transaction.savepoint()

    try:
        info = Info.objects.create(age=19)
        
        # 引发错误
        oh_my_god = int('abc')
        
        address = Address.objects.create(home='北京')
    except:
        # 回滚到 save_tag 的位置
        transaction.savepoint_rollback(save_tag)

    return HttpResponse('Create success...')
```

上面的代码运行之后，`Student` 表会成功保存，而另外两张表则都会失败。使用 `try` 的好处在于前端能正常运行。

除此之外，还有另一种方法可以将视图中的事务进行分组，实现更细腻的控制：

```python
# 装饰器不要了
# @transaction.atomic
def create_student(request):
    student = Student.objects.create(name='张三')

    # 事务
    with transaction.atomic:
        info = Info.objects.create(age=19)
        
        # 引发错误
        oh_my_god = int('abc')
        
        address = Address.objects.create(home='北京')

    return HttpResponse('Create success...')
```

效果是差不多的，仅有 `Student` 成功保存。

还有最后一个大杀器。如果你想让所有的数据库操作都是事务，那就在 `settings.py` 里配置：

```python
# settings.py

# 以 sqlite 为例
DATABASES = {
    'default': {
        'ENGINE': ...,
        'NAME': ...,
        # 加上这条
        'ATOMIC_REQUESTS': True,
    }
}

```

然后可以用 `non_atomic_requests` 标记不需要成为事务的视图：

```python
@transaction.non_atomic_requests
def create_student(request):
    ...
```

另外，**类视图**也是可以成为事务的：

```python
class CreateStudent(View):
    @transaction.atomic
    def get(self, request):
        ...
```

最后总结一下，并非任意对数据库的操作序列都是事务。数据库事务拥有 [ACID特性](https://zh.wikipedia.org/wiki/%E6%95%B0%E6%8D%AE%E5%BA%93%E4%BA%8B%E5%8A%A1)：

- **原子性（Atomicity）**：事务作为一个整体被执行，包含在其中的对数据库的操作要么全部被执行，要么都不执行。
- **一致性（Consistency）**：事务应确保数据库的状态从一个一致状态转变为另一个一致状态。一致状态的含义是数据库中的数据应满足完整性约束。
- **隔离性（Isolation）**：多个事务并发执行时，一个事务的执行不应影响其他事务的执行。
- **持久性（Durability）**：已被提交的事务对数据库的修改应该永久保存在数据库中。

> 关联官方文档：[Database transactions](https://docs.djangoproject.com/en/3.0/topics/db/transactions/)