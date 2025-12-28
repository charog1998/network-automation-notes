### Get报文
不同于`get-config`操作，NETCONF还提供了`get`操作，用来获取设备的配置信息和状态信息。例如，当我们想获取某端口的当前信息时，可以使用以下RPC请求：
```xml
<rpc message-id="100" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <get>
    <filter type="subtree">
      <top xmlns="http://www.h3c.com/netconf/data:1.0">
        <Ifmgr>
          <Interfaces>
            <Interface>
              <IfIndex>1</IfIndex>
            </Interface>
          </Interfaces>
        </Ifmgr>
      </top>
    </filter>
  </get>
</rpc>
```
依然可以通过`<filter>`标签对信息进行过滤，意为获取`IfIndex`为`1`的端口信息，服务端的回复如下：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="100">
  <data>
    <top xmlns="http://www.h3c.com/netconf/data:1.0">
      <Ifmgr>
        <Interfaces>
          <Interface>
            <IfIndex>1</IfIndex>
            <Name>GigabitEthernet0/0</Name>
            <AbbreviatedName>GE0/0</AbbreviatedName>
            ...
            <InetAddressIPV4>192.168.1.101</InetAddressIPV4>
            <InetAddressIPV4Mask>255.255.255.0</InetAddressIPV4Mask>
            <MAC>42-73-21-C2-01-05</MAC>
            ...
          </Interface>
        </Interfaces>
      </Ifmgr>
    </top>
  </data>
</rpc-reply>
```
除了获取设备的信息，`get`操作也可以通过`:ietf-netconf-monitoring`模块获取NETCONF服务器自身的信息，例如获取所支持的所有YANG模型信息：
```xml
<rpc message-id="101" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <get>
    <filter type='subtree'>
      <netconf-state xmlns='urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring'>
         <schemas/>
      </netconf-state>
    </filter>
  </get>
</rpc>
```
服务端回复如下，从中可以看到各个YANG模型的具体名称及版本等信息：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="101">
  <data>
    <netconf-state xmlns="urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring">
      <schemas>
        <schema>
          <identifier>ietf-yang-types</identifier>
          <version>2010-09-24</version>
          <format>yang</format>
          <namespace>urn:ietf:params:xml:ns:yang:ietf-yang-types</namespace>
          <location>NETCONF</location>
        </schema>
        ...
        <schema>
          <identifier>H3C-vxlan-data</identifier>
          <version>2019-12-09</version>
          <format>yang</format>
          <namespace>http://www.h3c.com/netconf/data:1.0</namespace>
          <location>NETCONF</location>
        </schema>
        ...
      </schemas>
    </netconf-state>
  </data>
</rpc-reply>
```
如果设备支持`get-schema`操作，那么可以使用下面的报文获取YANG模型的具体信息：
```xml
<rpc message-id="100" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <get-schema xmlns='urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring'>
    <identifier>H3C-vxlan-data</identifier>
    <version>2019-12-09</version>
    <format>yang</format>
  </get-schema>
</rpc>
```
服务端的返回信息如下，其中的`<data>`标签内即为YANG模型的内容：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="100">
  <data xmlns="urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring">
  module H3C-vxlan-data {
    namespace "http://www.h3c.com/netconf/data:1.0";
    prefix "vxlan-data";
    import comware-basetype {
         prefix "base";
    }
    import comware-extension {
         prefix "ext";
    }

    organization "NEW H3C Technologies Co., Ltd.";
    contact "Website: http://www.h3c.com";
    description "The module entities for vxlan data.";
    revision 2019-12-09 {
        description "Initial revision.";
    }
    ...
  </data>
</rpc-reply>
```

### 订阅通知
在实际使用过程中，常常需要对特定的系统事件进行订阅，例如利用下面的报文订阅服务端的**PING**操作：
```xml
<rpc message-id="100" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <create-subscription xmlns="urn:ietf:params:xml:ns:netconf:notification:1.0">
    <stream>NETCONF</stream>
    <filter>
      <event xmlns="http://www.h3c.com/netconf/event:1.0">
	    <Group>PING</Group>
      </event>
    </filter>
  </create-subscription>
</rpc>
```
发送后，服务端会返回一个**OK报文**，之后我们在设备上随便PING一个地址，等命令运行结束后，即可收到服务端返回的**Notificatin**：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<notification xmlns="urn:ietf:params:xml:ns:netconf:notification:1.0">
  <eventTime>2025-12-28T09:58:48</eventTime>
  <event xmlns="http://www.h3c.com/netconf/event:1.0">
    <Group>PING</Group>
    <Code>PING_STATISTICS</Code>
    <Slot>0</Slot>
    <Severity>Informational</Severity>
    <Context>Ping statistics for 192.168.1.1: 5 packet(s) transmitted, 5 packet(s) received, 0.0% packet loss, round-trip min/avg/max/std-dev = 0.627/0.828/1.049/0.147 ms.</Context>
  </event>
</notification>
```
新华三设备的事件订阅报文的完整格式如下：
```xml
<rpc message-id="100" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <create-subscription xmlns='urn:ietf:params:xml:ns:netconf:notification:1.0'>
    <stream>NETCONF_MONITOR_EXTENSION</stream>
    <filter>
      <NetconfMonitor xmlns='http://www.h3c.com/netconf/monitor:1.0'>
        <XPath>XPath</XPath>
        <Interval>interval</Interval>
        <ColumnConditions>
          <ColumnCondition>
            <ColumnName>ColumnName</ColumnName>
            <ColumnValue>ColumnValue</ColumnValue>
            <ColumnCondition>ColumnCondition</ColumnCondition>
          </ColumnCondition>
        </ColumnConditions>
        <MustIncludeResultColumns>
          <ColumnName>columnName</ColumnName>
        </MustIncludeResultColumns>
      </NetconfMonitor>
    </filter>
    <startTime>start-time</startTime>
    <stopTime>stop-time</stopTime>
  </create-subscription>
</rpc>
```
其中的参数含义如下：
|属性|含义|
|:-|:-|
|stream|订阅的事件流|
|NetconfMonitor|监控事件的过滤信息|
|XPath|监控事件的路径，格式为：`模块名[/子模块名]/表名`|
|interval|监控的时间间隔，取值范围为1～4294967，缺省值为300，单位为秒，即每隔300秒获取一次符合订阅条件的信息|
|ColumnName|监控列的名称，格式为：`[组名称.]列名称`|
|ColumnValue|监控列的过滤值|
|ColumnCondition|监控列的过滤条件：</br>more->大于</br> less->小于</br> notLess->不小于</br> notMore->不大于</br> equal->等于</br> notEqual->不等于</br> include->包含</br> exclude->不包含</br> startWith->开始于</br> endWith->结束于|
|start-time|订阅的开始时间|
|stop-time|订阅的结束时间|