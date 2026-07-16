NAT网关控制台不支持在同一个VPC内直接切换公网NAT网关实例。您可以通过在同一个VPC内新建一个公网NAT网关，再修改目标网段为0.0.0.0/0的路由条目的方式实现公网NAT网关所属交换机或私网IP地址的变更。

## 操作流程

本文以在同一个VPC内切换公网NAT网关来变更公网NAT网关所属交换机为例进行介绍。![国际站流程](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3116449261/p308956.png)

## 前提条件

开始前，请确保满足以下条件：

-   您已经在华东1（杭州）地域创建了一个VPC（名称为VPC1），并在该VPC中创建了两个交换机（名称为VSW1，位于可用区B；名称为VSW2，位于可用区H）。具体操作，请参见[搭建IPv4专有网络](https://help.aliyun.com/zh/vpc/getting-started/create-vpc-with-ipv4#task-1512598)。
    
-   您已经在交换机VSW1创建了一个名称为ECS1的ECS实例且不配置固定公网IP地址。具体操作，请参见[自定义购买实例](https://help.aliyun.com/zh/ecs/user-guide/create-an-instance-by-using-the-wizard#task-vwq-5g4-r2b)。
    
-   您已经在交换机VSW1创建了一个公网NAT网关A实例，且已配置了VPC1的SNAT条目和端口映射方式的DNAT条目（私网IP地址为ECS1的IP地址，公网端口和私网端口均为22，协议类型为TCP）。
    

## 步骤一：验证NAT网关A实例的功能

1.  登录VSW1下的ECS1实例。具体操作，请参见[ECS连接方式概述](https://help.aliyun.com/zh/ecs/user-guide/connect-to-instance#concept-tmr-pgx-wdb)。
    
2.  执行`ping`命令测试网络连通性。
    
3.  使用`curl myip.ipip.net`命令探测ECS1实例的公网出口IP。
    
    经测试，ECS1实例公网出口IP与NAT网关A实例中SNAT条目中的IP一致，即ECS1实例通过NAT网关A实例的SNAT功能主动访问互联网。
    
    ```
    [root@iZm5e5s2jiy4hpbp345r4jZ ~]# curl myip.ipip.net
    当前 IP: 118.xxx.xxx.230 来自于: 中国 山东 青岛 阿里云/电信/联通/移动/教育网
    ```
    
4.  登录本地Linux设备。
    
5.  执行`ssh root@公网IP`命令，此处的公网IP即为NAT网关A实例的DNAT条目中的公网IP地址，然后输入ECS1实例的登录密码，查看是否可以远程连接到实例。
    
    若界面上出现Welcome to Alibaba Cloud Elastic Compute Service!时，表示您已经成功连接到实例，即ECS1实例通过NAT网关A实例的DNAT功能提供公网访问能力。
    
    ```
    [root@iZm5e6xxx jfzdlZ ~]# ssh 118.xxx.xxx.230
    The authenticity of host '118.xxx.xxx.230 (118.xxx.xxx.230)' can't be established.
    ECDSA key fingerprint is SHA256:uyobLEZxxxgmd4f/sqWRrcnqjLxxxpNQnCyBzNw.
    Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
    Warning: Permanently added '118.xxx.xxx.230' (ECDSA) to the list of known hosts.
    root@118.xxx.xxx.230's password:
    Welcome to Alibaba Cloud Elastic Compute Service !
    Last login: Thu Aug 12 17:26:53 2021 from 100.xxx.xxx.237
    [root@iZm5e5xxx 45r4jZ ~]#
    ```
    

## 步骤二：创建NAT网关B实例并绑定EIP

NAT网关B实例关联的交换机为VSW2。

1.  登录[NAT网关管理控制台](https://vpc.console.aliyun.com/nat)。
    
2.  在**公网NAT网关**页面，单击**创建公网NAT网关**。
    
3.  在**NAT网关**页面，配置以下购买信息，然后单击**立即购买**。
    
    | **配置项** | **说明** |
    | --- | --- |
    | **地域** | 选择需要创建公网NAT网关的地域。 |
    | **网络及可用区** | 请选择NAT网关所属的VPC和交换机。创建成功后，无法进行修改或切换。 |
    | **网络类型** | 本文选择**公网NAT网关**。 - **公网NAT网关**：具备网络地址转换能力，可以绑定弹性公网IP，从而为ECS实例提供访问互联网的能力，实现私网和公网之间的通信。 - **VPC NAT网关**：同样具备网络地址转换能力，但无法绑定弹性公网IP，只能为ECS实例提供私网内部的地址转换，适用于内网地址隐藏、地址冲突规避等场景。 |
    | **弹性公网IP** | 本文选择**新购弹性公网IP**。 - **选择已有** **弹性公网IP实例**：选择**未绑定实例**的弹性公网IP。 - **新购弹性公网IP**：默认创建**BGP（多线）**类型的按使用流量计费的弹性公网IP，可根据自身业务需要选择**带宽峰值**。 **说明** - 如需绑定其他**线路类型**或**计费类型**的弹性公网IP，请先[申请弹性公网IP](https://help.aliyun.com/zh/eip/apply-for-new-eips)，然后**选择已有**进行绑定。 - 每绑定一个弹性公网IP，将占用NAT网关所在交换机的一个私网IP地址。请确保该交换机具有足够的可用私网IP地址，否则将无法成功绑定新的弹性公网IP。 - **稍后配置**：成功创建的NAT网关将不具备公网能力，用户需手动绑定弹性公网IP。 |
    

## 步骤三：为NAT网关B实例创建SNAT条目和DNAT条目

为NAT网关B实例创建的SNAT条目和DNAT条目除了公网IP地址外，其余的规则需要与NAT网关A实例的相同。

1.  登录[NAT网关管理控制台](https://vpc.console.aliyun.com/nat)。
    
2.  在顶部菜单栏，选择公网NAT网关的地域。
    
3.  在**公网NAT网关**页面，找到目标公网NAT网关实例，然后在**操作**列单击**设置SNAT**。
    
4.  在**SNAT管理**页签，单击**创建SNAT条目**。
    
5.  在**创建SNAT条目**页面，配置以下参数，然后单击**确定创建**。
    
    | **配置项** | **说明** |
    | --- | --- |
    | **SNAT条目粒度** | 本文选择**VPC粒度**。您可以根据实际业务需求，选择适合自身业务的SNAT条目粒度。 - **VPC粒度**：适用于需要让VPC内所有ECS实例，以及通过CEN或专线等产品实现内网互通并配置了0.0.0.0/0路由条目指向该VPC的其他VPC或数据IDC内的ECS实例，统一通过同一弹性公网IP访问公网的场景。 - **交换机粒度**：适用于对公网访问有精细控制需求，只允许指定的交换机具备公网访问能力的场景。 - **ECS/弹性网卡粒度**：适用于对公网访问有精细控制需求，只允许指定的ECS实例或弹性网卡具备公网访问能力的场景。 - **自定义网段粒度**：适用于需要灵活指定任意IP网段，通过NAT网关统一配置公网访问能力的场景，可覆盖VPC内、跨VPC或跨本地IDC等各种网络环境，满足复杂或定制化网络结构的需求。 **说明** 当您选择多个交换机或ECS/弹性网卡时，将为您创建多条SNAT条目，这些条目将使用相同的公网IP地址。 |
    | **选择弹性公网IP地址** | 选择用来提供公网访问的弹性公网IP。 |
    
6.  返回**公网NAT网关**页面，找到已创建的NAT网关B实例，然后在**操作**列单击**设置DNAT**。
    
7.  在**DNAT管理**页签，单击**创建DNAT条目**。
    
8.  在**创建DNAT条目**页面，配置以下参数，然后单击**确定创建**。
    
    | **配置** | **说明** |
    | --- | --- |
    | **选择弹性公网IP地址** | 选择要提供互联网通信的公网IP。本文选择绑定到NAT网关B实例的EIP。 |
    | **选择私网IP地址** | 选择要通过DNAT规则进行公网通信的ECS实例。 本文选择**通过ECS或弹性网卡进行选择**，然后在下拉列表中选择ECS1。 |
    | **端口设置** | 选择DNAT映射的方式。 本文选择**具体端口**，即DNAT端口映射方式，然后**公网端口**输入22，**私网端口**输入22，**协议类型**选择**TCP**。 |
    | **条目名称** | 输入DNAT条目的名称。 名称长度为2~128个字符，以大小写字母或中文开头， 可包含数字、下划线（\\_）和短划线（-）。 |
    

## 步骤四：修改系统路由表中的自定义路由条目

在VPC内创建第一个公网NAT网关时，系统会在VPC系统路由表中自动添加一条目标网段为0.0.0.0/0，下一跳为公网NAT网关的路由条目，用于将流量路由到该公网NAT网关。因此创建了NAT网关B实例后，VPC系统路由表中并没有目标网段为0.0.0.0/0，下一跳为NAT网关B实例的路由条目，NAT网关B实例无法使用。您必须手动修改VPC系统路由表中目标网段为0.0.0.0/0的路由条目指向NAT网关B实例，才能完成将VPC中的NAT网关A实例切换为NAT网关B实例。

1.  登录[专有网络管理控制台](https://vpcnext.console.aliyun.com/vpc)。
2.  在左侧导航栏，单击**路由表**。
3.  在顶部菜单栏，选择路由表所属的地域。
4.  在**路由表**页面，找到VPC1的路由表，然后单击路由表的ID。
    
5.  选择**路由条目列表** > **自定义路由条目**页签，找到目标网段为0.0.0.0/0，下一跳指向NAT网关A实例的自定义路由条目，然后在**操作**列单击**删除**。
    
6.  在**删除路由条目**对话框，单击**确定**。
    
7.  单击**添加路由条目**，在**添加路由条目**面板，根据以下信息配置自定义路由条目，然后单击**确定**。
    
    | **配置** | **说明** |
    | --- | --- |
    | **名称** | 输入路由条目的名称。 名称长度为2~128个字符之间，以英文字母或中文开头，可包含数字、短划线（-）和下划线（\\_）。 |
    | **目标网段** | 输入需要将流量转发到的目标网段。本文选择**IPv4网段**，然后输入0.0.0.0/0。 |
    | **下一跳类型** | 选择下一跳的类型。本文选择**NAT网关**。 |
    | **NAT网关** | 选择下一跳实例。本文选择NAT网关B实例。 |
    
    **说明**
    
    路由条目切换后，存量的访问连接需要重连之后才能恢复，建议您在业务低峰期执行路由条目切换操作。
    

## 步骤五：测试验证

验证NAT网关A实例的功能是否已经切换到NAT网关B实例。本文是以变更NAT网关所属交换机为例进行介绍，在操作的过程中，同时完成了变更NAT网关的私网IP地址。如果您需要通过在同一个交换机下切换NAT网关来变更其私网IP地址，也可以参考本文进行操作。

1.  登录VSW1下的ECS1实例。
    
2.  执行`ping`命令测试网络连通性。
    
3.  使用`curl myip.ipip.net`命令探测ECS1实例的公网出口IP。
    
    经测试，ECS1实例公网出口IP与NAT网关B实例中SNAT条目中的IP一致，即ECS1实例通过NAT网关B实例的SNAT功能主动访问互联网。
    
    ```
    [root@iZm5e5xxx ~]# curl myip.ipip.net
    当前 IP: 47.3x.xxx.215 来自于: 中国 山东 青岛 阿里云/电信/联通/移动/教育网
    ```
    
4.  登录本地Linux设备。
    
5.  执行`ssh root@公网IP`命令，此处的公网IP即为NAT网关B实例的DNAT条目中的公网IP地址，然后输入ECS1实例的登录密码，查看是否可以远程连接到实例。
    
    若界面上出现Welcome to Alibaba Cloud Elastic Compute Service!时，表示您已经成功连接到实例，即ECS1实例通过NAT网关B实例的DNAT功能提供公网访问能力。
    
    ```
    [root@iZmxxxxxxxxxxxxxjfzdlZ ~]# ssh 47.xxx.xxx.215
    root@47.xxx.xxx.215's password:
    Welcome to Alibaba Cloud Elastic Compute Service !
    Last login: Thu Aug 12 17:07:54 2021 from 47.xxx.xxx.0.13
    [root@iZm5xxx345r4jZ ~]#
    ```