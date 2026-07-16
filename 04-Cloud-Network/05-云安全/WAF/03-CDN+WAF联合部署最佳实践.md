本方案旨在通过Web应用防火墙（Web Application Firewall，简称WAF）为已接入内容分发网络（CDN）的域名提供安全防护。通过在CDN回源链路上部署WAF，实现对HTTP/HTTPS流量的实时检测与清洗，确保仅正常业务流量到达源站，有效抵御Web攻击。

## **适用范围**

-   **适用架构**：本文适用于“CDN+ECS”的动静混合架构，旨在确保静态资源继续由CDN加速的同时，由WAF专注于保护动态资源。若业务采用“CDN+OSS”纯静态托管架构，因OSS仅存储静态文件且不存在应用层攻击风险，接入WAF提供的防护有限，反而会增加回源链路与访问延迟，故不建议接入。
    
-   **操作前提**：目标域名已接入阿里云 CDN、DCDN 或其他厂商的 CDN 服务。
    
-   **操作说明**：本文以阿里云 CDN 为例阐述操作步骤，其逻辑同样适用于 DCDN 或其他厂商的 CDN 服务，操作时请参照执行。
    
-   **业务影响**：建议在业务低峰期执行本文操作，以最小化对业务的影响。
    

## **选择合适的接入方式**

WAF支持与其他云产品协同部署以构建纵深防御体系。在未接入WAF的架构中，用户请求经DNS解析至CDN节点后直接回源，导致攻击流量与正常业务流量直达源站服务器。

WAF提供CNAME接入与云产品接入两种模式，具体对比如下。请结合业务架构特性，选择适配的接入方案。

| **对比项** | **云产品接入** | **CNAME接入** |
| --- | --- | --- |
| 方案优势 | 无需调整CDN回源配置，对业务影响较小，适用于快速接入场景。 | 适用场景广泛，功能限制较少，支持跨账号及跨云部署。 |
| 接入对象 | 阿里云云产品实例。 | 域名。 |
| 使用限制 | - **账号限制**：未配置**多账号统一管理**时仅限接入本账号的云产品实例。 - **地域限制**：部分地域的云产品实例不支持接入。 - **协议限制**：不支持接入IPv6类型的ECS、CLB、NLB实例。 - **产品限制**：不支持接入OSS。 | 配置稍复杂，需配置CDN回源、获取真实客户端IP等。 |

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0469360871/CAEQbxiBgMD2i9O77BkiIDcyNGE5NWZkN2RiMDQ3YzA5M2M4ZjlmYzE4MjBiODQx3963382_20230830144006.372.svg)

如需了解更多的接入方式对比与原理介绍，请参见[接入概述](https://help.aliyun.com/zh/waf/web-application-firewall-3-0/user-guide/overview-8)。

## **操作步骤**

1.  **开通WAF（仅限WAF未开通时）**：若尚未开通WAF服务，请访问[Web应用防火墙3.0（按量付费）购买页](https://common-buy.aliyun.com/?commodityCode=waf_v2_public_cn)，初次使用建议选择**付费模式**为**按量付费**。具体购买流程，请参见[开通WAF 3.0按量付费实例](https://help.aliyun.com/zh/waf/web-application-firewall-3-0/user-guide/purchase-a-pay-as-you-go-waf-3-0-instance)。
    
2.  **前往WAF控制台**：登录[Web应用防火墙控制台](https://yundun.console.aliyun.com/?p=waf)，在顶部菜单栏，选择WAF实例的资源组和地域（**中国内地**、**非中国内地**），然后在左侧导航栏，单击**接入管理**。
    
3.  **接入资产**：从CNAME接入或云产品接入中选择**一种**方式完成资产接入。
    
    **说明**
    
    以下操作需参考CDN已配置的信息。为确保配置准确，请先前往CDN控制台确认域名、回源等相关配置后再继续操作。
    
    ## CNAME接入
    
    1.  在**CNAME接入**页签，单击**接入**。在**配置监听**页面，需要关注以下配置。
        
        | **配置项** | **说明** |
        | --- | --- |
        | **域名** | 填写已接入CDN的域名，仅支持填写一个需防护的域名，包括精确域名（如`www.aliyundoc.com`）或通配符域名（如`*.aliyundoc.com`）。 |
        | **协议类型****与端口** | 请根据CDN已配置的[回源协议与回源端口](https://help.aliyun.com/zh/cdn/user-guide/configure-the-origin-protocol-policy)进行选择： - **协议选择**：需与CDN回源协议保持一致。 - **端口选择**：需与CDN回源端口保持一致。 默认情况下，当CDN回源端口配置为443时，使用HTTPS协议回源；其余端口则使用HTTP协议回源。 若使用HTTPS协议，需上传与域名匹配的证书文件。若该证书此前已上传至本账号的**数字证书管理服务**，可直接选择已有证书进行配置。 |
        | **WAF前是否有七层代理（高防/CDN等）** | 由于业务前置了CDN，必须在此处选择**是**。若配置错误，WAF将无法获取真实客户端IP，导致报表数据将所有请求来源显示为CDN节点。 - **客户端IP判定方式**选择**【推荐】取指定Header字段中的第一个IP作为客户端源IP，避免XFF伪造**。 - **指定Header字段**填写 `ali-cdn-real-ip`。这是阿里云CDN回源请求中默认携带的、用于存储真实客户端IP的HTTP请求头。 **说明** 阿里云CDN回源请求中用于存储真实客户端IP的字段为 `ali-cdn-real-ip`。 若使用其他CDN产品，请查阅其官方文档以确认对应的字段名称。此外，也可以通过配置CDN增加自定义出站请求头，来使用自定义的回源字段。 |
        
    2.  单击**下一步**，进入**配置转发**页面，填写**服务器地址**后，单击**提交**。
        
        此处的服务器地址应与CDN控制台填写的源站地址一致。
        
    3.  在**接入完成**页，单击**复制CNAME**。
        
    4.  前往[CDN控制台](https://cdn.console.aliyun.com)。单击**域名管理**，定位至接入WAF的域名，单击**操作**列的**管理**。在**源站信息**区域，单击**操作**列的**编辑**，将**源站信息**修改为上一步复制的CNAME地址。此操作将CDN回源路径指向WAF。
        
    
    **重要**
    
    当存在以下场景时，还需执行相应的额外配置：
    
    -   **CDN回源HOST配置**：若已配置[默认回源HOST](https://help.aliyun.com/zh/cdn/user-guide/configure-the-default-origin-host)，需同步进行修改，将CDN回源路径指向WAF。
        
    -   **静态文件绕过WAF**：为减少性能损耗，若需使客户端对静态文件的请求绕过WAF，需[配置CDN条件源站](https://help.aliyun.com/zh/cdn/user-guide/configure-a-conditional-origin)或将相关资源加入[WAF白名单](https://help.aliyun.com/zh/waf/web-application-firewall-3-0/user-guide/configure-whitelist-rules-to-allow-specific-requests)。
        
    -   **源站记录真实客户端IP**：若需在源站服务器（如Nginx的 access.log）记录真实客户端IP，需配置源站以提取真实IP字段。详细信息，请参见[获取客户端真实 IP](https://help.aliyun.com/zh/waf/web-application-firewall-3-0/user-guide/obtain-the-real-ip-address-of-the-visitor)。
        
    -   **CNAME接入高级功能**：WAF的CNAME接入方式支持HTTPS、IPv6、回源负载均衡及高可用等高级功能。如需自定义相关配置，请参见[通过CNAME接入为网站开启WAF防护](https://help.aliyun.com/zh/waf/web-application-firewall-3-0/user-guide/add-a-domain-name-to-waf-in-cname-record-mode)。
        
    
    ## 云产品接入
    
    1.  在**云产品接入**页签，选择需接入的云产品类型，以ECS实例为例，单击**云服务器 ECS**，然后定位至目标实例，单击其**操作**列的**立即接入**。
        
        **说明**
        
        若接入其他云产品，请参照以下配置项，并依据对应的[云产品接入](https://help.aliyun.com/zh/waf/web-application-firewall-3-0/user-guide/cloud-native-mode/)文档完成配置。
        
    2.  在弹出的**立即接入**页面，单击**操作**列的**添加端口**，根据CDN已配置的[回源协议与回源端口](https://help.aliyun.com/zh/cdn/user-guide/configure-the-origin-protocol-policy)进行选择：
        
        -   **协议选择**：需与CDN回源协议保持一致。
            
        -   **端口选择**：需与CDN回源端口保持一致。
            
        
        默认情况下，当CDN回源端口配置为443时，使用HTTPS协议回源；其余端口则使用HTTP协议回源。
        
        若使用HTTPS协议，需上传与域名匹配的证书文件。若该证书此前已上传至本账号的**数字证书管理服务**，可直接选择已有证书进行配置。配置完成后单击**确定**。
        
    3.  返回**立即接入**页面，由于业务前置了CDN，必须在**WAF前是否有七层代理（高防/CDN等）**区域，选择**是**。若配置错误，WAF将无法获取真实客户端IP，导致报表数据将所有请求来源显示为CDN节点。
        
        -   **客户端IP判定方式**选择**【推荐】取指定Header字段中的第一个IP作为客户端源IP，避免XFF伪造**。
            
        -   **指定Header字段**填写 `ali-cdn-real-ip`。这是阿里云CDN回源请求中默认携带的、用于存储真实客户端IP的HTTP请求头。
            
        
        **说明**
        
        阿里云CDN回源请求中用于存储真实客户端IP的字段为 `ali-cdn-real-ip`。
        
        若使用其他CDN产品，请查阅其官方文档以确认对应的字段名称。此外，也可以通过配置CDN增加自定义出站请求头，来使用自定义的回源字段。
        
    4.  单击**确定**完成接入。
        
        **说明**
        
        为减少性能损耗，若需使客户端对静态文件的请求绕过WAF，还需[配置CDN条件源站](https://help.aliyun.com/zh/cdn/user-guide/configure-a-conditional-origin)或将相关资源加入[WAF白名单](https://help.aliyun.com/zh/waf/web-application-firewall-3-0/user-guide/configure-whitelist-rules-to-allow-specific-requests)。
        
    
4.  **验证测试**：在浏览器输入接入的网站域名，测试CDN与WAF接入是否成功。
    
    1.  在域名后输入Web攻击代码（例如`<被防护域名>/alert(xss)`，`alert(xss)`为用作测试的跨站脚本攻击代码），如果返回405拦截提示页面，表示攻击被拦截，WAF防护成功。
        
    2.  按**F12**打开浏览器开发者工具，刷新页面后切换至**Network**页签。单击目标静态资源，在**Headers**页签中定位至**X-Cache**字段，若显示**hit**而非**miss**，即表示命中缓存，CDN加速生效。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6705149771/p1070955.png)
        
5.  **配置WAF自定义防护规则**：WAF为接入的对象默认启用一系列防护规则，适用于日常防护场景，可以在**防护配置** > **防护对象**页面查看。当默认规则无法满足业务需求时（例如需将具备特定特征的请求加入白名单予以放行），可新建或修改防护规则。更多信息，请参见[防护配置概述](https://help.aliyun.com/zh/waf/web-application-firewall-3-0/user-guide/protection-configuration-overview)。
    

## **常见问题**

### **CNAME接入后，WAF控制台显示“****DNS解析未知，****域名启用了代理**”怎么办？

使用CNAME接入方式时，控制台出现此提示属于正常现象。这是因为域名的DNS解析直接指向了CDN，导致WAF无法直接获取解析状态，无需关注此提示。

如需确认接入是否成功，请参照前文提到的验证测试步骤进行实际测试即可。

### **接入WAF完成后，是否需要刷新CDN缓存？**

通常无需刷新CDN缓存。但在特定配置变更下，需手动执行刷新操作。具体说明如下：

1.  **无需刷新的情况**
    
    仅完成WAF接入配置，未对源站内容进行任何变更。由于源站静态资源未发生改变，CDN节点现有缓存依然有效。
    
2.  **需要刷新的情况**
    
    存在以下任一情况时，需手动刷新CDN缓存以确保配置生效：
    
    -   修改了源站的静态资源文件。
        
    -   调整了与缓存策略相关的HTTP响应头。
        
    -   启用了WAF的Bot管理功能，并配置了自动集成Web SDK。
        

### **接入完成后访问网站提示重定向的次数过多怎么办？**

通常是因为源站服务器配置了 HTTP 强制跳转 HTTPS 的规则，导致流量在 WAF/CDN 与源站之间形成了死循环。

需要在源站服务器的前一跳设备上，将回源协议配置为 HTTPS。根据采用的接入方式，具体配置位置如下：

-   **CNAME 接入**：前一跳设备为 WAF。
    
-   **云产品接入**：前一跳设备为 CDN。
    

更多信息，请参见[重定向次数过多的解决方案](https://help.aliyun.com/zh/cdn/support/too-many-redirects-occur-after-my-domain-name-is-accelerated-by-alibaba-cloud-cdn)。

### ESA控制台提供的WAF防护功能与本文的WAF有什么区别？

-   **计费方式区别**：ESA的WAF防护功能已深度集成，其产生的费用统一由ESA产品进行[计费](https://help.aliyun.com/zh/edge-security-acceleration/esa/user-guide/waf-overview/#ec8fdacb8bks6)；而本文介绍的WAF为独立云产品，需单独开通并按其自身的[计费方式](https://help.aliyun.com/zh/waf/web-application-firewall-3-0/billing-methods/)进行结算。
    
-   **功能区别**：ESA内置的WAF功能主要适配边缘安全加速场景，满足常见的网站防护需求；而本文介绍的WAF产品功能更为全面，不仅涵盖ESA WAF的所有能力，还提供覆盖全业务场景的防护规则。
    

### CDN引入WAF后是否需要修改域名DNS解析？

不需要修改域名DNS解析。无论采用云产品接入还是CNAME接入方式，客户端请求均先到达CDN节点，因此无需更改域名的DNS解析记录。但需注意以下配置调整：

若采用 CNAME接入方式，需将CDN的回源地址修改为WAF提供的CNAME地址，并在WAF配置获取客户端真实IP。具体操作请参见上文操作步骤。