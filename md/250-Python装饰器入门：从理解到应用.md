**装饰器（Decorator）**是 Python 非常重要的组成部分，它可以修改或扩展其他函数的功能，并让代码保持简短。

装饰器对初学者来说，理解起来有些困难。

因此，让我们从 Python 最基础的知识讲起。

## 一切皆对象

在 Python 中，**函数可以根据给定的参数返回一个值**：

```python
def hello(name):
    return 'Hello ' + name

print(hello('Bob'))

# 输出:
# Hello Bob
```

与 Python 的其他对象（如字符串、整数、列表等）一样，**函数也是对象**，也可以赋值给一个变量：

```python
def hello(name):
    return 'Hello ' + name

h = hello

print(hello)
# 输出:
# <function hello at 0x0000021A94EF1790>

print(h)
# 输出:
# <function hello at 0x0000021A94EF1790>

print(h('Jack'))
# 输出:
# Hello Jack
```

可以看到 `hello` 和 `h` 都指向同一个函数，而函数后加括号 `h('Jack')` 是对其进行了调用。

## 函数作为参数

既然函数是对象，那么当然也可以和其他 Python 对象一样，作为参数传递到另一个函数中去。

这种以其他函数作为参数的函数，又被称为**高阶函数**。

比如下面这个：

```python
def hi(func):
    name = func()
    print('Hi ' + name)
    
def bob():
    return 'Bob'

hi(bob)

# 输出:
# Hi Bob
```

注意 `bob` 函数作为参数时并没有被调用（没加括号），而是作为函数被传递到 `hi` 函数里，才在 `name = func()` 这里被真正调用的。

## 函数里的函数

除此之外，函数里面还可以定义函数：

```python
def hi():
    def bob():
        return 'Bob'
    print('Hi ' + bob())

hi()
# 输出:
# Hi Bob
```

此时的 `bob` 函数的作用域在 `hi` 之内的。如果在全局调用 `bob()` 会引发错误：

```python
>>> bob()
NameError: name 'bob' is not defined
```

## 函数作为返回值

很自然的，函数也可以作为其他函数的返回值，比如：

```python
def cook():
    def tomato():
        print('I am Tomato')
        
    return tomato

t = cook()
t()
# 输出:
# I am Tomato
```

函数可以作为参数、返回值，也可以内部定义。感觉很自然，对吧。

## 组合运用

接下来我们把前面的所有知识组合一下，像这样：

```python
def outer(func):
    def inner():
        print('Before func()..')
        func()
        print('After func()..')
    return inner


def hi():
    print('Hi World')


h = outer(hi)
h()

# 输出:
# Before func()..
# Hi World
# After func()..
```

- 函数 `outer` 的参数是函数 `hi` 
- `outer` 的返回值是函数 `inner`
- `hi` 在 `inner` 中进行了调用

`h = outer(hi)` 将 `outer` 的返回值（即 `inner` 函数）赋值给了 `h` 。

如果你不想赋值也可以，连起来写就是 `outer(hi)()` ，执行的效果是完全相同的。

**这就是一个简单的装饰器了！**

原函数 `hi` 的功能不变，但又成功附加了两行打印的语句。

## 你的第一个装饰器

把上面的代码修改为**装饰器**的写法：

```python
def outer(func):
    def inner():
        print('Before func()..')
        func()
        print('After func()..')
    return inner

@outer
def hi():
    print('Hi World')


hi()

# 输出:
# Before func()..
# Hi World
# After func()..
```

实际上 `@outer` 就等同于下面这一句：

```python
hi = outer(hi)
```

啊，这糖真甜。

## 装饰器的返回值

有时候原函数具有返回值，如果套用前面的装饰器：

```python
def outer(func):
    def inner():
        func()
    return inner

@outer
def one():
    return 1
    
print(one())

# 输出:
# None
```

因为装饰器返回的 `inner` 函数是不具有返回值的，因此原本函数的返回值就被”吃“掉了。

要解决此问题，就需要让 `inner` 函数把原函数的返回值丢出来，像这样：

```python
def outer(func):
    def inner():
        return func()
    return inner

@outer
def one():
    return 1
    
print(one())

# 输出:
# 1
```

## 带参数的原函数

原函数有可能带有参数：

```python
def outer(func):
    def inner():
        return func()
    return inner

@outer
def haha(name):
    return 'Haha ' + name
```

不幸的是，这样调用会报错：

```python
print(haha('Bob'))

>>> TypeError: inner() takes 0 positional arguments but 1 was given
```

你可以给 `inner` 函数加一个参数，但这样又不能适用无参数的函数了：

```python
def outer(func):
    def inner(name):
        return func(name)
    return inner

@outer
def haha(name):
    return 'Haha ' + name
    
@outer
def hehe():
    return 'Hehe'

print(haha('Bob'))
# 输出:
# Haha Bob

print(hehe())
# 输出报错:
# TypeError: inner() missing 1 required positional argument: 'name'
```

好在 Python 有 `*args` 和 `**kwargs` 可以接收任意数量的位置参数和关键字参数。

正确的解决方案是这样：

```python
def outer(func):
    def inner(*args, **kwargs):
        return func(*args, **kwargs)
    return inner

@outer
def haha(name):
    return 'Haha ' + name
    
@outer
def hehe():
    return 'Hehe'


print(haha('Bob'))
# 输出:
# Haha Bob

print(hehe())
# 输出:
# Hehe
```

## 你是谁

Python 具有强大的 **自省能力**， 即对象在运行时了解自身属性的能力。

比如，函数知道自己的**名字**：

```python
def my_func():
    pass

print(my_func.__name__)

# 输出:
# my_func
```

但是由于装饰器包装后的返回值是 `inner` 函数，因此函数的身份就变得混乱了：

```python
def outer(func):
    def inner(*args, **kwargs):
        return func(*args, **kwargs)
    return inner

@outer
def my_func():
    pass

print(my_func.__name__)
# 输出:
# inner
```

虽然是正确的，但是却不怎么有用。大多数时候我们关心的是原函数的内在属性，特别是对于依赖函数签名的原函数。

好在 Python 有内置的解决方案：

```python
import functools

def outer(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        return func(*args, **kwargs)
    return inner

@outer
def my_func():
    pass

print(my_func.__name__)

# 输出:
# my_func
```

甚至解决方案本身就是个 `@wraps()`  装饰器。

具体实现就不用你过多操心了，总之函数的身份又修改正确了。

## 这里要考，划重点

经过上述一顿折腾，现在可以总结出一个非常**标准的装饰器模板**了：

```python
import functools

def decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 原函数运行前
        # Do something
        value = func(*args, **kwargs)
        # 原函数运行后
        # Do something
        return value
    return wrapper
```

你可以在这个模板的基础上，衍生出功能复杂的装饰器。

## 一些例子

### 打印日志

装饰器非常经典的应用就是打印日志，比如打印时间、地点、访问记录等等。

拿前面的打印函数名举例：

```python
import functools

def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print('Calling: ' + func.__name__)
        return func(*args, **kwargs)
    return wrapper
    
@log
def some_func():
    pass

some_func()

# 输出:
# Calling: some_func
```

### 计时器

一个简易的计时器装饰器：

```python
import functools
import time

def time_it(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        #
        value = func(*args, **kwargs)
        #
        end = time.perf_counter()
        duration = end - start
        print(f'Duration: {duration}')
        return value
    return wrapper

@time_it
def another_func():
    time.sleep(1)

another_func()

# 输出:
# Duration: 1.004140400000324
```

### 减缓代码

下面这个装饰器可以让函数运行得更慢：

```python
import functools
import time

def slow_down(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        time.sleep(3)
        value = func(*args, **kwargs)
        print('Done.')
        return value
    return wrapper

@slow_down
def a_func():
    pass
```

为什么我要让代码运行得更慢？这样才方便以后帮雇主优化执行效率啊（这句划掉），也用于测试时模拟网络的卡顿环境。

总之装饰器的用法可以非常的花式，取决于你的业务需求。

下面让我们继续深入。

## 装饰器的参数

有的时候装饰器本身也需要接收参数，从而配置为不同的状态，比如打印日志时附带当前的用户名。

于是装饰器可能就变成了这样：

```python
@logit(name='Dusai')
...
```

但你要记得，不管怎么变化，**装饰器必须返回一个函数**。既然这里的装饰器多了一对括号，那就是多了一层调用，所以必须在之前无参数的情况下再增加一层的函数嵌套，也就是**三层嵌套的函数**：

```python
import functools

def logit(name):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            value = func(*args, **kwargs)
            print(f'{name} is calling: ' + func.__name__)
            return value
        return wrapper
    return decorator
    
@logit(name='Dusai')
def a_func():
    pass

a_func()

# 输出:
# Dusai is calling: a_func
```

上面这个装饰器等效于：

```python
a_func = log(name='Dusai')(a_func)
```

开始有点烧脑了吧。

## 类作为装饰器

虽然前面例子里的装饰器都是函数，但是装饰器语法其实**并不要求**本身是函数，而只要是一个**可调用对象**即可。

既然如此，那我只要在**类**里实现了 `__call__()` 方法，岂不是类实例也可以做装饰器？

还是上面那个 `@logit()` 装饰器，试一下用类来实现：

```python
import functools

class Logit():
    def __init__(self, name):
        self.name = name
        
    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            value = func(*args, **kwargs)
            print(f'{self.name} is calling: ' + func.__name__)
            return value
        return wrapper

@Logit(name='Dusai')
def a_func():
    pass

a_func()

# 输出:
# Dusai is calling: a_func
```

万变不离其宗，感受一下。

## 闭包与装饰器

通常来说，函数中的变量为**局部变量**，一但函数执行完毕，其中的变量就不可用了：

```python
def cook():
    food = 'apple'
    
cook()
print(food)
# 输出报错:
# NameError: name 'food' is not defined
```

但同样的情况到了**高阶函数**这里，就有点不对劲了。

```python
def cook():
    food = 'apple'
    def wrapper():
        print(food)
    return wrapper

value = cook()
value()
# 输出:
# apple
```

你发现 `cook()` 函数执行之后，按道理来说 `food` 变量就应该被销毁掉了。但实际上没有任何报错， `value()` 顺利的输出了 food 的值。

高阶函数中的内层函数携带外层函数中的参数、变量及其环境，一同存在的状态（即使已经离开了创造它的外层函数）被称之为**闭包**。被携带的外层变量被称为**自由变量**，有时候也被形容为外层变量被闭包**捕获**了。

发现没有，装饰器就是个天然的闭包。

## 带状态的装饰器

既然**装饰器就是闭包**，那么其中的**自由变量**就不会随着原函数的返回而销毁，而是伴随着原函数一直存在。利用这一点，装饰器就可以携带状态。

用下面这个计数器来理解一下：

```python
import functools
    
def counter(func):
    count = 0
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal count
        count += 1
        print(count)
        return func(*args, **kwargs)
    return wrapper

@counter
def whatever():
    pass

whatever()
whatever()
whatever()

# 输出:
# 1
# 2
# 3
```

通常闭包可以**使用**自由变量，但是不能**修改**其值。因此这里用 `nonlocal` 表明 `count` 不是内层函数的局部变量，并优先在与闭包作用域最近的自由变量中寻找 `count` 变量。

另一种带状态装饰器的解决方案是利用内层函数的属性：

```python
import functools
    
def counter(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.count += 1
        print(wrapper.count)
        return func(*args, **kwargs)
    wrapper.count = 0
    return wrapper
    
@counter
def whatever():
    pass
```

如果你的状态非常的复杂，那么可以考虑用**类装饰器**：

```python
class Counter():
    def __init__(self, start):
        self.count = start
        
    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            self.count += 1
            print(self.count)
            return func(*args, **kwargs)
        return wrapper

@Counter(start=0)
def whatever():
    pass
```

效果都差不多。

## 类的装饰器

实际上，装饰器不仅可以作用于函数，同样也可以作用于类：

```python
import functools

def logit(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print('-' * 10)
        print('Calling: ' + func.__name__)
        value = func(*args, **kwargs)
        print('-' * 10)
        return value
    return wrapper

@logit
class Tester():
    def __init__(self):
        print('__init__ ended')
    
    def a_func(self):
        print('a_func ended')
```

只不过效果可能和你预想的不太一样罢了：

```python
tester = Tester()
tester.a_func()

# 输出
# ----------
# Calling: Tester
# __init__ ended
# ----------
# a_func ended
```

**装饰器只在类实例化的时候起了效果**，而在调用其内部方法时并没有作用。

比较适合的用法是用装饰器实现**单例模式**：

```python
import functools

def singleton(cls):
    """使类只有一个实例"""
    @functools.wraps(cls)
    def wrapper(*args, **kwargs):
        if not wrapper.instance:
            wrapper.instance = cls(*args, **kwargs)
        return wrapper.instance
    wrapper.instance = None
    return wrapper

@singleton
class OnlyOne:
    pass

first = OnlyOne()
second = OnlyOne()

print(id(first))
# 输出: 1964238157376
print(id(second))
# 输出: 1964238157376
```

不过单例模式在 Python 中并没有其他语言中那么常见。

如果你想类中的方法也附加装饰器的功能，只需要直接在方法上放置装饰器即可：

```python
import functools

def logit(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print('-' * 10)
        print('Calling: ' + func.__name__)
        value = func(*args, **kwargs)
        print('-' * 10)
        return value
    return wrapper

class Tester():
    def __init__(self):
        print('__init__ ended')
    
    @logit
    def a_func(self):
        print('a_func ended')

tester = Tester()
tester.a_func()
# 输出:
# __init__ ended
# ----------
# Calling: a_func
# a_func ended
# ----------
```

## 叠加装饰器

装饰器可以叠加使用，像下面这样：

```python
import functools

def inc(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print('+' * 10)
        value = func(*args, **kwargs)
        print('+' * 10)
        return value
    return wrapper

def dec(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print('-' * 5)
        value = func(*args, **kwargs)
        print('-' * 5)
        return value
    return wrapper


@inc
@dec
def printer():
    print('I am here!')

printer()

# 输出:
# ++++++++++
# -----
# I am here!
# -----
# ++++++++++
```

上面的语法相当于：

```python
printer = inc(dec(printer))
```

这时候装饰器之间的顺序非常重要。

如果把两个装饰器位置互换：

```python
@dec
@inc
def printer():
    print('I am here!')

printer()

# 输出:
# -----
# ++++++++++
# I am here!
# ++++++++++
# -----
```

输出顺序改变，说明执行的顺序也改变了。

## 总结

以上就是**装饰器入门**所需的全部知识了：

- 装饰器是闭包的一种应用，是返回值为函数的高阶函数；
- 装饰器修饰可调用对象，也可以带有参数和返回值；
- 装饰器中可以保持状态。

复杂的理论是建立在简单的规则之上的。 Python 的学习者们切忌浮躁，练好九阴真经，方得万剑归宗。

---

本文参考：

- [Primer on Python Decorators](https://realpython.com/primer-on-python-decorators/#conclusion)
- [Python Decorators](https://www.programiz.com/python-programming/decorator)

> 作者杜赛，Python科普写手，著有 [Django搭建博客](https://www.dusaiphoto.com/topic/) 等系列教程。
