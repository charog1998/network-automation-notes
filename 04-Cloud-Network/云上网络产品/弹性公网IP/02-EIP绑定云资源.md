云资源绑定 EIP 后，具备公网通信能力。

## 绑定云资源

EIP 支持绑定的云资源有：[ECS](https://help.aliyun.com/zh/ecs/user-guide/overview-52)、[弹性网卡 ENI](https://help.aliyun.com/zh/ecs/user-guide/eni-overview)、[ALB](https://help.aliyun.com/zh/slb/application-load-balancer/alb-instance-overview)/[NLB](https://help.aliyun.com/zh/slb/network-load-balancer/user-guide/nlb-instance/)/[CLB](https://help.aliyun.com/zh/slb/classic-load-balancer/user-guide/clb-instance/)、[公网 NAT 网关](https://help.aliyun.com/zh/nat-gateway/user-guide/use-internet-nat-gateway-for-public-network-access)、[高可用虚拟IP](https://help.aliyun.com/zh/vpc/highly-available-virtual-ip-address-havip)。

### **绑定 ECS - 单 ECS 绑定单 EIP**

EIP 可直接绑定同地域、专有网络类型的 ECS 实例。

-   1 个 ECS 实例仅支持绑定 1 个 EIP。
    
-   绑定时，需确保 ECS 实例处于运行中或已停止状态，且没有配置固定公网 IP 或绑定其他 EIP。
    
-   EIP 以 NAT 模式和 ECS 实例绑定，只能处理 IP 层和传输层的地址和端口信息，不支持 NAT ALG（NAT应用层网关）涉及的相关协议。
    

### **控制台**

#### **EIP 绑定 ECS**

1.  前往[弹性公网IP](https://vpc.console.aliyun.com/eip/cn-hangzhou/eips)页面，在顶部菜单栏选择 EIP 所属地域。
    
2.  单击目标 EIP **操作**列的**绑定资源**，选择**云服务器 ECS 实例**，并选择对应的 ECS 实例。
    

#### **ECS 更换 EIP**

仅可通过解绑已有 EIP、绑定新 EIP 的方式，为 ECS 实例更换 EIP。

#### **找回 EIP**

EIP 不会变化。如果 EIP 到期、账号欠费未缴清账单，可能会被释放。可尝试[找回本账号在7天内释放的EIP](https://help.aliyun.com/zh/eip/elastic-ip-address#13bce237a8bn9)。

### **API**

调用[AssociateEipAddress](https://help.aliyun.com/zh/eip/developer-reference/api-vpc-2016-04-28-associateeipaddress-eips)，设置`InstanceType`为`EcsInstance`，绑定 EIP 与 ECS。

### **绑定 ENI - 单 ECS 绑定多 EIP**

1 个 ECS 实例仅支持绑定 1 个 EIP。当单个 ECS 实例需要部署多个独立公网服务时，可使用普通模式为 ECS 实例的弹性网卡绑定多 EIP。

> 每种[实例规格](https://help.aliyun.com/zh/ecs/user-guide/overview-of-instance-families#concept-sx4-lxv-tdb)支持绑定的辅助弹性网卡数量不同。

> 辅助弹性网卡绑定ECS实例后，部分镜像无法自动识别辅助弹性网卡的IP地址并添加路由，需要[配置辅助弹性网卡](https://help.aliyun.com/zh/ecs/user-guide/create-and-use-an-eni#task-1563594)。

> 普通模式下，EIP 以 NAT 模式与弹性网卡绑定，不支持 NAT ALG（NAT应用层网关）涉及的相关协议。支持绑定主弹性网卡和辅助弹性网卡，绑定的 EIP 数量取决于弹性网卡的私网 IP 数量，二者一一映射。

-   多弹性网卡：为单个 ECS 实例绑定多个辅助弹性网卡，并为每个辅助弹性网卡绑定 1 个 EIP。可为每个弹性网卡关联不同的安全组，配置不同的隔离策略，实现精细化安全访问控制。
    
-   [单网卡多 EIP](https://help.aliyun.com/zh/eip/associate-multiple-eips-with-a-secondary-eni-in-nat-mode)：无需网络隔离，只是简单地需要多个 EIP 承载不同的服务时，可以为单个 ECS 实例绑定 1 个辅助弹性网卡，并为辅助弹性网卡分配多个辅助私网IP，使用普通模式将多个 EIP 与辅助私网 IP 一一绑定。
    

### **控制台**

#### **绑定弹性网卡**

1.  前往[弹性公网IP](https://vpc.console.aliyun.com/eip/cn-hangzhou/eips)页面，在顶部菜单栏选择 EIP 所属地域。
    
2.  单击目标 EIP **操作**列的**绑定资源**，选择**弹性网卡**，选择普通模式与对应的辅助私网 IP 绑定。
    

### **API**

-   调用[AssociateEipAddress](https://help.aliyun.com/zh/eip/developer-reference/api-vpc-2016-04-28-associateeipaddress-eips)绑定EIP与弹性网卡：
    
    -   设置`InstanceType`为`NetworkInterface`。
        
    -   设置`Mode`为`NAT`。
        
-   调用[AssociateEipAddressBatch](https://help.aliyun.com/zh/eip/developer-reference/api-vpc-2016-04-28-associateeipaddressbatch-eips)批量绑定 EIP 与辅助弹性网卡。
    

### **绑定 ENI - EIP 网卡可见**

EIP 通过 NAT 方式映射到 ECS 实例的私网网卡，因此 ECS 实例网卡仅感知私网 IP 地址，无法查看 EIP。可使用 EIP 网卡可见模式绑定辅助弹性网卡，实现网卡可见。

-   以EIP网卡可见模式绑定后，不允许访问100.64.0.0/10网段，该网段为阿里云云服务专用网段，仅适用于私网访问。确保在 ECS 实例内配置 100.64.0.0/10 路由指向主网卡或其他辅助弹性网卡（该网卡不能以 EIP 网卡可见模式绑定 EIP）。
    
-   EIP 网卡可见模式绑定辅助弹性网卡使用限制较多，推荐[使用VPC附加网段实现EIP网卡可见](https://help.aliyun.com/zh/eip/expose-an-eip-on-an-nic-by-adding-a-secondary-cidr-block-to-a-vpc)：将公网 IP 段配置为 VPC 附加网段，在该网段下创建辅助弹性网卡与 EIP 绑定，挂载到 ECS 后即可在操作系统内直接管理该 EIP。
    

> 辅助弹性网卡绑定ECS实例后，部分镜像无法自动识别辅助弹性网卡的IP地址并添加路由，需要[配置辅助弹性网卡](https://help.aliyun.com/zh/ecs/user-guide/create-and-use-an-eni#task-1563594)。

> 绑定后，ECS 实例会自动生成一条出接口为辅助弹性网卡的路由，该条路由的优先级低于出接口为主网卡的路由，请根据业务需求[调整路由优先级](https://help.aliyun.com/zh/ecs/user-guide/configure-a-secondary-eni#78989a302b1a4)。

**EIP网卡可见模式**（不推荐）：EIP 将替换辅助弹性网卡的私网 IP，辅助弹性网卡将变为纯公网网卡，私网 IP 不可用。

-   不支持绑定主弹性网卡。EIP 只能绑定辅助弹性网卡上的主私网 IP。
    
-   需先绑定 EIP 与辅助弹性网卡，再将辅助弹性网卡绑定到 ECS 实例。
    
-   由于该模式下网卡的私网功能失效，如果使用的包年包月 EIP 到期释放后，需先解绑辅助弹性网卡与 ECS，再重新绑定才可恢复私网功能。
    
-   支持的地域：华东1（杭州）、华东2（上海）、华北1（青岛）、华北2（北京）、华北3（张家口）、华北5（呼和浩特）、华南1（深圳）、华南3（广州）、西南1（成都）、新加坡、印度尼西亚（雅加达）、德国（法兰克福）、英国（伦敦）、美国（弗吉尼亚）。
    
-   EIP 可支持全部 IP 协议类型，包括 NAT ALG（NAT应用层网关）涉及的相关协议。
    
-   要绑定的辅助弹性网卡所属VPC下不存在IPv4网关。
    

**多EIP网卡可见模式**（停止接受使用申请）：该模式下，辅助弹性网卡的私网IP和公网IP同时可用。但该模式已不再接受新用户的使用申请，已申请使用权限的用户可以继续使用。

-   不支持绑定主弹性网卡。辅助弹性网卡支持绑定 10 个 EIP。
    
-   支持的地域：华南1（深圳）、华东2（上海）、华北2（北京）、华北3（张家口）、西南1（成都）、新加坡、德国（法兰克福）、美国（弗吉尼亚）、英国（伦敦）。
    
-   支持的实例规格：ecs.d1ne、ecs.ebmc4、ecs.ebmg5、ecs.ebmhfg5、ecs.f1、ecs.gn5i、ecs.gn6v、ecs.i2、ecs.r1、ecs.re4、ecs.re4e、ecs.sccg5、ecs.sccgn6、ecs.scch5、ecs.g5、ecs.c5、ecs.r5、ecs.t5、ecs.sn2ne、ecs.se1ne、ecs.sn1ne。
    
-   EIP 可支持全部 IP 协议类型，包括 NAT ALG（NAT应用层网关）涉及的相关协议。
    
-   设置**多EIP网卡可见模式**后，辅助弹性网卡绑定的ECS实例必须开启DHCP功能，**多EIP网卡可见模式**才生效。
    
-   绑定后，调用[DescribeEipGatewayInfo](https://help.aliyun.com/zh/vpc/api-describeeipgatewayinfo#doc-api-Vpc-DescribeEipGatewayInfo)查询EIP的网关和子网掩码，并为 ECS 配置多个EIP：将辅助私网IP的网关和掩码修改为EIP的网关和掩码。
    

### **控制台**

#### **绑定弹性网卡**

1.  前往[弹性公网IP](https://vpc.console.aliyun.com/eip/cn-hangzhou/eips)页面，在顶部菜单栏选择 EIP 所属地域。
    
2.  单击目标 EIP **操作**列的**绑定资源**，选择**弹性网卡**，选择EIP网卡可见模式与对应的辅助私网 IP 绑定。
    

### **API**

-   调用[AssociateEipAddress](https://help.aliyun.com/zh/eip/developer-reference/api-vpc-2016-04-28-associateeipaddress-eips)绑定EIP与弹性网卡：
    
    -   设置`InstanceType`为`NetworkInterface`。
        
    -   设置`Mode`为`BINDED`或`MULTI_BINDED`。
        
-   调用[AssociateEipAddressBatch](https://help.aliyun.com/zh/eip/developer-reference/api-vpc-2016-04-28-associateeipaddressbatch-eips)批量绑定 EIP 与辅助弹性网卡。
    

### **绑定 NAT - 统一公网出口**

当多个 ECS 实例访问公网时，逐一配置 EIP 会增加成本。使用公网 NAT 网关的 SNAT 功能，可实现多个 ECS 实例共享 EIP 上网，节省成本的同时，通过隐藏实例的真实 IP 地址、限制入向连接提升安全性。

-   一个公网 NAT 网关支持绑定 20 个 EIP。
    
-   从2022年09月19日起，新创建的公网 NAT 网关绑定 EIP 时将占用 NAT 网关所在交换机的私网 IP （已有 NAT 网关实例不受影响），需确保 NAT 网关所在交换机内私网 IP 地址充足。
    

### **控制台**

#### **绑定弹性网卡**

1.  前往[弹性公网IP](https://vpc.console.aliyun.com/eip/cn-hangzhou/eips)页面，在顶部菜单栏选择 EIP 所属地域。
    
2.  单击目标 EIP **操作**列的**绑定资源**，选择**NAT 网关实例**，并选择对应的公网 NAT 网关实例。
    

### **API**

-   调用[AssociateEipAddress](https://help.aliyun.com/zh/eip/developer-reference/api-vpc-2016-04-28-associateeipaddress-eips)设置`InstanceType`为`Nat`，绑定 EIP 与公网 NAT 网关。
    
-   调用[AssociateEipAddressBatch](https://help.aliyun.com/zh/eip/developer-reference/api-vpc-2016-04-28-associateeipaddressbatch-eips)批量绑定 EIP 与公网 NAT 网关。
    

### **绑定负载均衡 - 统一公网入口**

推荐优先使用[应用型负载均衡ALB](https://help.aliyun.com/zh/slb/application-load-balancer/what-is-alb)和[网络型负载均衡NLB](https://help.aliyun.com/zh/slb/network-load-balancer/product-overview/what-is-nlb/)，在后端挂载不同可用区的多台后端服务器，通过将流量分发到不同的后端服务来扩展应用系统的服务吞吐能力，消除系统中的单点故障，提升应用系统的可用性。

### **控制台**

#### **绑定 ALB/NLB**

[弹性公网IP](https://vpc.console.aliyun.com/eip/cn-hangzhou/eips)页面不支持绑定。

-   新建实例时绑定：前往[ALB 购买页](https://common-buy.aliyun.com/?spm=5176.2020520102.content.2.7c5a7067rlggKa&commodityCode=slb_ealb_public_cn&request=%7B%22ord_time%22:%221:Hour%22,%22order_num%22:1,%22region%22:%22cn-hangzhou%22,%22address_type%22:%22Intranet%22,%22address_allocated_mode%22:%22Fixed%22,%22address_ip_version%22:%22Ipv4%22,%22ip_version%22:%22IPv4%22,%22alb_function_edition%22:%222%22,%22lcu%22:1%7D&regionId=cn-hangzhou)或[NLB 购买页](https://common-buy.aliyun.com/?spm=5176.2020520102.content.16.7c5a7067rlggKa&commodityCode=slb_nlb_public_cn&regionId=cn-hangzhou)，创建**公网**类型 ALB 实例或 NLB 实例。
    
-   变更实例网络类型：前往[ALB 列表页](https://slb.console.aliyun.com/alb/cn-hangzhou/albs)或[NLB 列表页](https://slb.console.aliyun.com/nlb/cn-hangzhou/nlbs)，在顶部菜单栏选择实例所在地域。单击目标实例 ID 进入详情页，将**网络类型**变更为公网。
    

#### **绑定 CLB**

1.  前往[弹性公网IP](https://vpc.console.aliyun.com/eip/cn-hangzhou/eips)页面，在顶部菜单栏选择 EIP 所属地域。
    
2.  单击目标 EIP **操作**列的**绑定资源**，选择**负载均衡 SLB 实例**，并选择对应的 CLB 实例。
    

### **API**

-   调用[CreateLoadBalancer](https://help.aliyun.com/zh/slb/application-load-balancer/developer-reference/api-alb-2020-06-16-createloadbalancer)设置`AddressType`为`Internet`，创建公网类型 ALB 实例。
    
-   调用[UpdateLoadBalancerAddressTypeConfig](https://help.aliyun.com/zh/slb/application-load-balancer/developer-reference/api-alb-2020-06-16-updateloadbalanceraddresstypeconfig)设置`AddressType`为`Internet`，将 ALB 实例的网络类型变更为公网。
    
-   调用[CreateLoadBalancer](https://help.aliyun.com/zh/slb/network-load-balancer/developer-reference/api-nlb-2022-04-30-createloadbalancer)设置`AddressType`为`Internet`，创建公网类型 NLB 实例。
    
-   调用[UpdateLoadBalancerAddressTypeConfig](https://help.aliyun.com/zh/slb/network-load-balancer/developer-reference/api-nlb-2022-04-30-updateloadbalanceraddresstypeconfig)设置`AddressType`为`Internet`，将 NLB 实例的网络类型变更为公网。
    
-   调用[AssociateEipAddress](https://help.aliyun.com/zh/eip/developer-reference/api-vpc-2016-04-28-associateeipaddress-eips)设置`InstanceType`为`SlbInstance`，绑定 EIP 与 CLB。
    

### **绑定 HaVip - IP 漂移**

使用[高可用虚拟IP（HaVip）](https://help.aliyun.com/zh/vpc/highly-available-virtual-ip-address-havip)功能，在云上可以实现同可用区服务器主备切换过程中服务IP不变。为 HaVip 绑定 EIP后，HaVip 可以通过 EIP 面向公网提供高可用服务。

-   使用高可用虚拟 IP 前，需登录[配额中心控制台](https://quotas.console.aliyun.com/products/vpc/quotas?spm=a2c4g.11186623.0.0.610ecda16wO953&query=vpc_privilege_allow_buy_havip_instance&keyword=buy_havip_instance)申请创建 HaVip 的权限。配额为1，代表可创建 HaVip，而单账号默认支持创建 50 个 HaVip。
    
-   一个高可用虚拟 IP 只能绑定一个 EIP。
    
-   高可用虚拟 IP 必须处于可用或已分配状态。
    

### **控制台**

#### **绑定 HaVip**

1.  前往[弹性公网IP](https://vpc.console.aliyun.com/eip/cn-hangzhou/eips)页面，在顶部菜单栏选择 EIP 所属地域。
    
2.  单击目标 EIP **操作**列的**绑定资源**，选择**高可用虚拟IP**，并选择对应的 HaVip 实例。
    

### **API**

调用[AssociateEipAddress](https://help.aliyun.com/zh/eip/developer-reference/api-vpc-2016-04-28-associateeipaddress-eips)设置`InstanceType`为`HaVip`，绑定 EIP 与 HaVip。

## 解绑云资源

-   按量付费 EIP 解绑资源后，仍需支付[EIP 配置费（公网 IP 保有费）](https://help.aliyun.com/zh/eip/pay-as-you-go/#section-tbh-f66-2wt)。不再需要时，建议及时[释放](https://help.aliyun.com/zh/eip/elastic-ip-address#1a5d5f577by23)。
    
-   包年包月 EIP 解绑资源后，如果不再使用，可以直接[退订](https://help.aliyun.com/zh/user-center/cancel-subscription/#b475cd1055o92)。
    

### **控制台**

单击目标 EIP **操作**列的**解绑资源**。

### **API**

调用[UnassociateEipAddress](https://help.aliyun.com/zh/eip/developer-reference/api-vpc-2016-04-28-unassociateeipaddress-eips)解绑 EIP 与云资源。