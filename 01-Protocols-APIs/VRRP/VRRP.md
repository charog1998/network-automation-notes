## VRRP

VRRP(Virtual Router Redundancy Protocol，虚拟路由器冗余协议)既能够实现网关的备份，又能解决多个网关之间互相冲突的问题，从而提高网络可靠性

类似于交换机的堆叠和集群，运行结果是提供了一台虚拟路由器，不过VRRP依靠协议实现，堆叠集群依靠硬件或软件实现

**VRRP组、VRID、Master路由器、Backup路由器**

一个VRRP组由多台路由器组成，使用相同的VRID（虚拟路由器ID），一个VRRP组只能存在一台Master路由器，其他设备为Backup路由器

**虚拟IP、MAC**

虚拟IP由管理员指定，一台虚拟路由器可以有多个地址

虚拟MAC地址的格式为`0000-5e00-01xx`，其中`xx`为VRID

### 报文

VRRP只有一种Advertisement报文，基于组播方式发送，目的地址为`224.0.0.18`

### 状态机


Master-->Backup: 收到优先级比本地大的报文
Backup-->Master: MASTER_DOWN定时器超时或收到优先级为0的通告报文或优先级比本地小的报文

Master-->Initialize: 收到shutdown消息
Initialize-->Master: 收到Startup且优先级为255

Backup-->Initialize: 收到shutdown消息
Initialize-->Backup: 收到Startup且优先级小于为255

**Master状态**

1. 定期(ADVERINTERVAL)发送VRRP报文
2. 以虚拟MAC地址响应对虚拟IP地址的ARP请求
3. 转发目的MAC地址为虚拟MAC地址的IP报文
4. 默认允许ping通虚拟IP地址
5. 当多台设备同时为Master时，若设备收到与自己优先级相同的报文时，会进一步比较IP地址的大小。如果收到报文的源IP地址比自己大，则切换到Backup状态否则保持Master状态

**Backup状态**
1. 接收Master设备发送的VRRP报文，判断Master设备的状态是否正常
2. 对虚拟IP地址的ARP请求，不做响应
3. 丢弃目的MAC地址为虚拟MAC地址的IP报文
4. 丢弃目的IP地址为虚拟IP地址的IP报文
5. 如果收到优先级和自己相同或者比自己优先级大的报文时，重置MASTER_DOWN定时器，不进一步比较IP地址的大小

*如果优先级相同则IP地址大的成为Master*

### 实验

**拓扑图**

![alt text](img/VRRP实验拓扑.png)

*交换机型号为H3C S6850*

#### 实验步骤

**配置vlan、为端口放行vlan**
略

**配置mstp**

配置两个实例分别对应vlan10和20

```bash
# 在每台交换机上配置MSTP
stp region-configuration
region-name hcip
revision-level 1
instance 1 vlan 10
instance 2 vlan 20
active region-configuration
quit

# 配置S1为实例1的根桥，实例2的备份根桥
[S1]stp instance 1 root primary 
[S1]stp instance 2 root secondary

# 配置S2为实例2的根桥，实例1的备份根桥
[S2]stp instance 2 root primary 
[S2]stp instance 1 root secondary 
```

**检查实例与Vlan的映射关系**

```bash
[S1]show stp region-configuration 
 Oper Configuration
   Format selector      : 0
   Region name          : hcip
   Revision level       : 1
   Configuration digest : 0x9357ebb7a8d74dd5fef4f2bab50531aa

   Instance  VLANs Mapped
   0         1 to 9, 11 to 19, 21 to 4094
   1         10
   2         20
```

**在S1和S2上查看实例1、2的状态**

```bash
[S1]show stp instance 1 br
 MST ID   Port                                Role  STP State   Protection
 1        GigabitEthernet1/0/10               DESI  FORWARDING  NONE
 1        GigabitEthernet1/0/11               DESI  FORWARDING  NONE
 1        GigabitEthernet1/0/12               DESI  FORWARDING  NONE

[S2]show stp instance 2 br
 MST ID   Port                                Role  STP State   Protection
 2        GigabitEthernet1/0/10               DESI  FORWARDING  NONE
 2        GigabitEthernet1/0/11               DESI  FORWARDING  NONE
 2        GigabitEthernet1/0/13               DESI  FORWARDING  NONE
```

可以看到都是指定接口因此已经成为了对应实例的根桥

**VRRP配置**

在S1、S2均创建VLANIF 10、20，分别加入VRRP组 10、20

手动配置VRRP优先级，使得S1的VLAN10成为 VRRP Master、S2的VLAN20成为 VRRP Master

```bash
# S1
interface Vlan-interface 10
ip address 10.0.10.1 255.255.255.0
vrrp vrid 10 virtual-ip 10.0.10.254
vrrp vrid 10 priority 120
quit

interface Vlan-interface 20
ip address 10.0.20.1 255.255.255.0
vrrp vrid 20 virtual-ip 10.0.20.254
quit

# S2
interface Vlan-interface 10
ip address 10.0.10.2 255.255.255.0
vrrp vrid 10 virtual-ip 10.0.10.254
quit

interface Vlan-interface 20
ip address 10.0.20.2 255.255.255.0
vrrp vrid 20 virtual-ip 10.0.20.254
vrrp vrid 20 priority 120
quit
```

**查看VRRP配置结果**

```bash
[S1]show vrrp 
IPv4 Virtual Router Information:  
 Running mode : Standard
 Total number of virtual routers : 2
 Interface          VRID  State        Running Adver   Auth             Virtual
                                       Pri     Timer   Type                IP
 ----------------------------------------------------------------------------
 Vlan10             10    Master       120     100     Not supported    10.0.10.254     
 Vlan20             20    Backup       100     100     Not supported    10.0.20.254 

[S2]show vrrp
IPv4 Virtual Router Information:  
 Running mode : Standard
 Total number of virtual routers : 2
 Interface          VRID  State        Running Adver   Auth             Virtual
                                       Pri     Timer   Type                IP
 ----------------------------------------------------------------------------
 Vlan10             10    Backup       100     100     Not supported    10.0.10.254     
 Vlan20             20    Master       120     100     Not supported    10.0.20.254 
```
可以看到配置结果符合预期

**创建BFD会话**

```bash
# S1
bfd static 1to2 peer-ip 10.0.10.2 interface Vlan-interface10 source-ip 10.0.10.1 
 discriminator local 1 
 discriminator remote 2 
 bfd min-transmit-interval 100
 bfd min-receive-interval 100
 bfd detect-multiplier 3
 quit

bfd static 1to2vlan20 peer-ip 10.0.20.2 interface Vlan-interface20 source-ip 10.0.20.1 
 discriminator local 11 
 discriminator remote 22 
 bfd min-transmit-interval 100
 bfd min-receive-interval 100
 bfd detect-multiplier 3
 quit

# 检查下会话信息
[S1]show bfd session 
 Total sessions: 2     Up sessions: 0     Init mode: Active

 IPv4 static session working in control packet mode:

 LD/RD            SourceAddr      DestAddr        State  Holdtime    Interface
 1/2              10.0.10.1       10.0.10.2       Down      /        Vlan10     
 11/22            10.0.20.1       10.0.20.2       Down      /        Vlan20 
```

```bash
# S2
bfd static 2to1 peer-ip 10.0.10.1 interface Vlan-interface10 source-ip 10.0.10.2 
 discriminator local 2 
 discriminator remote 1 
 bfd min-transmit-interval 100
 bfd min-receive-interval 100
 bfd detect-multiplier 3
 quit

bfd static 2to1vlan20 peer-ip 10.0.20.1 interface Vlan-interface20 source-ip 10.0.20.2 
 discriminator local 22 
 discriminator remote 11 
 bfd min-transmit-interval 100
 bfd min-receive-interval 100
 bfd detect-multiplier 3
 quit
```

**将VRRP与BFD相关联**

需要先使用`track 1 bfd static 1to2`创建与1to2关联的Track项

```bash
# S1
track 1 bfd static 1to2
quit

interface Vlan-interface10
#  ip address 10.0.10.1 255.255.255.0
#  vrrp vrid 10 virtual-ip 10.0.10.254
#  vrrp vrid 10 priority 120
 vrrp vrid 10 track 1 priority reduced 50
quit
# 意为当track项转为negative时将VRRP权限降低50
```

```bash
# S2
track 1 bfd static 2to1vlan20
quit

interface Vlan-interface20
#  ip address 10.0.20.2 255.255.255.0
#  vrrp vrid 20 virtual-ip 10.0.20.254
#  vrrp vrid 20 priority 120
 vrrp vrid 20 track 1 priority reduced 50
quit
```

#### 结果验证

在S1上关闭Vlanif10之后观察S2的VRRP状态

```bash
[S1-Vlan-interface10]shutdown
[S1-Vlan-interface10]show vrrp
IPv4 Virtual Router Information:  
 Running mode : Standard
 Total number of virtual routers : 2
 Interface          VRID  State        Running Adver   Auth             Virtual
                                       Pri     Timer   Type                IP
 ----------------------------------------------------------------------------
 Vlan10             10    Initialize   70      100     Not supported    10.0.10.254     
 Vlan20             20    Backup       100     100     Not supported    10.0.20.254

[S2-Vlan-interface20]show vrrp
IPv4 Virtual Router Information:  
 Running mode : Standard
 Total number of virtual routers : 2
 Interface          VRID  State        Running Adver   Auth             Virtual
                                       Pri     Timer   Type                IP
 ----------------------------------------------------------------------------
 Vlan10             10    Master       100     100     Not supported    10.0.10.254     
 Vlan20             20    Master       120     100     Not supported    10.0.20.254     
```
可以看到
1. S1在接收到shutdown消息后转为了Initialize状态
2. 如果在S1上重新打开Vlanif10则会恢复为1主2备的状态
3. 在检测到链路故障后S2升级为了Vlan10的Master设备

反之在S2上操作Vlanif20也有类似效果

#### 报文记录

在关闭S1的Vlanif10接口时

S1的动作为
```bash
%Mar 15 00:49:03:423 2025 S1 VRRP4/6/VRRP_STATUS_CHANGE: The status of IPv4 virtual router 10 (configured on Vlan-interface10) changed from Master to Initialize: Interface event received.
%Mar 15 00:49:03:424 2025 S1 BFD/5/BFD_CHANGE_FSM: Sess[10.0.10.1/10.0.10.2, LD/RD:1/2, Interface:Vlan10, SessType:Ctrl, LinkType:INET], Ver:1, Sta: UP->DOWN, Diag: 1 (Control Detection Time Expired)
%Mar 15 00:49:03:425 2025 S1 TRACK/6/TRACK_STATE_CHANGE: The state of track entry 1 changed from Positive to Negative.
%Mar 15 00:49:03:426 2025 S1 IFNET/3/PHY_UPDOWN: Physical state on the interface Vlan-interface10 changed to down.
%Mar 15 00:49:03:426 2025 S1 IFNET/5/LINK_UPDOWN: Line protocol state on the interface Vlan-interface10 changed to down.
```

S2的动作为
```bash
%Mar 15 00:49:06:154 2025 S2 BFD/5/BFD_CHANGE_FSM: Sess[10.0.10.2/10.0.10.1, LD/RD:2/1, Interface:Vlan10, SessType:Ctrl, LinkType:INET], Ver:1, Sta: UP->DOWN, Diag: 3 (Neighbor Signaled Session Down)
%Mar 15 00:49:06:759 2025 S2 VRRP4/6/VRRP_STATUS_CHANGE: The status of IPv4 virtual router 10 (configured on Vlan-interface10) changed from Backup to Master: Zero priority packet received.
```

重新打开S1的Vlanif10接口时

S1的动作为
```bash
%Mar 15 00:52:59:492 2025 S1 IFNET/3/PHY_UPDOWN: Physical state on the interface Vlan-interface10 changed to up.
%Mar 15 00:52:59:492 2025 S1 IFNET/5/LINK_UPDOWN: Line protocol state on the interface Vlan-interface10 changed to up.
%Mar 15 00:52:59:513 2025 S1 BFD/5/BFD_CHANGE_FSM: Sess[10.0.10.1/10.0.10.2, LD/RD:1/2, Interface:Vlan10, SessType:Ctrl, LinkType:INET], Ver:1, Sta: DOWN->UP, Diag: 0 (No Diagnostic)
%Mar 15 00:52:59:513 2025 S1 TRACK/6/TRACK_STATE_CHANGE: The state of track entry 1 changed from Negative to Positive.
%Mar 15 00:53:00:365 2025 S1 VRRP4/6/VRRP_STATUS_CHANGE: The status of IPv4 virtual router 10 (configured on Vlan-interface10) changed from Backup to Master: Preempt.
```

S2的动作为
```bash
%Mar 15 00:53:02:442 2025 S2 BFD/5/BFD_CHANGE_FSM: Sess[10.0.10.2/10.0.10.1, LD/RD:2/1, Interface:Vlan10, SessType:Ctrl, LinkType:INET], Ver:1, Sta: DOWN->INIT, Diag: 0 (No Diagnostic)
%Mar 15 00:53:02:442 2025 S2 BFD/5/BFD_CHANGE_FSM: Sess[10.0.10.2/10.0.10.1, LD/RD:2/1, Interface:Vlan10, SessType:Ctrl, LinkType:INET], Ver:1, Sta: INIT->UP, Diag: 0 (No Diagnostic)
%Mar 15 00:53:03:295 2025 S2 VRRP4/6/VRRP_STATUS_CHANGE: The status of IPv4 virtual router 10 (configured on Vlan-interface10) changed from Master to Backup: VRRP packet received.
```