Python 中的**生成器**（Generator）是十分有用的工具，它能够方便地生成迭代器（Iterator）。

这篇文章就来说说什么是生成器，它有什么作用以及如何使用。

## 普通函数

Python 中的普通函数通常是这样的：

```python
def normal():
    print('Before return..')
    return 1
```

函数里的语句将依次执行，并在遇到 `return` 时**立即终止**函数的运行并返回值。

因此，像下面这样连续写多个 `return` 是没有意义的：

```python
def normal():
    print('Before return..')
    return 1
    # 下面语句永远不会被执行
    print('After return..')
    return 2
```

## 生成器函数

把普通函数修改为生成器函数很简单，只需要把 `return` 替换成 `yield` 就行了，像这样：

```python
def gen():
    print('yield 1..')
    yield 1

    print('yield 2..')
    yield 2
    
    print('yield 3..')
    yield 3
```

试着来用用这个生成器：

```python
>>> gen = my_gen()
>>> gen
<generator object my_gen at 0x000002102AC5EAC0>
```

可以看到，`gen` 变量被赋值为一个 `generator` ，即生成器。

生成器有一个最重要的特点，即当它执行到 `yield` 语句并返回后，生成器不会被立即终止，而是暂停在当前 `yield` 的位置，等待下一次调用：

```python
>>> next(gen)
yield 1..

>>> next(gen)
yield 2..

>>> next(gen)
yield 3..

>>> next(gen)
Traceback (most recent call last):
  File "<ipython-input-34-6e72e47198db>", line 1, in <module>
    next(gen)
StopIteration
```

生成器用 `next()` 函数调用，每次调用都从上一次 `yield` 暂停的位置，继续向下执行。

当所有的 `yield` 执行完毕后，再一次调用 `next()` 就会抛出 `StopIteration` 错误，提示你生成器已经结束了。

既然会抛出错误，那就需要处理错误。用 `try` 语句完善一下就有：

```python
def my_gen():
    print('yield 1..')
    yield 1
    print('yield 2..')
    yield 2
    print('yield 3..')
    yield 3

gen = my_gen()
while True:
    try:
        next(gen)
    except StopIteration:
        print('Done..')
        break

# 输出:
# yield 1..
# yield 2..
# yield 3..
# Done..
```

## 迭代

`next()` 调用太啰嗦，通常我们用迭代的方式获取生成器的值：

```python
def my_gen():
    yield 1
    yield 2
    yield 3

gen = my_gen()
for item in gen:
    print(item)

# 输出:
# 1
# 2
# 3
```

`for` 语句不仅简洁，还自动帮我们处理好了生成器的终止。

以上就是生成器的的基础知识了。下面看几个它的应用。

## 读取大文件

假设你需要读取并处理数据流或大文件（比如 txt/csv 文件），可能会这么写：

```python
def csv_reader(file_name):
    file = open(file_name)
    result = file.read().split("\n")
    return result
```

通常这都是没啥问题的。但如果这个文件非常非常大，那么将会得到内存溢出的报错：

```python
Traceback (most recent call last):
  ...
  File "...", line 6, in csv_reader
    result = file.read().split("\n")
MemoryError
```

原因就在 `file.read().split("\n")` 一次性将所有内容加载到内存中，导致溢出。

解决此问题，用生成器可以这么写：

```python
def csv_reader(file_name):
    for row in open(file_name, "r"):
        yield row
```

由于这个版本的 `csv_reader()` 是个生成器，因此你可以通过遍历，加载一行、处理一行，从而避免了内存溢出的问题。

## 无限序列

理论上存储无限序列需要无限的空间，这是不可能的。

但是由于生成器一次只生成一个值，因此它可用于表示无限数据。（理论上）

比如生成所有偶数：

```python
def all_even():
    n = 0
    while True:
        yield n
        n += 2
        
even = all_even()
for i in even:
    print(i)
```

这个程序将无限的运行下去，直到你手动打断它。

## 优化内存

假设你需要 1 到 10000 的序列，考虑用列表和生成器两种形式保存它：

```python
def gen():
    for x in range(10000):
        yield x

# 生成器
my_gen = gen()
# 列表
my_list = [x for x in range(10000)]
```

来比较下它两的大小：

```python
>>> import sys

>>> sys.getsizeof(my_list)
87616
>>> sys.getsizeof(my_gen)
112
```

生成器有点像只是保存一个公式而已。而列表是老老实实的把数据计算并保存了。

实际上，生成器还有一种更简单的写法，像这样：

```python
# 列表推导式
my_list = [x for x in range(10000)]

# 生成器表达式
my_gen  = (x for x in range(10000))
```

它与列表推导式的区别就在于是用圆括号。

需要说明的是，通常生成器的迭代速度会比列表更慢。这在逻辑上也说得通，毕竟生成器的值需要即时计算，而列表的值摆在那就能用。空间和时间，根据情况选用。

## 生成器组合

有时候你需要把两个生成器组合成一个新的生成器，比如：

```python
gen_1 = (i for i in range(0,3))
gen_2 = (i for i in range(6,9))

def new_gen():
    for x in gen_1:
        yield x
    for y in gen_2:
        yield y

for x in new_gen():
    print(x)

# 输出:
# 0
# 1
# 2
# 6
# 7
# 8
```

这种组合迭代的形式不太方便，因此 Python 3.3 引入新语法 `yield from` 后，可以改成这样：

```python
def new_gen():
    yield from gen_1
    yield from gen_2
```

它代替了 `for` 循环，迭代并返回生成器的值。

> `yield from` 感觉上像是语法糖，不过它主要的应用场景是在协程中，这里就不展开探讨了。

## 生成器进阶语法

### 使用 .send()

既然生成器允许我们暂停控制流并返回数据，那么就有可能需要将某些数据传回生成器。数据交流总是双向的嘛。

举个例子：

```python
def gen():
    count = 0
    while True:
        count += (yield count)
```

`yield` 变成个表达式了，并且可以通过 `.send()` 传回数据：

```python
>>> g = gen()
>>> g.send(None)
0
>>> g.send(1)
1
>>> g.send(2)
3
>>> g.send(5)
8
```

稍微要注意的是首次调用时，必须要先执行一次 `next()` 或者 `.send(None)` 使生成器到达 `yield` 位置。

### 使用 .throw()

`.throw()` 允许用生成器抛出异常，像这样：

```python
def my_gen():
    count = 0
    while True:
        yield count
        count += 1
        
gen = my_gen()
for i in gen:
    print(i)
    if i == 3:
        gen.throw(ValueError('The number is 3...'))
        
# 输出:
# 0
# 1
# 2
# 3
# ValueError: The number is 3...
```

这在任何需要捕获异常的领域都很有用。

### 使用 .close()

`.close()` 可以停止生成器，比如把上面的例子改改：

```python
def my_gen():
    count = 0
    while True:
        yield count
        count += 1
        
gen = my_gen()
for i in gen:
    print(i)
    if i == 3:
        gen.close()
```

这次就不会抛出异常了，而是在迭代完数字 3 之后，生成器就顺利地停止了。

## 结论

以上就是生成器的大致介绍了。它可以暂停控制流，并在你需要的时候随时回到控制流，从上一次暂停的位置继续执行。

生成器有助于你处理大型数据流或者表达无限序列，是生成迭代器的有用工具。

---

参考链接：

- [Python Generators](https://www.programiz.com/python-programming/generator)
- [How to Use Generators and yield in Python](https://realpython.com/introduction-to-python-generators/)

> 作者杜赛，Python 科普写手，著有 [Django搭建个人博客](https://www.dusaiphoto.com/topic/) 等系列教程。
