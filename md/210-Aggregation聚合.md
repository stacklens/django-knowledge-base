Django 的 filter、exclude 等方法使得对数据库的查询很方便了。这在数据量较小的时候还不错，但如果数据量很大，或者查询条件比较复杂，那么查询效率就会很低。

提高数据库查询效率可以通过原生 SQL 语句来实现，但是它的缺点就是需要开发者熟练掌握 SQL。倘若查询条件是动态变化的，则编写 SQL 会更加困难。

对于以便捷著称的 Django，怎么能忍受这样的事。于是就有了**Aggregation聚合**。

聚合最好的例子就是官网给的案例了：

```python
# models.py

from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

class Publisher(models.Model):
    name = models.CharField(max_length=300)

class Book(models.Model):
    name = models.CharField(max_length=300)
    pages = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField()
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    pubdate = models.DateField()

class Store(models.Model):
    name = models.CharField(max_length=300)
    books = models.ManyToManyField(Book)
```

接下来可以这样求所有书籍的平均价格：

```python
>>> from django.db.models import Avg, Max, Min

>>> Book.objects.all().aggregate(Avg('price'))
{'price__avg': Decimal('30.67')}
```

实际上可以省掉 `all()` ：

```python
>>> Book.objects.aggregate(Avg('price'))
{'price__avg': Decimal('30.67')}
```

还可以指定返回的键名：

```python
>>> Book.objects.aggregate(price_avg=Avg('price'))
{'price_avg': Decimal('30.67')}
```

如果要获取所有书籍中的最高价格：

```python
>>> Book.objects.aggregate(Max('price'))
{'price__max': Decimal('44')}
```

获取所有书籍中的最低价格：

```python
>>> Book.objects.aggregate(Min('price'))
{'price__min': Decimal('12')}
```

`aggregate()` 方法返回的不再是 `QuerySet` 了，而是一个包含查询结果的字典。如果我要对 `QerySet` 中每个元素都进行聚合计算、并且返回的仍然是 `QuerySet` ，那就要用到 `annotate()` 方法了。

`annotate` 翻译过来就是**注解**，它的作用有点像给 `QuerySet` 中的每个元素临时贴上一个临时的字段，字段的值是分组聚合运算的结果。

比方说要给查询集中的每本书籍都增加一个字段，字段内容是外链到书籍的作者的数量：

```python
>>> from django.db.models import Count

>>> q = Book.objects.annotate(Count('authors'))
>>> q[0].authors__count
3
```

与 `aggregate()` 的语法类似，也可以给这个字段自定义个名字：

```python
>>> q = Book.objects.annotate(a_count=Count('authors'))
```

跨外链查询字段也是可以的：

```python
>>> s = Store.objects.annotate(min_price=Min('books__price'), max_price=Max('books__price'))

>>> s[0].min_price
Decimal('12')
>>> s[0].max_price
Decimal('44')
```

既然 `annotate()` 返回的是查询集，那么自然也可以和 `filter()`、`exclude()` 等查询方法组合使用：

```python
>>> b = Book.objects.filter(name__startswith="Django").annotate(num_authors=Count('authors'))
>>> b[0].num_authors
4
```

联用的时候 `filter` 、`annotate` 的顺序会影响返回结果，所以逻辑要想清楚。

也可以排序：

```python
>>> Book.objects.annotate(num_authors=Count('authors')).order_by('num_authors')
```

总而言之，`aggregate` 和 `annotate` 用于组合查询。当你需要对某些字段进行聚合操作时（比如Sum， Avg， Max），请使用 `aggregate` 。如果你想要对数据集先进行分组（Group By）然后再进行某些聚合操作或排序时，请使用 `annotate` 。

进行此类查询有时候容易让人迷惑，如果你对查询的结果有任何的疑问，最好的方法就是直接查看它所执行的 SQL 原始语句，像这样：

```python
>>> b = Book.objects.annotate(num_authors=Count('authors')).order_by('num_authors')
>>> print(b.query)
SELECT "aggregation_book"."id", "aggregation_book"."name",
"aggregation_book"."pages", "aggregation_book"."price",
"aggregation_book"."rating", "aggregation_book"."publisher_id", 
"aggregation_book"."pubdate", COUNT("aggregation_book_authors"."author_id") 
AS "num_authors" FROM "aggregation_book" LEFT OUTER JOIN "aggregation_book_authors" 
ON ("aggregation_book"."id" = "aggregation_book_authors"."book_id") 
GROUP BY "aggregation_book"."id", "aggregation_book"."name",
"aggregation_book"."pages", "aggregation_book"."price",
"aggregation_book"."rating", "aggregation_book"."publisher_id", 
"aggregation_book"."pubdate"
ORDER BY "num_authors" ASC
```

> 相关文档：[Aggregation](https://docs.djangoproject.com/en/3.0/topics/db/aggregation/)
>
> 复合使用聚合时的相互干扰问题：[Count and Sum annotations interfere with each other](https://stackoverflow.com/questions/56567841/django-count-and-sum-annotations-interfere-with-each-other)