## VRF

VRF(Virtual Routing and Forwarding，虚拟路由转发)技术通过在一台三层转发设备上创建多张路由表实现数据或业务的隔离，常用于MPLS VPN、防火墙等一些需要实现隔离的应用场景

又被称为**VPN Instance**，也就是在物理设备上建立多个VPN实例，每个实例都有独立的接口、路由表、路由协议进程

### 配置案例

**拓扑图**
![alt text](img/VRF配置实验-拓扑.png)

1. 本端主机有PC1、PC2分别配置192.168.1.1、192.168.2.1
2. 远端主机有PC3、PC4分别配置192.168.101.2、192.168.102.2
3. 本端和远端之间先通过交换机S1，再经过路由器R1连接远端的两个主机
4. 其中PC1和PC3代表生产网络、PC2和PC4代表管理网络，希望同一网络间互通，不同网络间通过VRF（即VPN-instance）进行隔离
5. 在S1上配置VLAN10和VLAN20分别对应生产网络和管理网络
6. R1和S1之间使用一个接口互联，因此需要在R1的这个接口上划分子接口并绑定不同的VPN-instance

#### 操作过程

**为四台PC配置IP地址和网关**

略

**在S1上配置VLAN，并在端口上放通VLAN**

```bash
system-view
vlan 10
 description Production
vlan 20
 description Management

interface GigabitEthernet1/0/1
 port link-type access
 port access vlan 10

interface GigabitEthernet1/0/2
 port link-type access
 port access vlan 20

interface GigabitEthernet1/0/3
 port link-type trunk
 port trunk permit vlan 10 20
```

**在R1上配置VPN实例**

```bash
ip vpn-instance vpn-prod
 description Production_Network
ip vpn-instance vpn-mgmt
 description Management_Network
```

**配置R1的下行端口**

因为是两个实例所以要拆成两个子接口，并且要用`vlan-type dot1q vid`这个命令放通对应的VLAN

```bash
interface GigabitEthernet0/0/0.10
 ip binding vpn-instance vpn-prod
 ip address 192.168.1.254 255.255.255.0
 vlan-type dot1q vid 10

interface GigabitEthernet0/0/0.20
 ip binding vpn-instance vpn-mgmt
 ip address 192.168.2.254 255.255.255.0
 vlan-type dot1q vid 20
```

**配置R1的上行端口**

```bash
interface GigabitEthernet0/0/1
 port link-mode route
 combo enable copper
 ip binding vpn-instance vpn-prod
 ip address 192.168.101.1 255.255.255.0
            
interface GigabitEthernet0/0/2
 port link-mode route
 combo enable copper
 ip binding vpn-instance vpn-mgmt
 ip address 192.168.102.1 255.255.255.0
```

#### 查看结果

**查看VPN实例信息**

```bash
<R1>show ip vpn-instance instance-name vpn-prod 
  VPN-Instance Name and Index : vpn-prod, 1
  Description : Production_Network
  Interfaces : GigabitEthernet0/0/0.10, GigabitEthernet0/0/1
  TTL mode: pipe

<R1>show ip vpn-instance instance-name vpn-mgmt 
  VPN-Instance Name and Index : vpn-mgmt, 2
  Description : Management_Network
  Interfaces : GigabitEthernet0/0/0.20, GigabitEthernet0/0/2
  TTL mode: pipe
```

**查看各实例的路由表**

```bash
<R1>display ip routing-table vpn-instance vpn-prod
Destinations : 8	Routes : 8

Destination/Mask   Proto   Pre Cost        NextHop         Interface
127.0.0.0/8        Direct  0   0           127.0.0.1       InLoop0
192.168.1.0/24     Direct  0   0           192.168.1.254   GE0/0/0.10
192.168.1.254/32   Direct  0   0           127.0.0.1       GE0/0/0.10
192.168.1.255/32   Direct  0   0           192.168.1.254   GE0/0/0.10
192.168.101.0/24   Direct  0   0           192.168.101.1   GE0/0/1
192.168.101.1/32   Direct  0   0           127.0.0.1       GE0/0/1
192.168.101.255/32 Direct  0   0           192.168.101.1   GE0/0/1
255.255.255.255/32 Direct  0   0           127.0.0.1       InLoop0

<R1>display ip routing-table vpn-instance vpn-mgmt
Destinations : 8	Routes : 8

Destination/Mask   Proto   Pre Cost        NextHop         Interface
127.0.0.0/8        Direct  0   0           127.0.0.1       InLoop0
192.168.2.0/24     Direct  0   0           192.168.2.254   GE0/0/0.20
192.168.2.254/32   Direct  0   0           127.0.0.1       GE0/0/0.20
192.168.2.255/32   Direct  0   0           192.168.2.254   GE0/0/0.20
192.168.102.0/24   Direct  0   0           192.168.102.1   GE0/0/2
192.168.102.1/32   Direct  0   0           127.0.0.1       GE0/0/2
192.168.102.255/32 Direct  0   0           192.168.102.1   GE0/0/2
255.255.255.255/32 Direct  0   0           127.0.0.1       InLoop0
```

全局的路由表中已经没有这两个实例中的路由信息了

```bash
<R1>show ip routing-table 
Destinations : 4	Routes : 4

Destination/Mask   Proto   Pre Cost        NextHop         Interface
127.0.0.0/8        Direct  0   0           127.0.0.1       InLoop0
127.0.0.1/32       Direct  0   0           127.0.0.1       InLoop0
127.255.255.255/32 Direct  0   0           127.0.0.1       InLoop0
255.255.255.255/32 Direct  0   0           127.0.0.1       InLoop0
```

**在PC1上尝试ping PC3和PC4**

```bash
<PC1>ping 192.168.101.1
Ping 192.168.101.1 (192.168.101.1): 56 data bytes, press CTRL_C to break
56 bytes from 192.168.101.1: icmp_seq=0 ttl=255 time=1.468 ms
56 bytes from 192.168.101.1: icmp_seq=1 ttl=255 time=0.466 ms
56 bytes from 192.168.101.1: icmp_seq=2 ttl=255 time=0.857 ms
56 bytes from 192.168.101.1: icmp_seq=3 ttl=255 time=0.572 ms
56 bytes from 192.168.101.1: icmp_seq=4 ttl=255 time=0.818 ms

--- Ping statistics for 192.168.101.1 ---
5 packet(s) transmitted, 5 packet(s) received, 0.0% packet loss
round-trip min/avg/max/std-dev = 0.466/0.836/1.468/0.348 ms


<PC1>ping 192.168.102.1
Ping 192.168.102.1 (192.168.102.1): 56 data bytes, press CTRL_C to break

--- Ping statistics for 192.168.102.1 ---
1 packet(s) transmitted, 0 packet(s) received, 100.0% packet loss
```
可以看到PC1能ping通PC3但是ping不通PC4

