## DHCP

动态主机配置协议，其实不光配置IP地址，各种网络参数的配置都由它完成

报文依靠UDP传输，使用67（服务器）、68（客户端）两个端口号

### 工作流程

1. **发现阶段**：客户端发送DISCOVER报文尝试发现服务器
2. **提供阶段**：服务器从接收到DISCOVER报文的端口的IP地址所在的地址池中为客户端提供一个IP地址，回复OFFER报文
3. **选择阶段**：如果有多个DHCP服务器返回了OFFER报文，则客户端只会选择第一个，并广播发送REQUEST报文通告自己选择的服务器以及自己的IP地址
4. **确认阶段**：对应的服务器收到REQUEST后会给客户端返回ACK报文用于确认

**对于可能出现的IP地址冲突**

- DHCP服务器收到DHCP DISCOVER报文时，给客户端分配IP地址前会发送Ping探测，如果能Ping通则标识该地址不可用，并选择其他IP地址分配给客户端

- DHCP客户端获取IP地址成功后，会立即发送**免费ARP报文**，如果收到响应，则发送DHCP DECLINE报文通知DHCP服务器该IP地址冲突，DHCP服务器标识该地址不可用，客户端发送DHCP DISCOVER报文重新申请IP地址

*免费的ARP报文指不同于普通ARP报文，它不是为了获取其他设备的MAC地址信息，而是用于通知其他设备自身的IP地址和ARP地址信息*

### 地址分配顺序

DHCP服务器按照如下次序为客户端选择IP地址:
1. DHCP服务器的数据库中与客户端MAC地址静态绑定的IP地址
2. 客户端以前曾经使用过的IP地址，即客户端发送的请求报文中请求IP地址选项的地址
3. 在DHCP地址池中，顺序查找可供分配的空闲IP地址，最先找到的IP地址
4. 如果在DHCP地址池中未找到可供分配的空闲IP地址，则依次查询超过租期、发生冲突的IP地址，如果找到可用的IP地址，则进行分配，否则报告错误

### DHCP Relay

DHCP Relay即DHCP中继，它是为解决DHCP服务器和DHCP客户端不在同一个广播域而提出的，提供了对DHCP广播报文的中继转发功能

能够把DHCP客户端的广播报文“透明地”传送到其它广播域的DHCP服务器上，同样也能够把DHCP服务器端的应答报文“透明地”传送到其它广播域的DHCP客户端

中继设备负责转发客户端和服务端之间的报文，相较于普通报文，有两个字段是用于中继的：

**HOPS**：表示当前报文经过的中继个数，由服务器或客户端设为0，每经过一个中继则加1，默认不能超过16，否则会被丢弃
**Giaddr**：表示客户端所在网段，由第一个中继将自己的ip地址填入，用于服务器为客户端分配ip

### DHCP Relay实验配置

![alt text](img/DHCP-Relay实验拓扑.png)

利用S1作为DHCP服务器，通过S3转发，为S4上的VLANIF10、20、30分配IP

并且由VLANIF30代表某台需要固定IP的设备（例如打印机），为其分配固定IP

#### 实验步骤

**在三台交换机上配置VLAN和VLANIF，并在接口放通**

略

**在S3与S1上的Vlanif分配IP**

```bash
# S3
interface Vlan-interface 10
ip address 10.0.10.3 24
quit
interface Vlan-interface 20
ip address 10.0.20.3 24
quit
interface Vlan-interface 30
ip address 10.0.30.3 24
quit
interface Vlan-interface 40
ip address 10.0.40.3 24
quit

# S1
interface Vlan-interface 40
ip address 10.0.40.1 24
quit
```

**在S1上打开DHCP并配置地址池**

```bash
dhcp enable

dhcp server ip-pool vlan10
 gateway-list 10.0.10.3
 network 10.0.10.0 mask 255.255.255.0
 dns-list 10.0.10.3
quit

dhcp server ip-pool vlan20
 gateway-list 10.0.20.3
 network 10.0.20.0 mask 255.255.255.0
 dns-list 10.0.20.3
quit

dhcp server ip-pool vlan30
 gateway-list 10.0.30.3
 network 10.0.30.0 mask 255.255.255.0
 dns-list 10.0.30.3
quit

# 检查地址池
[S1-Server]show dhcp server pool 
Pool name: vlan10
  Network: 10.0.10.0 mask 255.255.255.0 
  dns-list 10.0.10.3 
  expired day 1 hour 0 minute 0 second 0
  gateway-list 10.0.10.3 
  IP-in-use threshold 100
Pool name: vlan20
  Network: 10.0.20.0 mask 255.255.255.0 
  dns-list 10.0.20.3 
  expired day 1 hour 0 minute 0 second 0
  gateway-list 10.0.20.3 
  IP-in-use threshold 100
Pool name: vlan30
  Network: 10.0.30.0 mask 255.255.255.0 
  dns-list 10.0.30.3 
  expired day 1 hour 0 minute 0 second 0
  gateway-list 10.0.30.3 
  IP-in-use threshold 100
```

**查看S4上的Vlanif30的MAC地址，并在S1的地址池上绑定固定IP**

```bash
<S4-Client>show int Vlan-interface 30
Vlan-interface30
Current state: UP
Line protocol state: UP
......
......
IP packet frame type: Ethernet II, hardware address: 56f3-69e7-0102
......
......
```

配置S1的地址池

```bash
[S1-Server]dhcp server ip-pool vlan30
[S1-Server-dhcp-pool-vlan30]static-bind ip-address 10.0.30.2 mask 255.255.255.0 
hardware-address 56f3-69e7-0102
```

**打开S1上Vlanif40的DHCP Server**

```bash
[S1-Server]interface Vlan-interface 40
[S1-Server-Vlan-interface40]dhcp select server 
```

**在S1上配置去往中继设备的静态路由**

```bash
ip route-static 10.0.10.0 24 10.0.40.3
ip route-static 10.0.20.0 24 10.0.40.3
ip route-static 10.0.30.0 24 10.0.40.3
```

**在S3上配置中继**

```bash
interface Vlan-interface10
 dhcp select relay
 dhcp relay server-address 10.0.40.1
interface Vlan-interface20
 dhcp select relay
 dhcp relay server-address 10.0.40.1
interface Vlan-interface30
 dhcp select relay
 dhcp relay server-address 10.0.40.1
```

**在S4上允许接口使用DHCP获取IP**

```bash
interface Vlan-interface10
ip address dhcp-alloc 
quit

interface Vlan-interface20
ip address dhcp-alloc 
quit

interface Vlan-interface30
ip address dhcp-alloc 
quit
```

#### 实验结果

**在S4上查看接口IP**

```bash
[S4-Client]show ip int br
*down: administratively down
(s): spoofing  (l): loopback
Interface          Physical Protocol IP address/Mask    VPN instance Description
MGE0/0/0           down     down     --                 --           --         
Vlan10             up       up       10.0.10.1/24       --           --         
Vlan20             up       up       10.0.20.1/24       --           --         
Vlan30             up       up       10.0.30.2/24       --           --         
```

可以看到成功配置到了IP地址

#### 配合抓包进行观察

在Vlanif30上使用`ip addr dhcp-alloc`使用DHCP配置时

客户端与中继之间：
![alt text](img/DHCP抓包-1.png)
中继与服务器之间：
![alt text](img/DHCP抓包-2.png)

可以看到报文依次为客户端广播Discover，服务器回复Offer，客户端广播Request，服务器回复ACK

并且在收到ACK之后，客户端又发送了ARP广播报文探查是否有IP冲突，在确认没有冲突后又广播了自己的IP地址

使用`undo ip addr dhcp-alloc`取消DHCP配置时

客户端与中继之间：
![alt text](img/DHCP抓包-3.png)
中继与服务器之间：
![alt text](img/DHCP抓包-4.png)

由于Vlanif30是固定分配的IP地址，所以服务器没有进行ping测

在Vlanif10上实验会发现，服务器收到Discover报文，从地址池中选择IP地址后，确实ping了这个地址，在未ping通后再返回Offer

![alt text](img/DHCP抓包-5.png)