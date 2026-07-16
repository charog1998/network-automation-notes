公网 NAT 网关作为网络地址转换网关，通过转换和隐藏云服务的真实地址，避免对外暴露，提升公网访问的安全性。

创建公网 NAT 网关并绑定 EIP 后，可以：

-   配置 SNAT：多个 ECS 共享 EIP 访问公网，节省公网 IP 资源。
    
-   配置 DNAT：ECS 通过端口映射或 IP 映射，面向公网提供服务。
    

| **SNAT - 服务器访问公网** ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3545404871/CAEQWhiBgICMiqC3vxkiIGI4MzQyNmU5NWVlMzQ1M2FiMWYyYTcxYmI3ZTI0ZTQz3963382_20230830144006.372.svg) | **DNAT - 对外提供 Web 服务** ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3545404871/CAEQYhiBgIDD0NifyRkiIDAwZTMzYjgyZmM2MTQ3ZmU4MjE0ZDk3YjE5YjExYmQz3963382_20230830144006.372.svg) |
| --- | --- |

公网 NAT 网关支持两种容灾部署模式，创建时通过**容灾类型**选择。

> 单可用区容灾模式已在 NAT 网关支持的所有地域开放，如需使用请联系客户经理申请。

-   **跨可用区容灾**：NAT网关跨可用区冗余部署，单可用区故障时自动容灾切换。适用于您的ECS等实例分布在多个可用区、需要共享同一NAT网关访问公网的场景。
    
-   **单可用区容灾**：NAT网关部署在单一可用区内，只保障本可用区高可用。适用于您的业务集中在某一个可用区、使用独立NAT网关访问公网的场景。
    

## **SNAT - 服务器访问公网**

当多个 ECS 实例访问公网时，逐一配置 EIP 会增加成本。使用公网 NAT 网关的 SNAT 功能，可实现多个 ECS 实例共享 EIP 上网，节省成本的同时，通过隐藏实例的真实 IP 地址、限制入向连接提升安全性。

### **工作原理**

以 ECS 实例（私网IP：192.168.1.100）访问公网为例。

1.  路由转发：按照 VPC 路由表中指向 NAT 网关的路由规则，访问数据包被转发至公网 NAT 网关。
    
2.  SNAT（源地址转换）：NAT 网关接收到数据包后，根据 SNAT 规则配置将源 IP 地址192.168.1.100 转换为 NAT 网关绑定的EIP。同时记录原始五元组（协议、源IP、源端口、目的IP、目的端口）与转换后的五元组（协议、EIP、公网源端口、目的IP、目的端口）的对应关系。
    
3.  发往公网：经过地址转换后的数据包被发送至互联网。该请求的发起方为 EIP，而非ECS实例的私网IP。
    

当公网的目标服务器返回响应数据包时，将按照会话映射表还原为原始的私网IP，从而转发回 ECS 实例。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3545404871/CAEQYhiBgIDVt4rJyhkiIDY5OGZlNzgzN2NjYzRmMmQ5MTJjMmI1NzJhZDU2ODJj5700065_20250908150924.313.svg)

#### **SNAT 生效规则**

SNAT 功能配置后是否生效，取决于以下规则：

-   确保 VPC 内访问公网的流量被正确路由到 NAT 网关，即 VPC 路由表中访问公网目标网段的路由条目下一跳指向公网 NAT 网关。
    
    -   自动配置：如果 VPC 系统路由表中无`0.0.0.0/0` 路由，该 VPC 创建第一个公网 NAT 网关时，系统会自动添加此路由。
        
    -   手动配置：如果使用自定义路由表，或系统路由表中已存在 `0.0.0.0/0` 路由，需要手动添加或调整自定义路由条目。建议遵循最小权限原则，配置目标网段为访问的具体公网网段。
        
    -   [路由优先级](https://help.aliyun.com/zh/vpc/vpc-route-table/#b591890db5qjy)：当多条路由的目标网段重叠时，遵循最长前缀匹配原则转发流量。
        

-   出口 IP 优先级：实例持有的固定公网IP/EIP > DNAT IP映射（任意端口） > SNAT条目绑定的EIP。可参考[统一公网出口IP](https://help.aliyun.com/zh/nat-gateway/use-cases/unified-public-network-export-ips)调整网络架构。
    
-   SNAT 条目优先级：当多条 SNAT 条目源网段重叠时，遵循最长子网掩码匹配规则。例如，ECS粒度的SNAT条目源网段的子网掩码为`/32`，长度最长，优先级最高。
    

#### **路由配置与 SNAT 粒度配置的关系**

路由配置和 SNAT 粒度配置是两个独立的环节，分别控制不同层面：

-   [路由配置](#8fabf6c52ayg0)：决定哪些流量被引流到 NAT 网关。例如，在 VPC 系统路由表中配置 `0.0.0.0/0` 指向 NAT 网关，由于系统路由表默认关联 VPC 内所有交换机，该 VPC 下所有 ECS 实例访问公网的流量都会被路由到 NAT 网关。
    
-   [SNAT 粒度配置](#7266ad2206h1v)：决定进入 NAT 网关后，对哪些源 IP 地址做转换。例如，选择交换机粒度，则仅该交换机下的 ECS 实例的流量会做源地址转换。
    

建议路由配置的范围与 SNAT 粒度保持一致。例如，路由表在 VPC 系统路由表配置 `0.0.0.0/0` 指向 NAT 网关时，SNAT 选择 VPC 粒度可确保所有流量都能匹配 SNAT 规则；如果 SNAT 选择交换机粒度，仅该交换机下的流量会完成地址转换并访问公网，其他交换机的流量虽然也会被路由到 NAT 网关，但因无匹配的 SNAT 规则而无法访问公网。

### **1\. 创建公网 NAT 网关并绑定 EIP**

> 公网NAT网关需要绑定EIP才能正常工作。一个公网NAT网关最多可绑定20个EIP，可以前往[配额管理](https://vpc.console.aliyun.com/quota)页面自助提升配额。

> 从2022年09月19日起，新创建的公网NAT网关绑定一个EIP时将占用NAT网关所在交换机的一个私网IP（已有NAT网关实例不受影响），请确保NAT网关所在交换机内私网IP地址充足，否则无法成功绑定。

#### **控制台**

前往[NAT 网关 - 公网 NAT 网关购买页](https://vpc.console.aliyun.com/buy/nat?regionId=cn-hangzhou)。

-   **付费模式**：按量付费。
    
-   **地域**：选择创建公网 NAT 网关的地域。
    
-   **网络及可用区**：选择公网 NAT 网关所属的VPC和交换机。此处选择的交换机用于为 NAT 网关分配私网 IP，绑定 EIP 时将占用该交换机的一个私网 IP 地址。创建成功后无法修改。
    
-   **容灾类型**：选择 NAT 网关的容灾部署模式。
    
    -   **跨可用区容灾**（默认）：在主备两个可用区部署，当主可用区故障时自动切换至备可用区。
        
    -   **单可用区容灾**：仅在所选可用区内部署，通过设备级冗余保障高可用。实例费为跨可用区容灾的 50%，CU 费为 80%。
        
-   **弹性公网IP**：根据是否已创建 EIP 等情况选择。
    
    -   **选择已有**：选择未绑定实例的EIP。
        
    -   **新购弹性公网IP**：无可用 EIP 时选择。默认创建**BGP(多线)**类型的按使用流量计费的EIP，可根据自身业务需要选择**带宽峰值**。
        
        > 如需绑定BGP（多线）\_精品线路类型或其他计费类型的EIP，需先[申请EIP](https://help.aliyun.com/zh/eip/apply-for-new-eips)，创建时**选择已有**进行绑定。
        
    -   **稍后配置**：成功创建的NAT网关将不具备公网能力，用户需后续手动绑定EIP。
        
        创建完成后，单击目标公网NAT网关实例**弹性公网IP**列的**立即绑定**，可从已有弹性公网IP中选择或新购弹性公网IP并绑定。
        

#### **API**

-   调用[CreateNatGateway](https://help.aliyun.com/zh/nat-gateway/developer-reference/api-vpc-2016-04-28-createnatgateway-natgws#doc-api-Vpc-CreateNatGateway)创建公网NAT网关。
    
-   调用[ModifyNatGatewayAttribute](https://help.aliyun.com/zh/nat-gateway/developer-reference/api-vpc-2016-04-28-modifynatgatewayattribute-natgws#doc-api-Vpc-ModifyNatGatewayAttribute)修改公网NAT网关配置。
    
-   调用[AssociateEipAddress](https://help.aliyun.com/zh/eip/developer-reference/api-vpc-2016-04-28-associateeipaddress-eips)绑定EIP。
    

### **2\. 配置 SNAT 条目**

#### **控制台**

前往[公网 NAT 网关](https://vpc.console.aliyun.com/nat/cn-hangzhou/nats)页面。单击目标实例**操作**列的**设置SNAT**，单击**创建SNAT条目**。

-   **SNAT条目粒度**：SNAT 规则的生效范围，根据管理精细度需求选择。
    
    -   **VPC粒度**：所属VPC下的所有ECS均可以通过配置的SNAT规则访问公网。
        
    -   **交换机粒度**：所选交换机下的所有 ECS 实例可通过该 SNAT 条目经 NAT 网关访问公网。
        
        > 一个公网 NAT 网关支持为同一 VPC 内的多个交换机分别创建 SNAT 条目，各交换机下配置了 SNAT 规则的 ECS 实例均可通过该 NAT 网关访问公网。此处选择的交换机决定 SNAT 规则的生效范围，与创建 NAT 网关时选择的交换机无关。
        
    -   **ECS/弹性网卡粒度**：仅指定的ECS或弹性网卡可访问公网。
        
    -   **自定义网段粒度**：为指定的CIDR网段内的资源提供公网访问能力。
        
-   **选择弹性公网IP地址**：在下拉列表中选择提供公网访问的EIP。
    
    -   没有可选的EIP时，可在下拉列表单击**新购弹性公网IP并绑定**，在弹出的对话框中完成EIP的购买。
        
    -   可以选择多个EIP，业务连接会通过哈希算法分配到多个EIP，由于每个连接的流量不同，可能会出现多EIP业务流量不均匀的情况，建议将每个EIP加入到同一个共享带宽中以避免单EIP带宽达到上限导致业务受损。
        
-   **EIP亲和性**：选择多个EIP，未开启EIP亲和性时，同一个私网IP访问单一目的IP，可能使用不同的EIP。开启后，会使用相同的EIP。但访问单一目标的并发连接数过多时，会造成端口分配失败，需持续监控 [端口分配失败丢失数](https://help.aliyun.com/zh/nat-gateway/user-guide/view-monitoring-data#17ad1a6e34mm1)。
    

> 创建完成后，可单击目标条目**操作**列的**编辑**，修改EIP与EIP亲和性。

#### **API**

-   调用[CreateSnatEntry](https://help.aliyun.com/zh/nat-gateway/developer-reference/api-vpc-2016-04-28-createsnatentry-natgws)创建SNAT条目。
    
-   调用[ModifySnatEntry](https://help.aliyun.com/zh/nat-gateway/developer-reference/api-vpc-2016-04-28-modifysnatentry-natgws)修改指定的SNAT条目。
    

### **删除 SNAT 条目**

当不再需要某条 SNAT 规则，或需要删除公网 NAT 网关前清理关联资源时，可删除 SNAT 条目。

#### **控制台**

前往[公网 NAT 网关](https://vpc.console.aliyun.com/nat/cn-hangzhou/nats)页面。单击目标实例 ID 进入详情页，在**SNAT管理**页签，找到目标 SNAT 条目，单击**操作**列的**删除**。

#### **API**

-   调用[DeleteSnatEntry](https://help.aliyun.com/zh/nat-gateway/developer-reference/api-vpc-2016-04-28-deletesnatentry-natgws)删除指定的 SNAT 条目。
    

### **3\. 配置路由**

配置路由，确保 ECS 实例发往互联网的流量正确路由到 NAT 网关。

#### **控制台**

前往[专有网络控制台 - 路由表](https://vpc.console.aliyun.com/vpc/cn-hangzhou/route-tables)页面。在顶部菜单栏，选择公网NAT网关的地域。找到 ECS 实例所在交换机关联的路由表，单击 ID 进入详情页。

-   自动配置：如果创建该 VPC 内的第一个公网 NAT 网关，且 ECS 实例所在的交换机关联了系统路由表，系统会自动添加一条目标网段为 `0.0.0.0/0`、下一跳为该NAT网关的路由。此情况下，无需任何操作。
    
-   手动配置：如果 VPC 内已存在 `0.0.0.0/0` 路由或交换机绑定了自定义路由表，需在对应路由表中添加目标网段为需访问的具体公网网段、路由下一跳为 NAT 网关的自定义路由。
    

#### **API**

-   调用[CreateRouteEntry](https://help.aliyun.com/zh/vpc/developer-reference/api-vpc-2016-04-28-createrouteentry)添加单个路由条目
    
-   调用[ModifyRouteEntry](https://help.aliyun.com/zh/vpc/developer-reference/api-vpc-2016-04-28-modifyrouteentry)调整路由条目下一跳。
    

#### **验证网络连通性**

登录 ECS 实例，执行以下命令。

```
# 确保 ECS 实例所属的安全组已放行访问公网的对应流量
# 测试能否访问公网
ping www.aliyun.com

# 查看当前出口公网IP，应显示为NAT网关绑定的EIP
curl ifconfig.me
```

## **DNAT - 对外提供 Web 服务**

当 ECS 实例对外提供 Web 服务时，直接为其分配 EIP 会暴露实例的所有端口，增加安全风险。使用公网 NAT 网关的 DNAT 功能，可通过将 NAT 网关 EIP 的特定端口或所有流量转发至 ECS 实例，避免地址暴露。需确保 ECS 实例未绑定 EIP，才能配置 DNAT 条目。

### **工作原理**

以 ECS 实例（私网IP：192.168.1.100）面向公网提供服务为例。

1.  公网用户访问服务：数据包的目标 IP 为公网 NAT 网关绑定的用于提供服务的 EIP。
    
2.  DNAT（目标地址转换）：NAT 网关接收数据包后，根据 DNAT 规则，将 EIP 转换为ECS实例的私网 IP。同时记录地址转换的映射关系。
    
3.  访问服务：经过地址转换后的数据包转发至目标 ECS实例。
    

当目标 ECS 实例返回响应数据包时，将按照路由转发至公网 NAT 网关，并根据会话映射表转换为EIP，发送至公网用户。

> 仅配置 DNAT 条目时，ECS 接收数据包的源 IP 为公网 IP。因此，为 ECS 配置安全组入方向规则时，需使用真实的访问源 IP（即公网 IP）。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3545404871/CAEQYhiBgIC3.IzJyhkiIDFhMTJhMWMzYzkxNDQ0MjFiM2UyM2NlZDVjZWQ4ZDky5700065_20250908150924.313.svg)

### **配置 DNAT 条目**

> 此处仅说明如何配置 DNAT 条目。创建 NAT 网关、绑定 EIP 与路由配置可参考[服务器访问公网](#8ca4b0b781hl3)。

#### **控制台**

1.  前往[公网 NAT 网关](https://vpc.console.aliyun.com/nat/cn-hangzhou/nats)页面。在顶部菜单栏，选择公网NAT网关的地域。
    
2.  单击目标公网NAT网关实例**操作**列的**设置DNAT**，单击**创建DNAT条目**。
    
    -   **选择弹性公网IP地址**：选择公网用户访问的EIP。支持同一个EIP同时用于DNAT条目和SNAT条目。
        
    -   **选择私网IP地址**：选择对外提供服务的真实私网IP。支持通过ECS或弹性网卡进行选择或通过手动输入。
        
    -   **端口设置**：配置DNAT映射。
        
        -   **任意端口**：属于IP映射，任何访问该EIP的请求都将转发到目标ECS实例上，将占用全部端口。
            
            -   目标ECS实例也可以使用该EIP主动访问公网。该EIP不能再被其他DNAT条目或SNAT条目使用。
                
            -   如果公网NAT网关既配置了DNAT IP映射，又配置了SNAT条目，则ECS实例访问公网时，优先使用DNAT IP映射方式的EIP。
                
        -   **具体端口**：属于端口映射，以指定协议和端口访问该EIP的请求将转发到目标ECS实例的指定端口上。 配置**公网端口**（进行端口转发的外部端口或端口段）、**私网端口**（进行端口转发的内部端口或端口段）、**协议类型**（转发端口的协议类型）。
            
            -   输入的端口范围需要在1~65535之间，如果需要在端口段内转发，请在输入时以正斜线（/）隔开起始端口，例如10/20。公私网端口段中的端口数量一致，公私网需同为端口或者端口段，且需确保端口数量一致。例如**公网端口**设置为10/20，**私网端口**设置为80/90。
                
            -   当选择的EIP已创建SNAT条目，且需要设置大于`1024`的公网端口时，因SNAT默认分配端口范围在1025～65535之间，需单击**开启端口突破**。
                
                **重要**
                
                开启端口突破会导致部分存量SNAT的连接闪断，重连即可恢复，请谨慎操作。
                
    
    > 创建完成后，可单击目标条目**操作**列的**编辑**，修改EIP、私网IP和端口。
    

#### **API**

-   调用[CreateForwardEntry](https://help.aliyun.com/zh/nat-gateway/developer-reference/api-vpc-2016-04-28-createforwardentry-natgws)创建DNAT条目。
    
-   调用[ModifyForwardEntry](https://help.aliyun.com/zh/nat-gateway/developer-reference/api-vpc-2016-04-28-modifyforwardentry-natgws)修改指定的DNAT条目。
    

### **删除 DNAT 条目**

当不再需要某条 DNAT 规则，或需要删除公网 NAT 网关前清理关联资源时，可删除 DNAT 条目。

#### **控制台**

前往[公网 NAT 网关](https://vpc.console.aliyun.com/nat/cn-hangzhou/nats)页面。单击目标实例 ID 进入详情页，在**DNAT管理**页签，找到目标 DNAT 条目，单击**操作**列的**删除**。

#### **API**

-   调用[DeleteForwardEntry](https://help.aliyun.com/zh/nat-gateway/developer-reference/api-vpc-2016-04-28-deleteforwardentry-natgws)删除指定的 DNAT 条目。
    

## **资源清理**

公网 NAT 网关从创建完成到释放结束均收取实例费，处理流量时还将收取容量单位 CU 费。为避免非必要开销，当不再需要时，可按照以下步骤清理资源：

### **控制台**

1.  删除配置条目：在实例详情页的**SNAT管理**和**DNAT管理**页签，删除配置的条目。
    
2.  解绑并释放 EIP：在实例详情页的**绑定的弹性公网IP**页签，解除绑定。仅解绑 EIP，仍需支付 EIP 配置费，需前往[EIP](https://vpc.console.aliyun.com/eip/cn-hangzhou/eips)释放 EIP。
    
    未删除配置条目时，可**解除绑定**。
    
3.  删除公网 NAT 网关：单击目标公网NAT网关实例**操作**的**删除**。
    
    未解绑EIP、删除配置条目时，可选择**强制删除（删除 NAT 网关及其包含资源）**，由系统删除实例及相关资源。
    
    为实例开启删除保护，可避免误删。删除实例前，需关闭删除保护。
    

### **API**

1.  分别调用[DeleteSnatEntry](https://help.aliyun.com/zh/nat-gateway/developer-reference/api-vpc-2016-04-28-deletesnatentry-natgws)和[DeleteForwardEntry](https://help.aliyun.com/zh/nat-gateway/developer-reference/api-vpc-2016-04-28-deleteforwardentry-natgws)删除SNAT条目和DNAT条目。
    
2.  调用[UnassociateEipAddress](https://help.aliyun.com/zh/eip/developer-reference/api-vpc-2016-04-28-unassociateeipaddress-eips)解绑EIP。
    
3.  调用[DeleteNatGateway](https://help.aliyun.com/zh/nat-gateway/developer-reference/api-vpc-2016-04-28-deletenatgateway-natgws#doc-api-Vpc-DeleteNatGateway)删除公网NAT网关。
    

## **应用于生产环境**

### **最佳实践**

-   **网络规划**：为公网 NAT 网关创建独立的交换机，并预留足够的私网IP，避免因 IP 耗尽影响后续为 NAT 网关绑定多 EIP。
    
-   **精细化控制**：使用交换机粒度或 ECS 粒度的 SNAT 条目，遵循最小权限原则，仅为需要访问公网的资源开启权限。
    

### **容灾策略**

公网 NAT 网关支持以下两种容灾模式，创建时通过**容灾类型**选择。

|     | **跨可用区容灾（默认）** | **单可用区容灾** |
| --- | --- | --- |
| **部署方式** | 主备两个可用区各部署一套实例，备可用区由阿里云选择 | 仅在用户指定的可用区内部署，可用区内设备级冗余 |
| **故障切换** | 可用区故障时自动切换 | 可用区整体故障时不自动切换 |
| **适用场景** | 需要跨可用区自动容灾的业务 | 无跨可用区需求、希望降低成本或将故障半径收敛至单一可用区的业务 |
| **费用** | 基准价 | 实例费约为跨可用区的 50%，CU 费约为 80% |

**多 EIP 冗余**：为 SNAT 条目绑定多个 EIP。当某个 EIP 因攻击等原因不可用时，业务流量可以自动通过其他 EIP 流出。

### **风险防范**

-   **安全组配置**：公网 NAT 网关实现地址转换，后端 ECS 实例的安全防护仍依赖安全组和网络 ACL。请务必为 ECS 实例配置严格的入方向安全组规则，仅放行必要的端口。
    
-   **监控与告警**：为 NAT 网关的关键指标（如并发连接数、出入方向带宽等）配置告警规则，以便在资源接近瓶颈时及时收到通知并扩容。
    
-   **连接数限制**：业务需要大量连接到同一公网服务（如支付网关）时，需关注最大并发连接数（`N × 55,000, N 是 SNAT 条目配置的 EIP 数量`）。建议提前规划足够的 EIP 数量，并监控**端口分配失败丢失数**。
    
-   **ICMP 代回**：默认开启，通过Ping命令进行探测时，通过 NAT 网关将会收到正常的回复报文，这无法保证后端服务器正常。对于依赖 Ping 进行精细化监控的场景，需在详情页关闭**ICMP代回**。
    
    -   仅 DNAT 配置**任意端口**映射场景下，将ICMP报文转发至后端服务器。
        
    -   **具体端口**映射场景下，Ping将无法探测。可使用 `telnet <EIP> <公网端口>`直接探测映射的业务端口。
        

## **常见问题**

### **配置 SNAT 后无法访问公网**

可参考以下步骤排查：

1.  [路由配置](#1d450970e7amg)：在公网 NAT 网关实例详情页查看**指向NAT的专有网络路由信息**，确认是否有指向该公网NAT网关的路由条目。
    
2.  SNAT 条目配置：在公网 NAT 网关实例详情页的**SNAT管理**页签，确认SNAT条目的状态为**可用**。并确认访问公网的源地址在**源网段**内。
    
3.  访问控制：检查访问的公网对端是否配置了访问控制策略或将实例绑定的EIP加入了白名单。
    
4.  检查是否配置IPv4网关：[与 IPv4 网关结合使用](https://help.aliyun.com/zh/nat-gateway/support/nat-gateway-faq/#cbcda01f4bqc3)时，确保NAT网关为NAT模式，并正确配置路由。
    

### **访问公网连接超时或速度慢**

通常由以下原因导致：

-   带宽不足：[查看 NAT 网关绑定的 EIP 监控](https://help.aliyun.com/zh/nat-gateway/user-guide/view-monitoring-data#67c3239cdfk3m)，检查带宽使用率，接近100%时需提升带宽或增加 EIP 并加入共享带宽。
    
-   连接数超限：访问单一目标的并发连接数过多时，会造成端口分配失败，连接被丢弃。[查看 NAT 网关监控 - 端口分配失败丢失数](https://help.aliyun.com/zh/nat-gateway/user-guide/view-monitoring-data#17ad1a6e34mm1)，当持续增长时，增加 SNAT 规则中配置的 EIP 数量。
    

### **公网 NAT 网关处理私网流量**

NAT 网关本身不决定流量的走向，仅负责地址转换。流量是否会被发送到 NAT 网关，以及地址转换后流向何处，由 VPC 的路由表控制。

## **更多信息**

### **计费说明**

公网 NAT 网关收取[实例费和容量单位CU费](https://help.aliyun.com/zh/nat-gateway/nat-gateway-billing#902cb3fe942hs)。绑定的 EIP 有独立的[计费规则](https://help.aliyun.com/zh/eip/billing-overview)，费用由EIP收取。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3545404871/CAEQYRiBgIDvi7bCxxkiIGUwOGRkZmY3Y2M1NDRiMjU5MmUzMDI3NjE0ODEwYTVj4729461_20241029092552.793.svg)

### **配额**

| **配额名称** | **描述** | **默认限制** | **提升配额** |
| --- | --- | --- | --- |
| natgw\\_quota\\_nat\\_num\\_per\\_vpc | 单VPC内可以创建NAT网关的数量 | 5个  | 前往[配额管理页面](https://vpc.console.aliyun.com/quota)或[配额中心](https://quotas.console.aliyun.com/products/vpc/quotas?query=peer)申请提升配额。 |
| natgw\\_quota\\_eip\\_num\\_per\\_nat | 每个NAT网关可绑定的EIP数量 | 20个 |
| natgw\\_quota\\_snat\\_entry\\_num | 每个NAT网关中可保有的SNAT条目数量 | 40个 |
| natgw\\_quota\\_dnat\\_entry\\_num | 每个NAT网关中可保有的DNAT条目数量 | 100个 |