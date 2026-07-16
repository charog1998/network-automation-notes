使用转发路由器可以实现在多个专有网络VPC（Virtual Private Cloud）共用一个公网NAT网关，从而达到多VPC访问公网的效果。

## 背景信息

云企业网CEN（Cloud Enterprise Network）是运行在阿里云私有全球网络上的一张高可用网络。云企业网通过转发路由器TR（Transit Router）帮助您在跨地域VPC之间，VPC与本地数据中心IDC（Internet Data Center）间搭建私网通信通道。

转发路由器实例是地域范围内的核心转发网元，为您转发同地域或跨地域间的流量，并支持定义灵活的路由策略。在一个云企业网实例中，一个地域支持创建一个转发路由器实例。您可以将网络实例连接到企业版转发路由器。企业版转发路由器连接网络实例后，通过转发路由器路由表存储网络实例的路由。企业版转发路由器通过查询路由表中的路由条目信息转发网络实例的流量。

关于转发路由器的更多信息，请参见[转发路由器的工作原理](https://help.aliyun.com/zh/cen/product-overview/how-transit-routers-work#concept-1964186)。

## 场景示例

某公司在西南1（成都）地域创建了两个VPC，其名称分别为VPC-A和VPC-B。在VPC-A中，创建了vSwitch-A1和vSwitch-A2，并在vSwitch-A1中创建了公网NAT网关；在vSwitch-A2中创建ECS1实例。在VPC-B中，创建了vSwitch-B1和vSwitch-B2，并在vSwitch-B1中创建了ECS2实例。因公司业务需要，VPC-A与VPC-B都需要访问公网。

公司可以通过使用转发路由器并结合转发路由器路由表功能，然后在VPC-A中创建公网NAT网关，同时为公网NAT网关配置SNAT规则，实现VPC-A和VPC-B通过公网NAT网关访问公网。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2410781571/CAEQWhiBgIDd4_ONvxkiIDRhZDkzYWNlZDI2NzQ3YWE5YjYzZTdhYjNiYmVkY2Mw4527175_20240712113815.274.svg)

## 前提条件

-   您已经参考下表完成了VPC和vSwitch的创建。具体操作，请参见[创建和管理专有网络](https://help.aliyun.com/zh/vpc/create-and-manage-a-vpc#task-1012575)。
    
    | **VPC名称** | **地域** | **交换机名称** | **可用区和网段** |
    | --- | --- | --- | --- |
    | VPC-A | 西南1（成都） | vSwitch-A1 | 成都可用区A，192.168.10.0/24 |
    | vSwitch-A2 | 成都可用区B，192.168.20.0/24 |
    | VPC-B | vSwitch-B1 | 成都可用区A，172.16.10.0/24 |
    | vSwitch-B2 | 成都可用区B，172.16.20.0/24 |
    
-   您已经在vSwitch-A2中创建了ECS1实例，在vSwitch-B1中创建了ECS2实例。具体操作，请参见[自定义购买实例](https://help.aliyun.com/zh/ecs/user-guide/create-an-instance-by-using-the-wizard#task-vwq-5g4-r2b)。
    
-   您已经创建了云企业网实例。具体操作，请参见[创建云企业网实例](https://help.aliyun.com/zh/cen/user-guide/create-a-cen-instance#task-1680986)。
    
-   您已经在VPC实例所在地域创建了企业版转发路由器实例。具体操作，请参见[创建转发路由器实例](https://help.aliyun.com/zh/cen/user-guide/transit-routers#section-qmu-6ox-hcu)。
    

## 配置步骤

### **步骤一：创建公网NAT网关**

1.  登录[NAT网关管理控制台](https://vpc.console.aliyun.com/nat)。
    
2.  在**公网NAT网关**页面，单击**创建公网NAT网关**。
    
3.  在**NAT网关**页面，配置以下购买信息，然后单击**立即购买**。
    
    | **配置项** | **说明** |
    | --- | --- |
    | **地域** | 选择需要创建公网NAT网关的地域。 |
    | **网络及可用区** | 请选择NAT网关所属的VPC和交换机。创建成功后，无法进行修改或切换。 |
    | **网络类型** | 本文选择**公网NAT网关**。 - **公网NAT网关**：具备网络地址转换能力，可以绑定弹性公网IP，从而为ECS实例提供访问互联网的能力，实现私网和公网之间的通信。 - **VPC NAT网关**：同样具备网络地址转换能力，但无法绑定弹性公网IP，只能为ECS实例提供私网内部的地址转换，适用于内网地址隐藏、地址冲突规避等场景。 |
    | **弹性公网IP** | 本文选择**新购弹性公网IP**。 - **选择已有** **弹性公网IP实例**：选择**未绑定实例**的弹性公网IP。 - **新购弹性公网IP**：默认创建**BGP（多线）**类型的按使用流量计费的弹性公网IP，可根据自身业务需要选择**带宽峰值**。 **说明** - 如需绑定其他**线路类型**或**计费类型**的弹性公网IP，请先[申请弹性公网IP](https://help.aliyun.com/zh/eip/apply-for-new-eips)，然后**选择已有**进行绑定。 - 每绑定一个弹性公网IP，将占用NAT网关所在交换机的一个私网IP地址。请确保该交换机具有足够的可用私网IP地址，否则将无法成功绑定新的弹性公网IP。 - **稍后配置**：成功创建的NAT网关将不具备公网能力，用户需手动绑定弹性公网IP。 |
    
    创建成功后，您可以在**公网NAT网关**页面查看已创建的公网NAT网关实例。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4522990571/p975559.png)
    

### **步骤二：创建VPC连接并配置路由**

在西南1（成都）地域的转发路由器中创建VPC-A连接和VPC-B连接，并为转发路由器配置路由。

1.  登录[云企业网管理控制台](https://cen.console.aliyun.com/)，找到目标云企业网实例，单击目标实例ID。
    
2.  在**基本信息** > **转发路由器**页签，找到目标地域的转发路由器实例，在**操作**列单击**创建网络实例连接**。
    
    分别为VPC-A、VPC-B创建VPC连接。
    
    **说明**
    
    企业版转发路由器支持的地域和可用区，请参见[转发路由器的版本](https://help.aliyun.com/zh/cen/product-overview/what-is-cen/#section-4vf-t15-cco)。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9828421571/p977202.png)
    
3.  在**转发路由器路由表**页签，单击**创建路由条目**。
    
    添加0.0.0.0/0路由条目，并将其指向VPC-A，以便将IPv4流量转发至VPC-A。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9828421571/p977220.png)
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9828421571/p977236.png)
    

### **步骤三：配置VPC路由表**

在路由表中添加0.0.0.0/0，并将其指向转发路由器，以便将IPv4流量转发至转发路由器。

1.  登录[专有网络管理控制台](https://vpcnext.console.aliyun.com/vpc)。
2.  在左侧导航栏，单击**路由表**。
3.  在**路由表**页面，找到VPC-B的系统路由表，单击路由表的ID。
    
4.  在路由表详情页面，单击**路由条目列表** > **自定义路由条目**页签，然后单击**添加路由条目**。
    
5.  在**添加路由条目**面板，配置以下参数信息，然后单击**确定**。
    
    | **配置** | **说明** |
    | --- | --- |
    | **名称** | 输入路由条目的名称。 |
    | **目标网段** | 本文选择**IPv4网段**，然后设置**0.0.0.0/0**。 |
    | **下一跳类型** | 选择下一跳的实例类型。 本文选择**转发路由器**。 |
    | **转发路由器** | 本文选择VPC-B连接。 |
    
    您可以在**自定义路由条目**页签，查看已创建的指向VPC-B连接的路由条目。
    

### **步骤四：创建SNAT条目**

在NAT网关上配置相应的SNAT条目，以确保指定资源能够通过绑定的弹性公网IP访问互联网。

1.  在**公网NAT网关**页面，找到目标公网NAT网关实例，然后在**操作**列单击**设置SNAT**。
    
2.  在**SNAT管理**页签，单击**创建SNAT条目**。
    
3.  在**创建SNAT条目**页面，配置以下参数，然后单击**确定创建**。
    
    | **配置项** | **说明** |
    | --- | --- |
    | **SNAT条目粒度** | 本文选择**VPC粒度**。您可以根据实际业务需求，选择适合自身业务的SNAT条目粒度。 - **VPC粒度**：适用于需要让VPC内所有ECS实例，以及通过CEN或专线等产品实现内网互通并配置了0.0.0.0/0路由条目指向该VPC的其他VPC或数据IDC内的ECS实例，统一通过同一弹性公网IP访问公网的场景。 - **交换机粒度**：适用于对公网访问有精细控制需求，只允许指定的交换机具备公网访问能力的场景。 - **ECS/弹性网卡粒度**：适用于对公网访问有精细控制需求，只允许指定的ECS实例或弹性网卡具备公网访问能力的场景。 - **自定义网段粒度**：适用于需要灵活指定任意IP网段，通过NAT网关统一配置公网访问能力的场景，可覆盖VPC内、跨VPC或跨本地IDC等各种网络环境，满足复杂或定制化网络结构的需求。 **说明** 当您选择多个交换机或ECS/弹性网卡时，将为您创建多条SNAT条目，这些条目将使用相同的公网IP地址。 |
    | **选择弹性公网IP地址** | 选择用来提供公网访问的弹性公网IP。 |
    

## **结果验证**

1.  通过[Workbench控制台](https://ecs-workbench.aliyun.com/view/instance/network/vpc/access)依次登录ECS1、ECS2实例。
    
2.  执行`ping 223.5.5.5`命令。
    
    经验证，ECS1和ECS2实例均可成功访问公网。
    
    ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=)