本文介绍私网资产主动发起外联的风险、及对应的解决方案和当前典型的业务场景下的防护方案，并为您提供防护部署和运维的操作流程。

## **业务出站流量安全挑战**

随着网络攻击的复杂化，企业的安全建设也面临更艰巨的挑战。一般企业云上工作负载往往既有互联网访问的入向流量，也有业务资产主动发起的出向流量。然而，在考虑如何保护网络时，大多企业安全运维团队往往更多关注入向网络流量，并部署相对完善的安全措施。但是出向网络流量的安全往往被忽视，成为很多企业的安全防护体系短板，比如入向防护措施被绕过后攻击渗透至内网，造成窃取数据、下载安装恶意软件或对外连接恶意中控等。同时，由于企业安全管理措施疏忽，也可能会有内部人员对外非授权访问，或访问恶意网站应用等，造成敏感数据泄露等风险。

企业需要关注的潜在出向流量安全风险：

-   **恶意软件攻陷风险**
    
    当恶意攻击者绕过入向安全防护栈措施，攻陷企业内部工作负载后，往往会外联恶意中控，如回调进行勒索软件下载等。在攻击链路中，恶意软件感染一般是更大规模攻击的初始阶段之一，许多恶意软件仍然需要与命令和控制 (C&C) 服务器进行通信，建立连接，获取更新，请求命令以及将窃取的数据泄露到中控服务器。某些类型的勒索软件、僵尸网络、挖矿行为等都需要进行外联回调。这时候就需要及时告警和阻止恶意外联，防止对企业的IT基础设施、数字资产、开发系统等造成进一步破坏。
    
-   **数据泄露风险**
    
    盗取企业高价值数据往往是恶意攻击者的目标，一旦攻击成功，恶意攻击者可以获取企业的高价值数据，如财务数据、密码、电子邮件、个人身份信息等，并通过网络流量外传，用于非法兜售、财务欺诈、身份盗窃等恶意活动。攻击者还可能利用这些获取的信息对企业进一步提权或访问敏感数据系统等，给企业带来更多破坏性风险。
    
-   **内部人员风险**
    
    由于安全意识不足或企业安全管理措施疏忽等，内部人员在进行业务系统开发或运维时，可能对外调用访问一些不安全的Web服务、地理位置、IP等。或者有意将企业敏感数据上传至外部GitHub等公开或开源平台，给企业造成攻击入侵风险和敏感数据泄露风险。这是需要及时有效的监测这些风险行为，并及时告警及阻止，同时也需要进一步审计溯源。
    
-   **供应链风险**
    
    如果企业自身安全系统完善，但是由于业务中需要涉及三方开发系统，或者需要与供应商、子公司等业务互联互访，一旦相应供应商或子公司由于安全措施不足，导致被破坏攻陷后，攻击也会影响到企业，并进行恶意外联等。这就需要企业针对来自供应链方的流量也需要进行安全监控和审计，发现攻击后能及时溯源止损。
    
-   **出站流量合规风险**
    
    一些行业监管机构以及安全内审团队，针对出向流量提出来较明确和严格的监管要求，提升系统的安全性。比如[支付卡行业数据安全标准 (PCI DSS) v 4.0](https://www.pcisecuritystandards.org/document_library/)的要求：1.3.2要求限制源自持卡人数据环境 (CDE) 的出站流量。根据要求，仅允许被认为必要的出站流量。必须阻止所有其他出站流量。此要求旨在防止实体网络内的恶意个人和受损系统组件与不受信任的外部主机进行通信。因此，企业也需要针对出站流量进行严格的安全管理和审计。
    

## **解决方案**

针对出向流量安全管理，企业可以通过采用“**NAT网关+NAT边界防火墙**”的方案实现对出向流量的有效监控和保护。

-   NAT网关通过自定义SNAT、DNAT条目可为云上服务器提供对外公网服务、及主动访问公网能力。通过NAT网关的SNAT能力，当ECS主动发起对外访问连接时，ECS会通过SNAT地址池中的EIP访问互联网，避免将私网直接暴露在公网，提升资产安全性。
    
-   NAT边界防火墙为云防火墙的NAT边界安全能力，可针对NAT转化前的VPC内资源（例如ECS、ECI等）通过NAT网关直接访问互联网时，进行4~7层流量安全保护，审计和拦截未授权的流量访问，降低未经授权的访问、数据泄露、恶意流量攻击等安全风险。云防火墙的访问控制策略相比NAT网关的SNAT规则，可以精细化的管控访问的目的IP、目的域名、目的区域、协议、端口及应用。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7839137271/CAEQQRiBgMDAmbbx9RgiIDFiNmZiMDljMjc1ODQzY2FhZGZmN2FlMGQ5MTMxZTEw3974287_20230905104416.134.svg)

## **方案架构**

### **场景一：多个VPC出向流量安全**

某企业机构在云上主要为数据中心系统开发业务，主要有两个专有网络VPC，一个为生产VPC，一个为测试VPC，日常开发环境中有外部软件调用需求（两个VPC都有外联），如jar包启动更新等，需企业员工开发仅授权访问正常业务，不允许非授权外联，以避免安全风险。

#### **部署方案**

-   每个VPC内部署一个NAT网关，在NAT网关上配置SNAT策略，实现私网ECS绑定NAT EIP访问公网。
    
-   每个NAT网关部署一个NAT边界防火墙，在NAT边界防火墙上配置白名单机制的ACL访问控制策略，不允许访问未经授权的IP和域名。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8839137271/CAEQQRiBgIDI8Ies9xgiIDM2ZTlhMWRkOGY1NTQ0Y2M5NGU2OWU4M2I5ZGYwNWEx4384339_20240415104546.173.svg)

### **场景二：统一DMZ VPC出向流量安全**

某金融机构在云上主要为证券保险业务，有多个业务VPC，包括中台VPC、第三方系统VPC、行情VPC等，所有VPC均通过DMZ访问公网，日常环境中有外部支付服务、外部行情服务及监管服务业务访问需求，需仅授权访问正常业务，不允许非授权外联，造成安全风险。同时需对所有出向访问流量实时监控审计，及时发现异常流量和攻击。

#### **部署方案**

-   仅DMZ VPC内部署一个NAT网关，在NAT网关上配置SNAT策略，实现私网ECS绑定NAT EIP访问公网，其他VPC通过云企业网互联访问DMZ VPC实现外网访问。
    
-   仅DMZ VPC的NAT网关前部署一个NAT边界防火墙，在NAT边界防火墙上配置白名单机制的ACL访问控制策略，不允许访问未经授权的IP和域名。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8839137271/CAEQQRiBgICW24ms9xgiIGFmYmQ3ZTU5ZTRhNjRlMDA5NGU1ZjM4ZmRjOTEzNmQy4384339_20240415110232.292.svg)

### **场景三：单VPC内多个交换机的出向流量安全**

某大型跨国机构在云上单个VPC中，由于业务访问较为复杂，对外访问系统较多，需要针对不同的资产做安全防护，实现更精细化安全策略管理。

#### **部署方案**

-   业务VPC内基于不同交换机部署NAT网关，其中一个NAT网关绑定了多个EIP。在NAT网关上配置SNAT策略，实现私网ECS绑定NAT EIP访问公网。
    
-   每个NAT网关分别对应部署一个NAT边界防火墙，在NAT边界防火墙配置白名单机制的ACL访问控制策略，不允许访问未经授权的IP和域名。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8839137271/CAEQQRiBgICMv4qs9xgiIGQ3ZDJmMzFjODMzMTQ4MGJhMDFjNjljZDAyNTk0ZTJj4384339_20240415112507.346.svg)

## **部署指导**

## 步骤一：部署NAT网关

1.  登录[NAT网关管理控制台](https://vpc.console.aliyun.com/nat)，根据业务场景，为对应的VPC创建公网NAT网关。具体操作，请参见[创建公网NAT网关实例](https://help.aliyun.com/zh/nat-gateway/user-guide/use-internet-nat-gateway-for-public-network-access)。
    
2.  为创建的公网NAT网关绑定EIP。具体操作，请参见[创建和管理公网NAT网关实例](https://help.aliyun.com/zh/nat-gateway/user-guide/use-internet-nat-gateway-for-public-network-access#xref-25n-qj2-gvv)。
    
    **重要**
    
    公网NAT网关需要绑定EIP才能正常工作。
    
3.  为公网NAT网关创建SNAT条目，实现无公网IP的ECS实例访问互联网。具体操作，请参见[创建SNAT条目](https://help.aliyun.com/zh/nat-gateway/create-a-snat-entry)。
    
    云防火墙的NAT边界防火墙能力只支持NAT网关配置了SNAT条目，并且不存在DNAT条目。否则无法开启NAT边界防火墙。
    

## 步骤二：创建并开启NAT边界防火墙

#### 前提条件

-   已开通云防火墙服务，并且购买了足够数量的NAT边界防火墙授权数。具体操作，请参见[购买云防火墙服务](https://help.aliyun.com/zh/cloud-firewall/cloudfirewall/getting-started/purchase-cloud-firewall)。
    
-   已创建公网NAT网关，具体操作，请参见[创建和管理专有网络](https://help.aliyun.com/zh/vpc/create-and-manage-a-vpc)。
    
    **重要**
    
    目前，NAT边界防火墙仅支持防护公网NAT网关。
    
    NAT网关满足以下条件：
    
    -   NAT网关所在的地域支持开通NAT边界防火墙。NAT边界防火墙支持的地域，请参见[支持的地域](https://help.aliyun.com/zh/cloud-firewall/cloudfirewall/product-overview/supported-regions)。
        
    -   NAT网关已至少绑定1个EIP，并且NAT网关绑定的EIP不超过10个。相关内容，请参见[创建和管理公网NAT网关实例](https://help.aliyun.com/zh/nat-gateway/user-guide/use-internet-nat-gateway-for-public-network-access)。
        
    -   NAT网关已配置了SNAT条目，并且不存在DNAT条目。相关内容，请参见[创建和管理SNAT条目](https://help.aliyun.com/zh/nat-gateway/create-a-snat-entry#task-491135)。
        
        如果NAT网关存在DNAT条目，您需要先删除DNAT条目，才可以开启NAT边界防火墙。具体操作，请参见[创建和管理DNAT条目](https://help.aliyun.com/zh/nat-gateway/create-a-dnat-entry)。
        
    -   NAT网关所在的VPC已配置了0.0.0.0指向该NAT网关的路由条目。相关内容，请参见[创建和管理路由表](https://help.aliyun.com/zh/vpc/user-guide/create-and-manage-route-table)。
        
    -   NAT网关所在的VPC能够分配至少28位的子网段。
        

#### **操作步骤**

如果NAT网关没有同步到NAT边界防火墙资产列表中，您可以单击列表右上角**同步资产**进行手动同步，手动同步资产需要5~10分钟，请耐心等待。

1.  登录[云防火墙控制台](https://yundun.console.aliyun.com/?p=cfwnext)。，在左侧导航栏选择**防火墙开关**。
    
2.  单击**NAT边界防火墙**页签，在目标NAT网关的**操作**列单击。
    
3.  在**创建NAT边界防火墙**面板，创建并开启NAT边界防火墙信息。具体操作，请参见[NAT边界防火墙](https://help.aliyun.com/zh/cloud-firewall/cloudfirewall/user-guide/nat-firewalls)。
    
4.  创建完成后，需要定位到目标NAT网关，在**开关**列开启NAT边界防火墙开关。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5217153171/p791932.png)
    

## 步骤三：配置访问控制策略

1.  登录[云防火墙控制台](https://yundun.console.aliyun.com/?p=cfwnext)。
    
2.  在左侧导航栏，选择**防护配置** > ****访问控制**** > ****NAT边界****。
    
3.  在**NAT边界**页面，选择待配置的NAT网关，单击**创建策略**。
    
    云防火墙会自动同步您当前账号下关联的NAT网关，您可以单击下拉框选择待配置的NAT网关。
    
    ![image..png](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=)
    
4.  在**创建策略-NAT边界**面板，配置访问控制策略。单击**确定**。具体操作，请参见[配置NAT边界访问控制策略](https://help.aliyun.com/zh/cloud-firewall/cloudfirewall/user-guide/nat-firewall)。
    
    ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=)
    

## 步骤四：验证防护方案是否生效

1.  登录VPC的ECS实例，执行curl命令（例如curl www.*test*.com）模拟业务访问互联网。关于如何登录ECS实例，请参见[ECS远程连接方式概述](https://help.aliyun.com/zh/ecs/user-guide/connect-to-instance#concept-tmr-pgx-wdb)。
    
2.  登录[云防火墙控制台](https://yundun.console.aliyun.com/?p=cfwnext)。
    
3.  在左侧导航栏，选择**日志监控** > **日志审计**。
    
4.  在**流量日志** > **NAT边界**页签，源IP设置为ECS的私网IP，搜索流量日志，查看访问控制策略生效则表示NAT边界防火墙能够防护NAT网关出向流量。
    
    ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=)
    

## **运维指导**

### **异常流量分析**

### 步骤一：排查NAT边界是否存在超量流量

1.  登录[云防火墙控制台](https://yundun.console.aliyun.com/?p=cfwnext)。在左侧导航栏，单击总览。
    
2.  在**总览**页面，查看流量趋势，发现某个时间点存在异常流量峰值。
    
    **说明**
    
    超过购买的防护带宽时，趋势图上会显示已购NAT边界处理能力，方便您了解流量超过防护带宽多少。
    
    ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=)
    

如果排查有异常流量峰值，您需要查看私网外联资产明细，定位异常IP。具体步骤，请参见[步骤二](#8a00ed820eaw9)。

### 步骤二：根据私网外联资产明细，定位异常IP

1.  登录[云防火墙控制台](https://yundun.console.aliyun.com/?p=cfwnext)。
    
2.  在左侧导航栏，选择**流量分析** > **主动外联**。
    
3.  在**外联明细** > **私网外联资产**页签，根据访问流量进行排序，重点排查访问流量过大的资产IP，判定是否存在异常访问。
    
    ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=)
    

如果定位出异常IP，您需要结合日志审计数据做进一步判断。具体操作，请参见[步骤三](#aa4fedf221egb)。

## 步骤三：结合日志审计数据，判断异常流量是否符合业务需要

1.  登录[云防火墙控制台](https://yundun.console.aliyun.com/?p=cfwnext)。
    
2.  在左侧导航栏，选择**日志监控** > **日志审计**。
    
3.  在**流量日志** > **NAT边界**页签，源IP设置为ECS的私网IP，搜索流量日志，查看**源IP**、**源端口**和**目的端口**，判断异常流量是否符合业务需要。
    
    ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=)
    

### **运维建议**

如果您排查出异常流量峰值，且判定该流量确实是业务所需，可以参考如下建议进行运维：

-   **扩充云防火墙防护带宽**
    
    具体操作，请参见[续费说明](https://help.aliyun.com/zh/cloud-firewall/cloudfirewall/product-overview/renewal#task-2026254)。
    
-   **优化业务部署**
    
    例如，您的业务需要访问阿里云[OSS服务](https://help.aliyun.com/zh/oss/user-guide/regions-and-endpoints)或[SLS服务](https://help.aliyun.com/zh/sls/endpoints)时，建议您使用内网Endpoint访问，以节省公网流量带宽。
    
-   **为不需要防护的IP关闭云防火墙**
    
    具体操作，请参见[关闭NAT边界防火墙](https://help.aliyun.com/zh/cloud-firewall/cloudfirewall/user-guide/nat-firewalls#section-tj7-uj4-cjq)。