**闭包**（Closure）是 Python 中一个重要的工具。

对于初学者来说，闭包是比较难懂的概念。因此让我们从 Python 基础开始，逐步理解闭包。

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

## 函数里的函数

同时，函数里面还可以定义函数：

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

函数可以作为返回值，也可以内部定义。这种在函数里传递、嵌套、返回其他函数的情况，称之为**高阶函数**。

> 除此之外，函数还可以作为其他函数的参数。

## 闭包与自由变量

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

甚至于，即使将 `cook()` 函数销毁了，`food` 的值都还存在：

```python
def cook():
    food = 'apple'
    def wrapper():
        print(food)
    return wrapper

value = cook()

# 删除原函数
del cook

value()
# 输出:
# apple
```

高阶函数中，内层函数携带外层函数中的参数、变量及其环境，一同存在的状态（即使已经离开了创造它的外层函数）被称之为**闭包**。被携带的外层变量被称为**自由变量**，有时候也被形容为外层变量被闭包**捕获**了。

理解了上面这段话，那么恭喜你，你已经理解闭包的大部分内容了。

为了把整个事情讲得更清楚，让我们继续深入。

## 参数捕获

很多时候，我们希望闭包所捕获的自由变量可以根据不同的情况有所区分。

很简单，把它作为外层函数的参数就可以了：

```python
def cook(name):
    def wrapper():
        print('I am cooking ' + name)
    return wrapper


apple = cook('apple')
pear = cook('pear')

apple()
# 输出: I am cooking apple
pear()
# 输出: I am cooking pear
```

你看，外层函数的参数也可以成为自由变量，被封装到内层函数所在的环境中。

这种局部变量起作用的特定环境，有时候被称为**作用域**或者**域**。

## 函数生成

既然外层函数可以携带参数，那被返回的内层函数当然也可以带参数：

```python
def outer(x):
    def inner(y):
        print(x + y)
    return inner

outer(1)(2)
# 输出:
# 3
```

看到两个括号就代表进行了两次函数调用。第一个括号对应 `outer` 的参数 `x` ，第二个括号里对应 `inner` 的参数 `y`。

因此，利用闭包携带参数并返回函数的这个特性，可以很方便的在一个底层的函数框架上，组装出不同的功能。

比如：

```python
def add(x):
    def inner(y):
        print(x + y)
    return inner

add_one = add(1)
add_ten = add(10)

add_one(5)
# 输出:
# 6
add_ten(5)
# 输出:
# 15
```

外层函数传递的参数甚至可以是个函数。你可以想象能玩出多少花样。

## 状态持有

闭包中的自由变量有两个神奇的特性。

第一个特性是，自由变量在闭包存在的期间，其中的值也会一直存在。因此闭包可以持有**状态**。

举个栗子：

```python
# 记录每次取得的分数
def make_score():
    lis = []
    def inner(x):
        lis.append(x)
        print(lis)
    return inner

score = make_score()

score(82)
score(66)
score(100)
# 输出:
# [82]
# [82, 66]
# [82, 66, 100]
```

可以看出 `score` 闭包打印的列表记录了每次调用的结果。

另一个特性是，闭包与闭包之间的状态是**隔离**的。

还是举个栗子：

```python
def make_score():
    lis = []
    def inner(x):
        lis.append(x)
        print(lis)
    return inner

first = make_score()
second = make_score()

first(1)
first(2)
# 输出:
# [1]
# [1, 2]

second(3)
second(4)
# 输出:
# [3]
# [3, 4]
```

以上两个特性，使得闭包像一个微型的类，因为状态持有和数据隐藏是类的基本功能嘛。

它两在使用上的建议是：如果你的状态比较简单，那么可以用闭包来实现；相反则使用类。

## 不变量状态

在上面的例子里，闭包用 `lis.append()` 直接操作了自由变量。

但如果要操作的自由变量是个**不变量**，比如数值型、字符串等，那么记得加 **nonlocal** 关键字：

```python
# 记录成绩总分
def make_score():
    total = 10
    def inner(x):
        nonlocal total
        total += x
        print(total)
    return inner

total = make_score()
total(5)
# 输出:
# 15
```

此关键字就是在告诉解释器：接下来的 `total` 不是本函数里的局部变量，你最好去闭包或是别的地方找找。

## 延迟陷阱

有个跟闭包相关的常见陷阱：

```python
funcs = []
for i in range(3):
    def inner():
        print(i)
    funcs.append(inner)
        
funcs[0]()
funcs[1]()
funcs[2]()
# 输出:
# 2
# 2
# 2
```

直觉上好像应该输出 `0, 1, 2` ，但实际上是 `2, 2, 2` 。这是因为函数 `inner` 是延迟执行的，直到真正调用前，都是没进行内部操作的。

加上这句就清楚了：

```python
funcs = []
for i in range(3):
    def inner():
        print(i)
    funcs.append(inner)

print(f'i is: {i}')
# 输出:
# i is: 2
funcs[0]()
funcs[1]()
funcs[2]()
# 输出:
# 2
# 2
# 2
```

解决方案就是用闭包将 `i` 的值立即捕获：

```python
funcs = []
for i in range(3):
    def outer(a):
        def inner():
            print(a)
        return inner
    funcs.append(outer(i))

print(f'i is: {i}')
funcs[0]()
funcs[1]()
funcs[2]()
# 输出:
# i is: 2
# 0
# 1
# 2
```

对闭包的概念讲解基本上就这样。

接下来继续补充点闭包的常见应用。

## 组合函数

在上面**[函数生成]**的章节中，我们已经体验过利用闭包捕获参数、从而生成新函数的能力了。

更棒的是，被捕获的参数也可以是函数。

比如说，可以用闭包实现函数的拼接：

```python
# 这个函数是重点
def compose(g, f):
    def inner(*args, **kwargs):
        return g(f(*args, **kwargs))
    return inner

# 被拼接函数1
def remove_first(lis):
    return lis[1:]

# 被拼接函数2
def remove_last(lis):
    return lis[:-1]

# 这里进行了函数的合成
middle = compose(remove_first, remove_last)
new_lis = middle([1, 2, 3, 4, 5])

print(new_lis)
# 输出:
# [2, 3, 4]
```

很方便的用两个简单的函数，合成出更复杂一点的新函数，提高代码复用的能力。

## 柯里化

最后，让我们来看个更复杂的应用：

```python
# 柯里化闭包函数
def curry(f):
    argc = f.__code__.co_argcount
    f_args = []
    f_kwargs = {}
    def g(*args, **kwargs):
        nonlocal f_args, f_kwargs
        f_args += args
        f_kwargs.update(kwargs)
        if len(f_args)+len(f_kwargs) == argc:
            return f(*f_args, **f_kwargs)
        else:
            return g
    return g


# 无关紧要的原函数
def add(a, b, c):
    return a + b + c

# c_add 是被柯里化的新函数
c_add = curry(add)
```

执行上面的代码后， `c_add` 这个函数就**非常魔性**了。来看看效果。

首先，原函数 `add` 必须接收3个参数，否则就会报错：

```python
>>> add(1,2,3)
6
>>> add(1)
TypeError: add() missing 2 required positional arguments: 'b' and 'c'
```

但是 `c_add` 是很有想法的函数，它居然可以**只接收部分参数**！

试一试，只提供一个参数：

```python
>>> c_add(1)
<function __main__.curry.<locals>.g(*args, **kwargs)>
```

没报错。

接着输入第二个参数：

```python
>>> c_add(2)
<function __main__.curry.<locals>.g(*args, **kwargs)>
```

然后输入最后一个参数：

```python
>>> c_add(3)
6
```

参数集齐后，终于得到了正确的结果。神奇吧。

像 `c_add` 这种函数，可以只接收一部分的参数（通常是每次只接收一个参数），并返回一个携带状态的新函数的函数，称为它被**柯里化**了。

前面已经多次说过了，更棒的是这些参数也可以是函数。

因此在有的函数式编程语言中，柯里化函数就像接龙一样，把很多简单函数组合为一个复杂的函数，比如在 Haskell 中：

```python
fn = ceiling . negate . tan . cos . max 50
```

这种被称为**无值风格**，有助于清晰表达函数的意义，以及将复杂问题分解为简单问题。

> 柯里化和无值风格又是另一个大题目了。有兴趣的读者可以在评论区告诉我，是否要开一篇新文章探讨。

扯远了。让我们回到上面那个实现柯里化的 `curry` 函数的逻辑：

- 它返回一个闭包，并且将闭包接收到的参数记录在自由变量中
- 如果当前参数过少，则返回一个继续接收参数的新函数
- 如果当前参数足够，则执行原函数并返回结果

## 结论

总结一下闭包的几个特性：

- 它是一个嵌套函数
- 它可以访问外部作用域中的自由变量
- 它从外层函数返回

闭包的应用多样，但基本都是利用了其能够捕获自由变量的特点。除了以上所列举的以外，闭包另一个重要的应用就是**装饰器**。我写过一篇详细的[装饰器入门](https://www.dusaiphoto.com/article/139/)的文章，读者可结合闭包一起理解，也欢迎和我探讨。

---

本文参考：

- [Python Closures](https://www.programiz.com/python-programming/closure)
- [Closures and Decorators in Python](https://towardsdatascience.com/closures-and-decorators-in-python-2551abbc6eb6)

> 作者杜赛，Python科普写手，著有 [Django搭建博客](https://www.dusaiphoto.com/topic/) 等系列教程。
