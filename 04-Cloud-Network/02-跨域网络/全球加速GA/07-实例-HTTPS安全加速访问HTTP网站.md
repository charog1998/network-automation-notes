您可以使用全球加速服务实现HTTPS安全加速访问HTTP网站，提升客户端访问HTTP网站的速度和安全性。

## 场景示例

本文以以下场景为例。某公司的总部在美国硅谷，总部有一台自建服务器，服务器上部署了HTTP网站，客户端主要分布在中国香港。该公司的网站服务面临以下挑战：

-   HTTP以明文方式传输数据，缺乏对网站验证的方法，导致网站系统面临极大的安全风险。
    
-   跨国公网不稳定，经常出现延迟、抖动、丢包等网络问题。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8837930871/CAEQSBiBgMC48uKFhBkiIDcxOTI2Yjg4ZTEwZTRmOTNiZmM5ZjI1MTU4YmM5NTU43963382_20230830144006.372.svg)

-   HTTP以明文方式传输数据，缺乏对网站验证的方法，导致网站系统面临极大的安全风险。
    
-   跨国公网不稳定，经常出现延迟、抖动、丢包等网络问题。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8837930871/CAEQSBiBgMC48uKFhBkiIDcxOTI2Yjg4ZTEwZTRmOTNiZmM5ZjI1MTU4YmM5NTU43963382_20230830144006.372.svg)

-   HTTP以明文方式传输数据，缺乏对网站验证的方法，导致网站系统面临极大的安全风险。
    
-   跨国公网不稳定，经常出现延迟、抖动、丢包等网络问题。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8837930871/CAEQSBiBgMC48uKFhBkiIDcxOTI2Yjg4ZTEwZTRmOTNiZmM5ZjI1MTU4YmM5NTU43963382_20230830144006.372.svg)

您可以部署全球加速服务，并配置HTTPS协议监听，加速中国香港用户访问美国硅谷地域的HTTP网站，同时对客户端的访问请求进行HTTPS加密，有效保障数据传输的安全性。

## 前提条件

-   您已经购买了SSL证书，并申请了该SSL证书。更多信息，请参见[证书选型与购买](https://help.aliyun.com/zh/ssl-certificate/purchase-an-ssl-certificate#task-q3j-zfp-ydb)和[提交证书申请](https://help.aliyun.com/zh/ssl-certificate/submit-a-certificate-application#concept-wxz-3xn-yfb)。
    
-   您的后端服务器已配置了HTTP 80服务。
    
-   您已为后端域名配置了DNS解析，即已配置了A记录将域名指向后端服务器的公网IP。
    

**说明**

本文操作以使用Nginx配置后端HTTP 80服务，并使用阿里云云解析 DNS（Alibaba Cloud DNS）[配置解析记录](https://help.aliyun.com/zh/dns/add-a-dns-record#topic-2035899)为例。如果您使用的DNS解析服务为非阿里云云解析DNS，请参见您的DNS服务商操作指导。

## 配置步骤

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8837930871/CAEQSBiBgMDt9.SFhBkiIGY0YmRhZDBhM2Y1YzRiZjc5MmQwYzcwMzhkZDUzMzBi3963382_20230830144006.372.svg)

**说明**

本文以按量付费的标准型全球加速实例为例，为您介绍如何配置全球加速服务实现HTTPS安全加速访问HTTP网站。创建按量付费的标准型全球加速实例前，请先了解以下信息：

-   按量付费GA实例采用**按流量**的带宽计费方式，无需绑定带宽包。接入全球加速网络产生的流量费用统一由云数据传输 CDT（Cloud Data Transfer）结算出账。更多信息，请参见[流量计费](https://help.aliyun.com/zh/ga/product-overview/pay-by-data-transfer#concept-2261223)。
    
-   首次使用按量付费GA实例，您需要在[服务开通](https://common-buy.aliyun.com/?commodityCode=ga_afterpay_public_cn)页面根据提示开通按量付费全球加速服务。
    

## **步骤一：配置实例基础信息**

1.  登录[全球加速管理控制](https://ga.console.aliyun.com/list)。
    
2.  在**实例列表**页面，单击**创建标准型按量付费实例**。
    
3.  在**实例基础配置**向导页面，根据以下信息进行配置，然后单击**下一步**。
    
    | **配置** | **说明** |
    | --- | --- |
    | **全球加速实例名称** | 输入全球加速实例名称。 |
    | **实例计费方式** | 默认为**按量付费**。 使用按量付费的标准型全球加速实例，产生的费用包括：实例费、性能容量单位CU费和流量费。 - 关于实例费、性能容量单位CU费的更多信息，请参见[按量付费全球加速实例计费](https://help.aliyun.com/zh/ga/product-overview/billing-of-pay-as-you-go-ga-instances)。 - 关于流量费，请参见[流量计费](https://help.aliyun.com/zh/ga/product-overview/pay-by-data-transfer)。 |
    | **资源组** | 选择标准型全球加速实例所属的资源组。 该资源组为当前阿里云账号在资源管理中创建的资源组。更多信息，请参见[创建资源组](https://help.aliyun.com/zh/resource-management/resource-group/user-guide/create-a-resource-group#task-xpl-kjm-4fb)。 |
    

## **步骤二：配置加速区域**

为全球加速实例配置加速区域，指定可以加速访问后端服务的用户所在的地域并为其分配加速带宽。

在**配置加速区域**向导页面，根据以下信息配置加速区域，然后单击**下一步**。

| **配置** | **说明** |
| --- | --- |
| **加速区域** | 在下拉列表中选中需要进行访问加速的一个地域或多个地域，然后单击**添加至列表**。 本文在**亚太**区域下选中**中国香港**地域。 |
| **分配带宽** |   |
| **带宽峰值** | 设置加速地域的带宽。每个加速地域支持分配的带宽范围为2~10000 Mbps。 此处带宽峰值仅作限速，产生的流量费用统一由CDT结算出账。 本文保持默认值**200** Mbps。 **重要** 如果带宽峰值设置过低，可能出现限速从而导致流量被丢弃，请合理规划带宽峰值，确保和业务需求匹配。 |
| **IP地址协议** | 选择接入全球加速服务的IP地址协议。 本文保持默认值**IPv4**。 |
| **公网质量类型** | 选择接入全球加速服务的公网质量类型。 本文选择**BGP(多线)**。 |

## 步骤三：配置监听

监听负责检查连接请求，根据您指定的端口和协议处理来自客户端的入站连接。每个监听都关联一个终端节点组，通过指定要分发流量的地域，将终端节点组与监听关联。关联后，全球加速会将流量分配到与监听关联的终端节点组内的最佳终端节点。

在**配置监听**配置向导页面，根据以下信息配置监听，然后单击**下一步**。

此处仅介绍本文强相关的配置项，其余配置项可保持默认配置。更多信息，请参见[添加和管理智能路由类型监听](https://help.aliyun.com/zh/ga/user-guide/add-and-manage-intelligent-routing-listeners#section-ncm-izu-muk)。

| **配置** | **说明** |
| --- | --- |
| **路由类型** | 选择路由类型。 本文选择**智能路由**。 |
| **协议** | 选择监听的协议类型。 本文选择**HTTPS**。 |
| **端口** | 指定用来接收请求并向终端节点进行转发的监听端口，端口取值范围：**1-65499**。 本文输入**443**。 |
| **选择服务器证书** | 选择您已经申请的服务器证书。 |

## 步骤四：配置终端节点组和终端节点

1.  在****配置终端节点组****配置向导页面，根据以下信息配置终端节点组和终端节点，然后单击**下一步**。
    
    此处仅介绍本文场景强相关配置项，关于终端节点配置项更多信息，请参见[添加和管理智能路由类型监听的终端节点组](https://help.aliyun.com/zh/ga/user-guide/create-and-manage-the-endpoint-groups-of-intelligent-routing-listeners)。
    
    | **配置** | **说明** |
    | --- | --- |
    | ****地域**** | 选择终端节点组所属的地域。 本文选择**美国（硅谷）**。 |
    | **终端节点配置** | 终端节点是客户端请求访问的目标主机。您可以根据以下信息配置终端节点： - **后端服务类型**：选择**自定义公网IP**。 - **后端服务**：输入要加速的后端服务的IP地址。 - **权重**：输入终端节点的权重，权重取值范围：0~255。全球加速根据您配置的权重按比例将流量路由到终端节点。 本文保持默认值**255**。 **警告** 如果某个终端节点的权重设置为0，全球加速将终止向该终端节点分发流量，请您谨慎操作。 |
    | **后端服务协议** | 选择后端服务器使用的服务协议。 本文保持默认配置为**HTTP**。 |
    | **端口映射** | 当您监听的端口和您终端节点提供服务的端口不相同时，您需要输入端口映射关系。 - **监听端口**：只能填写当前监听的端口。本文输入443。 - **终端节点端口**：您终端节点提供服务的端口。本文输入80。 |
    
2.  在**配置审核**向导页面，确认信息，然后单击**提交**。
    
    **说明**
    
    创建GA实例预计耗时3~5分钟，请您耐心等待。
    
3.  **可选：**创建任务完成后，在创建任务详情列表下方，单击**进入实例详情**，然后在实例详情页，可选择**实例信息**、**监听**、**加速区域**等页签查看实例配置信息。
    

## 步骤五：配置CNAME解析

您需要将要访问的域名通过DNS解析到全球加速的CNAME地址，访问请求才能转发到全球加速，实现加速效果。

1.  在[域名解析](https://dns.console.aliyun.com/?spm=a2c4g.11186623.0.0.9b0a5ad1tRuDNs#/dns/domainList)页面，找到目标自有域名，在**操作**列单击**解析设置**。
    
    **说明**
    
    对于非阿里云注册域名，需先[添加域名](https://help.aliyun.com/zh/dns/domain-management#topic-2035895)到云解析控制台，才可以进行域名解析设置。
    
2.  在解析设置页面，找到已有的A记录，在**操作**列单击**修改**。
    
3.  在**编辑记录**面板，选择**记录类型**为**CNAME**，并将**记录值**修改为全球加速实例分配的CNAME地址，然后单击**确定**。
    
    您可以在**实例列表**页面查看全球加速实例分配的CNAME地址。
    

**说明**

如果您需要根据客户端所属地域智能返回解析结果，需确保云解析DNS已升级至企业标准版或企业旗舰版。如何升级，请参见[续费](https://help.aliyun.com/zh/dns/renewal#section-pf7-cok-x5h)。

完成升级后，您可以修改已有A记录的默认解析线路为具体的地域解析线路，并添加CNAME记录指向全球加速实例分配的CNAME地址。

## 步骤六：访问测试

完成以下操作，测试客户端是否可以通过HTTPS方式访问部署在美国硅谷的HTTP网站，并实现访问加速。

**说明**

本教程以Alibaba Cloud Linux 3.2104 LTS 64位操作系统为例进行测试。不同类型的操作系统测试命令可能会有差异，具体测试命令请参见您操作系统的操作指南。

1.  检测CNAME配置是否生效。
    
    **方式1：DNS控制台一键检测**
    
    1.  在[域名解析](https://dns.console.aliyun.com/?spm=a2c4g.11186623.0.0.9b0a5ad1tRuDNs#/dns/domainList)页面，找到目标自有域名，在**操作**列单击**解析设置**。
        
    2.  在解析设置页面，找到已添加的CNAME解析记录，在**操作**列单击**生效检测**。
        
    3.  在**网络拨测工具**页面下方的**检测结果**区域，查看解析结果。
        
        当**解析结果**列显示为全球加速的CNAME值时，则表示CNAME配置已经生效。
        
    
    **方式2：手工验证**
    
    1.  在接入地域（本文为中国香港）的电脑中打开命令行窗口。
        
    2.  对域名执行以下命令。
        
        ```
        ping <网站域名>
        ```
        
        当返回的解析结果与全球加速的CNAME值一致，则表示CNAME配置已经生效。
        
        ```
        [root@xxx ~]# ping xxx.est.cloud
        PING ga-bp1xxx.com (8.218.xxx.xxx) 56(84) bytes of data.
        64 bytes from 8.218.xxx.xxx (8.218.xxx.xxx): icmp_seq=1 ttl=101 time=1.15 ms
        64 bytes from 8.218.xxx.xxx (8.218.xxx.xxx): icmp_seq=2 ttl=101 time=1.06 ms
        64 bytes from 8.218.xxx.xxx (8.218.xxx.xxx): icmp_seq=3 ttl=101 time=1.09 ms
        ^C
        --- ga-bp1xxx.com ping statistics ---
        3 packets transmitted, 3 received, 0% packet loss, time 2002ms
        rtt min/avg/max/mdev = 1.063/1.097/1.145/0.051 ms
        ```
        
    
2.  执行以下命令，测试客户端是否能通过HTTPS方式正常访问部署在美国硅谷的HTTP网站。
    
    ```
    curl https://<网站域名>
    ```
    
    图 1. 访问结果
    
    ```
    [root@xxx HKclient ~]# curl https://xxxst.cloud
    &lt;!DOCTYPE html&gt;
    <html>
    <head>
    <title>HTTP Server Test Page</title>
    <style>
        body {
                width: 35em;
                margin: 0 auto;
                font-family: Tahoma, Verdana, Arial, sans-serif;
            }
    </style>
    </head>
    <body>
    <h1>Welcome to HTTP Server Test Page!</h1>
    <p>This is ECS1.</p>
    </body>
    </html>
    ```
    
3.  如需测试加速效果，请参见[测试GA的加速效果](https://help.aliyun.com/zh/ga/use-cases/use-the-network-dial-test-tool-to-test-the-acceleration)。