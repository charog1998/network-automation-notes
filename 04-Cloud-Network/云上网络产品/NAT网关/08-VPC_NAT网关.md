VPC NAT 网关可以将 VPC 内的私网 IPv4 地址转换为 NAT IP，解决地址冲突网络的互访或满足使用指定地址访问的诉求。

-   [私网地址冲突解决](https://help.aliyun.com/zh/nat-gateway/use-cases/access-when-vpc-addresses-conflict-through-vpc-nat-gateway)：网段重叠的 VPC 无法互连，可添加附加网段并创建 VPC NAT 网关，通过地址转换解决地址冲突。
    
-   [使用指定地址互访](https://help.aliyun.com/zh/nat-gateway/use-cases/use-a-vpc-nat-gateway-and-an-express-connect-circuit-to-connect-a-data-center-to-a-vpc)：金融证券等受监管行业，云上业务使用 VPC NAT 网关，可确保通过固定的、指定的私网IP地址访问本地IDC。
    

VPC NAT 网关支持两种容灾类型：

> 单可用区容灾模式已在 NAT 网关支持的所有地域开放，如需使用请联系客户经理申请。

-   **跨可用区容灾**（默认）：NAT网关跨可用区冗余部署，单可用区故障时自动容灾切换。
    
-   **单可用区容灾**：NAT网关部署在单一可用区内，只保障本可用区高可用；实例费约为跨可用区的 50%，CU 费约为 80%。
    

## 工作原理

以云上云下使用固定的、指定的私网 IP 地址互访为例。

-   云上业务访问本地 IDC：VPC 内的多个 ECS 实例访问本地 IDC，均使用指定的 NAT IP 访问。
    
    1.  **路由转发**：按照 VPC 路由表中指向 NAT 网关的路由规则，ECS 实例发出的访问数据包被转发至VPC NAT 网关。
        
    2.  **SNAT（源地址转换）**：VPC NAT网关接收到数据包后，根据 SNAT 条目配置，将数据包的源 IP 地址从 ECS 实例 IP（例如：192.168.1.10）转换为指定的 NAT IP（192.168.10.2）。同时，在内部会话表中记录下转换的映射关系。
        
    3.  **发往对端私网**：经过地址转换后的数据包被发送至本地IDC。对于本地 IDC，该请求的发起方是 NAT IP，而非 ECS 实例。
        
    4.  **响应与反向转换**：本地 IDC 返回的响应包，目标地址为 NAT IP。VPC NAT网关将按照会话映射表还原为原始的私网IP，从而转发回 ECS 实例。
        
-   本地 IDC 访问云上业务：本地 IDC 主动向固定的 NAT IP (192.168.10.2) 发起请求。VPC NAT 网关会根据 DNAT 规则，将该请求的目标 IP 从 NAT IP 转换为 VPC 内实际提供服务的 ECS 实例私网 IP (例如：192.168.1.10)，从而将外部访问流量准确地引入到目标服务器。
    

需注意：VPC NAT 网关本身不决定流量的走向，仅负责地址转换。流量是否会被发送到 NAT 网关，以及地址转换后流向何处，由 VPC 的路由表控制。

> 与其他 VPC、本地 IDC 的连通，需通过云企业网（CEN）、物理专线等产品实现。

-   配置 VPC 出向路由（ VPC 到外部网络）：确保 VPC 路由表中已添加目的地址为对端网络（如本地 IDC）、下一跳为 VPC NAT 网关的路由条目，确保 VPC 内实例发起的访问请求，可转发至 NAT 网关进行 SNAT 转换。
    
-   声明 NAT IP：当使用自定义 NAT IP地址段时，确保 VPC 路由表中已添加目的地址为该 NAT IP 地址段、下一跳为 VPC NAT 网关的路由条目，声明该地址段的归属，确保 DNAT 入向流量与 SNAT 回程流量在 VPC 内可正确转发。
    
-   配置外部网络路由（外部网络到 VPC）：确保对端网络已配置路由，目的地址为 NAT IP 地址段，确保来自外部网络的响应包或主动访问请求，可转发至 NAT 网关。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1762589771/CAEQYxiBgIDj3K230RkiIDEwYTAxMmVkMGI2NjQ2MDc5MTE5NmMyYjQwZTJkMzk35286340_20250618134928.042.svg)

## 创建 VPC NAT 网关

### **控制台**

前往[NAT 网关 - VPC NAT网关购买页](https://vpc.console.aliyun.com/buy/nat?regionId=cn-hangzhou&networkType=intranet)。

-   **付费类型**：按量付费。
    
-   **地域**：选择创建 VPC NAT网关的地域。
    
-   **容灾类型**：选择 NAT 网关的容灾部署模式。
    
    -   **跨可用区容灾**（默认）：在主备两个可用区部署，当主可用区故障时自动切换至备可用区。
        
    -   **单可用区容灾**：仅在所选可用区内部署，通过设备级冗余保障高可用。实例费为跨可用区容灾的 50%，CU 费为 80%。
        
-   **网络及可用区**：选择VPC NAT 网关所属的VPC和交换机。为便于路由管理，建议为 VPC NAT 网关规划并使用独立的交换机。
    
-   **私网IP**：作为默认 NAT IP，可从交换机网段（默认NAT IP地址段）中指定 NAT IP。如未配置，则系统指定。
    
-   **私网IP Prefix**：可批量创建 NAT IP。需先为 VPC NAT 网关所属的交换机创建预留网段，VPC NAT 会将预留网段拆分为`/28`掩码的 IP Prefix。指定 IP Prefix 后，系统将为 NAT 网关添加该网段下全部 16 个地址作为 NAT IP。
    

### **API**

调用[CreateNatGateway](https://help.aliyun.com/zh/nat-gateway/api-createnatgateway#doc-api-Vpc-CreateNatGateway)创建VPC NAT网关。通过 `AvailabilityMode` 参数指定容灾类型：`CrossAZ`（默认，跨可用区容灾）或 `SingleAZ`（单可用区容灾）。

## 配置 NAT IP 和地址段

NAT IP 用于配置 SNAT 条目与 DNAT 条目，在地址转换时替代 ECS 实例的真实 IP，作为统一的源地址或目的地址。NAT IP 需从 NAT IP 地址段中分配。

-   默认 NAT IP 地址段：系统使用 VPC NAT 网关所属交换机网段作为默认 NAT IP 地址段。
    
    -   创建时配置的私网 IP 作为默认 NAT IP，可自行指定。如不配置，则系统指定。后续可添加 NAT IP。
        
    -   支持从交换机预留网段中配置私网 IP Prefix，用于批量创建 NAT IP。
        
-   新建 NAT IP 地址段：分配非所属交换机网段下的 NAT IP。
    
    -   建议使用RFC私网地址10.0.0.0/16、172.16.0.0/16、192.168.0.0/16这三个私网网段及其子网作为地址段，支持的子网掩码位数范围为16至32位。
        
    -   如需使用公网网段，需使用[用户网段](https://help.aliyun.com/zh/vpc/frequently-asked-questions#ae48aa3b34yle)保证该网段在专有网络地址段范围内，再将其作为NAT IP地址段。
        
    -   不能与VPC NAT网关所属VPC的私网网段重叠。如果需要将私网地址转换为VPC私网网段内的其他地址，请在对应的VPC私网网段内创建交换机，并在该交换机中创建新的VPC NAT网关提供私网地址转换服务。
        

### **控制台**

#### **配置 NAT IP 地址段**

-   默认 NAT IP 地址段：系统默认使用 VPC NAT 网关所属交换机网段，无法删除。
    
-   新建 NAT IP 地址段：前往[VPC NAT网关](https://vpc.console.aliyun.com/vpc-nat/cn-hangzhou/nats)页面，单击目标VPC NAT网关实例ID进入详情页，选择**NAT IP**页签，单击**新建地址段**。
    

#### **配置 NAT IP**

-   从默认 NAT IP 地址段中添加：
    
    -   创建 VPC NAT 网关时，配置的私网 IP 作为默认 NAT IP，可自行指定。如不配置，则系统自动指定。默认 NAT IP 无法删除。
        
    -   逐个添加 NAT IP：前往[VPC NAT网关](https://vpc.console.aliyun.com/vpc-nat/cn-hangzhou/nats)页面，单击目标VPC NAT网关实例ID进入详情页，选择**NAT IP**页签，单击**添加NAT IP**。
        
        -   **选择地址段**：选择VPC NAT网关下默认 NAT IP 地址段。
            
        -   **分配方式**：**随机分配IP**或从所选地址段中指定**IP地址**来**手动分配IP**。
            
    -   使用 IP Prefix 批量添加 NAT IP：前往[VPC NAT网关](https://vpc.console.aliyun.com/vpc-nat/cn-hangzhou/nats)页面，单击目标VPC NAT网关实例ID进入详情页，在**NAT IP**页签下选择**NAT IP Prefix**，单击**添加IP Prefix**。
        
        -   批量添加：选择**随机分配**，指定分配的 IP Prefix 个数，将从 VPC NAT 网关所在交换机的预留网段中随机添加指定数量、未分配的`/28`掩码的 IP Prefix。
            
        -   逐个添加：选择**手动分配**，指定 VPC NAT 网关所在交换机的预留网段中未分配的`/28`掩码的 IP Prefix。
            
-   从新建 NAT IP 地址段中添加：单击目标VPC NAT网关实例ID进入详情页，选择**NAT IP**页签，单击**添加NAT IP**。
    
    -   **选择地址段**：选择VPC NAT网关下新建的NAT IP地址段。
        
    -   **分配方式**：**随机分配IP**或从所选地址段中指定**IP地址**来**手动分配IP**。
        

### **API**

-   调用[CreateNatIpCidr](https://help.aliyun.com/zh/nat-gateway/api-createnatipcidr#doc-api-Vpc-CreateNatIpCidr)新建NAT IP地址段。
    
-   调用[CreateNatIp](https://help.aliyun.com/zh/nat-gateway/api-createnatip#doc-api-Vpc-CreateNatIp)添加NAT IP地址。
    
-   调用[DeleteNatIp](https://help.aliyun.com/zh/nat-gateway/developer-reference/api-vpc-2016-04-28-deletenatip-natgws)删除NAT IP地址。
    
-   调用[DeleteNatIpCidr](https://help.aliyun.com/zh/nat-gateway/developer-reference/api-vpc-2016-04-28-deletenatipcidr-natgws)删除NAT IP地址段。
    

## **配置 SNAT 条目**

### **控制台**

前往[VPC NAT网关](https://vpc.console.aliyun.com/vpc-nat/cn-hangzhou/nats)页面，单击目标VPC NAT网关实例**操作**列的**SNAT管理**，单击**创建SNAT条目**。

-   **SNAT条目粒度**：SNAT 规则的生效范围，根据管理精细度需求选择。
    
    -   **专有网络粒度**：所属VPC下的所有ECS均可以通过配置的SNAT规则访问外部网络。
        
    -   **交换机粒度**：仅指定的交换机下的ECS可访问外部网络。
        
    -   **ECS粒度**：仅指定的ECS或弹性网卡可访问外部网络。
        
    -   **自定义网段粒度**：指定的CIDR网段内的资源可访问外部网络。
        
-   ****选择NAT IP地址****：在下拉列表中选择一个或多个用来访问外部私网的NAT IP地址。可以在下拉列表选择**新建NAT IP**，创建后选择。
    
-   **NAT IP亲和性**：选择多个NAT IP，未开启亲和性时，同一个私网IP访问单一目的IP，可能使用不同的NAT IP。开启后，会使用相同的NAT IP。但访问单一目标的并发连接数过多时，会造成端口分配失败，需持续监控[端口分配失败丢失数](https://help.aliyun.com/zh/nat-gateway/user-guide/monitor-and-maintain-vpc-nat-gateways#00f2861e03eoo)。
    

> 创建完成后，可单击目标条目**操作**列的**编辑**，修改NAT IP地址与NAT IP亲和性。

### **API**

-   调用[CreateSnatEntry](https://help.aliyun.com/zh/nat-gateway/developer-reference/api-vpc-2016-04-28-createsnatentry-natgws)创建SNAT条目。
    
-   调用[ModifySnatEntry](https://help.aliyun.com/zh/nat-gateway/developer-reference/api-vpc-2016-04-28-modifysnatentry-natgws)修改指定的SNAT条目。
    
-   调用[DeleteSnatEntry](https://help.aliyun.com/zh/nat-gateway/developer-reference/api-vpc-2016-04-28-deletesnatentry-natgws)删除SNAT条目。
    

## **配置 DNAT 条目**

**重要**

创建DNAT条目后，您还需要确保目标ECS实例的安全组入方向规则已放行DNAT映射的端口。例如，如果DNAT将公网端口30081映射到ECS的30081端口，则需要在安全组中添加一条入方向规则：协议类型选择**自定义TCP**，端口范围填写对应的映射端口（如30081/30081），授权对象填写`0.0.0.0/0`或指定的源IP段。如果安全组未放行对应端口，即使DNAT配置正确，从公网访问该端口仍会超时。

### **控制台**

前往[VPC NAT网关](https://vpc.console.aliyun.com/vpc-nat/cn-hangzhou/nats)页面，单击目标VPC NAT网关实例**操作**列的**DNAT管理**，单击**创建DNAT条目**。

-   **选择NAT IP地址**：选择供外部私网访问的NAT IP 。支持将一个NAT IP 同时用于 DNAT 条目（端口映射方式）和 SNAT 条目。
    
-   **选择私网IP地址**：选择使用 DNAT 规则进行通信的真实私网IP。支持通过 ECS 或弹性网卡进行选择或通过手动输入。
    
-   **端口设置**：配置 DNAT 映射。
    
    -   ****任意端口****：属于 IP 映射，任何访问该 NAT IP 的请求都将转发到目标 ECS 实例。
        
        -   目标 ECS 实例也可以使用该 NAT IP 主动访问外部网络。该 NAT IP 不能再被其他 DNAT 条目或 SNAT 条目使用。
            
        -   如果 NAT 网关既配置了 DNAT IP 映射，又配置了 SNAT 条目，则 ECS 实例会优先通过 DNAT IP 映射方式的 NAT IP 地址访问外部网络。
            
    -   **具体端口**：属于端口映射，以指定协议和端口将访问该 NAT IP 的请求转发到目标 ECS 实例的指定端口上。 配置****前端端口****（NAT IP 被外部网络访问的端口）、**后端端口**（映射的目标 ECS 实例端口）、**协议类型**（转发端口的协议类型）。
        
        -   端口范围需要在1~65535之间，不支持在端口段内转发。
            
        -   当选择的 NAT IP 已创建SNAT条目，且需要设置大于`1024`的端口时，因 SNAT 默认分配端口范围在1025～65535之间，需**开启端口突破**。
            
            **重要**
            
            但开启端口突破会导致部分存量SNAT的连接闪断，重连即可恢复，请谨慎操作。
            

> 创建完成后，可单击目标条目**操作**列的**编辑**，修改NAT IP地址、私网IP地址和端口。

### **API**

-   调用[CreateForwardEntry](https://help.aliyun.com/zh/nat-gateway/developer-reference/api-vpc-2016-04-28-createforwardentry-natgws)创建DNAT条目。
    
-   调用[DeleteForwardEntry](https://help.aliyun.com/zh/nat-gateway/developer-reference/api-vpc-2016-04-28-deleteforwardentry-natgws)删除DNAT条目。
    

## 资源清理

VPC NAT 网关从创建完成到释放结束均收取实例费，处理流量时还将收取容量单位 CU 费。为避免非必要开销，当不再需要时，可按照以下步骤清理资源：

### **控制台**

1.  删除配置条目：在实例详情页的**SNAT管理**和**DNAT管理**页签，删除配置的条目。
    
2.  删除 NAT IP 地址：
    
    -   手动添加的 NAT IP：在实例详情页的**NAT IP**页签，单击目标NAT IP地址**操作**列的**删除**，或选择多个NAT IP地址，在页面下方单击**删除**。
        
    -   使用 IP Prefix 添加的 NAT IP：在实例详情页的**NAT IP**页签，选择**NAT IP Prefix**，单击目标NAT IP Prefix**操作**列的**删除**，解除所有关联关系后，将删除 IP Prefix 以及批量创建的全部 NAT IP。
        
    
3.  删除新建 NAT IP 地址段：在实例详情页的**NAT IP**页签，单击目标 NAT IP 地址段右侧![删除](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2419105261/p290291.png)图标。
    
4.  删除VPC NAT 网关：单击目标实例**操作**的**删除**。
    
    未删除 NAT IP、配置条目时，可选择**强制删除（删除 NAT 网关及其包含资源）**，由系统删除实例及相关资源。
    
    在实例详情页开启**删除保护**，可避免误删。删除实例前，需关闭删除保护。
    

### **API**

1.  分别调用[DeleteSnatEntry](https://help.aliyun.com/zh/nat-gateway/developer-reference/api-vpc-2016-04-28-deletesnatentry-natgws)和[DeleteForwardEntry](https://help.aliyun.com/zh/nat-gateway/developer-reference/api-vpc-2016-04-28-deleteforwardentry-natgws)删除SNAT条目和DNAT条目。
    
2.  调用[DeleteNatIp](https://help.aliyun.com/zh/nat-gateway/developer-reference/api-vpc-2016-04-28-deletenatip-natgws)删除NAT IP地址。
    
3.  调用[DeleteNatIpCidr](https://help.aliyun.com/zh/nat-gateway/developer-reference/api-vpc-2016-04-28-deletenatipcidr-natgws)删除NAT IP地址段。
    
4.  调用[DeleteNatGateway](https://help.aliyun.com/zh/nat-gateway/developer-reference/api-vpc-2016-04-28-deletenatgateway-natgws#doc-api-Vpc-DeleteNatGateway)删除VPC NAT网关。
    

## **应用于生产环境**

### **最佳实践**

-   **网络规划**：为便于路由管理，为 VPC NAT 网关规划并使用独立的交换机。
    
-   **精细化控制**：使用交换机粒度或 ECS 粒度的 SNAT 条目，遵循最小权限原则，仅为需要访问外部网络的资源开启权限。
    
-   **高可用容灾**：VPC NAT 网关支持跨可用区容灾（默认）和单可用区容灾两种模式。跨可用区容灾模式下，NAT网关跨可用区冗余部署，单可用区故障时自动容灾切换。单可用区容灾模式下，NAT网关部署在单一可用区内，费用更低，适用于客户业务本身已做到可用区分离部署的场景。
    

### **风险防范**

-   **安全组配置**：VPC NAT 网关实现地址转换，后端 ECS 实例的安全防护仍依赖安全组和网络 ACL。请务必为 ECS 实例配置严格的入方向安全组规则，仅放行必要的端口。
    
-   **监控与告警**：为 VPC NAT 网关的关键指标（如并发连接数、出入方向带宽等）配置告警规则，以便在资源接近瓶颈时及时收到通知并扩容。
    
-   **连接数限制**：业务需要大量连接到同一服务时，需关注最大并发连接数（`N × 55,000, N 是 SNAT 条目配置的 NAT IP 数量`）。建议提前规划足够的 NAT IP 数量，并监控**端口分配失败丢失数**。
    

## **更多信息**

### **计费说明**

VPC NAT 网关收取[实例费和容量单位CU费](https://help.aliyun.com/zh/nat-gateway/nat-gateway-billing#902cb3fe942hs)。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1762589771/CAEQYRiBgIDvi7bCxxkiIGUwOGRkZmY3Y2M1NDRiMjU5MmUzMDI3NjE0ODEwYTVj4729461_20241029092552.793.svg)

### **配额**

| **配额名称** | **描述** | **默认限制** | **提升配额** |
| --- | --- | --- | --- |
| natgw\\_quota\\_nat\\_num\\_per\\_vpc | 单VPC内可以创建NAT网关的数量 | 5个  | 前往[配额管理页面](https://vpc.console.aliyun.com/quota)或[配额中心](https://quotas.console.aliyun.com/products/vpc/quotas?query=peer)申请提升配额。 |
| natgw\\_quota\\_nat\\_ip\\_num\\_per\\_vpc\\_nat | 每个VPC NAT网关可创建的NAT IP数量 | 15个 |
| natgw\\_quota\\_snat\\_entry\\_num | 每个NAT网关中可保有的SNAT条目数量 | 40个 |
| natgw\\_quota\\_dnat\\_entry\\_num | 每个NAT网关中可保有的DNAT条目数量 | 100个 |