本方案通过云防火墙IPS攻击检测结果与NAT会话日志关联集成，帮助用户快速定位存在风险的私网IP，实现网络攻击的快速溯源分析。

## **业务风险**

企业在云上VPC环境下，往往会采用公网NAT网关，通过转换和隐藏云服务私网地址，防止私网地址直接暴露，构建安全隔离的流量的公网出入口。同时在公网出入口也会部署防火墙等安全设备，对NAT进出互联网的流量进行过滤。而当遭受公网网络攻击或非法外联时，通常只能定位到风险NAT弹性公网IP，难以快速定位到具体ECS等私网IP，无法及时进行攻击溯源以及风险处置。

## **解决方案**

为了解决这个问题，阿里云防火墙（CFW）联动NAT会话日志推出了**IPS私网溯源**能力。通过自动关联NAT网关会话日志，并直接显示被攻击服务实例的私有IP地址，帮助企业快速准确地定位受攻击资产，从而采取有效的应对措施。

-   **云防火墙IPS能力**：云防火墙（CFW）IPS引擎主要对公网出向和入向攻击流量进行检测并防护。所有接入云防火墙的网络流量都会经过云防火墙IPS引擎过滤，再转发出去。针对网络流量，云防火墙通过深度数据包协议识别网络流量中的协议并进行包解析，并通过IPS引擎和威胁情报进行流过滤和包过滤。如果命中了威胁引擎模式以及IPS规则动作，那么该攻击数据包将被丢弃或放行，从而实现对攻击的实时告警和拦截。同时，云防火墙会详细记录IPS攻击日志。
    
-   **NAT会话日志**：NAT 网关（NAT Gateway）提供会话日志功能，当用户为NAT网关创建SNAT条目，有流量经过NAT网关时，SNAT会话将以日志的形式进行记录，便于溯源和监控。会话日志捕获的SNAT会话以日志的形式写入SLS中。每条会话日志记录会捕获特定捕获窗口中的特定五元组网络流。同时针对入向DNAT，可以通过端口映射定位到具体私网。
    

### **出站流量攻击私网溯源：**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0834996371/CAEQURiBgIDA6_ynohkiIDJhNzMwZTVkYjA3NDQ3Njc5MzBjOTE1ZTE1YzhjMmE04803854_20250109133403.685.svg)

### **入站流量攻击溯源：**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0834996371/CAEQURiBgMCq4v6nohkiIDAwZmQxMzEwNGZiMDQ0Mzk5MjM0NThiOTI2ZWRjMWZi4803854_20250109133403.685.svg)

## **场景示例**

以某中型新零售企业的云上电子商城业务为例。为了保证服务稳定及安全，企业在DMZ VPC部署了NAT网关作为所有对公网流量通信出口和入口，降低暴露风险。同时企业采用云防火墙，开启互联网边界防火墙，对NAT弹性公网IP流量进行过滤和防护。某天晚上，安全运维团队接收到警报提示存在异常流量，疑似有机器漏洞被攻击者入侵，被植入木马对外发起恶意访问流量，访问某境外IP，并主动下载bash脚本和植入了CoinMiner家族木马。安全运维团队需要快速定位到正面临威胁的异常后端服务器业务。

此时，云防火墙**IPS私网溯源**能力就能发挥重要作用。企业开启该能力后，系统能够自动关联分析NAT网关的会话日志与云防火墙IPS攻击日志，将每条NAT会话日志记录捕获的特定捕获窗口中的特定五元组网络流与云防火墙记录的每条IPS事件日志自动关联，分钟级快速定位风险私网IP。这样，安全运维人员就可以更快地识别出问题私网服务器，并快速配置该服务器禁止对外访问的ACL访问控制策略和清除木马，及时止损和防止风险扩散。

## **使用须知**

-   云防火墙按量版和包年包月均支持该能力。NAT网关按CU计费的公网NAT网关支持该能力。按规格计费的NAT网关实例不支持开启会话日志服务。
    
-   开启IPS私网溯源，云防火墙自身不增加额外费用，但系统会在您的NAT网关会话日志中**创建索引**，并进行查询，会产生一定费用，关于日志服务的收费，请参见SLS收费标准。
    
-   在IPS私网溯源开启状态下，如果发现**NAT网关会话日志**的索引未开启，或者索引中缺失溯源所需字段，系统会自动重新创新索引，或者在索引中添加需要的字段。
    

## **开启配置**

1.  登录[云防火墙控制台](https://yundun.console.aliyun.com/?p=cfwnext)，在左侧导航栏选择**防护配置** > **IPS配置**，在高级设置区域中找到**IPS私网溯源**卡片，点击**查看配置**打开配置页面。
    
2.  在**IPS私网溯源**页面可以看到支持溯源的公网资产列表，对应**NAT网关**需先开启**互联网防火墙保护**和**NAT会话日志**，云防火墙才能进行IPS私网溯源。在点击**操作**开关时会有对应提示，点击链接按指引开启即可。或参考下列详细配置文档：
    
    -   **互联网防火墙保护**开启：[开启防火墙开关](https://help.aliyun.com/zh/cloud-firewall/cloudfirewall/user-guide/internet-firewall#section-ct5-2rq-cfb)
        
    -   **NAT会话日志**开启：[NAT会话日志配置流程](https://help.aliyun.com/zh/nat-gateway/user-guide/session-log-overview/#2391d5d258mkz)
        

具体操作，请参见[IPS私网溯源](https://help.aliyun.com/zh/cloud-firewall/cloudfirewall/user-guide/prevention-configuration#22561fbf1egi5)。

## **溯源数据查看**

**重要**

云防火墙IPS私网溯源功能联动NAT网关会话日志能力，由于NAT网关日志捕获和投递有一定数据延迟，您查询私网溯源结果预计会有约20分钟延迟。

在**IPS私网溯源状态**开启后，您可以在以下场景中查看到溯源数据。

### **检测响应** > **入侵防御**

列表：

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7114746371/p881169.png)

详情页：

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7114746371/p881196.png)

### **检测响应** > **失陷感知**

列表：

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7114746371/p881215.png)

详情页：

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7114746371/p881228.png)

### **日志监控** > **日志审计**

**事件日志** > **互联网边界**页签中：

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7114746371/p882514.png)

## **更多文档**

-   查看更多云防火墙IPS攻击防护配置：[IPS配置](https://help.aliyun.com/zh/cloud-firewall/cloudfirewall/user-guide/prevention-configuration)
    
-   通过NAT网关和NAT防火墙防护私网出站流量安全的最佳实践：[通过NAT网关和NAT防火墙防护私网出站流量安全的最佳实践](https://help.aliyun.com/zh/cloud-firewall/cloudfirewall/use-cases/protect-the-outbound-traffic-of-assets)