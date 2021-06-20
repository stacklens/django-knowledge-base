Python 中的**生成器**（Generator）是十分有用的工具，它能够方便地生成迭代器（Iterator）。

这篇文章就来说说什么是生成器，它有什么作用以及如何使用。

## 普通函数

Python 中的普通函数通常是这样的：

```python
def normal():
    print('Before return..')
    return 1
```

函数里的语句将依次执行，并在遇到 `return` 时立即终止函数的运行并返回值。

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

可以看到，`gen` 变量为 `generator` ，即生成器。

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

