有的时候我们需要将“一对多” `ForeignKey` 关联到**多个不同的模型**。什么意思？比如博客文章，它的作者既可以是独立的用户 `Person`，也可以是某一个群组 `Group`；但是 `ForeignKey` 显然只支持关联到单个模型的，怎么办？

解决方案有很多种，我最喜欢的是这样：

```python
# 群组
class Group(models.Model):
    name = models.CharField(max_length=100)

# 用户
class Person(models.Model):
    name = models.CharField(max_length=100)

# 起过渡作用的桥接模型
class Owner(models.Model):
    # 用户
    person = models.OneToOneField(
        Person,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    # 群组
    group = models.OneToOneField(
        Group,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    
# 文章
class Post(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
```

关键点是 `ForeignKey` 关联了一个 `Owner` 桥接模型，再由 `Owner` 与实际的作者作“一对一”的关联。

在使用它时，可能还需要一个辅助函数确定 `Owner` 到底关联了谁：

```python
class Owner(...):
    ...
    def get_owner(self):
        # 获取非空 Owner 对象
        if self.person is not None:
            return self.person
        elif self.group is not None:
            return self.group
        raise AssertionError("Neither is set")
```

在视图中可以这样取得实际的 `owner` ：

```python
owner = post.owner.get_owner()
```

这种方式有一些**缺点**，比如多了一个 `Owner` 桥接表、需要写更多辅助函数保证 `owner` 的正确性，但就我个人来说，我觉得它在简洁、效率上是个不错的折中。

另外在个人博客的开发中，需要用到这种技巧的主要地方就是**评论模块**了，尝试去解决吧。

> 实际上 Django 有一个专门处理对应不同模型的外键，叫 `GenericForeignKey`，但我不太喜欢，有兴趣的同学请读[官方文档](https://docs.djangoproject.com/en/3.0/ref/contrib/contenttypes/)。有关这个话题还有一篇经典的文章[为什么你应该避免使用GenericForeignKey](https://lukeplant.me.uk/blog/posts/avoid-django-genericforeignkey/)，里面介绍了 5 种替代方案，值得一读。