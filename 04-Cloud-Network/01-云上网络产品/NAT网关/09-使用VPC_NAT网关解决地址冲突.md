为了连通网段重叠的 VPC，可添加附加网段并创建 VPC NAT 网关，通过地址转换解决地址冲突。

## **工作原理**

### **地址冲突原因**

网段重叠的 VPC 和交换机中的 ECS 互访时：

-   配置对端VPC网段作为目标网段：流量会优先匹配系统路由，在 VPC 内部转发，无法抵达对端 VPC。
    
-   配置对端交换机网段作为目标网段：无法配置与已有系统路由目标网段相同或更明细的自定义路由。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8221833771/CAEQYxiBgMDk5.HD0BkiIDAyN2M0MDlhZGRlYTRiMmQ5NmIzZWFkMjliMDkwOWY04585827_20240820105942.020.svg)

### **NAT 解决方案**

1.  **添加附加IPv4网段**：为 2 个 VPC 分别添加不重叠的附加网段，提供不冲突的私网地址。
    
2.  **地址转换**：使用 VPC NAT 网关转换 ECS 的私网 IP，解决私网地址冲突。
    
3.  **VPC 互通**：将 VPC 接入转发路由器，并配置自定义路由条目，确保流量正确转发。
    

### **流量路径示例**

某企业在华东1（杭州）地域计划连通已创建的 2 个 VPC，但 VPC 网段重叠。使用 VPC NAT 网关实现地址转换，并结合路由配置确保流量转发至 VPC NAT 网关后，可部署云企业网/对等连接实现私网互通。

以 ECS\_A（私网IP：192.168.0.86）访问 VPC\_NATGW\_B（私网IP：10.0.0.53）为例。

1.  按照 ECS\_A 所在交换机绑定的自定义路由表的路由配置，访问数据包转发至 VPC\_NAT 网关。
    
2.  按照 VPC\_NAT\_A 配置的 SNAT 规则，数据包的源 IP 将转换为 NAT IP（172.16.0.89）。
    
3.  按照 VPC\_A 系统路由表的路由配置，数据包将转发至转发路由器 TR，再由 TR 转发至 VPC\_B，从而到达 VPC\_B 的VPC NAT网关。
    
4.  按照 VPC\_NAT\_B 配置的 DNAT 规则，数据包的目的地址将转换为 ECS\_B，流量转发至目标服务器，从而实现 ECS 互访。
    

当 ECS\_B 返回响应数据包时，将按照会话映射表还原为原始的私网 IP，并按照路由最终送达 ECS\_A。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8221833771/CAEQYxiBgMDK6PDizBkiIDc3ZjQ3NjAxMThhMDQ1NjE4NzcwN2JhNjliZTIyMzA04585827_20240820105942.020.svg)

## **操作步骤**

以流量路径的示例场景为例。

### 步骤一：配置附加网段

1.  添加附加网段：
    
    1.  前往[专有网络列表页](https://vpcnext.console.aliyun.com/vpc/cn-hangzhou/vpcs)。在顶部菜单栏选择 VPC 所属地域。
        
    2.  单击目标VPC ID，选择**网段管理**页签，单击**添加附加IPv4网段**，分别为VPC\_A、VPC\_B添加附加网段。
        
2.  创建交换机：前往[创建交换机页面](https://vpc.console.aliyun.com/vpc/cn-hangzhou/switches/new)。
    
    -   **专有网络**：分别为 VPC\_A、VPC\_B 创建交换机。
        
    -   **IPv4网段**：选择已添加的附加IPv4网段。
        
    

### **步骤二：配置VPC NAT网关**

创建 VPC NAT 网关并配置 SNAT 条目和 DNAT 条目，将各自 VPC 中的 ECS 实例私网 IP 与 NAT IP 互相转换，解决地址冲突。

1.  创建 VPC NAT 网关：前往[VPC NAT 网关购买页](https://vpc.console.aliyun.com/buy/nat?regionId=cn-hangzhou&networkType=intranet)。
    
    -   **地域**：选择 VPC 所属地域。
        
    -   **网络及可用区**：分别为VPC\_A、VPC\_B创建VPC NAT网关，选择使用附加网段创建的交换机。
        
    
2.  配置 SNAT 条目：VPC NAT 网关将按照配置的 SNAT 规则将数据包的源 IP 转换为 NAT IP 地址。
    
    1.  前往[VPC NAT 网关列表页](https://vpc.console.aliyun.com/vpc-nat/cn-hangzhou/nats)，在顶部菜单栏选择 VPC NAT 所属地域。
        
    2.  单击目标 VPC NAT 实例**操作**列的**SNAT**管理。单击**创建SNAT条目**。
        
        -   **SNAT条目粒度**：本文选择**专有网络粒度**，可以根据自身需求调整。
            
        -   **选择NAT IP地址**：选择 VPC NAT 网关的私网 IP。
            
        
3.  配置 DNAT 条目：VPC NAT 网关将按照配置的 DNAT 规则将数据包的目的 IP 转换为 NAT IP 地址。
    
    1.  前往[VPC NAT 网关列表页](https://vpc.console.aliyun.com/vpc-nat/cn-hangzhou/nats)，在顶部菜单栏选择 VPC NAT 所属地域。
        
    2.  单击目标 VPC NAT 实例**操作**列的**DNAT**管理。单击**创建DNAT条目**。
        
        -   **选择NAT IP地址**：选择 VPC NAT 网关的私网 IP。
            
        -   **选择私网IP地址**：选择 VPC 中需互通的 ECS 实例。
            
        -   **端口设置**：本文以SSH服务作为内网互通的验证方式。SSH 服务采用面向连接的TCP协议传输，应用22号端口。故配置**具体端口**的前端端口和后端端口均为22，协议类型选择TCP。
            
            > 可以根据自身实际需求创建对应的DNAT条目。
            
        

### **步骤三：**连通 VPC

1.  创建 VPC 连接：
    
    > [转发路由器支持的地域和可用区](https://help.aliyun.com/zh/cen/product-overview/regions-and-zones-that-support-transit-router)。
    
    > 本示例为同账号同地域 VPC 互通。需根据 VPC 账号与地域归属，参考[跨地域VPC互通](https://help.aliyun.com/zh/cen/getting-started/inter-region-vpc-interworking)或[跨账号VPC互通](https://help.aliyun.com/zh/cen/getting-started/use-enterprise-edition-transit-routers-to-connect-vpcs-across-regions-and-accounts)。
    
    1.  前往[云企业网管理控制台](https://cen.console.aliyun.com/)，单击**创建云企业网实例**。选择**单独创建**并**确认**。
        
    2.  创建成功后，单击**创建网络实例连接** > **创建地域内连接**。
        
        > 本文示例中地址冲突的 VPC 位于同地域，需创建地域内连接。需要连通不同地域的 VPC 时，选择创建跨地域连接。
        
        > 也可以单击已创建的 CEN ID，在基本信息页签下单击 VPC 下的![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7542091771/p1054575.png)创建地域内连接。
        
        -   **实例类型**：选择专有网络（VPC）。
            
        -   **地域**：选择 VPC 所属地域。
            
        -   **资源归属UID**：根据 VPC 的账号归属选择。本文选择**同账号**。
            
        -   **网络实例**：选择 VPC\_A。
            
        -   **交换机**：为实现多可用区容灾，至少选择两个可用区。必须包含 VPC NAT 网关所在的交换机。
            
        -   **高级配置**：全部勾选。
            
        
    3.  创建完成后，单击**继续创建连接**，为 VPC\_B 创建 VPC 连接。
        
2.  配置路由：
    
    NAT 网关本身不决定流量的走向，仅负责地址转换。流量是否会被发送到 NAT 网关，以及地址转换后流向何处，由 VPC 的路由表控制。
    
    1.  创建自定义路由表并绑定交换机：
        
        1.  前往[路由表列表页](https://vpc.console.aliyun.com/vpc/cn-hangzhou/route-tables)，在顶部菜单栏选择 VPC 所属地域。
            
        2.  单击**创建路由表**。
            
            -   **专有网络**：分别为VPC\_A、VPC\_B创建路由表。
                
            -   **绑定对象类型**：选择交换机。
                
            
        3.  在路由表列表页，单击目标自定义路由表**绑定资源**列的**立即绑定**，绑定 ECS 实例所在的交换机。
            
    2.  配置路由条目：单击目标路由表 ID，在**自定义路由条目**页签，单击**添加路由条目**，配置目标网段与下一跳。
        
        按照下表配置路由，确保流量正确转发。
        
        | **专有网络** | **路由表** | **目标网段** | **下一跳** |
        | --- | --- | --- | --- |
        | VPC\\_A | 系统路由表 | 10.0.0.0/24 | 转发路由器 |
        | 自定义路由表 | 10.0.0.0/24 | VPC\\_NATGW\\_A |
        | VPC\\_B | 系统路由表 | 172.16.0.0/24 | 转发路由器 |
        | 自定义路由表 | 172.16.0.0/24 | VPC\\_NATGW\\_B |
        

### **步骤四：**结果验证

登录 ECS\_A 实例，执行如下命令。

```
# 通过访问VPC_NATGW_B实例的 NAT IP（10.0.0.53），远程登录 ECS_B 实例
# 确保 ECS_B 实例所属安全组已放通22号端口
ssh root@10.0.0.53
# 查看实例网卡 IP
ifconfig
```

可确认 ECS\_A 实例通过 VPC\_NATGW\_A 的 NAT IP（172.16.0.89）访问 VPC\_NATGW\_B 的NAT IP（10.0.0.53），从而远程登录到 ECS\_B 实例。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5554921671/p1013732.png)

## 计费说明

-   [VPC NAT网关](https://help.aliyun.com/zh/nat-gateway/nat-gateway-billing)：收取实例费与容量单位 CU 费。
    
-   [云企业网 CEN](https://help.aliyun.com/zh/cen/product-overview/billing-rules)：地域内连接，收取连接费和流量处理费。跨地域连接还收取跨地域带宽费。