当单个 ECS 实例需要多个 EIP 承载不同的服务时，需要使用普通模式为 ECS 实例的弹性网卡绑定多 EIP。

> 主网卡和辅助弹性网卡均支持绑定多 EIP，可根据实际组网进行选择。本文以辅助弹性网卡为例。

## 工作原理

1.  绑定多 EIP：为 ECS 实例绑定分配了多个私网 IP 的辅助弹性网卡，将多个 EIP 以普通模式与私网 IP 一一绑定。
    
2.  配置策略路由，确保出入流量路径一致：
    
    -   入向流量：当外部请求访问某个EIP时，系统会自动将流量转发到该 EIP 绑定的私网 IP。
        
    -   出向流量：为 ECS 实例配置策略路由，确保 ECS 实例能从正确的 EIP 返回响应流量。策略路由根据数据包的源 IP（即私网 IP）来决定其下一跳和出口设备（辅助弹性网卡），确保多网卡环境下路由对称，避免路由冲突。
        

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3283260871/CAEQYhiBgMDepOaFyxkiIDA0ZjA2YmUwNjIxYTRlZjZiNzczZjgxZWEwYmYxY2Qw4852813_20250418102431.140.svg)

## 适用范围

-   ECS 的不同[实例规格族](https://help.aliyun.com/zh/ecs/user-guide/overview-of-instance-families#concept-sx4-lxv-tdb)支持绑定的弹性网卡数量、可分配辅助私有 IP 数量不同。
    
    例如，`ecs.c6.large`实例规格的 ECS 实例，最多支持绑定 2 张弹性网卡（包括主网卡和辅助弹性网卡），每张网卡最多支持 6 个私网 IP。其中，主网卡和辅助弹性网卡均支持通过主私网 IP 绑定 1 个 EIP，通过辅助私网 IP 绑定 5 个 EIP。
    
-   普通模式下，EIP 以 NAT 模式与弹性网卡绑定，不支持 NAT ALG（NAT应用层网关）涉及的相关协议。
    
    -   支持绑定主弹性网卡和辅助弹性网卡。
        
    -   支持绑定的 EIP 数量取决于弹性网卡的私网 IP 数量，二者一一映射。
        
-   如果 ECS 实例所在 VPC 由 [IPv4 网关](https://help.aliyun.com/zh/vpc/ipv4-gateway-overview#1bab451593mxr)集中控制公网访问，需确保已配置路由指向 IPv4 网关允许 ECS 实例访问公网。
    

## **操作步骤**

### **步骤一：绑定多 EIP**

1.  为 ECS 实例绑定分配了多个私网 IP 的辅助弹性网卡：
    
    > 已有辅助弹性网卡时，可直接与 ECS 实例绑定。
    
    1.  前往[ECS 控制台 - 弹性网卡页面](https://ecs.console.aliyun.com/networkInterfaces/region/cn-hangzhou?resourceGroupId=rg-acfm2xy4qkf2qra)，在页面上方选择 ECS 实例所属地域。
        
    2.  单击**创建弹性网卡**。
        
        > [其余参数](https://help.aliyun.com/zh/ecs/user-guide/eni-overview#977920c31ax48)保持默认。创建完成后，可单击目标弹性网卡**操作**列的**管理弹性网卡 IP**，增加/删除/修改私网 IP。
        
        -   选择 ECS 实例所属的专有网络、交换机和安全组。
            
        -   主私网 IP：可指定交换机中未使用的 IP。不指定时，系统将从交换机的空闲地址中为弹性网卡随机分配。创建完成后，不支持修改。
            
        -   辅助私网 IPv4：选择**自动分配**，填入计划分配的辅助私网 IP 数量。
            
        
    3.  单击目标弹性网卡**操作**列的**绑定实例**，选择目标 ECS 实例。
        
2.  配置操作系统识别辅助私网 IP：
    
    > 本文以 Alibaba Cloud Linux 3.2 操作系统为例。更多方式，可参考[配置操作系统识别辅助私网IP地址](https://help.aliyun.com/zh/ecs/user-guide/assign-secondary-private-ip-addresses#631d72ee0epg2)。
    
    1.  登录 ECS 实例，执行`ip a`查看并确认网卡信息。
        
        -   网卡标识：eth0（主网卡）、eth1（辅助弹性网卡）。
            
        -   网卡状态：`state UP` 代表网卡状态正常，即网卡已经在实例内部生效。如果网卡状态为`state DOWN`，需要[配置Linux操作系统识别网卡](https://help.aliyun.com/zh/ecs/user-guide/create-and-use-an-eni#b23ba7dca4wug)。
            
        
        ```
        2: eth0: &lt;BROADCAST,MULTICAST,UP,LOWER_UP&gt; mtu 8500 qdisc mq state UP group default qlen 1000
            link/ether 00:xxx:ff
            altname enp0s5
            altname ens5
            inet 192.168.0.3/24 brd 192.168.0.255 scope global dynamic noprefixroute eth0
                valid_lft 1892159940sec preferred_lft 1892159940sec
            inet6 xxx/64 scope link
                valid_lft forever preferred_lft forever
        3: eth1: &lt;BROADCAST,MULTICAST,UP,LOWER_UP&gt; mtu 8500 qdisc mq state UP group default qlen 1000
            link/ether 00:xxx:ff
            altname enp0s7
            altname ens7
            inet 192.168.0.252/24 brd 192.168.0.255 scope global dynamic noprefixroute eth1
                valid_lft 1892159958sec preferred_lft 1892159958sec
            inet6 xxx/64 scope link noprefixroute
                valid_lft forever preferred_lft forever
        ```
        
    2.  使用`nmcli con`配置辅助私网 IP。
        
        1.  执行`sudo vim /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg`新建文件，写入`network: {config: disabled}`配置项，禁用[cloud-init自动初始化网络配置](https://help.aliyun.com/zh/ecs/user-guide/assign-secondary-private-ip-addresses#070ea1b65f9qq)，避免重启后配置失效。
            
        2.  执行`nmcli con show`查看`eth1`的网络连接名。
            
            ```
            [root@ixxx Z ~]# nmcli con show
            NAME                UUID                                  TYPE       DEVICE
            System eth0         5fb06bd0-0bb0-7ffb-45f1-d6edd65f3e03  ethernet   eth0
            Wired connection 1  c8c8d113-cd19-3945-a292-1a89d8bab4e8  ethernet   eth1
            ```
            
        3.  执行以下命令，配置辅助弹性网卡的辅助私网 IPv4 地址、默认网关。
            
            > 可执行`route -n`查看默认网关。
            
            ```
            sudo nmcli con modify "<eth1 网络连接名>" ipv4.addresses <辅助私网 IPv4 地址 1>,<辅助私网 IPv4 地址 2>
            sudo nmcli con modify "<eth1 网络连接名>" ipv4.gateway <默认网关>
            ```
            
            ```
            sudo nmcli con modify "Wired connection 1" ipv4.addresses 192.168.0.1/24,192.168.0.2/24
            sudo nmcli con modify "Wired connection 1" ipv4.gateway 192.168.0.253
            ```
            
    3.  执行`sudo nmcli con up "<eth1 网络连接名>"`，激活修改后的网络连接。返回信息出现类似`Connection successfully activated`时，代表配置成功。再次执行`ip a`，可查看到辅助私网 IP。
        
        ```
        eth1: &lt;BROADCAST,MULTICAST,UP,LOWER_UP&gt; mtu 8500 qdisc mq state UP group default qlen 1000
            link/ether 00:xxx:ff
            altname enp0s7
            altname ens7
            inet 192.168.0.1/24 brd 192.168.0.255 scope global noprefixroute eth1
               valid_lft forever preferred_lft forever
            inet 192.168.0.2/24 brd 192.168.0.255 scope global secondary noprefixroute eth1
               valid_lft forever preferred_lft forever
            inet 192.168.0.252/24 brd 192.168.0.255 scope global secondary dynamic noprefixroute eth1
               valid_lft 1892159981sec preferred_lft 1892159981sec
            inet6 fe80::xxx/64 scope link noprefixroute
               valid_lft forever preferred_lft forever
        ```
        
3.  创建多个 EIP 并绑定辅助弹性网卡：
    
    1.  前往[EIP 购买页](https://common-buy.aliyun.com/?commodityCode=eip&regionId=cn-hangzhou-dg-a01#/buy)。
        
        > 此处仅列出相关配置项，具体选型原则可参考[EIP选型指引](https://help.aliyun.com/zh/eip/elastic-ip-address#2ee08a57efl7r)。
        
        -   **付费模式**：按量付费适用于业务量不固定的场景，包年包月适用于长期稳定的业务。本文选择**按量付费**。
            
        -   **地域和可用区**：与 ECS 实例所在地域保持一致。
            
        -   **线路类型**：仅部分地域支持选择。
            
        -   **安全防护**：仅按量付费模式下的BGP（多线）EIP支持选择。
            
        -   **地址池**：已有[IP地址池](https://help.aliyun.com/zh/eip/ip-address-pools)的情况下，可以选择从已有IP地址池中分配EIP。
            
        -   **购买数量**：选择计划绑定的 EIP 数量。
            
        
    2.  将 EIP 与辅助弹性网卡的多个私网 IP 一一绑定：
        
        1.  前往[弹性公网IP](https://vpc.console.aliyun.com/eip/cn-hangzhou/eips)页面，在顶部菜单栏选择 EIP 所属地域。
            
        2.  单击目标 EIP **操作**列的**绑定资源**，选择**弹性网卡**，并选择对应的辅助私网 IP。
            

### **步骤二：配置策略路由**

为 ECS 实例配置策略路由，确保流量进出路径一致。

1.  登录 ECS 实例，为辅助弹性网卡`eth1`添加默认路由：创建路由表`table 1001`、私网 IP 的对应路由策略。
    
    ```
    ip -4 route add default via <默认网关> dev eth1 metric 1001 && \
    ip -4 route add default via <默认网关> dev eth1 table 1001 && \
    ip -4 rule add from <辅助弹性网卡的私网 IPv4 地址 1> lookup 1001 && \
    ip -4 rule add from <辅助弹性网卡的私网 IPv4 地址 2> lookup 1001 && \
    ip -4 rule add from <辅助弹性网卡的私网 IPv4 地址 3> lookup 1001
    ```
    
2.  执行`ip route list table 1001 && ip rule list`，可查看创建的路由表和策略路由。
    
    ```
    [root@iZ ~]# ip route list table 1001 && ip rule list
    default via 192.168.0.253 dev eth1
    0:      from all lookup local
    32763:  from 192.168.0.2 lookup 1001
    32764:  from 192.168.0.1 lookup 1001
    32765:  from 192.168.0.252 lookup 1001
    32766:  from all lookup main
    32767:  from all lookup default
    ```
    
3.  配置开机时自动更新路由，避免重启实例后配置失效。
    
    1.  执行`vim /etc/rc.local`，将创建路由表和策略路由的相关命令写入文件。
        
    2.  执行`sudo chmod +x /etc/rc.local`，添加执行权限。
        

### **步骤三：结果验证**

#### **验证出站 IP**

登录 ECS 实例，执行`curl --interface <辅助弹性网卡的私网 IP> https://ifconfig.me`，确认从不同私网 IP 发起访问的公网出口 IP 是对应绑定的EIP。

```
[root@iZbxxx ~]# echo $(curl --silent --interface 192.168.0.2 https://ifconfig.me)
47.xxx.xxx.13
[root@iZbxxx ~]# echo $(curl --silent --interface 192.168.0.1 https://ifconfig.me)
121.xxx.xxx.23
[root@iZbxxx ~]# echo $(curl --silent --interface 192.168.0.252 https://ifconfig.me)
121.xxx.xxx.175
```

#### **验证出入流量路径**

1.  登录其他可访问公网的测试 ECS，执行`ping <辅助弹性网卡绑定的 EIP>`。
    
2.  同时登录本 ECS 实例，执行`tcpdump -i eth1 icmp`，在 `eth1` 捕获 ICMP协议的数据包。
    

可查看到，数据包从`eth1`进入，依然从`eth1`回复，流量进出路径一致。

```
[root@iZbp1xxx_uv2Z ~]# tcpdump -i eth1 icmp
dropped privs to tcpdump
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on eth1, link-type EN10MB (Ethernet), capture size 262144 bytes
10:14:34.410905 IP 47.xxx.xxx.250 > iZbpxxx_uv2Z: ICMP echo request, id 19, seq 1, length 64
10:14:34.410944 IP iZbpxxx_juv2Z > 47.xxx.xxx.250: ICMP echo reply, id 19, seq 1, length 64
10:14:35.412272 IP 47.xxx.xxx.250 > iZbpxxx_juv2Z: ICMP echo request, id 19, seq 2, length 64
10:14:35.412307 IP iZbpxxx_juv2Z > 47.xxx.xxx.250: ICMP echo reply, id 19, seq 2, length 64
10:14:36.413675 IP 47.xxx.xxx.250 > iZbpxxx_uv2Z: ICMP echo request, id 19, seq 3, length 64
10:14:36.413707 IP iZbpxxx_juv2Z > 47.xxx.xxx.250: ICMP echo reply, id 19, seq 3, length 64
```

## **应用于生产环境**

-   **风险防范**：本方案使用单点 ECS 实例，建议使用负载均衡确保业务高可用。但需注意，实例重启或网络配置变更可能导致业务中断。
    
-   **监控与告警**：为辅助弹性网卡的网络流量、CPU和内存使用率等关键指标设置监控告警，以便及时发现异常。
    
-   **安全加固**：为辅助弹性网卡配置最小权限的安全组规则，仅放行业务必需的端口和源IP地址。
    

## **计费说明**

-   [EIP 计费](https://help.aliyun.com/zh/eip/billing-overview)：
    
    -   EIP 配置费（公网 IP 保有费）：
        
        -   按量付费EIP：当与辅助弹性网卡绑定时，即使没有公网流量，也会收取EIP配置费（公网IP保有费）。
            
        -   包年包月EIP：不收取 EIP 配置费。
            
    -   公网网络费：
        
        -   按量付费EIP：按所选的计费方式（按固定带宽或按使用流量）收取费用。
            
        -   包年包月EIP：按照带宽峰值计费。
            
-   其他资源计费：ECS实例等资源按其自身计费规则收费，辅助弹性网卡本身免费。