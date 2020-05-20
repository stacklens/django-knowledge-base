如果你不熟悉 Web 开发，那你可能很难理解数据迁移为什么是一个强力的功能。

## 对象关系映射

通俗的讲，数据库是你存放数据的地方（废话）。关系型数据库又是数据库中的一种，其中的数据以表的形式组织，表具有一定数量的列、任意数量的行，每张表又可以通过外键连接其他的表。

表中每列都有特定的数据类型，这就是 Django 里常说的字段了。每一行就是表中的一条数据。比如下面这个：

| id(integer) | title(string) | created(datetime)   |
| ----------- | ------------- | ------------------- |
| 1           | Django        | 2020-05-09 07:57:50 |
| 2           | vs            | 2020-05-10 09:58:05 |
| 3           | Flask         | 2020-05-17 17:00:13 |
| ...         | ...           | ...                 |

关系型数据库的增删改查等操作，需要用到的是 SQL 语言。Django 为了保护程序员的头发，附带了一个对象关系映射器（简称 ORM），可以将数据库 SQL 映射到面向对象的 Python 中来，使得你可以在 Django 中像操作普通对象一样操作数据库。其直观表现就是模型 （Model）。

上面的表写成模型长这样：

```python
class Post(models.Model):
    # id 字段不需要自己写
    title = models.TextField()
    created = models.DateTimeField()
```

但是定义好了模型，数据库中的表并不会神奇的出现，你还需要把模型转化为对数据库的操作，这就是迁移 Migrations。

## 迁移工作流

新建一个项目，并在项目中创建一个叫 `mig` 的 app。

然后必须在 `INSTALLED_APPS` 配置中添加 `mig` ，并且 `mig` 还得带有 `migrations/` 目录以及目录下的 `__init__.py` 文件，否则 Django 不会为这个 app 创建任何迁移。

在 `models.py` 中创建如下模型：

```python
# mig/models.py

from django.db import models
from django.utils import timezone

class Pen(models.Model):
    price = models.IntegerField()
    color = models.CharField(default='black', max_length=20)
    purchase_date = models.DateTimeField(default=timezone.now)
```

具有价格、颜色、购买日期的笔，很合理。

接下来在命令行执行 `makemigrations` 指令：

```python
> python manage.py makemigrations
# 下面是输出
Migrations for 'mig':
  mig\migrations\0001_initial.py
    - Create model Pen
Following files were affected 
 D:\...\mig\migrations\0001_initial.py
```

如上面的输出文字所述，指令执行完毕后会生成 `mig/migrations/0001_initial.py` 文件。来看看这个文件的内容：

```python
from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):
    initial = True
    
    dependencies = []
    
    operations = [
        migrations.CreateModel(
            name='Pen',
            fields=[
                ('id', models.AutoField(...')),
                ('price', models.IntegerField()),
                ('color', models.CharField(...)),
                ('purchase_date', models.DateTimeField(...)),
            ],
        ),
    ]
```

就是一个普通的 Python 文件嘛：

- `initial` ：初次迁移。
- `dependencies`：因为是初次迁移，没有依赖项，所以这里为空。
- `operations`：迁移的具体操作就在这里了。`CreateModel` 表示创建新表，`name` 即表名，`fields` 则是表中的字段。

注意这个时候数据库是没有变化的。直到执行了 `migrate` 指令：

```python
> python manage.py migrate
# 下面是输出
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, mig, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
  Applying mig.0001_initial... OK  # mig 的迁移
  ...
```

输出中似乎有很多不认识的迁移，不要虚，那些是 Django 自身运行所需要的表。关键是这个 `Applying mig.0001_initial... OK`，表示 `mig` 的迁移已经成功了。

打开数据库可以看到多了 `mig_pen` 表，并且里面的字段和模型是完全匹配的。

## 迁移文件

初次迁移完成后，你突然发现 `price` 字段不应该为整型，以便正确表示带小数的金额：

```python
class Pen(models.Model):
    price = models.DecimalField()
    ...
```

执行完迁移后，又多出了 `mig\migrations\0002_auto_20200519_1659.py` 文件：

```python
class Migration(migrations.Migration):
    dependencies = [
        ('mig', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pen',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=7),
        ),
    ]
```

此时 `dependencies` 列表不再为空了，里面是本次迁移所依赖的文件，即第一次迁移的 `0001_initial.py` 。由此的注意事项：

- `migrations` 目录下的迁移文件非常重要并且**相互依赖**，一般情况下不要随意去修改（虽然 Django 允许你手动维护）。
- 通常情况下，对数据库的操作尽可能通过迁移的方式。如果因为某些原因需要手动修改，那么你需要做好手动维护的准备。

继续回到代码。 `operations` 列表中的 `AlterField` 表示这次是更改操作。Django 内部有一套机制来尽可能的判断用户对模型的操作的具体类型，但是如果你一次进行了很多复杂的改动（比如同时进行多项修改、删除、新增），那么它也会犯糊涂，不知道你想干什么。为了避免这种尴尬的事情，对数据库下手不要太重哦。

再修改模型试试：

```python
class Pen(models.Model):
    price = models.DecimalField(max_digits=7, decimal_places=2)
    # 我不想要 color 字段了
    # color = models.CharField(default='black', max_length=20)
    purchase_date = models.DateTimeField(default=timezone.now)
```

新增的迁移文件如下：

```python
# 0003_remove_pen_color.py

class Migration(migrations.Migration):
    dependencies = [
        ('mig', '0002_auto_20200519_1659'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pen',
            name='color',
        ),
    ]

```

你可以更清楚的看出迁移文件的工作模式了，即每个迁移文件记录的仅仅是和上一次的变化，每一次对数据库的操作是高度依赖的。

你还可以通过指令查看迁移文件将实际执行的 SQL 操作：

```python
> python manage.py sqlmigrate mig 0003
...
BEGIN;
--
-- Remove field color from pen
--
CREATE TABLE "new__mig_pen" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "price" decimal NOT NULL, "purchase_date" datetime NOT NULL);
INSERT INTO "new__mig_pen" ("id", "price", "purchase_date") SELECT "id", "price", "purchase_date" FROM "mig_pen";
DROP TABLE "mig_pen";
ALTER TABLE "new__mig_pen" RENAME TO "mig_pen";
COMMIT;
```

## 迁移记录表

很好，我们已经知道迁移文件的工作方式了。

现在我们尝试一下不修改模型，直接迁移：

```python
> python manage.py makemigrations

No changes detected

> python manage.py migrate

Operations to perform:
  Apply all migrations: ..., mig, ...
Running migrations:
  No migrations to apply.
```

没有任何迁移被执行。所以 Django 是如何得知哪些操作已经执行过了、哪些操作还没执行呢？

奥秘就在于数据库中的 `django_migrations` 表。这是由 Django 自动管理的表，里面记录了你每一次迁移的历史回溯：

| id   | app  | name                    | applied        |
| ---- | ---- | ----------------------- | -------------- |
| ...  | ...  | ...                     | ...            |
| 14   | mig  | 0001_initial            | 2020-05-19 ... |
| 15   | mig  | 0002_auto_20200519_1659 | 2020-05-19 ... |
| 16   | mig  | 0003_remove_pen_color   | 2020-05-19 ... |
| ...  | ...  | ...                     | ...            |

表里的每一条记录都和迁移文件是对应的，如果这个表里已经有迁移记录了，那么对应的迁移文件中的指令就不再执行了。

### 作死1号

接下来我们来作个死，手动将最后一个迁移文件 `0003_remove_pen_color.py` 删除掉，再重新执行迁移：

```python
> python manage.py makemigrations

Migrations for 'mig':
  mig\migrations\0003_remove_pen_color.py
    - Remove field color from pen

> python manage.py migrate

Operations to perform:
  Apply all migrations: ...mig, ...
Running migrations:
  No migrations to apply.
```

除了 `0003_remove_pen_color.py` 文件被重新创建外，没有任何事情发生，因为迁移记录表中已经有对应的 0003 号记录了，数据库操作不会重复执行。

### 作死2号

再次手动将 `0003_remove_pen_color.py` 文件删除掉，并且新增一个模型字段：

```python
class Pen(models.Model):
    price = models.DecimalField(max_digits=7, decimal_places=2)
    purchase_date = models.DateTimeField(default=timezone.now)
    
    # 上一次迁移时的删除更改
    # color = models.CharField(default='black', max_length=20)
    # 手动删除 0003 文件后，添加此字段
    length = models.IntegerField(default=10)
```

再次迁移：

```python
> python manage.py makemigrations

Migrations for 'mig':
  mig\migrations\0003_auto_20200520_1051.py
    - Remove field color from pen
    - Add field length to pen

> python manage.py migrate

Operations to perform:
  Apply all migrations: admin, auth, contenttypes, demo, mig, sessions
Running migrations:
  Applying mig.0003_auto_20200520_1051... OK
```

虽然迁移内容不同，但是由于新增字段导致 0003 号文件名称发生了变化，数据库更改还是成功执行了。

但是这里是有坑的。让我们来看看实际的 SQL 指令：

```python
> python manage.py sqlmigrate mig 0003

BEGIN;
--
-- Remove field color from pen
--
...
--
-- Add field length to pen
--
CREATE TABLE "new__mig_pen" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "length" integer NOT NULL, "price" decimal NOT NULL, "purchase_date" datetime NOT NULL);
INSERT INTO "new__mig_pen" ("id", "price", "purchase_date", "length") SELECT "id", "price", "purchase_date", 10 FROM "mig_pen";
DROP TABLE "mig_pen";
ALTER TABLE "new__mig_pen" RENAME TO "mig_pen";
COMMIT;
```

由于内部迁移机制，如果你之前的 `Pen` 表已经有数据了，那么这些数据中的  `length` 字段数据将全部被替换成默认值 10。

### 作死3号

这次我们不搞最后一条 0003 号文件了。把 0002 号文件删了，重新迁移试试...

```python
> python manage.py makemigrations

Traceback (most recent call last):
  File "D:\...\django_manage.py", line 43, in <module>
  ...
django...NodeNotFoundError: Migration mig.0003_auto_20200520_1115 dependencies reference nonexistent parent node ('mig', '0002_auto_20200519_1659')
```

报错意思是说，我现在要迁移 0003 号文件了，但是发现居然找不到 0002 号文件，所以干不下去了。意料之中。怎么办？

**第一种方式：**既然如此，那我把 0003 号文件的依赖改掉呢：

```python
class Migration(migrations.Migration):
    dependencies = [
        # ('mig', '0002_auto_20200519_1659'),
        ('mig', '0001_initial'),
    ]

    operations = [
        ...
    ]

```

这次迁移是可以成功的，而且 Django 还补了个 0004 号文件把缺失的操作给补上了。

**第二种方式：**将缺失的依赖之后的迁移文件全部删除，也可以成功迁移。

**第三种方式：**



### 作死4号

换一种更深入的作死姿势。假设现在最后一条迁移文件是 `0004_a.py` 。首先删掉它，然后对模型进行修改：

```python
class Pen(models.Model):
    ...
    # 比方说，删除掉 length 字段
    # length = models.IntegerField(default=10)
```

现在重新 `makemigrations` （注意不要 `migrate` ）：

```python
> python manage.py makemigrations

Migrations for 'mig':
  mig\migrations\0004_b.py
    - Remove field length from pen
    ...
```

Django 自动生成了迁移文件 `0004_b.py`。精彩的来了，把这个 `0004_b.py` 的名称修改为 `0004_a.py`，然后执行 `migrate` ：

```python
> python manage.py migrate

Operations to perform:
  Apply all migrations: ..., mig, ...
Running migrations:
  No migrations to apply.
```

删除 `length` 字段的指令没执行！这是因为数据库 `django_migrations` 表已经有同名记录了，Django 觉得这个文件里的操作都执行过了，就不再执行了。

这样子的结果就是 Model 和数据库字段不一致，在进行相关 ORM 操作时就会出现各种报错。不要以为这种情况很少见，在自动生成迁移文件的过程中是有可能发生的。