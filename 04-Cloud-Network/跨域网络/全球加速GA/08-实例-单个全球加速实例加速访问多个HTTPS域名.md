通过在一个全球加速实例上配置多个证书，可实现同时加速访问多个HTTPS域名。

## 场景示例

本文以以下场景为例。某公司的总部在美国硅谷，总部在阿里云上创建了两台服务器，两台服务器均部署了Web服务，并通过不同的域名对外提供服务。客户端主要分布在中国香港地域，该公司的Web服务面临以下挑战：

-   公网传输不稳定，经常出现延迟、抖动、丢包等网络问题。
    
-   多台服务器通过不同的域名对外提供服务，为网站配置加速服务时，一般需要分别为每个域名进行加速，成本较高。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6746740871/CAEQQRiBgMDQ2JGa9hgiIDI0ZGQxNzQyYTg0MjQ3NDZhYWFjMmZiMDJiYzViYzhh3963382_20230830144006.372.svg)

为解决上述问题，该公司计划部署全球加速服务，并配置HTTPS协议监听。HTTPS协议监听可以通过以下功能实现同时加速多个HTTPS域名访问：

-   支持绑定多个证书，可以将多个域名关联到同一个HTTPS协议监听上。
    
-   支持配置基于域名的转发策略，通过匹配不同的域名访问请求，将访问请求转发至后端相应的服务器。
    
-   支持对客户端的访问请求进行数据加密，能有效保障数据传输的安全性。
    

当前该公司Web服务器的服务信息以及该公司使用全球加速服务后对客户端访问请求的转发规划如下：

| **配置规划** | **访问域名1**`***xxx*****test.cloud**` | **访问域名2**`***xxx*****test.fun**` |
| --- | --- | --- |
| 监听协议 | HTTPS |   |
| 监听端口 | 443 |   |
| 对应证书 | 默认证书A | 扩展证书B |
| 对应转发策略 | 默认转发策略 | 自定义转发策略 |
| 对应终端节点组 | 默认终端节点组 | 虚拟终端节点组 |
| 对应服务器 | 服务器1 | 服务器2 |
| 服务器服务协议 | HTTP | HTTPS |
| 服务器服务端口 | 80  | 443 |
| 服务器公网IP | 47.XX.XX.62 | 47.XX.XX.34 |

**说明**

全球加速中配置的证书用于加密从客户端至全球加速阶段的数据。从全球加速至后端服务器阶段的数据加密通过后端服务器安装的证书实现。全球加速中配置的证书可以与后端服务器安装的证书相同。

## 前提条件

-   您已经购买并申请了SSL证书。具体操作，请参见[证书选型与购买](https://help.aliyun.com/zh/ssl-certificate/purchase-an-ssl-certificate#task-q3j-zfp-ydb)和[提交证书申请](https://help.aliyun.com/zh/ssl-certificate/submit-a-certificate-application#concept-wxz-3xn-yfb)。
    
-   您已将证书文件上传至后端服务器。具体操作，请参见[通过云助手上传文件到ECS实例](https://help.aliyun.com/zh/ecs/user-guide/upload-files-to-ecs-instances#topic-1950448)。
    
-   您的后端服务器1和服务器2已分别配置了HTTP 80和HTTPS 443服务。
    
-   您已分别为域名1`*xxx*test.cloud`和域名2`*xxx*test.fun`配置了DNS解析，即已配置了A记录将域名指向后端服务器的公网IP。
    

**说明**

本文使用Nginx配置后端HTTP 80和HTTPS 443服务，并使用阿里云云解析 DNS（Alibaba Cloud DNS）[配置解析记录](https://help.aliyun.com/zh/dns/add-a-dns-record#topic-2035899)为例。如果您使用的DNS解析服务为非阿里云云解析DNS，请参见您的DNS服务商操作指导。

## 配置步骤

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6746740871/CAEQQRiBgMD6x5Oa9hgiIDA1NDZmYjIzMDg3NzRiOWQ5NjViZDNiY2YzYTlkYzg54210981_20240213143608.814.svg)

**说明**

本文以按量付费的标准型全球加速实例为例，为您介绍如何配置全球加速服务加速访问多个HTTPS域名。创建按量付费的标准型全球加速实例前，请先了解以下信息：

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

在**配置监听**配置向导页面，配置监听，然后单击**下一步**。

| **配置** | **说明** |
| --- | --- |
| **监听名称** | 输入监听的名称。 |
| **路由类型** | 选择路由类型。 本文选择**智能路由**。 |
| **协议** | 选择监听的协议类型。 本文选择**HTTPS**。 |
| **端口** | 指定用来接收请求并向终端节点进行转发的监听端口，端口取值范围：**1-65499**。 本文输入**443**。 |
| **选择服务器证书** | 选择您已经申请的服务器证书。 本文选择您已申请的证书A。 |
| **TLS安全策略** | 选择您业务所需的TLS安全策略。 TLS安全策略包含HTTPS可选的TLS协议版本和配套的加密算法套件。关于TLS安全策略，请参见[TLS安全策略](https://help.aliyun.com/zh/ga/user-guide/tls-security-policies#concept-2130168)。 本文不作配置时，默认选择**tls\\_cipher\\_policy\\_1\\_0**。 |
| **客户端亲和性** | 选择是否保持客户端亲和性。保持客户端亲和性，即客户端访问有状态的应用程序时，可以将来自同一客户端的所有请求都定向到同一终端节点。 本文选择**源 IP**。 |
| **附加HTTP头字段** | 选中所需的附加HTTP头字段。 本文保持默认配置。 **单击查看附加HTTP头字段信息。** - 通过`GA-ID`头字段获取全球加速实例ID。 - 通过`GA-AP`头字段获取GA加速地域的信息。 - 通过`GA-X-Forwarded-Proto`头字段获取GA实例的监听协议。 - 通过`GA-X-Forwarded-Port`头字段获取GA实例的监听端口。 - 通过`X-Real-IP`头字段获取真实的客户端IP。 |

## 步骤四：配置终端节点组和终端节点

1.  在****配置终端节点组****配置向导页面，配置终端节点组和终端节点，然后单击**下一步**。
    
    此处仅介绍本文场景强相关配置项，关于终端节点配置项更多信息，请参见[添加和管理智能路由类型监听的终端节点组](https://help.aliyun.com/zh/ga/user-guide/create-and-manage-the-endpoint-groups-of-intelligent-routing-listeners)。
    
    | **配置** | **说明** |
    | --- | --- |
    | ****地域**** | 选择终端节点组所属的地域。 本文选择**美国（硅谷）**。 |
    | **终端节点配置** | 终端节点是客户端请求访问的目标主机。您可以根据以下信息配置终端节点： - **后端服务类型**：选择**阿里云公网 IP**。 - **后端服务**：输入要加速的后端服务的IP地址。本文输入服务器1的公网IP地址47.XX.XX.62。 - **权重**：输入终端节点的权重，权重取值范围：0~255。全球加速根据您配置的权重按比例将流量路由到终端节点。 本文保持默认值**255**。 **警告** 如果某个终端节点的权重设置为0，全球加速将终止向该终端节点分发流量，请您谨慎操作。 |
    | **保持客户端源IP** | 默认开启保持客户端源IP功能，支持后端服务查看客户端源IP地址。HTTP监听将从HTTP的x-forward-for字段读取客户端源IP地址。更多信息，请参见[保持客户端源IP](https://help.aliyun.com/zh/ga/user-guide/preserve-client-ip-addresses#task-2416386)。 |
    | **后端服务协议** | 选择后端服务器使用的服务协议。 默认配置为**HTTP**。 |
    | **端口映射** | 当您监听的端口和您终端节点提供服务的端口不相同时，您需要输入端口映射关系。 - **监听端口**：只能填写当前监听的端口。本文输入443。 - **终端节点端口**：您终端节点提供服务的端口。本文输入80。 |
    | **流量调配** | 配置到不同终端节点组的流量比例。 取值范围：0~100。 本文保持默认值**100**%。 |
    | **健康检查** | 开启或关闭健康检查。 开启后，可以通过健康检查来判断终端节点的运行状态。关于健康检查更多信息，请参见[开启和管理健康检查](https://help.aliyun.com/zh/ga/user-guide/enable-and-manage-health-checks#task-2382619)。 本文保持默认关闭状态。 |
    
2.  在**配置审核**向导页面，确认信息，然后单击**提交**。
    
    **说明**
    
    创建GA实例预计耗时3~5分钟，请您耐心等待。
    
3.  **可选：**创建任务完成后，在创建任务详情列表下方，单击**进入实例详情**，然后在实例详情页，可选择**实例信息**、**监听**、**加速区域**等页签查看实例配置信息。
    
4.  配置虚拟终端节点组。
    
    1.  在实例详情页面，单击**监听**页签。
        
    2.  在**监听**页签，找到目标监听，在**默认终端节点组**列单击终端节点组ID。
        
    3.  在**终端节点组**页签下的**虚拟终端节点组**区域，单击**添加虚拟终端节点组**。
        
    4.  在**添加终端节点组**页面，根据以下信息进行配置，然后单击**创建**。
        
        此处配置除以下列出的参数外，其余参数与上文默认终端节点组配置一致。
        
        -   **后端服务类型**：选择**阿里云公网 IP**。
            
        -   **后端服务**：输入服务器2的公网IP地址47.XX.XX.34。
            
        -   **后端服务协议**：选择**HTTPS**。
            
        -   **端口映射**：无需配置端口映射关系。
            
            如果您监听的端口和您终端节点提供服务的端口相同，您无需填写端口映射关系，全球加速自动将访问请求发送至终端节点的监听端口。
            
        

## 步骤五：绑定扩展证书

为HTTPS监听绑定扩展证书，可以将多个域名关联到同一个HTTPS协议监听上。配合基于域名的转发策略可以将不同域名的访问请求转发至不同的虚拟终端节点组。

以下步骤通过为HTTPS监听绑定证书B，将域名2`*xxx*test.fun`与HTTPS监听关联。

1.  在**监听**页签下，找到目标HTTPS协议监听，单击监听ID。
    
2.  在监听详情页面下，单击**证书管理**页签。
    
3.  在**证书管理**页签下的**扩展证书**区域，单击**绑定证书**。
    
4.  在**绑定证书**对话框，根据以下信息配置扩展证书，然后单击**确定**。
    
    -   **证书**：选择需要绑定的证书。本文选择证书B。
        
    -   **关联域名**：选择该证书下需要使用全球加速服务加速访问的域名。本文选择域名2`*xxx*test.fun`。
        
    

## 步骤六：添加转发策略

HTTPS协议监听接收到访问请求后，会优先匹配自定义转发策略，在满足匹配条件后，HTTPS协议监听将访问请求转发至对应终端节点组中。如果访问请求未匹配到任何自定义转发策略，将会直接通过默认转发策略被转发至默认终端节点组中。

以下步骤为服务器2对应的虚拟终端节点组创建自定义转发策略，将访问域名2`*xxx*test.fun`的所有请求转发至服务器2。

1.  在**监听**页签下，找到目标HTTPS协议监听，单击监听ID。
    
2.  在监听详情页面，单击**转发策略**页签。
    
3.  在**转发策略**页签下，单击**插入新策略**。
    
4.  在**插入新策略**区域，根据以下信息配置转发策略，并单击**确定**。
    
    | **参数** | **说明** |
    | --- | --- |
    | **策略名称** | 输入转发策略的名称。 |
    | **转发条件** | 配置转发条件。 本文选择**域名**，并输入要匹配的域名2*xxx*test.fun。 |
    | **那么转发动作是** | 选择转发动作类型及转发目标。 本文选择**转发至**，并选择[步骤四：配置终端节点组和终端节点](#127509c043h17)已创建的虚拟终端节点组。 |
    

## 步骤七：配置CNAME解析

您需要将要加速的域名1`*xxx*test.cloud`和域名2`*xxx*test.fun`通过DNS解析到全球加速的CNAME地址，访问请求才能转发到全球加速，实现加速效果。

1.  在[域名解析](https://dns.console.aliyun.com/?spm=a2c4g.11186623.0.0.9b0a5ad1tRuDNs#/dns/domainList)页面，找到目标自有域名1`*xxx*test.cloud`，在**操作**列单击**解析设置**。
    
    **说明**
    
    对于非阿里云注册域名，需先[添加域名](https://help.aliyun.com/zh/dns/domain-management#topic-2035895)到云解析控制台，才可以进行域名解析设置。
    
2.  在解析设置页面，找到已有的A记录，在**操作**列单击**修改**。
    
3.  在**编辑记录**面板，选择**记录类型**为**CNAME**，并将**记录值**修改为全球加速实例分配的CNAME地址，然后单击**确认**。
    
    您可以在**实例列表**页面查看全球加速实例分配的CNAME地址。
    
4.  参考上述步骤，为域名2`*xxx*test.fun`修改已有A记录为CNAME记录。
    

**说明**

如果您需要根据客户端所属地域智能返回解析结果，需确保云解析DNS已升级至企业标准版或企业旗舰版。如何升级，请参见[续费](https://help.aliyun.com/zh/dns/renewal#section-pf7-cok-x5h)。

完成升级后，您可以修改已有A记录的默认解析线路为具体的地域解析线路，并添加CNAME记录指向全球加速实例分配的CNAME地址。

## 步骤八：访问测试

测试客户端是否可以通过不同域名访问部署在美国硅谷的Web服务，并实现访问加速。

**说明**

-   本文以阿里云Alibaba Cloud Linux 3操作系统为例进行测试。不同类型的操作系统测试命令可能会有差异，具体测试命令请参见您操作系统的操作指南。
    
-   使用全球加速服务后的加速效果以您的实际业务测试为准。
    

### **测试网站连通性**

1.  在接入地域（本文为中国香港）的电脑中打开命令行窗口。
    
2.  对域名1`*xxx*test.cloud`和域名2`*xxx*test.fun`分别执行以下命令，验证CNAME配置是否生效。
    
    ```
    ping ＜网站域名＞
    ```
    
    当返回的解析结果与全球加速的CNAME值一致，则表示CNAME配置已经生效。
    
    ```
    [root@iZjxxx ~]# ping xxx_test.cloud
    PING ga-bp1xxx9.com (8.217.xxx.xxx) 56(84) bytes of data.
    64 bytes from 8.217.xxx.xxx (8.217.xxx.xxx): icmp_seq=1 ttl=101 time=1.59 ms
    64 bytes from 8.217.xxx.xxx (8.217.xxx.xxx): icmp_seq=2 ttl=101 time=1.59 ms
    64 bytes from 8.217.xxx.xxx (8.217.xxx.xxx): icmp_seq=3 ttl=101 time=1.60 ms
    ^C
    --- ga-bp1xxx9.com ping statistics ---
    3 packets transmitted, 3 received, 0% packet loss, time 2002ms
    rtt min/avg/max/mdev = 1.593/1.595/1.598/0.002 ms
    [root@iZjxxx ~]# ping xxx_test.fun
    PING ga-bp1xxx.com (8.217.xxx.xxx) 56(84) bytes of data.
    64 bytes from 8.217.xxx.xxx (8.217.xxx.xxx): icmp_seq=1 ttl=96 time=1.58 ms
    64 bytes from 8.217.xxx.xxx (8.217.xxx.xxx): icmp_seq=2 ttl=96 time=1.53 ms
    64 bytes from 8.217.xxx.xxx (8.217.xxx.xxx): icmp_seq=3 ttl=96 time=1.51 ms
    ^C
    --- ga-bp1xxx9.com ping statistics ---
    3 packets transmitted, 3 received, 0% packet loss, time 2002ms
    rtt min/avg/max/mdev = 1.508/1.539/1.576/0.042 ms
    ```
    
3.  对域名1`*xxx*test.cloud`和域名2`*xxx*test.fun`分别执行以下命令，测试网站是否连通及证书是否获取正常。
    
    ```
    curl -v https://<网站域名> --resolve <网站域名>:<监听端口>:<加速IP>
    ```
    
    此处以域名1`*xxx*test.cloud`测试结果为例。当返回结果包含对应的证书信息及响应信息，则表示网站服务正常。
    
    ```
    [root@iZxxx]# curl -v https://xxx_test.cloud --resolve xxx_test.cloud:443:8.217.xxx
    * Added xxx_test.cloud:443:8.217.xxx to DNS cache
    * Rebuilt URL to: https://xxx_test.cloud/
    * Hostname xxx_test.cloud was found in DNS cache
    *   Trying 8.217.xxx...
    * TCP_NODELAY set
    * Connected to xxx_test.cloud (8.217.xxx) port 443 (#0)
    * ALPN, offering h2
    * ALPN, offering http/1.1
    * successfully set certificate verify locations:
    *   CAfile: /etc/pki/tls/certs/ca-bundle.crt
      CApath: none
    * TLSv1.3 (OUT), TLS handshake, Client hello (1):
    * TLSv1.3 (IN), TLS handshake, Server hello (2):
    * TLSv1.2 (IN), TLS handshake, Certificate (11):
    * TLSv1.2 (IN), TLS handshake, Server key exchange (12):
    * TLSv1.2 (IN), TLS handshake, Server finished (14):
    * TLSv1.2 (OUT), TLS handshake, Client key exchange (16):
    * TLSv1.2 (OUT), TLS change cipher, Change cipher spec (1):
    * TLSv1.2 (OUT), TLS handshake, Finished (20):
    * TLSv1.2 (IN), TLS handshake, Finished (20):
    * SSL connection using TLSv1.2 / ECDHE-RSA-AES128-GCM-SHA256
    * ALPN, server accepted to use h2
    * Server certificate:
    *  subject: CN=xxx_test.cloud
    *  start date: Mar  1 00:00:00 2024 GMT
    *  expire date: Mar 31 23:59:59 2025 GMT
    *  subjectAltName: host "xxx_test.cloud" matched cert's "xxx_test.cloud"
    *  issuer: C = US; O = DigiCert Inc; CN = DigiCert Global G2 TLS RSA SHA256 2020 CA1
    *  SSL certificate verify ok.
    * Using HTTP2, server supports multi-use
    * Connection state changed (HTTP/2 confirmed)
    > GET / HTTP/2
    > Host: xxx_test.cloud
    > User-Agent: curl/7.61.1
    > Accept: */*
    > 
    < HTTP/2 200 
    < content-type: text/html; charset=utf-8
    < 
    * Connection #0 to host xxx_test.cloud left intact
    *  subject: CN=xxx_test.cloud
    *  start date: Sep 13 00:00:00 2023 GMT
    *  expire date: Sep 12 23:59:59 2024 GMT
    *  subjectAltName: host "xxx_test.cloud" matched cert's "xxx_test.cloud"
    *  issuer: C=US; O=DigiCert Inc; OU=www.digicert.com; CN=Encryption Everywhere DV TLS CA - G2
    *  SSL certificate verify ok.
    * Using HTTP2, server supports multi-use
    * Connection state changed (HTTP/2 confirmed)
    * Copying HTTP/2 data in stream buffer to connection buffer after upgrade: len=0
    * Using Stream ID: 1 (easy handle 0x55d6e15b76b0)
    > GET / HTTP/2
    > Host: xxx_test.cloud
    > User-Agent: curl/7.61.1
    > Accept: */*
    > 
    * Connection state changed (MAX_CONCURRENT_STREAMS == 128)!
    &lt; HTTP/2 200
    &lt; date: Thu, 14 Sep 2023 09:00:09 GMT
    &lt; content-type: text/html
    &lt; content-length: 299
    &lt; last-modified: Mon, 11 Sep 2023 10:27:09 GMT
    &lt; etag: &quot;64feeb7d-12b&quot;
    &lt; accept-ranges: bytes
    &lt; 
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
    <p>This is ECS01.</p>
    </body>
    </html>
    * Connection #0 to host xxx_test.cloud left intact
    ```
    

### **测试加速效果**

如需测试加速效果，请参见[测试GA的加速效果](https://help.aliyun.com/zh/ga/use-cases/use-the-network-dial-test-tool-to-test-the-acceleration)。