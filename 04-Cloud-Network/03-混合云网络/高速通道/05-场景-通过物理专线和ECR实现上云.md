本文为您介绍如何使用两条物理专线和专线网关ECR，实现本地数据中心IDC通过主备冗余链路接入方式上云并和云上专有网络VPC互通。

## 场景示例

某企业在华北2（北京）拥有本地IDC，且在同地域已创建转发路由器TR及专有网络VPC。现需要通过专线网关ECR功能，使本地IDC中的服务器通过主备冗余链路方式访问云上服务。正常情况下仅用主链路转发流量，当BFD探测到主链路不可达时，流量将被切换至备链路，确保业务不受影响。

具体步骤如下：

1.  部署物理专线：部署两条物理专线，分别连接本地IDC的不同CPE设备和VBR，两条专线形成主备冗余链路。
    
2.  创建边界路由器VBR：在华北2（北京）创建两个VBR（VBR1、VBR2），作为本地IDC与VPC间的私有网络桥梁。
    
3.  创建专线网关ECR：创建ECR作为本地IDC与云上VPC的转发服务组件。
    
4.  绑定VBR和TR至ECR：将VBR1、VBR2及转发路由器TR绑定至ECR，建立物理专线与云资源的逻辑关联。
    
5.  配置BGP并开启BFD：配置本地IDC与VBR间的BGP动态路由，并启用BFD功能，实现路由快速收敛及链路故障自动切换。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1821930871/CAEQXxiBgMDQo6jBwhkiIDRlZGZiNDVmYTAwYzQzOThiZDYwMGE3NjViYTliNTFi4122902_20231220095134.007.svg)

## 前提条件

-   已在华北2（北京）地域[创建专有网络VPC](https://help.aliyun.com/zh/vpc/create-and-manage-a-vpc)，且该VPC中的ECS部署了相关业务。
    
-   已在华北2（北京）地域创建[转发路由器TR](https://help.aliyun.com/zh/cen/user-guide/transit-routers)，且为该转发路由器TR[创建VPC连接](https://help.aliyun.com/zh/cen/user-guide/connect-vpcs/)。
    
-   确保VPC中ECS绑定的安全组配置的规则，允许本地IDC的流量访问。具体参见[添加安全组规则](https://help.aliyun.com/zh/ecs/user-guide/add-a-security-group-rule#concept-sm5-2wz-xdb)。
    

## **操作步骤**

### **步骤一：申请物理端口**

本文使用高可靠模式的[强大容灾能力](https://help.aliyun.com/zh/document_detail/2580081.html)申请端口，申请后系统将创建2个物理端口实例。

### **步骤二：创建边界路由器VBR**

1.  登录[高速通道管理控制台](https://expressconnectnext.console.aliyun.com/)，在顶部菜单栏选择华北2（北京）地域。
    
2.  在**物理端口**页面，单击目标物理端口实例，在详情页单击**创建边界路由器**，创建VBR1。
    
3.  在**创建边界路由器**面板，选择账号类型为**当前账号**，配置以下关键参数，单击**确定**。
    
    关键参数包括：**物理专线接口**选择独享专线并在下拉框中选择对应的物理专线接口实例，**VLAN ID**（例如`1308`），**设置VBR带宽值**（例如`200Mb`），**阿里云侧IPv4互联IP**（例如`10.10.1.3`），**客户侧IPv4互联IP**（例如`10.10.1.2`），**IPv4子网掩码**（例如`255.255.255.0`）。
    
4.  重复上述步骤，创建边界路由器VBR2，单击**确定**。
    
    VBR2 的物理专线接口信息配置参数：物理专线接口选择 **独享专线**，**VLAN ID** 填写 `1309`，VBR 带宽值选择 **200Mb**，**阿里云侧IPv4互联IP** 填写 `10.10.2.3`，**客户侧IPv4互联IP** 填写 `10.10.2.2`，**IPv4子网掩码** 填写 `255.255.255.0`，**支持IPv6** 选择 **不开启**。
    

### **步骤三：创建并绑定专线网关ECR至TR和VBR**

1.  **创建专线网关ECR**
    
    1.  在左侧导航栏，单击**专线网关**，然后单击**创建专线网关**。
        
    2.  在对话框中输入 **ASN** 为`64512`，其余参数保持默认值，勾选计费规则，单击**确定**。
        
2.  **绑定专线网关ECR至VBR**
    
    1.  单击目标ECR实例ID，在**VBR**页签单击**添加VBR**。
        
    2.  在弹出的对话框配置以下参数，单击**确定**。
        
        -   **资源归属**：选择`同账号`。
            
        -   **地域**：`华北2（北京）`。
            
        -   **网络实例**：选择已创建的VBR1实例。
            
    3.  重复以上步骤绑定专线网关ECR至VBR2。
        
3.  **绑定专线网关ECR至TR**
    
    1.  单击目标ECR实例ID，然后单击 **TR** 页签。
        
    2.  单击关联转发路由器，在对话框中配置以下参数（未列出参数保持默认值），单击**确定**。
        
        -   **CEN ID**：选择已创建的云企业网实例。
            
        -   **地域**：`华北2（北京）`。
            
        -   **转发路由器**：选择已创建的转发路由器实例。
            

### **步骤四：配置BGP并开启BFD**

您需要为本地网关设备和VBR配置BGP邻居关系。当两者的BGP邻居状态均为**已建立**时，表示BGP会话成功建立，可以开始交换路由信息。

邻居关系建立后，本地IDC即可通过BGP自动学习到云上路由。在本地网关设备侧宣告本地IDC网段，使VBR自动学习到本地IDC的路由。完成上述配置，本地IDC的服务器即可访问云上资源。

#### **在VBR侧配置BGP路由**

1.  登录[高速通道管理控制台](https://expressconnectnext.console.aliyun.com/)为VBR1配置BGP路由。
    
2.  在左侧导航栏单击**边界路由器VBR**，找到目标VBR1实例ID，进入详情页配置BGP路由：
    
    1.  单击**创建BGP组**，配置如下参数，单击**确定**。
        
        -   **Peer AS号**：输入本地IDC侧网络的AS号`6***3`。
            
        -   **本端AS号**：输入阿里云侧AS号`64512`（VBR的BGP ASN继承ECR的ASN）。
            
    2.  单击**创建BGP邻居**，配置如下参数，并勾选**启用BFD**，单击**确定**。
        
        -   **BGP组**：选择已创建的BGP组。
            
        -   **BGP邻居IP**：输入BGP邻居的IP地址。本文输入CPE1连接物理专线的接口的IP地址10.10.1.5。
            
3.  重复以上步骤为VBR2配置BGP路由。
    

#### **在IDC侧配置BGP路由**

##### **IDC发布至VPC的BGP路由**

在CPE1和CPE2侧调整IDC发布192.168.0.0/16网段路由的AS-Path长度（AS-Path长度越短，优先级越高），来控制从IDC发布至VPC的路由选路优先级。

本文选择为CPE2追加 AS-Path，通过增加AS-Path长度，降低VBR2实例向VPC发布本地IDC网段的优先级，使VBR1成为主链路，VBR2成为备链路，两条专线在流量下云方向形成主备冗余链路。

**说明**

不同厂商的不同设备配置命令会有所不同，本文仅列出配置关键参数，具体配置命令请咨询设备厂商，根据实际进行配置。

| **配置** | **CPE1** | **CPE2** |
| --- | --- | --- |
| Vlan Tag | 1308 | 1309 |
| Network | 192.168.0.0/16 | 192.168.0.0/16 |
| BGP ASN | 6\\*\\*\\*3 | 6\\*\\*\\*4 |
| Interface IP | 10.10.1.5 | 10.10.2.5 |
| AS-Path | A   | B，A |

##### **VPC发布至IDC的BGP路由**

在IDC侧通过调整从VBR1和VBR2学习到VPC网段10.0.0.0/8路由的BGP选路属性，使VBR1成为主链路、VBR2成为备链路，两条专线在流量上云方向形成主备冗余链路。

### **步骤五：验证测试**

1.  网络连通性测试。
    
    登录VPC实例下的ECS实例，执行`ping <本地IDC客户端的IP地址>`命令，尝试访问本地IDC中的客户端。
    
    收到如下响应报文，表示本地IDC和VPC实例之间的网络已连通。
    
    ```
    [root@China xxx 2564ek5zZ ~]$ ping 192.168.3.20
    PING 192.168.3.20 (192.168.3.20) 56(84) bytes of data.
    64 bytes from 192.168.3.20: icmp_seq=1 ttl=60 time=1.38 ms
    64 bytes from 192.168.3.20: icmp_seq=2 ttl=60 time=1.17 ms
    64 bytes from 192.168.3.20: icmp_seq=3 ttl=60 time=1.16 ms
    64 bytes from 192.168.3.20: icmp_seq=4 ttl=60 time=1.15 ms
    64 bytes from 192.168.3.20: icmp_seq=5 ttl=60 time=1.16 ms
    64 bytes from 192.168.3.20: icmp_seq=6 ttl=60 time=1.16 ms
    64 bytes from 192.168.3.20: icmp_seq=7 ttl=60 time=1.11 ms
    ^C
    --- 192.168.3.20 ping statistics ---
    7 packets transmitted, 7 received, 0% packet loss, time 6006ms
    rtt min/avg/max/mdev = 1.113/1.179/1.379/0.086 ms
    ```
    
2.  执行`traceroute`命令查看两条物理专线是否实现主备链路冗余链路。如果未安装`traceroute`，以CentOS系统为例可参考执行`sudo yum install traceroute`安装。
    
    -   **VPC到IDC方向**
        
        登录VPC内的ECS实例，执行 `traceroute <本地IDC客户端的IP地址>` 命令，收到如下响应报文表示VPC到IDC方向的流量通过主链路VBR1转发。
        
        ```
        $ traceroute 192.168.3.20
        traceroute to 192.168.3.20 (192.168.3.20), 30 hops max, 60 byte packets
         1  100.64.1.241 (100.64.1.241)  1.451 ms  2.301 ms  2.827 ms
         2  100.64.1.241 (100.64.1.241)  2.047 ms  2.559 ms  1.790 ms
         3  10.10.1.5 (10.10.1.5)  1.124 ms  1.208 ms  1.320 ms    # VBR1
         4  192.168.3.20 (192.168.3.20)  1.391 ms  1.283 ms  1.385 ms
        ```
        
    -   **IDC到VPC方向**
        
        登录本地IDC下的客户端，执行`traceroute <VPC下的ECS实例IP>`命令，收到如下响应报文表示IDC到VPC方向的流量通过主链路VBR1转发。
        
        ```
        [xxx@alf3tw6Z ~]$ traceroute 10.1.2.61
        traceroute to 10.1.2.61 (10.1.2.61), 30 hops max, 60 byte packets
         1  100.64.0.81 (100.64.0.81)  0.890 ms  1.154 ms  1.360 ms
         2  100.64.0.81 (100.64.0.81)  1.618 ms  1.871 ms  2.099 ms
         3  10.10.1.3 (10.10.1.3)  0.854 ms  0.976 ms  0.686 ms
         4  10.1.2.61 (10.1.2.61)  1.360 ms  1.349 ms  1.338 ms
        ```
        
3.  模拟VBR1链路故障。本文通过[故障演练](https://help.aliyun.com/zh/express-connect/user-guide/failover-test)功能模拟断开主链路VBR1，测试流量是否切换至备链路。
    
4.  再次执行`traceroute`命令测试流量是否会被切换到VBR2链路。
    
    -   **VPC到IDC方向**
        
        登录VPC下的ECS实例，执行`traceroute <本地IDC客户端的IP地址>`命令，收到如下响应报文表示VPC到IDC方向流量已被切换到VBR2。
        
        其中第3跳 10.10.2.5 即为VBR2。
        
        ```
        [root@lppy32564ek5zZ ~]$ traceroute 192.168.3.20
        traceroute to 192.168.3.20 (192.168.3.20), 30 hops max, 60 byte packets
         1  100.64.2.1 (100.64.2.1)  1.774 ms  2.834 ms  2.048 ms
         2  100.64.2.1 (100.64.2.1)  1.360 ms  2.279 ms  2.585 ms
         3  10.10.2.5 (10.10.2.5)  1.201 ms  1.455 ms  1.340 ms
         4  192.168.3.20 (192.168.3.20)  1.342 ms  1.358 ms  1.332 ms
        ```
        
    -   **IDC到VPC方向**
        
        登录本地IDC下的客户端，执行`traceroute <VPC下的ECS实例IP>`命令，收到如下响应报文表示IDC到VPC方向流量已被切换到VBR2。
        
        ```
        [xxx zazcq7ialf3tw6Z ~]$ traceroute 10.1.2.61
        traceroute to 10.1.2.61 (10.1.2.61), 30 hops max, 60 byte packets
        1  100.64.1.65 (100.64.1.65)  1.442 ms  1.360 ms  1.469 ms
        2  100.64.1.65 (100.64.1.65)  2.082 ms  2.069 ms  2.056 ms
        3  10.10.2.3 (10.10.2.3)  1.292 ms  1.281 ms  1.266 ms
        4  10.1.2.61 (10.1.2.61)  1.411 ms  1.995 ms  1.982 ms
        ```
        

## **相关文档**

若您需要实现负载专线上云，请参见[本地IDC通过ECR实现负载专线链路上云](https://help.aliyun.com/zh/express-connect/use-cases/the-local-idc-can-use-ecr-to-link-the-load-to-the-cloud)。