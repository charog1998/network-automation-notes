### Edit-config报文
既然可以通过Get-config报文获取设备的配置，那么就可以通过**Edit-config报文**对设备的某些或全量配置进行修改，结合之前获取到的接口管理信息，我们尝试修改接口的**描述**，如下：
```xml
<rpc message-id="100" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <edit-config>
    <target>
      <running/>
    </target>
    <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <top xmlns="http://www.h3c.com/netconf/config:1.0">
        <Ifmgr xc:operation="merge">
          <Interfaces>
            <Interface>
              <IfIndex>1</IfIndex>
              <Description>edit-test</Description>
            </Interface>
          </Interfaces>
        </Ifmgr>
      </top>
    </config>
  </edit-config>
</rpc>
```
服务端会回复一个OK报文，如下：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="100">
  <ok/>
</rpc-reply>
```
登录到设备上，查看端口信息可以看到我们的修改已经生效了，如下：
```bash
[netconf-test]show int br
Brief information on interfaces in route mode:
Link: ADM - administratively down; Stby - standby
Protocol: (s) - spoofing
Interface            Link Protocol Primary IP      Description                
GE0/0                UP   UP       192.168.1.101   edit-test
GE0/1                DOWN DOWN     --              
GE0/2                DOWN DOWN     --              
GE5/0                DOWN DOWN     --              
GE5/1                DOWN DOWN     --              
GE6/0                DOWN DOWN     --              
GE6/1                DOWN DOWN     --              
InLoop0              UP   UP(s)    --              
NULL0                UP   UP(s)    --              
REG0                 UP   --       --              
Ser1/0               DOWN DOWN     --              
Ser2/0               DOWN DOWN     --              
Ser3/0               DOWN DOWN     --              
Ser4/0               DOWN DOWN     --  
```
可以看到我们使用了`xc:operation="merge"`指定了修改`<Ifmgr>`节点下的配置时的操作，NETCONF规定了五种操作：
- `create`：创建叶子节点或子树。如果服务器配置中已存在任何部分，则事务失败。
- `merge`：如果叶子节点或子树不存在，则创建；如果已存在，则更新为给定的值。
- `replace`：移除服务器上当前节点以下的叶子节点或子树，然后用给定的值替换。
- `delete`：删除叶子节点或子树。如果在服务器中不存在，事务失败。
- `remove`：如果叶子节点或子树存在，则删除。如果不存在，则不执行任何操作。

在不指定`operation`属性值时，会使用缺省值，默认为`"merge"`。
#### 增量下发
增量下发选项`incremental`放置在列上，对于类似`vlan permitlist`列表集合性质的列，可能支持**增量下发**，用户请求XML中有增量下发选项时，最终执行结果不影响本列原有的数据。增量下发只支持`edit-config`，但不支持`edit-config`中的`replace`。

尝试增量下发一个接口的VLAN配置，2接口原有`untagvlanlist`为12-15，下发后为1-10，12-15。XML请求如下：
```xml
<rpc message-id="100" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:h3c="http://www.h3c.com/netconf/base:1.0">
  <edit-config>
    <target>
      <running/>
    </target>
    <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <top xmlns="http://www.h3c.com/netconf/config:1.0">
        <VLAN  xc:operation="merge">
          <HybridInterfaces>
            <Interface>
              <IfIndex>2</IfIndex>
              <UntaggedVlanList h3c:incremental="true">1-10</UntaggedVlanList>
            </Interface>
          </HybridInterfaces>
        </VLAN>
      </top>
    </config>
  </edit-config>
</rpc>
```

#### 额外选项
执行`<edit-config>`操作时，可指定一个测试选项，使用`<test-option>`节点来决定当前配置是否下发。

该节点的缺省值为`test-then-set`，全部取值为：
- `test-then-set`：如果没有错误则将配置设置到系统。
- `set`：将配置设置到系统。
- `test-only`：只测试，并不下发配置到系统。语法检查通过，就返回ok成功，否则失败。

如果下发一个仅测试的配置，XML请求如下：
```xml
<rpc message-id="100" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <edit-config>
    <target>
      <running/>
    </target>
    <test-option>test-only</test-option>
    <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
    ...
    </config>
  </edit-config>
</rpc>
```
在执行`<edit-config>`的过程中，如果遇到一个实例配置出错，缺省情况下会直接返回错误，并提供错误选项，通过错误选项取值的不同，在发生错误的时候进行不同的处理操作。

`<error-option>`节点用于设置一个实例配置出错后，后续实例配置的处理方式，缺省值为`stop-on-error`，全部取值为：
- `stop-on-error`：停止处理，返回错误。此选项为缺省选项。
- `continue-on-error`：继续处理，但是报告错误。
- `rollback-on-error`：停止并回滚配置。