我们在写 Django 程序时，很容易犯的错误是让**视图**承担了太多不应该负责的功能，以致让其快速膨胀。当你感觉某一个功能对模型的关注度远远超过视图自身时，就应该考虑此功能是不是放错位置了。

在这个前提下，将适当的业务逻辑摆放到**模型**中就是宝贵的学问了。

比如下面展示的这两个模型方法：

```python
class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def full_name_with_midname(self, midname):
        return f"{self.first_name} {midname} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
```

很显然这两个方法对 `Person` 的关注度很高，因此写在模型中是很合适的。

在视图中这样子调用：

```python
name1 = person.full_name  # return 'Du Sai'
name2 = person.full_name_with_midname('Trump')  # return 'Du Trump Sai'
```

因为用了 `@property` 装饰器，所以可以像获取变量一样调用 `def full_name()` 了，很适合用于计算型变量。

这个例子看起来不足为奇，但如果模块功能复杂、语句很多时，将逻辑从视图中抽离有助于保持视图的清爽，也方便复用。