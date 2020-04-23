开发个人博客时，博客文章的模型通常包含有**浏览量计数**、**最近更新时间**两个字段，像这样：

```python
class Post(models.Model):
    # 文章浏览量
    views = models.IntegerField(default=0)
    # 最近更新时间
    updated = models.DateTimeField(auto_now=True)
    
    # other fields...
    
    # 增加浏览量的方法
    def increase_view(self):
        self.views += 1
        self.save()
```

每当访客打开文章详情页面时，浏览量需要 +1，所以在视图调用 `increase_view`：

```python
def some_view(request, id):
    post = Post.objects.get(id=id)
    post.increase_view()
    ...
```

> 还有更好的自增方式，后面章节再讲。

这样弄的结果就是浏览量虽然正确的增加了，但是最近更新时间 `updated` 也一起更新了，这显然不是我们想要的。

正确的写法是要传入 `update_fields` 参数，控制需要更新的字段：

```python
...
def increase_view(self):
    self.views += 1
    self.save(update_fields=['views'])
```

这样就可以只更新 `views` 字段了，其他字段都保持原状。