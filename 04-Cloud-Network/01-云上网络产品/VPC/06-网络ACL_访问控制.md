# 网络ACL

您可以创建网络ACL并将其与交换机绑定，通过配置网络ACL规则，精确控制出入交换机的流量。

## 工作原理

### **作用范围**

网络ACL仅对绑定交换机内的弹性网卡生效。

1.  网络ACL会控制依赖弹性网卡实现网络通信的云资源的流量，例如ECS、ECI、NLB等实例。
    
    > 由于RDS、CLB等实例不依赖弹性网卡，流量不会被网络ACL控制。RDS实例的访问控制由其[白名单](https://help.aliyun.com/zh/rds/apsaradb-rds-for-mysql/configure-an-ip-address-whitelist-for-an-apsaradb-rds-for-mysql-instance)实现，CLB实例通过[访问控制策略](https://help.aliyun.com/zh/slb/classic-load-balancer/user-guide/access-control)实现。
    
    > 网络ACL不会控制绑定了[网卡可见模式EIP](https://help.aliyun.com/zh/eip/associate-an-eip-with-a-secondary-eni-1#section-p20-xda-tzy)的辅助弹性网卡的流量。
    
2.  通过私网连接PrivateLink的方式访问云服务时，流量经过终端节点网卡，会受网络ACL规则管控。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7511539771/CAEQYxiBgIDT4Je00xkiIDQ3YjdjM2ZlN2U2YjRlZTI5NjA2MTlhNjAzMjNjZWFl4553391_20240801095024.466.svg)

### **规则生效机制**

1.  每条规则有生效顺序，系统将从生效顺序为1的规则开始，根据IP版本、协议类型、源/目的地址及端口范围，依次判断流量是否匹配。流量匹配到首条规则后，执行指定的允许/拒绝策略。
    
    > 针对入方向规则和出方向规则，端口范围始终匹配流量的目的端口。
    
    > 入方向规则仅支持配置源地址，出方向规则仅支持配置目的地址。单条规则不支持同时配置源地址和目的地址。
    
    > 网络ACL在拒绝流量时采用drop操作，发起端不会收到任何响应，表现为请求超时或者无法建立连接。
    
2.  网络ACL规则是无状态的。当配置入方向规则来允许特定流量进入交换机时，响应流量不会被自动允许，您必须创建**允许**响应流量返回客户端临时端口的出方向规则。当客户端向服务器发起请求时，会从临时端口范围中随机选择一个端口，接收服务器的响应。
    
    > 为了保证各种类型的客户端都能正常访问您的服务，您可以设置1024-65535的临时端口范围。
    
    不同类型的客户端的临时端口范围
    
    | **客户端** | **临时端口范围** |
    | --- | --- |
    | Linux | 32768/61000 |
    | Windows Server 2003 | 1025/5000 |
    | Windows Server 2008及更高版本 | 49152/65535 |
    | NAT网关 | 1024/65535 |
    

示例配置中，存在两条源/目的地址范围有重叠的自定义规则。当IP为192.168.0.1的客户端通过HTTPS协议访问子网内的服务时，流量会首先匹配到生效顺序为1的规则，因此被拒绝；而当IP为192.168.1.1的客户端访问时，流量按顺序匹配到生效顺序为2的规则，因此被允许，且响应流量按照生效顺序为1的出方向规则发送回客户端的临时端口。

> 当服务需开放大量端口，但部分端口需要拒绝访问时，您需要确保拒绝规则的优先级高于允许规则。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8511539771/CAEQWhiBgMCEk.jIwBkiIDQwMTYwYTRlNWJiMzQ2YWI5NmFlYzUwZDU2YTg4YTk05346050_20250626112318.323.svg)

### **与安全组的区别**

| **对比项** | **网络ACL** | **安全组** |
| --- | --- | --- |
| 作用范围 | 根据网络ACL规则控制出入交换机的流量。 | ECS实例级别的访问控制方式。ECS 实例关联的多个安全组的规则将按固定的策略排序，共同决定是否放行实例出入站的流量。 |
| 返回数据流状态 | 无状态：返回数据流必须被规则明确允许。 | 有状态：返回数据流会被自动允许，不受任何规则的影响。 |
| 规则匹配顺序 | 按照规则生效顺序，依次判断流量是否匹配。 | 先按照优先级排序：优先级相同时，授权策略为拒绝的规则排在授权策略为允许的规则之前。 排序完成后，依次匹配已排序好的规则。 |
| 与ECS实例的关联关系 | 每个交换机仅允许绑定一个网络ACL。 | 一个ECS实例可加入多个安全组。 |
| 规则地址配置 | 入方向规则仅支持配置源地址，出方向规则仅支持配置目的地址。单条规则不支持同时配置源地址和目的地址。 | 入方向规则配置授权对象（源地址），出方向规则配置授权对象（目的地址）。 |

## 创建/删除网络ACL

您可以创建网络ACL，并将其与交换机关联，来控制出入交换机的流量。

当您为仅有IPv4网段的VPC创建网络ACL时，系统默认在入方向和出方向添加以下规则：

-   云服务规则：允许使用阿里云的私网域名解析服务与ECS元数据服务。优先级固定最高，无法修改和删除。
    
    > 1、阿里云默认DNS服务器IP为100.100.2.136、100.100.2.138，用于解析内网域名。
    
    > 2、MetaServer的IP为100.100.100.200，提供了ECS实例必需的元数据服务，确保实例正常运行。
    
-   自定义规则：允许所有IPv4流量，以确保创建网络ACL后不会影响同一VPC内不同交换机之间的私网互通。您可以配置自定义规则，精确控制进出交换机的流量。
    
-   系统规则：用于拒绝未匹配其他规则的IPv4流量。优先级固定最低，无法修改和删除。
    

如果ACL所属的VPC开启了IPv6，入方向和出方向将再添加允许所有IPv6流量的自定义规则、拒绝所有IPv6流量的系统规则。

> 网络ACL仅允许绑定所属VPC内的交换机，每个交换机仅允许绑定一个网络ACL。

### **控制台**

#### **创建网络ACL**

1.  前往[专有网络控制台-网络ACL](https://vpc.console.aliyun.com/nacl/cn-hangzhou/nacls)，在页面上方选择目标地域后，单击**创建网络ACL**。
    
2.  配置**所属专有网络**，需选择计划与网络ACL关联的交换机所属的VPC。
    

#### **关联交换机**

单击实例ID或**操作**列的**管理**，进入**已绑定资源**页签，单击**关联交换机**，选择一个或多个目标交换机并**确定关联**。关联的交换机将按照网络ACL规则控制出入交换机的流量。如需解除控制，您可以在该页签下，单击目标交换机**操作**列的**解绑**。

您也可以在目标交换机详情页的**网络ACL**参数项，绑定、更换或解绑网络ACL。

#### **删除网络ACL**

需先确保已解除与交换机的关联。在目标网络ACL的**操作**列，单击**删除**。

### **API**

-   调用[CreateNetworkAcl](https://help.aliyun.com/zh/vpc/developer-reference/api-vpc-2016-04-28-createnetworkacl)创建网络ACL。
    
-   调用[AssociateNetworkAcl](https://help.aliyun.com/zh/vpc/developer-reference/api-vpc-2016-04-28-associatenetworkacl)绑定网络ACL与交换机。
    
-   调用[UnassociateNetworkAcl](https://help.aliyun.com/zh/vpc/developer-reference/api-vpc-2016-04-28-unassociatenetworkacl)解除网络ACL与交换机的绑定。
    
-   调用[DeleteNetworkAcl](https://help.aliyun.com/zh/vpc/developer-reference/api-vpc-2016-04-28-deletenetworkacl)删除网络ACL。
    

### **Terraform**

> 与控制台逻辑不同，Terraform仅支持将网络ACL与一个交换机关联。

> Resources：[alicloud\_network\_acl](https://registry.terraform.io/providers/aliyun/alicloud/latest/docs/resources/network_acl)

```
# 指定网络ACL的地域
provider "alicloud" {
  region = "cn-hangzhou"
}

# 指定VPC ID
variable "vpc_id" {
  default = "vpc-bp1k******" # 修改为VPC的实际ID
}

# 指定交换机ID
variable "vswitch_id" {
  default = "vsw-bp1y******" # 修改为交换机的实际ID
}

# 创建网络ACL并关联交换机 
resource "alicloud_network_acl" "example_network_acl" {
  vpc_id           = var.vpc_id # 指定网络ACL所属VPC
  network_acl_name = "example_network_acl_name"
  resources {
    resource_id   = var.vswitch_id # 指定网络ACL关联的交换机
    resource_type = "VSwitch"
  }
}
```

## 配置网络ACL规则

-   创建网络ACL后，系统将默认添加允许/拒绝所有流量的网络ACL规则。
    
-   您可以配置自定义规则，精确控制特定流量进出交换机。基于**协议类型**、**IP版本**、**源地址**/**目的地址**、**端口范围**匹配到网络ACL规则后，系统将对流量执行指定**策略**，允许/拒绝对应的流量。
    
    -   协议类型为`TCP(6)`/`UDP(17)`时，可以调整端口范围。取值范围为0~65535，设置格式为`起始端口/终止端口`，但不能设置为`-1/-1`（表示不限制端口）。选择其他协议类型时，端口范围无法设置，默认为`-1/-1`。
        
    -   仅网络 ACL 所属 VPC 开启 IPv6 时，您可以添加 IPv6 类型的出入方向规则。
        
    -   添加/修改/删除网络ACL规则后，会自动应用到与网络ACL绑定的交换机。
        
-   您可以将常用 IP 地址段统一管理在[前缀列表](https://help.aliyun.com/zh/vpc/vpc-prefix-lists)中，在网络 ACL 规则中引用。修改前缀列表后，网络 ACL 规则会自动同步更新。
    
    -   前缀列表的**最大条目数**（而非实际包含的条目数），会占用网络 ACL 规则的配额。您可尝试通过调低最大条目数、合并相邻IP段、清理无用条目等方式来降低配额超限风险。
        
    -   前缀列表是地域级资源，仅限创建地域内使用，不可跨地域引用或共享。一个前缀列表不能同时包含 IPv4 和 IPv6 CIDR地址块。
        

常用端口列表

| **端口** | **服务** | **说明** |
| --- | --- | --- |
| 21  | FTP | FTP服务所开放的端口，用于上传、下载文件。 |
| 22  | SSH | SSH端口，用于通过命令行模式或远程连接软件（例如PuTTY、Xshell、SecureCRT等）连接Linux实例。 |
| 23  | Telnet | Telnet端口，用于Telnet远程登录ECS实例。 |
| 25  | SMTP | SMTP服务所开放的端口，用于发送邮件。 |
| 53  | DNS | 用于域名解析服务器（Domain Name Server，简称DNS）协议。 |
| 80  | HTTP | 用于HTTP服务提供访问功能，例如，IIS、Apache、Nginx等服务。 |
| 110 | POP3 | 用于POP3协议，POP3是电子邮件接收的协议。 |
| 143 | IMAP | 用于IMAP（Internet Message Access Protocol）协议，IMAP是用于接收电子邮件的协议。 |
| 443 | HTTPS | 用于HTTPS服务提供访问功能。HTTPS是一种能提供加密和通过安全端口传输的协议。 |
| 1433 | SQL Server | SQL Server的TCP端口，用于供SQL Server对外提供服务。 |
| 1434 | SQL Server | SQL Server的UDP端口，用于获取SQL Server使用的TCP/IP端口号和IP地址等信息。 |
| 1521 | Oracle | Oracle通信端口，ECS实例上部署了Oracle SQL需要放行的端口。 |
| 3306 | MySQL | MySQL数据库对外提供服务的端口。 |
| 3389 | Windows Server Remote Desktop Services | Windows Server Remote Desktop Services（远程桌面服务）端口，可以通过这个端口使用软件连接Windows实例。 |
| 8080 | 代理端口 | 与80端口类似，8080端口通常用于提供`WWW`代理服务，用于实现网页浏览。如果您使用了8080端口，当访问网站或使用代理服务器时，需要在IP地址后面加上冒号和8080（例如：`IP地址:8080`）。在安装Apache Tomcat服务后，默认的服务端口为8080。 |
| 137、138、139 | NetBIOS协议 | NetBIOS协议常被用于Windows文件、打印机共享和Samba。 - UDP端口137和138通常用于网上邻居传输文件时的通信。 - 通过端口139，连接试图获取NetBIOS/SMB服务。 |

> 1、配置[DHCP选项集](https://help.aliyun.com/zh/vpc/dhcp-option-set-and-dns-hostname)后，您需要添加放行指定DNS服务器的出入方向规则。未添加规则，可能会造成域名解析异常。

> 2、使用负载均衡时，您需要在出入方向规则中添加允许监听端口接收到的请求转发至后端服务器、健康检查端口的请求发送至后端服务器的规则。

### **控制台**

在目标网络ACL的**入方向规则**/**出方向规则**页签，您可参考以下步骤，来配置自定义规则。

> 由于网络ACL规则是无状态的，当您设置入方向规则来允许特定流量进入交换机时，需要设置相应的出方向规则。

#### **添加规则**

-   手动配置：在目标网络ACL的**入方向规则**/**出方向规则**页签，单击**管理入方向规则**/**管理出方向规则**。
    
    -   单击**添加IPv4规则**/**添加IPv6规则**，逐条配置。
        
    -   如果您需要对多个IP地址段进行统一的访问控制，您可以选择**快速添加规则**，通过**优先级**来设置插入规则的位置。
        
    -   将常用 IP 地址段统一管理在前缀列表后，可单击**添加IPv4规则**/**添加IPv6规则**，选择**IP版本**为**VPC前缀列表**，配置**源地址**/**目的地址**为前缀列表。
        
-   批量导入：如需批量添加不同策略的规则，您可以使用提供的模板，批量**导入规则**。
    
    -   模板中列出的所有配置项均需填写，缺少配置项的规则将无法导入。
        
    -   不支持引用前缀列表。
        
    -   成功导入的规则将在原有规则的基础上顺序添加，不会覆盖原有规则。
        

#### **调整规则顺序**

单击**管理入方向规则**/**管理出方向规则**，上下拖动规则来调整生效顺序。

#### **删除规则**

在目标网络ACL规则的**操作**列单击**删除**。

### **API**

-   调用[UpdateNetworkAclEntries](https://help.aliyun.com/zh/vpc/developer-reference/api-vpc-2016-04-28-updatenetworkaclentries)更新网络ACL规则。与控制台逻辑不同的是，该API将对ACL规则进行全量更新。如果只传入新增规则，将会删除原有规则，仅保留新传入的规则。因此，增加规则时必须传入所有需要保留的规则。
    
-   调用[CopyNetworkAclEntries](https://help.aliyun.com/zh/vpc/developer-reference/api-vpc-2016-04-28-copynetworkaclentries)将网络ACL的规则完整复制到另一个网络ACL。为保证所有规则都能被目标网络ACL正确地识别和接收，您需确保两个网络ACL所属的VPC均只有IPv4网段或均开启了IPv6。未开启IPv6的VPC中的网络ACL无法配置IPv6类型的规则，若将规则完整复制到已开启IPv6的VPC的网络ACL时，系统不会自动添加允许所有IPv6流量的自定义规则，可能影响IPv6通信。
    

### **Terraform**

本示例分别在入方向和出方向添加了拒绝规则，您应根据实际的访问控制策略调整规则配置。

> Resources：[alicloud\_network\_acl](https://registry.terraform.io/providers/aliyun/alicloud/latest/docs/resources/network_acl)

```
# 指定网络ACL的地域
provider "alicloud" {
  region = "cn-hangzhou"
}

# 指定VPC ID
variable "vpc_id" {
  default = "vpc-bp1k******" # 修改为VPC的实际ID
}

# 指定交换机ID
variable "vswitch_id" {
  default = "vsw-bp1y******" # 修改为交换机的实际ID
}

# 创建网络ACL并绑定交换机
resource "alicloud_network_acl" "example_network_acl" {
  vpc_id           = var.vpc_id # 指定网络ACL所属VPC
  network_acl_name = "example_network_acl_name"
  resources {
    resource_id   = var.vswitch_id # 指定网络ACL关联的交换机
    resource_type = "VSwitch"
  }
  ingress_acl_entries { # 指定入方向规则
    network_acl_entry_name = "example-ingress"
    protocol               = "tcp"         # 协议类型
    source_cidr_ip         = "10.0.0.0/24" # 源地址 
    port                   = "20/80"       # 端口范围
    policy                 = "drop"        # 策略
  }
  egress_acl_entries { # 指定出方向规则
    network_acl_entry_name = "example-egress"
    protocol               = "tcp"
    destination_cidr_ip    = "10.0.0.0/24" # 目的地址 
    port                   = "20/80"       # 端口范围
    policy                 = "drop"        # 策略
  }
}
```

## 网络ACL规则配置示例

### **限制不同交换机下ECS的互通**

同一VPC内的不同交换机之间默认私网互通，如需限制不同交换机下的资源互通，您可以使用网络ACL拒绝特定IP的访问。

如图，您可以为交换机1绑定的网络ACL配置出入方向规则，禁止交换机1中的实例与ECS06互通。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8511539771/CAEQYxiBgMDWkpy00xkiIDNiZjlkYzI5NDc2MTQxYmRiNTljMTg3YmUxOTZlNmFi5274221_20250627113930.173.svg)

### **仅允许特定IP访问云上服务**

使用高速通道实现线下IDC与VPC互通后，线下IDC中的所有资源都可以访问云上服务。您可以使用网络ACL仅允许特定IP访问，拒绝其他访问。

如图，您可以为交换机绑定的网络ACL配置出入方向规则，仅允许云下服务器1和云下服务器2访问交换机内的实例。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8511539771/CAEQWhiBgIDVop_cwBkiIGUwY2FiYjlmNWNhZjQ2Y2M5NmYwM2RlMWFiMzVmM2Zi5274221_20250627113930.173.svg)

## 更多信息

### **计费说明**

网络ACL功能不收费。

### **支持的地域**

#### **公有云支持的地域**

| **区域** | **支持网络ACL的地域** |
| --- | --- |
| 亚太-中国 | 华东1（杭州）、华东2（上海）、华东5 （南京-本地地域-关停中）、华北1（青岛）、华北2（北京）、华北3（张家口）、华北5（呼和浩特）、华北6（乌兰察布）、华南1（深圳）、华南2（河源）、华南3（广州）、西南1（成都）、西北2（中卫）、中国香港、华中1（武汉-本地地域）、华东6（福州-本地地域-关停中） |
| 亚太-其他 | 日本（东京）、韩国（首尔）、新加坡、马来西亚（吉隆坡）、印度尼西亚（雅加达）、菲律宾（马尼拉）、泰国（曼谷）、马来西亚（柔佛州） |
| 欧洲与美洲 | 德国（法兰克福）、英国（伦敦）、法国（巴黎）、美国（硅谷）、美国（弗吉尼亚）、墨西哥 |
| 中东  | 阿联酋（迪拜）、沙特（利雅得）- 合作伙伴运营 |

#### **金融云支持的地域**

| **区域** | **支持网络ACL的地域** |
| --- | --- |
| 亚太  | 华南1 金融云、华东2 金融云、华北2 金融云（邀测） |

##### **政务云支持的地域**

| **区域** | **支持网络ACL的地域** |
| --- | --- |
| 亚太  | 华北2 阿里政务云1 |

### **配额**

| **配额名称** | **描述** | **默认限制** | **提升配额** |
| --- | --- | --- | --- |
| vpc\\_quota\\_nacl\\_ingress\\_entry | 单个网络ACL支持创建的入方向规则数量 > 网络ACL所属VPC开启了IPv6时，支持创建的IPv4/IPv6入方向规则，默认均为20条。 | 20条 | 前往[配额管理页面](https://vpc.console.aliyun.com/quota)或[配额中心](https://quotas.console.aliyun.com/products/vpc/quotas?query=peer)申请提升配额。 |
| vpc\\_quota\\_nacl\\_egress\\_entry | 单个网络ACL支持创建的出方向规则数量 > 网络ACL所属VPC开启了IPv6时，支持创建的IPv4/IPv6入方向规则，默认均为20条。 | 20条 |
| nacl\\_quota\\_vpc\\_create\\_count | 单个VPC支持创建的网络ACL数量 | 20个 |

# 访问控制

阿里云提供**安全组**和**网络ACL**两种访问控制方式，可实现VPC内实例级别或交换机级别的网络隔离。

-   [安全组](https://help.aliyun.com/zh/ecs/user-guide/overview-44)：安全组是VPC内的虚拟防火墙，能够控制进出ECS实例的流量。通过将具有相同安全需求并相互信任的ECS实例放入相同的安全组，可以划分安全域，保障云上资源的安全。
    
-   [网络ACL](https://help.aliyun.com/zh/vpc/network-acl-overview)：网络ACL能够控制进出交换机的流量。通过将多个交换机绑定相同的网络ACL，可统一控制进出多个交换机的流量。
    

| **对比项** | **安全组** | **网络ACL** |
| --- | --- | --- |
| 示意图 | ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5847204571/CAEQXxiBgICa0.7pwRkiIDg1ZTUxOTIwNGQwOTRlZTU5OTYwM2UyM2UyZTQ5MDhk5274221_20250627113930.173.svg) |   |
| 作用范围 | 实例级别 您可以将安全组绑定一个或多个ECS。 | 交换机级别 您可以将网络ACL绑定一个或多个交换机。 |
| 工作方式 | 有状态，自动允许回包。 例如允许入方向访问80端口的流量时，您只需为`请求`添加入方向规则，无需配置出方向规则，相关`响应`流量会自动放行。 | 无状态，回包需单独放行。 例如允许入方向访问80端口的流量时，您既要为`请求`添加入方向规则，也要为`响应`添加出方向规则。 |
| 组内控制策略 | 普通安全组：可选组内互通或隔离。 企业级安全组：默认组内隔离。 | 不控制同一个交换机内的ECS实例间的流量。 |
| 应用场景 | 实例间互访、对外开放端口 | 交换机级别的隔离、跨交换机访问控制 |