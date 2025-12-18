### NETCONF基本网络架构
RFC6244文件中提供了NETCONF-YANG的网络架构图：
```
                       +----------------------------+
                       |Server (device)             |
                       |    +--------------------+  |
                       |    |      configuration |  |
            +----+     |    |     ---------------|  |
            |YANG|+    |    | m d  state data    |  |
            |mods||+   |    | e a ---------------|  |
            +----+|| -----> | t t  notifications |  |
             +----+|   |    | a a ---------------|  |
              +----+   |    |      operations    |  |
                       |    +--------------------+  |
                       |           ^                |
                       |           |                |
                       |           v                |
     +------+          |     +-------------+        |
     |      | -------------> |             |        |
     |Client| <rpc>    |     |  NETCONF    |        |
     | (app)|          |     |   engine    |        |
     |      | <------------  |             |        |
     +------+ <rpc-reply>    +-------------+        |
                       |       /        \           |
                       |      /          \          |
                       |     /            \         |
                       | +--------+   +---------+   |
                       | | config |   |system   |+  |
                       | |  data- |   |software ||+ |
                       | |   base |   |component||| |
                       | +--------+   +---------+|| |
                       |               +---------+| |
                       |                +---------+ |
                       +----------------------------+
```
这个架构中的主要元素有：
1. 客户端（Client），主要作用如下：
    - 利用NETCONF协议对网络设备进行系统管理。
    - 向NETCONF Server发送**RPC请求**，查询或修改一个或多个具体的参数值。
    - 接收NETCONF Server主动发送的**告警和事件**，以获知被管理设备的当前状态。
2. 服务器（Server），主要用于维护被管理设备的信息数据并响应客户端的请求。
    - NETCONF Server收到Client的**请求**后会进行数据解析，然后给NETCONF Client返回响应。
    - 当设备发生故障或其他事件时，NETCONF Server利用Notification机制主动将设备的**告警和事件**通知给Client，向Client报告设备的当前状态变化。


### NETCONF会话流程
常见的NETCONF流程通常如下：
```mermaid
sequenceDiagram
    participant C as 客户端应用
    participant S as 服务端（设备）

    %% 步骤1：建立NETCONF会话
    C->>S: 建立NETCONF会话
    %% 步骤2：交互hello消息，交换能力列表
    C->>S: 发送<hello>消息（携带自身能力列表）
    S->>C: 回复<hello>消息（携带自身能力列表）
    note over C: 获知[S]所支持的YANG模块
    %% 步骤3：客户端发送rpc操作
    C->>S: 发送基于YANG模块定义的操作<br/>（XML格式封装在<rpc>元素内）
    %% 步骤4：服务端解析rpc
    note over S: 接收并解析<rpc>元素
    %% 步骤5：合法性校验
    note over S: 对照YANG模块数据模型<br/>校验请求内容合法性
    %% 步骤6：执行操作
    note over S: 执行请求操作<br/>（可能修改配置数据存储区）
    %% 步骤7-8：服务端发送rpc-reply响应
    note over S: 构建响应消息（含处理结果/索要数据/错误信息）
    S->>C: 发送响应消息<br/>（XML格式封装在<rpc-reply>元素内）
    %% 步骤9：客户端解析响应
    note over C: 接收并解析<rpc-reply>元素
    %% 步骤10：后续处理
    note over C: 检查响应消息<br/>根据业务需求完成后续处理
```


