## WLAN

### VLAN Pool

**现有网络面临的挑战**

无线网络终端的移动性导致特定区域（例如酒店大堂、餐厅、场馆的入口等）IP地址请求较多

通常情况下，一个SSID只能对应一个业务VLAN，如果通过扩大子网增加IP地址则会导致广播域扩大，大量的广播报文会造成网络拥塞

VLAN Pool是一种把多个VLAN放在一个池中并提供分配算法的VLAN分配技术，又称为VLAN池。实现一个SSID对应多个VLAN的操作

**分配流程**

1. 用户终端从某个VAP接入，判断VAP是否有绑定VLAN Pool
2. 如果该VAP对应的模板绑定了VLAN POOL，使用VLANPoOl的分配算法分配一个VLAN，VLAN Pool有顺序分配和hash分配两种分配算法
3. 给终端分配一个VLAN
4. 终端从VLAN Pool分配的VLAN上线

### WLAN三层组网AC发现机制

默认情况下三层设备是不会转发广播或组播报文的，因此如果不在同一个子网，AP向AC发送的Discover报文是无法通过路由器的

通常解决办法是在DHCP报文中加入Option 43字段，其中包含AC的IP地址列表

### 漫游

指终端在不同的AP覆盖范围内移动时，保证业务不中断

需要两个AP：
1. SSID相同
2. 安全模板的配置相同（名称可以不同，内容必须相同）
3. 认证模板的认证方式和参数也要相同

#### 漫游方式

**二层漫游-直接转发**

终端从HAP移动到FAP后，直接使用FAP和FAC下挂的网关转发流量

*H代表Home，F代表Foreign*

**三层漫游-直接转发**

HAP和HAC之间不通过CAPWAP隧道封装，默认报文需要经过网管转发给HAP进行中转

**三层漫游-隧道转发**

HAP和HAC之间通过CAPWAP隧道封装，报文无需返回HAP，直接通过HAC转发

### AC可靠性

|对比项|切换速度|主备AC异地部署|约束条件|适用范围|
|-|-|-|-|-|
|VRRP双机热备|主备切换速度快，对业务影响小。通过配置VRRP抢占时间，相比于其他备份方式实现更快的切换|不建议主备AC异地部署|主备AC的型号和软件版本需完全一致。一台备AC只支持为一台主AC提供备份|对可靠性要求高，且无须异地部署主备AC的场景|
|双链路双机热备|AP状态切换慢，需等待检测到CAPWAP断链超时后才会切换，主备切换后终端不需要重新上线|支持|主备AC的型号和软件版本需完全一致，一台备AC只支持为一台主AC提供备份|对可靠性要求高，且要求异地部署主备AC的场景|
|N+1备份|AP状态切换慢，需等待检测到CAPWAP断链超时后才会切换，AP、终端均需要重新上线，业务会出现短暂中断|支持|主备AC产品形态可以不同，AC的软件版本必须一致。一台备AC支持为多台主AC提供备份能降低购买设备的成本。|对可靠性要求较低，对成本控制要求较高的场景|

### 准入控制

常见三种认证方式

|对比项|适合场景|客户端需求|优点|缺点|
|-|-|-|-|-|
|802.1X认证|新建网络、用户集中、信息安全要求严格的场景|需要|安全性高|部署不灵活|
|MAC认证|打印机、传真机等哑终端接入认证的场景|不需要|无需安装客户端|需登记MAC地址，管理复杂|
|Portal认证|用户分散、用户流动性大的场景|不需要|部署灵活|安全性不高|

### WLAN基础与漫游配置实操

![alt text](img/WLAN配置实验.png)

#### 数据规划

|配置项|参数|
|-|-|
|AP 管理 VLAN|VLAN10、20|
|STA 业务 VLAN|VLAN11、21|
|DHCP 服务器|S3 作为 DHCP 服务器为 AP、STA 分配 IP 地址|
|AP 的IP 地址池|10.0.10.0/24、10.0.20.0/24|
|STA 的IP 地址池|10.0.11.0/24、10.0.21.0/24|
|AC 的源接口 IP 地址|VLANIF100(10.0.100.254)、VLANIF200(10.0.200.254)|
|AP 组|名称:ap-group1、ap-group2 引用模板:VAP 模板 departX|
|域管理模板|名称:default 国家码:中国(CN)|
|SSID 模板|名称:departX SSID 名称:roam|
|安全模板|名称:departX 安全策略:WPA-WPA2+PSK+AES 密码:huawei123|
|VAP 模板|名称:departX 转发模式:直接转发 业务 VLAN:VLAN11、21 引用模板:SSID 模板 departX、安全模板 departX|

#### 步骤

**在S3、S4、AC1、AC2上创建VLAN并在接口上放通对应的VLAN**

```bash
# S3
vlan 10 11 20 21 100 200
int g 1/0/1
port link-type trunk
port trunk permit vlan 100
quit
int g 1/0/2
port link-type trunk
port trunk permit vlan 200
quit
int g 1/0/3
port link-type trunk
port trunk permit vlan 20 21
quit
int g 1/0/4
port link-type trunk
port trunk pvid vlan 10
port trunk permit vlan 10 11
quit
```

```bash
# S4
vlan 20 21
int g 1/0/3
port link-type trunk
port trunk permit vlan 20 21
quit
int g 1/0/4
port link-type trunk
port trunk pvid vlan 20
port trunk permit vlan 20 21
quit
```

注意要将交换机下行的端口默认VLAN分别设置为10、20

```bash
# AC1
vlan 100
int g 1/0/12
port link-type trunk
port trunk permit vlan 100
quit
```

```bash
# AC2
vlan 200
int g 1/0/13
port link-type trunk
port trunk permit vlan 200
quit
```

**在S3、AC1、AC2上创建Vlanif**

按照规划，10、20为管理VLAN，11、21为业务VLAN，100、200分别用于与AC1、AC2进行三层通信

```bash
# S3
int Vlan-interface 10
description ap1_mgnt
ip addr 10.0.10.1 24
quit
int Vlan-interface 11
description ap1_service
ip addr 10.0.11.1 24
quit
int Vlan-interface 20
description ap2_mgnt
ip addr 10.0.20.1 24
quit
int Vlan-interface 21
description ap2_service
ip addr 10.0.21.1 24
quit
int Vlan-interface 100
description to_AC1
ip addr 10.0.100.1 24
quit
int Vlan-interface 200
description to_AC2
ip addr 10.0.200.1 24
quit
```

检查Vlanif情况

```bash
[S3]show int Vlan-interface br
Brief information on interfaces in route mode:
Link: ADM - administratively down; Stby - standby
Protocol: (s) - spoofing
Interface            Link Protocol Primary IP        Description              
Vlan10               UP   UP       10.0.10.1         ap1_mgnt
Vlan11               UP   UP       10.0.11.1         ap1_service
Vlan20               UP   UP       10.0.20.1         ap2_mgnt
Vlan21               UP   UP       10.0.21.1         ap2_service
Vlan100              UP   UP       10.0.100.1        to_AC1
Vlan200              UP   UP       10.0.200.1        to_AC2
```

```bash
# AC1
int Vlan-interface 100
description to_S3_CAPWAP
ip addr 10.0.100.254 24
quit
```

```bash
# AC2
int Vlan-interface 200
description to_S3_CAPWAP
ip addr 10.0.200.254 24
quit
```

**在AC1、AC2上配置去往AP管理网段的路由**

```bash
[AC1]ip route-static 10.0.10.0 255.255.255.0 10.0.100.1
[AC2]ip route-static 10.0.20.0 255.255.255.0 10.0.200.1
```

**在S3上打开DHCP并配置地址池**

```bash
dhcp enable

dhcp server ip-pool ap1
 gateway-list 10.0.10.1
 network 10.0.10.0 mask 255.255.255.0
 # option 43 ip-address 10.0.100.254 这条不好使，不管是ip-address还是ascii都不好使
 # 只能用十六进制字符，前面是固定的，最后八位是对应的IPv4地址转换来的
 option 43 hex 80070000010A0064FE
quit

dhcp server ip-pool ap2
 gateway-list 10.0.20.1
 network 10.0.20.0 mask 255.255.255.0
 # option 43 ip-address 10.0.200.254
 option 43 hex 80070000010A00C8FE
quit

dhcp server ip-pool service_a
 gateway-list 10.0.11.1
 network 10.0.11.0 mask 255.255.255.0
 dns-list 10.0.11.1
quit

dhcp server ip-pool service_b
 gateway-list 10.0.21.1
 network 10.0.21.0 mask 255.255.255.0
 dns-list 10.0.21.1
quit
```

**在S3的Vlanif 10、20、11、21上打开DHCP服务**

```bash
interface Vlan-interface10
 dhcp select server
 quit
interface Vlan-interface11
 dhcp select server
 quit
interface Vlan-interface20
 dhcp select server
 quit
interface Vlan-interface21
 dhcp select server
 quit
```

由于AP设备的Vlanif1默认打开了DHCP，此时可以看到AP1和2已经取到了IP地址

**配置AC1**

在 AC1 上指定 VLANIF100为 CAPWAP 源接口，创建 ap-group depart1，采用 MAC地址认证的方式关联 AP，将 AP 命名为 ap1，关联到 ap-group depart1，配置参数模板关联到 VAP模板，在ap-group depart1 中调用 vap-profile depart1

*华三设备上没有手动配置CAPWAP隧道的接口的命令，应该是默认使用Option 43学到的IP地址对应的接口*

```bash
wlan ap-group depart1
 region-code CN
 vlan 1
 vlan 11
 ap-model WA6320-HCL
  radio 1
   radio enable
   service-template depart1 vlan 11
  radio 2
   radio enable
   service-template depart1
  gigabitethernet 1
 ap ap1
 quit

wlan ap ap1 model WA6320-HCL
 mac-address 6291-cd28-0500

wlan service-template depart1
 ssid ceshi
 service-template enable

wlan auto-ap enable
wlan auto-persistent enable
```

local-user 00e007021235 class network
 service-type lan-access
 quit
00e0-0702-1235