接下来我们准备通过实验来观察NETCONF工作时使用的几种报文，为此我使用了华三云实验室制作的HCL工具。

在工具中添加一个**路由器MSR36-20**和一个**Host本地主机**，并且令路由器的**GE0/0接口**与本地主机的**VirtualBox Host-Only Ethernet Adapter网卡**互联，通常VirtualBox分配的这张网卡的地址是`192.168.56.1/24`，因此我们将路由器的GE0/0接口**IP地址**也配置在这个子网下即可与主机实现**互通**。

具体的配置如下：
```
# H3C Netconf YANG 初始化配置脚本
# 实验平台为HCL 5.10.3
# 实验设备为MSR36-20，系统版本为H3C Comware Software, Version 7.1.064，Release 0427P22
# 进入系统视图
system-view

# 创建本地用户
local-user zzy class manage
 password simple 123456qwer
 service-type ssh
 authorization-attribute user-role network-admin

# SSH相关配置
ssh server enable
ssh user zzy service-type all authentication-type password

# NETCONF配置
netconf ssh server enable

# VTY线路配置
user-interface vty 0 15
 authentication-mode scheme
 protocol inbound ssh
 user-role network-admin
 quit

# 接口配置
interface GigabitEthernet 0/0
 ip address 192.168.56.101 255.255.255.0
```
配置后可先使用Ping命令验证是否连通，连通后可使用SSH命令：`ssh zzy@192.168.56.101 -p 830 -s netconf`命令进入**NETCONF子系统**。

### Hello报文
在进入**NETCONF子系统**之后，我们的终端作为客户端会收到服务端发送的**Hello报文**，节选如下：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
	<capabilities>
		<capability>urn:ietf:params:netconf:base:1.0</capability>
		<capability>urn:ietf:params:netconf:base:1.1</capability>
		<capability>urn:ietf:params:netconf:capability:notification:1.0</capability>
		...
		<capability>urn:h3c:params:netconf:capability:h3c-netconf-ext:1.0</capability>
		<capability>urn:h3c:params:netconf:capability:h3c-save-point:1.0</capability>
		...
		<capability>http://www.h3c.com/netconf/data:1.0-VXLAN?module=VXLAN&amp;revision=2020-03-31</capability>
		<capability>http://www.h3c.com/netconf/config:1.0-VXLAN?module=VXLAN&amp;revision=2020-03-31</capability>
		...
	</capabilities>
	<session-id>1</session-id>
</hello>
```
客户端可以从**Hello报文**中获取到服务端支持的NETCONF能力或操作，例如`<capability>urn:ietf:params:netconf:capability:notification:1.0</capability>`，这些能力的名称一般可以简写为`:notification`。

在NETCONF1.0系统中，**Hello报文**还会将其支持的所有YANG模型通过能力的方式传递过来。为了避免Hello报文过于冗长，在1.1版本中改为利用**YANG Module Library**来提供YANG模型的查询功能。

在收到服务端的，**Hello报文**后，客户端也需要回复**Hello报文**，如下：
```xml
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
    <capability>urn:ietf:params:netconf:base:1.1</capability>
  </capabilities>
</hello>
]]>]]>
```
其中最后一行的`]]>]]>`是NETCONF的**结束标识符**，用来表示一条报文的结束位置。