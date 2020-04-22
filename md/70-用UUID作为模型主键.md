主键是数据库中每个条目的标识符，通常也是唯一的，用来索引到特定的数据条目。

如果你在定义模型时没有显式的指定主键，那么`Django` 会贴心的送你一个自增的 `id` 主键：

```python
class SomeModel(model.Model):
    # 下面这个 id 字段是不需要写的，django 自动附送
    # id = models.AutoField(primary_key=True)
    
    ...
```

这个 `id` 主键从 1 开始计数，每有一条新的数据则 +1，保证了主键不重复。

通常你用这个自增主键就够了，但是有些情况下用它又不合适：居心不良的黑客可以通过 `id` 的值轻易得知当前数据库中的数据总条目、各条数据的大致创建时间、甚至可以推断出相邻数据的主键。

如果你有这样的担心，那么用 `UUID` 作为主键非常合适。 `UUID` 是一种全局唯一标识符，通常用32位的字符串来表现，像这样：`9cd0c6fa-846e-11ea-8191-94e6f7639b8c` ，它可以保证全球范围内的唯一性。

方法是这样：

```python
import uuid

class SomeModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    ...
```

从主键本身，基本看不出来任何有价值的信息，完美。它是 `python` 的标准库，记得导入。