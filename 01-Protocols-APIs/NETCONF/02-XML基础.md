先来看一个XML文件的内容示例：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<students xmlns:stu="http://www.example.com/student"
          xmlns:edu="http://www.example.com/education">
  
  <stu:student id="1001">
    <stu:name>张三</stu:name>
    <stu:age>20</stu:age>
    <!-- 表示学生头像 -->
    <stu:avatar url="https://example.com/avatars/1001.jpg"/>
    <edu:major>计算机科学</edu:major>
    <edu:grade>A</edu:grade>
    <courses>
      <course code="CS101">编程基础</course>
      <course code="MA202">高等数学</course>
    </courses>
    <!-- 表示已完成学籍注册 -->
    <stu:auditPassed/>
  </stu:student>
</students>
```
### 标签
标签是XML文档的基本单元，用于定义数据的逻辑结构。
1. **标签的分类**
    - **开始标签与结束标签**：如`<name>张三</name>`，其中`<name>`是开始标签，`</name>`是结束标签，中间是元素的文本内容。
    - **空标签**：无内容的元素可简写为单标签，如`<stu:auditPassed/>`、`<stu:avatar url="https://example.com/avatars/1001.jpg"/>`，必须以`/>`结尾。
    - **根标签**：XML文档有且仅有一个根标签，是所有其他元素的父节点，如上例中的`<students>`。
2. **标签的语法规则**
    - 标签名区分大小写，如`<Name>`和`<name>`是两个不同标签。
    - 标签名不能以数字或标点符号开头，不能包含空格、冒号（除命名空间前缀分隔外）等特殊字符。
    - 标签必须正确嵌套，不能交叉，如`<a><b></a></b>`是非法的，正确应为`<a><b></b></a>`。

### 属性
属性是标签的额外信息，用于对元素进行补充说明，与标签内容相比，更适合表示**元数据**或**标识信息**。
1. **属性的语法特点**
    - 属性必须定义在开始标签或空标签内，格式为`属性名="属性值"`，属性值必须用单引号或双引号包裹，如`<stu:student id="1001">`。
    - 一个标签可以有多个属性，但同一标签内不能出现同名属性，如`<user name="李四" name="王五"/>`是非法的。
    - 属性值不能包含未转义的特殊字符（如`<`、`>`、`&`），若需使用需通过实体引用（如 `&lt;` 代表 `<`、`&gt;` 代表 `>`、`&amp;` 代表 `&`、`&quot;` 代表 `"`、`&apos;` 代表 `'`）。
2. **属性与子标签的选择原则**
    - 若信息是元素的**固有标识**（如ID、编号）或**简单元数据**（如单位、类型），优先用属性，如`<course code="CS101">编程基础</course>`。
    - 若信息是**复杂数据**、**可重复数据**或**需要进一步嵌套**，优先用子标签，如`<contact><phone>139xxx</phone><email>xxx@com</email></contact>`。

### 命名空间
当XML文档整合多个来源的标签时，命名空间通过唯一标识区分同名标签，是实现XML模块化和复用的关键。
1. **命名空间的定义与使用**
    - **默认命名空间**：无需前缀，格式为`xmlns="URI"`，如`<students xmlns="http://example.com/school">`，此时`<students>`及其子元素默认属于该命名空间。
    - **带前缀的命名空间**：格式为`xmlns:前缀="URI"`，如`xmlns:edu="http://www.example.com/education""`，使用时需通过前缀标识元素，如`<edu:major>计算机科学</edu:major>`。
    - **命名空间的继承**：子元素会继承父元素的命名空间，若子元素需切换命名空间，可重新声明前缀或默认命名空间。
2. **命名空间的URI特性**
    - 命名空间的URI（统一资源标识符）仅用于**唯一标识**，无需实际可访问（如`http://example.com/school`只是一个标识，并非真实网址）。
    - 相同URI的命名空间视为同一命名空间，与前缀无关，如`xmlns:sch="http://example.com/school"`和`xmlns:school="http://example.com/school"`指向同一命名空间。

### 其他组成部分
除了上述三大核心元素，XML文档还包含以下关键组件，共同构成完整的语法体系：
1. **XML声明**
    - 位于文档最开头，是可选但推荐的部分，用于指定XML版本、编码格式等，格式为`<?xml version="1.0" encoding="UTF-8"?>`。
2. **文本内容**
    - 标签之间的纯文本，是XML存储数据的主要载体，如`<stu:age>20</stu:age>`中的`20`。
    - 若文本包含特殊字符（`<`、`>`、`&`等），需使用实体引用或CDATA段处理。
3. **注释**
    - 格式为`<!-- 注释内容 -->`，用于对XML文档进行说明，解析器会忽略注释内容，不参与数据解析。
    - 注释不能嵌套，也不能出现在XML声明之前或标签内部。
4. **CDATA段**
    - 格式为`<![CDATA[ 内容 ]]>`，用于包裹包含大量特殊字符的文本（如代码、HTML片段），解析器将其视为纯文本，不解析内部的XML语法。
5. **处理指令**
    - 用于向XML解析器或应用程序传递指令，格式为`<?指令名 指令内容?>`，如`<?xml-stylesheet type="text/css" href="style.css"?>`，用于指定XML的样式表。
    - 当然，在NETCONF服务器上通常只会用到`<?xml version="1.0" encoding="UTF-8"?>`。

### RPC机制
**RPC**（Remote Procedure Call）的中文是**远程过程调用**，意为向服务器发送操作指令。

在NETCONF的服务端和客户端通信的过程中，除了一开始的Hello报文外，其余都是**RPC**或**RPC-Reply**报文。

RPC报文中会有一个属性`message-id`，服务端在回复时的RPC-Reply报文会携带相同的`message-id`。这样客户端就可以知道服务端回复的到底是哪个报文。

一个典型的**RPC报文**如下：
```xml
<?xml version="1.0" encoding="UTF-8"?> 
<rpc message-id="1" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <get-config> 
    <source> 
      <running/> 
    </source> 
    <filter type="subtree"> 
      <authors xmlns="http://example.com/ns/bookzone"/> 
      <books xmlns="http://example.com/ns/bookzone"/> 
    </filter> 
  </get-config> 
</rpc>
```
首先在`<rpc>`中定义了默认命名空间`urn:ietf:params:xml:ns:netconf:base:1.0`，因此`<rpc>、<get-config>、<source>、<running>、<filter>`等标签都是IETF定义的标准标签。

接下来我们借用了之前制作的`bookzone-example`模型，`<authors xmlns="http://example.com/ns/bookzone"/> `表示使用了`bookzone-example`模型中的`authors`标签/容器。

其中`<get-config>`表示此RPC是请求获取配置数据存储的全部或部分内容。`<source>`表示对应的配置数据库。而`<filter>`意味着客户端只需要获取与此标签内的YANG元素对应的数据。

如果服务端支持`bookzone-example`模型，那么它就会回复运行数据库中的`authors`和`books`及其内部元素的列表信息。

对应的**RPC-Reply**报文可能是下面这样：
```xml
<?xml version="1.0" encoding="UTF-8"?> 
<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="1"> 
  <data> 
    <authors xmlns="http://example.com/ns/bookzone"> 
      <author> 
        <name>Douglas Adams</name> 
        <account-id>1010</account-id> 
      </author> 
      <author> 
        <name>Malala Yousafai</name> 
        <account-id>1011</account-id> 
      </author> 
      <author> 
        <name>Michael Ende</name> 
        <account-id>1001</account-id> 
      </author> 
      <author> 
        <name>Per Espen Stoknes</name> 
        <account-id>1111</account-id> 
      </author> 
      <author> 
        <name>Sun Tu</name> 
        <account-id>1100</account-id> 
      </author> 
    </authors> 
    <books xmlns="http://example.com/ns/bookzone"> 
      <book> 
        <title>I Am Malala</title> 
        <author>Malala Yousafzai</author> 
        <format> 
          <isbn>9780297870913</isbn> 
          <format-id>hardcover</format-id> 
        </format> 
      </book> 
      <book> 
        <title>The Art of War</title>
        ...
```
与`<get-config>`标签对应，`<data>`标签的内容即为服务端对客户端的回应。其中含有一些由`bookzone-example`模型定义的作者与书籍信息。