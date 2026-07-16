自建DNS支持在转发规则上开启**DoH转发优先**，将域名查询请求通过DNS over HTTPS（DoH）加密协议，转发至**阿里云移动解析HTTPDNS**服务，实现传输加密，避免发生域名被劫持等安全问题。

## **应用场景**

企业部署自建DNS集群承接内网域名解析时，公网域名查询仍需转发至外部DNS服务器进行解析。传统转发模式默认采用 UDP/TCP 53 端口进行明文传输，存在以下风险：

-   查询请求与响应可能被监听、篡改或劫持，导致访问异常或安全风险。
    
-   难以满足金融、政企等行业对域名解析传输安全及可监管性的合规要求。
    

针对上述问题，自建DNS支持在转发规则中开启**DoH转发优先**，从而实现：

-   域名请求匹配相应转发规则后，优先通过HTTPS加密通道转发至阿里云[移动解析HTTPDNS](https://help.aliyun.com/zh/dns/httpdns-what-is-mobile-resolution-httpdns)服务，有效规避安全风险。
    
-   若DoH请求失败，则自动降级为UDP协议，转发至目标DNS服务器，保证解析可靠性。
    

## **计费说明**

使用阿里云移动解析HTTPDNS服务会产生解析费用，HTTPS（含DoH/DoT）按5倍HTTP流量计费。具体计费标准和免费额度请参见[HTTPDNS产品计费](https://help.aliyun.com/zh/dns/httpdns-product-billing)。

## 前提条件

开始配置前，请确认以下条件已满足：

-   已开通并部署自建DNS解析集群，集群状态为正常运行。详情请参考[软件部署](https://help.aliyun.com/zh/dns/software-deployment)。
    
    **说明**
    
    该功能依赖自建DNS V3.0.1 及以上版本，旧版本不支持。
    
-   已开通阿里云移动解析HTTPDNS服务，完成**DoT/DoH接入**的加密地址配置，并保证该地址的**“启用状态”为开启**。详情请参考[DNS over HTTPs(DoH)](https://help.aliyun.com/zh/dns/httpdns-dns-over-https-doh)。
    
-   自建DNS解析集群可访问移动解析HTTPDNS的DoH接入地址，默认使用HTTPS 443端口出方向访问。
    

## 配置步骤

### 步骤一：配置转发规则

1.  访问[云解析DNS-内网域名解析](https://dnsnext.console.aliyun.com/privateDNS)。
    
2.  在**转发管理**页面选择**转发规则**页签，再点击**添加转发规则**。
    
3.  在**添加转发规则**面板，配置以下参数：
    
    | **参数** | **说明** |
    | --- | --- |
    | **转发域名 (Zone)** | 填写需要转发解析请求的域名（Zone）。 - 如需支持全部域名（根域）转发，请输入英文句号：`.` - 支持顶级域名转发，例如：`com`，`cn`，`top`等。 - 如果解析请求同时命中多个转发域名，按照最长Zone匹配优先生效规则。 |
    | **外部DNS系统的IP地址:端口** | DNS查询流量被转发的目标服务器的IP地址和端口，最多可配置6个，支持私网IP地址和公网IP地址。该地址作为DoH不可用时的明文降级出口。 |
    | **生效范围设置** | 选择此转发规则生效的自建DNS集群，确保策略正确下发到目标集群。 |
    
4.  单击**确定**完成规则添加。添加成功后，转发规则列表中将显示该规则。
    

### 步骤二：开启DoH转发优先

为已添加的转发规则启用DoH转发优先，将域名查询经由加密通道发送至解析服务HTTPDNS。

1.  在**转发管理** > **转发规则**列表内，找到步骤一中添加的转发规则。
    
2.  选中该规则，单击列表下方的**DoH转发优先**。
    
3.  在**DoH转发优先**配置面板，开启该功能，并在**阿里云移动解析HTTPDNS服务**下拉框中选择可用的DoH接入地址。
    
    如暂无可用接入地址，请参考[DNS over HTTPs(DoH)](https://help.aliyun.com/zh/dns/httpdns-dns-over-https-doh)，完成**DoT/DoH接入**的加密地址配置后获取。
    
4.  单击**确定**。规则列表中，该转发规则的“转发域名”列将显示DoH标签，表示DoH转发优先已生效。
    

**说明**

除阿里云移动解析HTTPDNS服务外，本功能也支持接入其他厂商的HTTPDNS服务。您可在**其他自定义HTTPDNS服务商**输入框中，手动填写其提供的DoH加密接入地址（需符合 RFC 8484 标准），完成转发配置。

### 步骤三：验证配置

配置完成后，可通过以下方法验证DoH转发是否生效：

1.  使用 `dig` 或 `nslookup` 命令，针对命中该转发规则的域名发起解析请求，确认解析结果正常返回。
    
2.  查看[自建DNS解析日志](https://help.aliyun.com/zh/dns/intranet-dns-resolution-log)和[移动解析HTTPDNS解析日志](https://help.aliyun.com/zh/dns/httpdns-resolution-log)，若两侧记录的查询域名、记录类型和解析结果一致，且HTTPDNS 侧“接入协议”显示为 `DoH`、“源 IP”为自建DNS集群的出口IP，即表示DoH 转发已生效并形成端到端审计链路。