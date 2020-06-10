有些时候我们需要**对数据库进行一连串的操作**，如果其中某一个操作失败，那么其他的操作也要跟着回滚到操作以前的状态。

举个例子。某天你到银行存了 100 块钱，所以你的账户的数据库表就应该减去 100 块，银行的账户上增加 100 块。但如果数据库在执行银行账户增加 100 块时操作失败了，那岂不是你就平白无故损失掉 100 块钱，那你不得把银行屋顶给拆了。

这种情况下就需要用到**事务**这个概念了，即把一组操作捆绑到一起，大家生死与共，要么都成功，要么都失败，结成人民统一战线。

说这么多，Django 里如何实现事务？看下面的例子：

```python
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

通常我们会这样写视图：

```python
def create_student(request):
    student = Student.objects.create(name='张三')
    info = Info.objects.create(age=19)
    address = Address.objects.create(home='北京')

    return HttpResponse('Create success...')
```

很正常对吧。接下来使个坏，让程序故意引发错误：

```python
def create_student(request):
    student = Student.objects.create(name='张三')
    info = Info.objects.create(age=19)
    
    # 引发错误
    oh_my_god = int('abc')
    
    address = Address.objects.create(home='北京')

    return HttpResponse('Create success...')
```

这就有问题了，前面的 `Student` 和 `Info` 都正常保存进数据库了，但是 `Address` 却由于前一句报错，所以没有执行保存操作，因此学生信息就变成了不完整的垃圾数据了。

解决办法就是把视图函数编程转化为**事务**：

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

有的时候视图里有很多的数据操作，如果我只想标记其中一部分为事务也是有办法的：

```python
from django.db import transaction

@transaction.atomic
def create_student(request):
    student = Student.objects.create(name='张三')

    save_tag = transaction.savepoint()

    try:
        info = Info.objects.create(age=19)
        oh_my_god = int('abc')
        address = Address.objects.create(home='北京')
    except:
        transaction.savepoint_rollback(save_tag)

    return HttpResponse('Create success...')
```

