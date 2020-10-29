# Test Markdown

[TOC]

## Test Render

### Basic format

斜体：Emphasis, aka italics, with *asterisks 单星号* or _underscores 单下划线_.

加粗：Strong emphasis, aka bold, with **asterisks 双星号** or __underscores 双下划线__.

斜体加粗：Combined emphasis with **asterisks 双星号 and _underscores 单下划线_**.

删除线（非标准语法）：Strikethrough uses ~~two tildes 双波浪线~~. ~~`删除线加行内代码`~~

高亮（非标准语法）：==test 双等号==

verylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongEND

verylongverylong verylongverylong verylongverylong verylongverylong verylongverylong verylongverylong verylongverylong verylongverylong verylongverylong verylongverylong verylongverylong verylongverylong verylongverylong verylongverylong verylongverylong END

行内代码：`verylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongEND`

行内代码：`verylongverylong verylongverylong verylongverylong verylongverylong verylongverylong verylongverylong verylongverylong verylongverylong verylongverylong verylongverylong verylongverylong verylongverylong verylongverylong verylongverylong verylongverylong END`

Test links using `[]()`: [https://www.example.com/](https://www.example.com/), [http://www.example.com/](http://www.example.com/), [test.html](test.html), [#123456](#123456), [alert(1)](javascript:alert(1)), [someone@example.com](mailto:someone@example.com)

Test links using `<>`: <https://www.example.com/>, <someone@example.com>

Test long link: <https://www.example.com/very/long/very/long/very/long/very/long/very/long/very/long/very/long/very/long/very/long/very/long/very/long/very/long/very/long/very/long/very/long/very/long/very/long/very/long/very/long/very/long/very/long/very/long/very/long/END/>

引用：

> 我没说过这句话 —— 鲁迅

### verylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongEND

### Font

一去二三里烟村四五家亭台六七座八九十支花

```text
一去二三里烟村四五家亭台六七座八九十支花
```

The quick brown fox jumps over the lazy dog 0123456789

```text
The quick brown fox jumps over the lazy dog 0123456789
```

### Table

English | Number
--------|----
one     | 1
two     | 2
three   | 3

### List

Unordered list using `-`

- a b c d e f g h i j k
- aa bb cc dd ee ff gg hh ii jj kk
- list files: `ls -alh`
- `uid=0(root) gid=0(root) groups=0(root)`
- verylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongEND
- `verylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongverylongEND`

Ordered list using `1.`, `2.`, etc.

1. a b c d e f g h i j k
2. aa bb cc dd ee ff gg hh ii jj kk
3. list files: `ls -alh`
4. `uid=0(root) gid=0(root) groups=0(root)`

嵌套无序列表：

- a b c
- d e f
    - a b c
    - d e f
        - a b c
        - d e f
        - g h i
    - g h i
- j k l

嵌套有序列表：

1. a b c
2. d e f
    1. a b c
    2. d e f
        1. a b c
        2. d e f
        3. g h i
    3. g h i
3. j k l

### Task list

非标准语法

- [ ] Eat
- [x] Code
    - [x] HTML
    - [x] CSS
    - [x] JavaScript
- [ ] Sleep

### 脚注

Footnotes[^1] have a label[^@#$%] and the footnote's content.

[^1]: This is a footnote content.
[^@#$%]: A footnote on the label: "@#$%".

Test footnotes qwerty[^2] uiop[^3].

[^2]: 2222
[^3]: 3333

///Footnotes Go Here///

### 自动 `<br>` 换行

第一行。
第二行。

### 警告

type 为 `success`

!!! success
    大吉大利，晚上吃鸡！

type 为 `info`，无 title

!!! info ""
    这是一条普通信息
    
    测试链接 [example.com](https://www.example.com/)
    
    多行文字

type 为 `warning`

!!! warning
    Nuclear missile launched!

    Weather control device activated!

type 为 `danger`，手动指定 title

!!! danger "严重错误"
    CPU 100% 内存 100%

### Code blocks

Code block with ` ``` `:

```
## include <stdio.h>
int main()
{
    printf("Let's try some code.\n");
    printf("this line is very very loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooong\n");
    printf("this line is very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very long\n");

    return 0;
}
```

Code block with ` ```text`

```text
## comment aabb
## include <stdio.h>
import requests
```

Code block with ` ```python`

```python
## comment aabb
## include <stdio.h>
import requests
```

Code block with ` ```c`

```c
## comment aabb
## include <stdio.h>
import requests
```

Code highlighting test 1

```python
import os
import sys.stdout as out

"""
Author: asdfgh
"""

@abcd.efgh(123, 456.789, "sample string", test=True)
def qwerty(foo, bar="baz"):
    """qwerty function"""
    llll = [123, 456.789, None, "123 \'456\' 789", True]
    while True:
        if foo >= 0 and bar is not None:
            print("%s %r" % (bar, foo))
            print(', '.join(llll))
            foo -= 1

## sample class
## qqq www eee rrr ttt yyy
class Human(object):
    def __init__(self, name=None): ## TODO: set user age
        self.name = name ## set user name
        self.judge = lambda x: x >= 0

user = Human("Abcd")

try:
    with open('abc.txt', 'w') as f:
        f.write(user.name)
except Exception as e:
    print(type(e), repr(e), dir(e))
```

Code highlighting test 2

```cpp
/* 
This is a sample C++ file
*/

#include <iostream>
#define true false

using namespace std;

// A sample class
class Human {
    private double length = 123.456;
    private int age = 0;
    private char name[] = "Hello";

    public void birthday() {
        age++;
        cout << name << endl;
        print("Happy Birthday!");
    }
}

int main() {
    char *_str      = "a normal string";
    wchar_t *L_str  = L"a wide string";
    char16_t *u_str = u"utf-16 string";

    std::cout << _str << std::endl;

    return 0;
}
```

### Images

Small image (198 x 192):

![Test small image](test-small.jpg)

Large image (2400 x 1500):

![Test large image](test-large.png)

### LaTeX Math

非标准语法

Inline LaTeX: $\lim_{x\rightarrow0} \frac{\sin(x)}{x} = 1$

Block LaTex:

$$\lim_{x\rightarrow0} \frac{\sin(x)}{x} = 1$$

### `------` (`<hr>` tag)

------

## This is header 2

Using Python

### This is header 3 `<xyzabc />` tag

test markdown

#### Same header 4

test test

#### Same header 4

1234567890

#### Same header 4

qwerty

##### This is header 5

five

###### This is header 6

Last header

End test
