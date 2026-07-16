CC攻击（Challenge Collapsar攻击）是DDoS攻击的一种，通过持续发送高并发请求，耗尽服务器的计算资源或数据库连接，导致业务响应延迟、页面加载缓慢，典型特征包括QPS飙升和带宽占用增加。为保护暴露在公网的云服务器ECS实例免受此类攻击，可为其开启Web应用防火墙（Web Application Firewall，简称WAF）防护，有效抵御CC攻击，保障业务稳定运行。

## **适用范围**

-   ECS实例已部署Web服务，通过公网IP对外提供服务。
    
-   ECS实例位于以下地域：**西南1（成都）、华北2（北京）、华北3（张家口）、华东1（杭州）、华东2（上海）、华南1（深圳）、华北1（青岛）、中国（香港）、马来西亚（吉隆坡）、印度尼西亚（雅加达）、新加坡**。若不满足以上要求，请使用[CNAME接入](https://help.aliyun.com/zh/waf/web-application-firewall-3-0/user-guide/add-a-domain-name-to-waf-in-cname-record-mode)。
    

## **步骤一：开通按量付费WAF实例**

1.  访问[Web应用防火墙3.0（按量付费）购买页](https://common-buy.aliyun.com/?commodityCode=waf_v2_public_cn)。
    
2.  选择**资产类型**为**Web应用防火墙3.0**，并选择**付费模式**为**按量付费**后，完成如下配置。
    
    | **配置项** | **说明** |
    | --- | --- |
    | **地域** | 决定WAF防护节点的位置，若部署网站的ECS实例位于中国内地，请选择**中国内地**，其他情况下，请选择**非中国内地**。 |
    | **WAF版本** | 默认为**按量付费版**，无需配置。 |
    | **服务关联角色** | 为了提供流量访问控制、监控分析等服务，WAF需要访问您的云服务资源，请点击**创建服务关联角色**，系统会自动创建角色**AliyunServiceRoleForWaf**，无需手动对此角色做任何修改。 |
    
3.  单击**立即购买**并完成下单。
    

## **步骤二：接入ECS实例**

1.  登录[Web应用防火墙3.0控制台](https://yundunnext.console.aliyun.com/?p=wafnew)，在顶部菜单栏选择资源组和地域（**中国内地**、**非中国内地**），然后在左侧导航栏单击**接入管理**。选择**云产品接入**页签，在左侧云产品类型列表，选择**云服务器 ECS**。
    
2.  在右侧列表，找到目标ECS实例，在**操作**列单击**立即接入**。如果找不到目标实例，请单击页面右上角**同步资产**，若仍无法找到，说明实例不满足[适用范围](#80a109c4780x0)。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2536734571/p965604.png)
    
3.  在**选择需要添加的实例&端口**区域，单击**操作**列的**添加端口**。
    
4.  在弹出的**添加端口**页面，根据网站的端口与协议类型进行配置。
    
    -   **标准 HTTP 网站**
        
        若需接入的网站地址为 `http://yourdomain.com`，请选择**协议类型**为**HTTP**，**端口**为 **80**。
        
    -   **标准 HTTPS 网站**
        
        若需接入的网站地址为`https://yourdomain.com`，请选择**协议类型**为**HTTPS**，**端口**为 **443**。
        
    -   **非标准端口网站**
        
        若需接入的网站地址明确包含端口号（格式为 `域名:端口号`），则需按实际端口填写。例如：
        
        -   `http://yourdomain.com:8080` ，**协议类型**：**HTTP**，**端口**：**8080**。
            
        -   `https://yourdomain.com:8443`，**协议类型**：**HTTPS**，**端口**：**8443**。
            
    
    #### **HTTP协议**
    
    1.  在**端口**区域，填写网站使用的端口。
        
    2.  在**协议类型**区域，选择**HTTP**。
        
    
    #### **HTTPS协议**
    
    1.  在**端口**区域，填写网站使用的端口。
        
    2.  在**协议类型**区域，选择**HTTPS**。
        
    3.  保持**HTTP2**、**TLS协议版本**、**加密套件**、**扩展证书**配置为默认设置。
        
    4.  在**默认证书**区域，选择证书上传方式：
        
        -   **手动上传**：适用于证书未上传至阿里云数字证书管理服务（原 SSL 证书）的场景。
            
        -   **选择已有证书**：从阿里云数字证书管理服务（原 SSL 证书）中选择已签发或已上传的证书。
            
            #### **手动上传**
            
            -   **证书名称**：为证书设置一个唯一的名称，不能与已上传的证书名称重复。
                
            -   **证书文件**：请使用文本编辑器打开并粘贴 **PEM、CER、CRT 格式**的证书文本内容。
                
                格式示例：`-----BEGIN CERTIFICATE-----......-----END CERTIFICATE-----`
                
                -   格式转换：若证书是 PFX、P7B 等格式，请使用[证书工具](https://help.aliyun.com/zh/ssl-certificate/use-the-certificate-toolkit#section-7pl-isf-owk)将其转换为 PEM 格式。
                    
                -   证书链：若包含中间证书，请按照 “服务器证书、中间证书” 的顺序拼接后粘贴。
                    
            -   **私钥文件**：请使用文本编辑器打开并粘贴 PEM 格式的私钥文本内容。
                
                格式示例：`-----BEGIN RSA PRIVATE KEY-----......-----END RSA PRIVATE KEY-----`
                
            
            #### **选择已有证书**
            
            从证书下拉列表中选择要上传到WAF的证书。
            
            **说明**
            
            若WAF控制台提示“**证书链完整性校验失败，使用该证书可能会影响您的业务访问**”，表示证书链存在完整性问题。请检查证书内容的正确性与完整性后，在数字证书管理服务控制台重新上传。具体操作，请参见[上传、同步和共享SSL证书](https://help.aliyun.com/zh/ssl-certificate/upload-an-ssl-certificate#concept-g5c-3xn-yfb)。
            
    
5.  保持其他配置为默认设置，单击**确定**。
    
6.  **（可选）查看防护对象**：此时ECS实例已完成接入，WAF已自动创建一个名为`实例id-端口-资产类型`的防护对象，并为该防护对象默认启用Web核心防护规则等模块的防护规则，可以在**防护配置** > **防护对象**页面查看。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2536734571/p965611.png)
    
7.  **验证基础防护效果**：在浏览器访问ECS实例上托管的网站，并在其URL后附加Web攻击测试代码（例如`http://yourdomain.com/alert(xss)`），若返回WAF的405拦截提示页面，表示攻击被拦截，WAF防护成功。
    

## **步骤三：配置CC防护规则**

1.  在左侧导航栏，选择**防护配置** > **Web 核心防护**。
    
2.  在页面下方**CC防护**区域，单击**新建模板**。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4278803671/p1025467.png)
    
3.  在**新建模板**面板，完成以下配置。
    
    | **配置项** | **说明** |
    | --- | --- |
    | **模板名称** | 为该模板设置一个便于识别的名称。 |
    | **是否设置为默认模板** | 保持默认未开启状态。 |
    | **防护模式** | - **正常模式**：仅拦截特征显著的异常请求，误报率低。适用于日常业务运行及流量平稳场景。 - **严格模式**：采用高强度检测算法，能有效阻断CC攻击，但误报风险较高。仅在正常模式失效且出现响应延迟、资源（CPU/内存）负载异常时建议启用。 **说明** **严格模式**仅适用于网页（含H5）业务，请勿用于API接口或原生应用（Native App），以免造成大量误拦截。 |
    | **动作** | 定义请求命中防护规则后的处置方式，选择**JS挑战**。 |
    | **生效对象** | 在**待选择对象**区域勾选ECS实例对应的防护对象，单击![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4278803671/p1025940.png)图标将其移至右侧**已选择**区域。 |
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0445793771/p1061232.png)
    
4.  单击**确定**。![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=)
    

## **步骤四：查看攻击防护数据**

配置完成后，可以前往左侧导航栏**总览**页面。查看**防护总览**、**攻击情况Top10**等信息，进行业务安全分析。![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=)

请根据实际需求选择后续操作：

-   **继续使用WAF（推荐）**：前往[进阶优化](#2763ff2b4bww0)。
    
-   **暂不使用WAF**：前往[释放资源](#326f1cf74c90c)以停止计费。
    

## 进阶优化：增强防护与成本控制

在本文提供的配置基础上，若希望继续使用WAF，可按以下方式进一步调整配置，以适配具体业务特征，从而获取更强的安全防护能力与更低的成本。

-   **多模块协同防护**：本文仅启用CC防护模块，可结合以下多个防护模块实现协同防御。
    
    -   [自定义规则](https://help.aliyun.com/zh/waf/web-application-firewall-3-0/user-guide/configure-custom-rules-to-defend-against-specific-requests)：基于灵活的匹配条件与规则动作，针对特定攻击特征实施精准防护。例如，通过配置频率控制规则实现访问限流。 
        
    -   [白名单](https://help.aliyun.com/zh/waf/web-application-firewall-3-0/user-guide/configure-whitelist-rules-to-allow-specific-requests)：允许符合指定特征的请求通过，如可信IP地址。 
        
    -   [IP黑名单](https://help.aliyun.com/zh/waf/web-application-firewall-3-0/user-guide/configure-ip-address-blacklist-rules-to-block-specific-requests)：阻断已知恶意IP的访问。 
        
    -   [区域封禁](https://help.aliyun.com/zh/waf/web-application-firewall-3-0/user-guide/configure-region-blacklist-rules-to-block-requests-from-specific-regions)：一键封禁来自特定地理区域的请求。例如，当业务仅面向中国境内用户，且检测到大量境外攻击时，可启用该功能。
        
-   **进阶接入配置**：WAF提供多种资源接入方式，可根据业务需求进行选择。
    
    -   [云产品接入ECS实例](https://help.aliyun.com/zh/waf/web-application-firewall-3-0/user-guide/add-an-ecs-instance-to-waf)：本文采用此接入方式，旨在快速接入云产品实例。如存在TLS版本、加密套件、多证书配置需求，请参见[增强安全防护等级（HTTPS）](https://help.aliyun.com/zh/waf/web-application-firewall-3-0/user-guide/add-an-ecs-instance-to-waf#e7b840911bd0s)；如存在WAF前七层代理设置（如CDN）、流量标记等配置需求，请参见[获取真实客户端信息](https://help.aliyun.com/zh/waf/web-application-firewall-3-0/user-guide/add-an-ecs-instance-to-waf#4629aef72dtfa)。
        
    -   [CNAME接入](https://help.aliyun.com/zh/waf/web-application-firewall-3-0/user-guide/add-a-domain-name-to-waf-in-cname-record-mode)：通过域名接入，适用场景更广、使用限制更少、支持功能更多。
        
-   **成本优化建议**：
    
    -   [SeCU资源包](https://help.aliyun.com/zh/waf/web-application-firewall-3-0/secu-resource-plans)：SeCU资源包是按量付费版WAF的成本优化方案，在开通按量付费WAF实例后，可购买SeCU资源包抵扣按量付费WAF产生的总费用。
        
    -   [包年包月版WAF](https://help.aliyun.com/zh/waf/web-application-firewall-3-0/user-guide/purchase-a-subscription-waf-3-0-instance)：当计划长期使用WAF时，建议购买包年包月版WAF以获得更优单价。
        

## **释放资源停止计费**

完成快速入门教程后，若不再需要在教程中开通的WAF，可以参照以下步骤关闭WAF停止计费。

**警告**

-   **计费提示**：按量付费版WAF除请求处理费用外，还收取功能费用（包括WAF实例本身的费用等）。开通WAF后，无论是否接入资源，均会产生费用。若不再需要使用WAF，请及时关闭WAF实例。
    
-   **CNAME接入注意事项**：若仅通过本文所述云产品方式接入，可忽略本项。若已配置CNAME接入，请在关闭WAF实例前，确保相关网站域名的DNS解析已回切至源站。
    

1.  前往左侧导航栏**总览**页面，在顶部菜单栏，选择WAF实例的资源组和地域（**中国内地**、**非中国内地**）。
    
2.  若显示如下界面，请单击右上角**访问控制台**。若未显示如下界面，请跳过此步骤。![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=)
    
3.  在页面右侧区域单击**关闭WAF**，在页面弹出的提示框中勾选相关内容后单击**确定**。![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=)