**元类**（Metaclass）是面向对象编程中一个深奥的概念，它几乎隐藏在所有的 Python 代码后面，但通常你根本意识不到这点。

相比其他面向对象语言，Python 甚至允许你可以自定义元类。自定义元类的使用向来很有争议，就像下面这位大佬所说的名言：

> “元类是99%的开发者都不需要用到的黑魔法。如果你在犹豫是否需要用到它，那答案就是不需要（真正需要的人肯定知道为什么要用，并且不需要解释原因）。”
>
> ​    —    *Tim Peters*

虽然使用元类不是必需的，但理解它还是值得的，因为可以帮助更好地理解 Python 的奥妙。

谁还不希望掌握一点黑魔法呢？

## 一切皆对象

在我最近的文章中，**一切皆对象**都快被说烂了。但是 Python 中很多特性都跟这相关，因此让我们还是从一切皆对象开始说起。

随便定义几个对象：

```python
a = 1
b = {'x': 2, 'y': 3}
c = [4, 5]

class Foo:
    pass

foo = Foo()
```

对象需要从属某个**类型**，以表明自己是个什么样的对象。而用 `type()` 函数可以获取到某个对象的类型。

比如上面这些：

```python
>>> type(a)
int
>>> type(b)
dict
>>> type(c)
list
>>> type(foo)
__main__.Foo
```

a、b、c 的类型分别是整型、字典和列表，而 foo 实例的类型是 `Foo` 类。

让我们进一步思考：类也是对象，那**类的类型**是什么呢？

来试试：

```python
>>> type(Foo)
type
```

`Foo` 类的类型是 `type` 。 `type` 实际上就是个元类，也就是 Python 在幕后创建**所有类**的元类。

顺带一说，Python 中**所有**的对象都是从**类**派生出来的，包括内置的整型、字符串、列表等。因此：

```python
>>> type(int)
type
>>> type(dict)
type
>>> type(list)
type
```

有点烧脑对吧，但其实元类并不复杂。换句话说，**元类只是用于创建类的东西**，也可以称为类工厂。

> 所谓元类，就是创建类的类。类用于创建类实例；元类用于创建类。
>
> 即：元类 -> 类 -> 类实例

## type魔法

`type()` 函数除了可以查看对象的类型外，更强大的是它还可以接收三个参数来**动态创建类**。

调用时 `type(name, bases, dct)` 三个参数分别是：

- `name` 字符串类型，指定要创建的类名
- `bases` 元组类型，指定该类的父类
- `dct` 字典类型，存放该类的所有属性和方法

举个栗子：

```python
Bar = type('Bar', (), {})
```

调用下试试：

```python
>>> Bar
__main__.Bar

>>> b = Bar()
>>> b
<__main__.Bar at 0x253b636abe0>
```

这就相当于下面的代码：

```python
class Bar:
    pass
```

它两是等价的。实际上 Python 解释器在遇到 `class` 定义时，幕后也是调用 `type()` 创建出类的。

再看一个例子：

```python
Foo = type('Foo', (Bar,), {})
```

这就相当于：

```python
class Foo(Bar):
    pass
```

如果类里有属性和方法呢？

看最后一个例子：

```python
Calc = type(
    'Calc',
    (),
    {
        'num': 100,
        'half': lambda x: x.num / 2
    }
)
```

试试调用其属性和方法：

```python
>>> calc = Calc()

>>> calc.num
100

>>> calc.half()
50.0
```

这就相当于：

```python
class Calc:
    num = 100
    def half(self):
        return self.num / 2
```

另外， `lambda` 表达式只能定义比较简单的函数。复杂函数你可以单独定义，然后赋值进去，比如：

```python
def f(obj):
    return 1

Yeah = type(
    'Yeah',
    (),
    {
        'hi': f
    }
)
```

## 自定义元类

自定义元类的主要目的是在创建类时，动态更改类的某些行为。

回到这个例子：

```python
class Foo:
    pass
```

如果要在创建**类实例**时动态修改属性，可以修改类的 `__new__` 方法：

```python
class Foo:
    pass

def new(cls):
    obj = object.__new__(cls)
    obj.num = 100
    return obj

Foo.__new__ = new
```

测试下：

```python
>>> foo = Foo()
>>> foo.num
100
```

那如果我创建**类**也想动态修改属性呢？由于类都是由 `type` 创建出来的，那我是否应该修改 `type` 的 `__new__` 方法？

试一下：

```python
def new(cls):
    obj = type.__new__(cls)
    obj.num = 100
    return obj

type.__new__ = new

# 输出:
# Traceback (most recent call last):
#   File "...", line 25, in <module>
#     type.__new__ = new
# TypeError: can't set attributes of built-in/extension type 'type'
```

type 是所有类的模板，修改它的特性非常危险。Python 不允许你这么瞎搞，直接报错了。

一种解决方案就是**自定义元类**：

```python
class MyMeta(type):
    def __new__(cls, name, bases, dct):
        obj = super().__new__(cls, name, bases, dct)
        obj.num = 100
        return obj
```

这就是个简单的自定义元类了。让我们一步步拆解：

- 因为 `type` 是元类，因此继承它的子类也是元类。
- 元类创建对象时会调用 `__new__` 方法，因此可以在这里对创建的类进行动态修改。

接着看 `__new__` 内部：

- 第一句，原封不动调用父类 `type` 创建类时的动作。
- 第二句，给创建出来的类附加额外的 `num` 属性。
- 第三句，把创建好的类返回。

那么像这样去使用它：

```python
class Foo(metaclass=MyMeta):
    pass
```

测试下功能：

```python
>>> Foo.num
100
```

没想象中那么复杂，对吧？之所以觉得元类很复杂，是因为它被用到的场合通常都很纠结，比如库开发或者ORM设计等。

最后看几个自定义元类应用的例子。

### 元类应用

### 子类方法限制

假设你是个库的作者，你要求用户继承你的类**必须**实现特定的方法，比如下面这个：

```python
# 库提供的父类
class Father():
    def foo(self):
        return self.bar()

# 用户写的子类
class Child(Father):
    def bar(self):
        return True
```

该怎么办？用户会写出什么代码是无法预料的。可以强制子类必须实现某些方法吗？

元类就可以办到：

```python
class Meta(type):
    def __new__(cls, name, bases, dct, **kwargs):
        if name != 'Father' and 'bar' not in dct:
            raise TypeError('Class must contain bar() method.')
        return super().__new__(cls, name, bases, dct, **kwargs)

# 添加了元类
class Father(metaclass=Meta):
    def foo(self):
        return self.bar()
```

如果子类不实现 `bar()` 方法，运行则会立即报错：

```python
# 用户写的子类
class Child(Father):
    pass

# 输出报错:
# TypeError: Class must contain bar() method.
```

稍微要注意的是实际上元类中的 `__new__` 方法还可以接收关键字参数。如果像这样定义基类：

```python
# 库提供的父类
class Father(metaclass=Meta, value=10):
    ...
```

那么这个 `value` 就会成为关键字参数传递到 `__new__` 中。

### 动态添加方法

动态给子类添加属性或方法算是元类的基础用法了。

比如说，我只想让名叫 `Apple` 的子类具有 `sayHi()` 方法：

```python
class Meta(type):
    def __new__(cls, name, bases, dct, **kwargs):
        if name == 'Apple':
            dct.update({
                    'sayHi': lambda: 'Hi I am Apple'
                })
        return super().__new__(cls, name, bases, dct, **kwargs)


class Food(metaclass=Meta):
    pass
    
class Apple(Food):
    pass

class Pear(Food):
    pass
```

调用下试试：

```python
>>> Apple.sayHi()
'Hi I am Apple'

>>> Pear.sayHi()
AttributeError: type object 'Pear' has no attribute 'sayHi'
```

除了判断类的名称外，你可以编写更加复杂的判据，来实现业务的要求。

### ORM

相比上面的例子，元类更多的被用到 API 的设计中，比较典型的就是 Web 框架的**对象关系映射**（ORM）中。

拿 Django 举例。Django 的 ORM  允许你这样定义与数据库映射的模型：

```python
class Person(models.Model):
    name = models.CharField(max_length=30)
    age = models.IntegerField()
```

如果你试图赋值并取得模型中的值：

```python
person = Person(name='bob', age=35)

print(person.age)
# 输出:
# 35
```

这不是很奇怪吗？ `age` 属性不管是赋值还是取值，都是一个普通的整型 `int` 。但在 `Person` 类中定义时它明明指定的是 `IntegerField` 对象，甚至还可以直接从数据库里取到 `age` 的值。

原因就是在于 `models.Model` 中定义的元类（以及其他辅助方法），将背后的复杂逻辑转化成了非常简单的语句，方便了框架的使用者。

## 写在最后

就如文章最开始说的，与其使用元类这种晦涩又容易出错的工具，大部分开发者至少有三种更好的替代方案：

- 继承
- 猴子补丁
- 装饰器

90% 的情况下，你其实根本不需要动态修改类。

如果真的需要，那么 99% 的情况下，你不应该用元类，而是用上述的几种方法。

尽管如此，理解元类是有益的，可以让你对 Python 的理解更深刻，并且可以意识到何时它才应该成为你的工具。

---

本文参考：

- [Python Metaclasses](https://realpython.com/python-metaclasses/)
- [SO](https://stackoverflow.com/questions/100003/what-are-metaclasses-in-python)
- [Understanding Python Metaclass](https://lotabout.me/2018/Understanding-Python-MetaClass/)

> 作者杜赛，Python 科普写手，著有 [Django搭建个人博客](https://www.dusaiphoto.com/topic/) 等系列教程。