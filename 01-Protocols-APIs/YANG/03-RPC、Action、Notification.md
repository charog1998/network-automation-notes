### Pyang
前面我们已经拥有了一个比较完整的YANG模型了，把它命名为一个`bookzone-example.yang`文件。在进行下一步操作前，我们先来尝试使用一个用来辅助分析和处理YANG模型的命令行工具：
**安装**
```sh
# Ubuntu/Debian
sudo apt install pyang

# CentOS/RHEL
sudo yum install pyang

# macOS
brew install pyang

# Python pip
pip install pyang
```
**使用树状结构显示**
```bash
> pyang -f tree .\bookzone-example.yang
module: bookzone-example
  +--rw authors
  |  +--rw author* [name]
  |     +--rw name          string
  |     +--rw account-id?   uint32
  +--rw books
  |  +--rw book* [title]
  |     +--rw title       string
  |     +--rw author?     -> /authors/author/name
  |     +--rw language?   language-type
  |     +--rw format* [isbn]
  |        +--rw isbn         ISBN-10-or-13
  |        +--rw format-id    identityref
  |        +--rw price?       decimal64
  +--rw users
     +--rw user* [user-id]
        +--rw user-id    string
        +--rw name?      string
```
其中：
- `?` 表示可选（optional）
- `*` 表示零个或多个（list）
- `rw` 表示可读可写

### RPC、Action
在YANG模型中由**客户端 Client**向**服务端 Server**传达通知的动作在YANG模型中被称为**RPC（远程过程调用）**或者**Action**。
- *在Netconf中，**Client**通常为运管平台或者工程师使用的各种工具，负责发起会话和配置操作。**Server**为运行在网络设备上的Netconf进程，负责监听客户端的连接，处理请求并返回响应。*

二者的区别在于：
- **RPC**作用于全局操作，独立于任何数据节点，定义的位置通常位于模块顶层。
- **Action**需要绑定到特定的数据节点（`containers`、`lists`）上。
- *`action`是YANG 1.1版本新加入的关键字，YANG 1.0版本中只能使用指定输入参数的`rpc`实现针对特定节点的操作。*

与其他编程语言的**方法/函数**概念类似，**RPC和Action**也有`input`和`output`参数。

在之前的内容中，我们定义了关于图书管理的基本内容，但是都是比较静态的信息。实际上管理系统往往会定义**库存管理**之类的动态信息，最简单来说，某用户购买了某个版本的某种图书，这就要求我们在模型中定义一个**购买**动作。

这个动作的`input`可能包含表示购买者的`user`和表示被购买书籍的`book`以及购买数量的`nmber-of-copies`，其中`book`可能只包含`title`和`format`。

如果是**RPC形式**的`/purchase`，就需要在定义中指明`user`参数；而如果是**Action形式**的`/users/user[name="janl"]/purchase`，由于`action purchase`定义在`user`内部所以在调用路径上已经指明了操作的`user`是哪一个

一个完整的`/users/user/purchase`可能是下面这样：
```yang
action purchase { 
  input { 
    leaf title { 
      type leafref { 
        path /books/book/title; 
      } 
    } 
    leaf format { 
      type leafref { 
        path /books/book/format/format-id; 
      } 
    } 
    leaf number-of-copies { 
      type uint32 { 
        range 1..999; 
      } 
    } 
  } 
  output { 
    choice outcome { 
      case success { 
        leaf success { 
          type empty; 
          description 
            "Order received and will be sent to specified user. 
             File orders are downloadable at the URL given below."; 
        } 
        leaf delivery-url { 
          type string; 
          description 
            "Download URL for file deliveries."; 
        } 
      } 
      leaf out-of-stock { 
        type empty; 
        description 
          "Order received, but cannot be delivered at this time. 
           A notification will be sent when the item ships."; 
      } 
      leaf failure { 
        type string; 
        description 
          "Order cancelled, for reason stated here."; 
      } 
    } 
  } 
}
```
可以看到上例中使用`choice-case`关键字为`purchase`行为定义了三个可能的输出：`success`,`out-of-stock`,`failure`。其中`out-of-stock`和`failure`由于只有一个YANG元素，因此可以省略`case`这一层，这也是YANG 1.1的新特性。

可以看到`out-of-stock`是一个`empty`类型的叶子节点，这种节点可以被创建和删除，但是无法赋值，通常被用来作为标志位。

把我们新建的action添加到users/user/下，再用pyang查看下树状结构：
```sh
> pyang -f tree .\bookzone-example.yang

module: bookzone-example
  +--rw authors
  |  +--rw author* [name]
  |     +--rw name          string
  |     +--rw account-id?   uint32
  +--rw books
  |  +--rw book* [title]
  |     +--rw title       string
  |     +--rw author?     -> /authors/author/name
  |     +--rw language?   language-type
  |     +--rw format* [isbn]
  |        +--rw isbn         ISBN-10-or-13      
  |        +--rw format-id    identityref        
  |        +--rw price?       decimal64
  +--rw users
     +--rw user* [user-id]
        +--rw user-id     string
        +--rw name?       string
        +---x purchase
           +---w input
           |  +---w title?              -> /books/book/title
           |  +---w format?             -> /books/book/format/format-id
           |  +---w number-of-copies?   uint32
           +--ro output
              +--ro (outcome)?
                 +--:(success)
                 |  +--ro success?        empty
                 |  +--ro delivery-url?   string
                 +--:(out-of-stock)
                 |  +--ro out-of-stock?   empty
                 +--:(failure)
                    +--ro failure?        string
```
其中：
- `x` 表示操作/动作 (action/rpc)
- `ro` 表示只读，通常表示系统状态、统计信息、操作结果等
- `w` 表示输入参数

### Notification
在上面的购买动作中，我们设计了一种`out-of-stock`（缺货）的输出结果，当返回这种结果时，我们的管理系统依然接受了订单，并且会在稍后进行派送，派送时会发送给用户一个通知，这在YANG模型中就叫做**Notification**。

一个派送通知与购买行为类似，组成要素为表示购买者的`user`和表示被购买书籍的`book`以及购买数量的`nmber-of-copies`，整体来看可能是下面这样：
```yang
notification shipping { 
  leaf user { 
    type leafref { 
      path /users/user/name; 
    } 
  } 
  leaf title { 
    type leafref { 
      path /books/book/title; 
    } 
  } 
  leaf format { 
    type leafref { 
      path /books/book/format/format-id; 
    } 
  } 
  leaf number-of-copies { 
    type uint32; 
  } 
}
```
**Notification**与**RPC**类似，定义于模块顶层，将这个**Notification**添加到我们已经构造的yang文件中，再次使用pyang查看下树状结构：
```sh
> pyang -f tree .\bookzone-example.yang
  +--rw authors
  |  +--rw author* [name]
  |     +--rw name          string
  |     +--rw account-id?   uint32
  +--rw books
  |  +--rw book* [title]
  |     +--rw title       string
  |     +--rw author?     -> /authors/author/name
  |     +--rw language?   language-type
  |     +--rw format* [isbn]
  |        +--rw isbn         ISBN-10-or-13      
  |        +--rw format-id    identityref
  |        +--rw price?       decimal64
  +--rw users
     +--rw user* [user-id]
        +--rw user-id     string
        +--rw name?       string
        +---x purchase
           +---w input
           |  +---w title?              -> /books/book/title
           |  +---w format?             -> /books/book/format/format-id
           |  +---w number-of-copies?   uint32
           +--ro output
              +--ro (outcome)?
                 +--:(success)
                 |  +--ro success?        empty
                 |  +--ro delivery-url?   string
                 +--:(out-of-stock)
                 |  +--ro out-of-stock?   empty
                 +--:(failure)
                    +--ro failure?        string

  notifications:
    +---n shipping
       +--ro user?               -> /users/user/name
       +--ro title?              -> /books/book/title
       +--ro format?             -> /books/book/format/format-id
       +--ro number-of-copies?   uint32
```
同时在yang文件前面添加`revision`修订记录：
```yang
revision 2025-12-15 { 
  description 
    "Added action purchase and notification shipping."; 
}
```