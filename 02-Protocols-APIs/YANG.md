如何来描述各种网络协议的具体配置内容，这个问题就和面对对象编程的第一步： **抽象** 异曲同工。
设想一个图书集团，如何在图书管理系统中来保存每一种书籍呢。大概会创建下面这样的一个类：
```python
class Book:
    def __init__(self, title:str, author:str, isbn:str, price:float):
        """
        Args:
            title: 书名
            author: 作者
            isbn: 国际标准书号
            price: 价格
        """
        self.title = title
        self.author = author
        self.isbn = isbn
        self.price = price
```
这个类的每一个实例代表每一种书籍，并且依据这个类在数据库中创建一个专门的表用来存储书记的元数据。

同样，在网络领域，如何表示如此多的网络协议呢，答案依然是使用统一的数据模型，例如本文讨论的 **YANG** 模型。
上述的书籍类可以表示为以下的YANG模式（被称为 **Schema**）：
```yang
container books { 
    list book { 
        key title; 
 
        leaf title { 
            type string; 
        } 
        leaf isbn { 
            type string; 
            mandatory true; # 表示这个属性是强制要求的
        } 
        leaf author { 
            type string; 
        } 
        leaf price { 
            type decimal64 { 
                fraction-digits 2; 
            } 
            units sim-dollar; 
        } 
    } 
}
```
其中`list`类似于**类**，`key`类似于**主键**代表了实例的唯一标识路径，`leaf`类似于类的**属性**；

如果用数据库来比较，`container`类似于**Database**，`list`类似于**Table**，`leaf`类似于**Column**。