负载均衡SLB（Server Load Balancer）是一种对流量进行按需分发的服务，通过将流量分发到不同的后端服务器来扩展应用系统的吞吐能力，并且可以消除系统中的单点故障，提升应用系统的可用性。负载均衡SLB产品家族包括应用型负载均衡ALB（Application Load Balancer）、网络型负载均衡NLB（Network Load Balancer ）、传统型负载均衡CLB（Classic Load Balancer），您可根据您的实际需求选择合适的负载均衡产品。

## 产品简介

阿里云提供全托管式在线负载均衡服务，具有即开即用、超大容量、稳定可靠、弹性伸缩、按需付费等特点，适合超大规模互联网应用，如春节红包、双十一秒杀抢购、大规模在线物联网应用等高并发场景。与传统的硬件型负载均衡自建方案相比，无需一次性大额投入，便可拥有天猫双十一级别的流量分发处理能力。同时，与开源的负载均衡自建方案相比，阿里云负载均衡稳定可靠，配备专业的运维团队，免费提供7×24小时不间断技术支持服务，帮助您提升运维效率。

## 产品类型

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8701316771/CAEQVRiBgIDA2rOgrBkiIDFlYTUzNTc2MDdlZTQyNzU4NTJjYzBlODY4NDNkMjVm4735862_20241029141038.886.svg)

阿里云负载均衡SLB支持以下类型的负载均衡：

-   应用型负载均衡 ALB（Application Load Balancer）：专门面向七层，提供业务处理性能，例如HTTPS卸载能力。单实例每秒查询数QPS（Query Per Second）可达100万次。同时ALB提供基于内容的高级路由特性，例如基于HTTP报头、Cookie和查询字符串进行转发、重定向和重写等，是阿里云官方云原生Ingress网关。更多信息，请参见[什么是应用型负载均衡ALB](https://help.aliyun.com/zh/slb/application-load-balancer/what-is-alb#concept-2011635)。
    
-   网络型负载均衡 NLB（Network Load Balancer）：面向万物互联时代推出的新一代四层负载均衡，支持超高性能和自动弹性能力，单实例可以达到1亿并发连接。NLB面向大规模终端连接、高并发消息服务、音视频传输等业务场景针对性地推出了TCPSSL卸载、新建连接限速、全端口监听等高级特性，在物联网MQTTS加密卸载等场景为用户提供多种辅助手段，是适合IoT业务的新一代负载均衡。更多信息，请参见[什么是网络型负载均衡NLB](https://help.aliyun.com/zh/slb/network-load-balancer/product-overview/what-is-nlb/#concept-2223473)。
    
-   传统型负载均衡 CLB（Classic Load Balancer）：支持TCP、UDP、HTTP和HTTPS协议，具备良好的四层处理能力，以及基础的七层处理能力。更多信息，请参见[什么是传统型负载均衡CLB](https://help.aliyun.com/zh/slb/classic-load-balancer/product-overview/what-is-clb/#concept-whs-lp4-tdb)。
    

### 产品功能特性对比


| **对比项** | **ALB（应用型）** | **NLB（网络型）** | **CLB（传统型）** |
| :--- | :--- | :--- | :--- |
| **产品定位** | 七层应用负载，专注HTTP/HTTPS/QUIC，提供高级路由功能 | 四层网络负载，专注TCP/UDP/TCPSSL，支持大规模SSL卸载 | 基础四层+简单七层，支持TCP/UDP/HTTP/HTTPS |
| **架构与性能** | NFV虚拟化，弹性伸缩<br>**单实例：100万QPS** | NFV虚拟化，弹性扩缩容<br>**单实例：1亿并发** | 物理机架构<br>**单实例：100万并发 / 5万QPS** |
| **转发能力** | 基于内容路由、标头改写、重定向、重写、限速等高级七层特性 | TCPSSL卸载、洪峰限速、优雅中断、Anyport等高级四层特性 | 仅支持基础域名或URL转发 |
| **后端类型** | ECS / ENI / ECI / IP地址 / 函数计算FC | ECS / ENI / ECI / IP地址 | ECS / ENI / ECI |
| **运维能力** | **全自动弹性**<br>随业务峰值自动伸缩，无需干预 | **全自动弹性**<br>随业务峰值自动伸缩，无需干预 | **需人工管理**<br>按规格售卖，需预估峰值并手动变配 |
| **云原生集成** | **原生Ingress网关**<br>支持流量拆分、镜像、灰度、蓝绿发布 | 支持ACK/ASK集成（K8s 1.24+） | 支持较弱，需结合ACK/ASK使用 |
| **典型场景** | 互联网高并发七层业务、音视频大流量低时延、云原生灰度发布 | 四层大流量高并发（IoT/车联网）、多活容灾、IDC云上出入口 | 传统网站四层分发、高性能网络分流、同城/跨地域灾备 |


### 产品计费对比

应用型负载均衡 ALB、网络型负载均衡 NLB和传统型负载均衡 CLB的计费说明如下。您可以分别查看并了解负载均衡三个子产品的计费方式及组成。

### ALB计费说明

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8701316771/CAEQYxiBgMCOy9Dj0hkiIGMzMzNlMjg0MWRiMTQwMWI5M2YwNDEwMTY5OGE0YjBh3926471_20230822152343.335.svg)

-   关于ALB资源包介绍，请参见[ALB资源包](https://help.aliyun.com/zh/slb/application-load-balancer/introduction-to-alb-resource-plans#concept-2113835)。
    
-   关于ALB按量付费定价及说明，请参见[ALB计费规则](https://help.aliyun.com/zh/slb/application-load-balancer/alb-billing-rules#concept-2012118)。
    

### NLB计费说明

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8701316771/CAEQURiBgIDVmNmJmhkiIGExMjZkODJlM2RiMzQ3YTI4NGFmNDA3YWQ0MDQxMzI53926471_20230822152343.335.svg)

-   关于NLB资源包介绍，请参见[NLB资源包](https://help.aliyun.com/zh/slb/network-load-balancer/product-overview/nlb-resource-plans)。
    
-   关于NLB按量付费定价及说明，请参见[NLB计费规则](https://help.aliyun.com/zh/slb/network-load-balancer/product-overview/nlb-billable-items#concept-2226387)。
    

### CLB计费说明

CLB按量付费的计费组成如下图所示。有关CLB按量付费定价及计费说明，请参见[按量付费](https://help.aliyun.com/zh/slb/classic-load-balancer/product-overview/pay-as-you-go)。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9701316771/CAEQYxiBgMCqutTj0hkiIDU5ODZmMjg4MWIzZjRhMmY5NGRjYWI1YWY2MGRiMDUz3926471_20230822152343.335.svg)

CLB包年包月实例已于2024年12月01日00:00:00停止新购。详细信息请参见[传统型负载均衡CLB包年包月停售公告](https://help.aliyun.com/zh/slb/product-overview/announcement-of-suspension-of-traditional-load-balancing-clb-package-year-and-month)。

**CLB包年包月的计费组成**

CLB包年包月的计费组成如下图所示。有关CLB包年包月定价及计费说明，请参见[包年包月（停止新购）](https://help.aliyun.com/zh/slb/classic-load-balancer/product-overview/package-year-and-month-stop-new-purchase#concept-hjm-zrt-tdb)。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9701316771/CAEQVRiBgMCXmKSsqhkiIGIzYTU4YTg5ODNiMzRiMjE4YWI0M2IxMmYwMTU5Mjll3926471_20230822152343.335.svg)

ALB、NLB和CLB的LCU定价及用量定义对比如下。

| **子产品** | **LCU单价** **单位：元/个/小时** | **LCU用量定义** | **文档链接** |
| --- | --- | --- | --- |
| 应用型负载均衡 ALB | 0.049 | ALB**一个LCU包含：** - 每秒25个新建连接 - 3000个并发连接（每分钟取样） - 每小时处理1GB的请求和响应的流量数据 - 每小时处理1000个规则 **说明** 影响规则评估数的指标包含转发规则数、AScript可编程脚本行数和扩展证书个数，这三个指标的免费额度均为25。 | [LCU费](https://help.aliyun.com/zh/slb/application-load-balancer/alb-billing-rules#section-e63-vy8-0h6) |
| 网络型负载均衡 NLB | 0.037 | **对于TCP流量，**NLB**一个LCU包含**： - 每秒800个新建TCP连接 - 100000个并发TCP连接（每分钟取样） - 每小时处理1GB的TCP请求和响应的流量数据 **对于UDP流量，**NLB**一个LCU包含：** - 每秒400个新建UDP连接 - 50000个并发UDP连接（每分钟取样） - 每小时处理1GB的UDP请求和响应的流量数据 **对于TCPSSL流量，**NLB**一个LCU包含：** - 每秒50个新建TCPSSL连接 - 3000个并发TCPSSL连接（每分钟取样） - 每小时处理1GB的TCPSSL请求和响应的流量数据 | [LCU费](https://help.aliyun.com/zh/slb/network-load-balancer/product-overview/nlb-billable-items#section-vwu-of3-7db) |
| 传统型负载均衡 CLB | 0.049 | **对于TCP流量，**CLB**一个LCU包含：** - 每秒800个新建TCP连接 - 100000个并发TCP连接（每分钟取样） - 每小时处理1GB的TCP请求和响应的流量数据 **对于UDP流量，**CLB**一个LCU包含**： - 每秒400个新建UDP连接 - 50000个并发UDP连接数（每分钟取样） - 每小时处理1GB的UDP请求和响应的流量数据 **对于HTTP(S)流量，**CLB**一个LCU包含**： - 每秒25个新建HTTP(S)连接 - 3000个并发HTTP(S)连接（每分钟取样） - 每小时处理1GB的HTTP(S)请求和响应的流量数据 - 每小时处理1000个规则 **说明** 影响规则评估数的指标为转发规则数，免费额度为25。 | [LCU&规格费](https://help.aliyun.com/zh/slb/classic-load-balancer/product-overview/pay-as-you-go#section-8tl-tu5-tlm) |

## 产品优势

**多协议支持**

多种协议支持，满足多样化的应用场景。

-   基础协议：支持包含TCP协议和UDP协议的四层负载均衡；支持HTTP协议和HTTPS协议的七层负载均衡。
    
-   高级协议：
    
    -   ALB：支持QUIC协议，对音视频和移动互联网应用更友好；支持gRPC协议，实现微服务间的API通信。
        
    -   NLB：支持TCPSSL协议，可对SSL证书进行集中管理及卸载，有效提升后端业务处理效率。
        

**多层次容灾**

提供多层次的容灾策略与高可用保障体验。

-   健康检查：定时检测后端服务器运行状况，一旦检测到后端服务器异常，则不会再转发流量到异常实例，保证业务可用性。
    
-   多可用区：在地域内采用多可用区部署，实现同城容灾。
    
-   会话同步：采用集群部署，各服务器之间会话同步，支持热升级，避免单服务器故障对业务的影响。
    

**更安全可靠**

自带基础安全防护能力，降低安全建设成本，让网络更省心更安心。

-   网络层安全防护：四层负载均衡支持DDoS、SYN Flood、UDP Flood、ACK Flood、ICMP Flood、DNS Flood等攻击防护。
    
-   应用层安全防护：七层负载均衡除了具备四层安全防护能力，还支持一键集成WAF（Web Application Firewall），让应用层更加可靠。
    
-   证书管理：针对HTTPS协议、QUIC协议和TCPSSL协议提供集中化的证书管理系统，满足您安全可靠的传输需求。
    

**性能保障**

流量分发能力和多种路由功能，具有性能保障能力。

-   性能保障型实例：CLB推出性能保障型实例，实现不同实例间的性能隔离，提供相应规格下的性能保障。
    
-   弹性能力：ALB单实例最大支持100万QPS，NLB单实例最大支持1亿并发连接和100 Gbps带宽。除流量分发处理能力外，还可以自动弹性伸缩以应对突发的不稳定流量。
    

**灵活的调度策略**

多种调度算法与转发模式，提升应用部署灵活性。

-   调度算法：支持加权轮询、加权最小连接数、源IP哈希、四元组哈希、一致性哈希和QUIC ID哈希等调度算法，可根据自身需求选择相应算法来分配用户流量。
    
-   转发规则：支持配置请求方向和响应方向的转发规则，根据不同的转发条件和动作进行流量调度，提升应用系统灵活性。
    

**多种管理途径与付费方式**

根据业务特征灵活选择实例类型与付费方式，多种管理途径运用负载均衡。

-   灵活的管理方式：可基于管理控制台、OpenAPI与SDK等方式实现负载均衡的创建、配置与管理。
    
-   多种付费方式：提供后付费与预付费两种不同的结算模式，支持按流量与按固定带宽两种计费方式。
    

## **相关文档**

-   负载均衡全系列产品支持免费试用，如果您未领用过试用权益，可参考下方对应教程进行产品试用体验：
    
    -   ALB产品试用教程：[通过ALB实现应用流量高级负载分发](https://help.aliyun.com/zh/document_detail/611014.html)。
        
    -   NLB产品试用教程：[通过NLB搭建高可用服务](https://help.aliyun.com/zh/document_detail/611685.html)。
        
    -   CLB产品试用教程：[通过CLB将四层或七层业务流量分发至ECS](https://help.aliyun.com/zh/document_detail/612746.html)。
        
-   负载均衡产品详细介绍可参考：
    
    -   [什么是应用型负载均衡ALB](https://help.aliyun.com/zh/slb/application-load-balancer/what-is-alb)。
        
    -   [什么是网络型负载均衡NLB](https://help.aliyun.com/zh/slb/network-load-balancer/product-overview/what-is-nlb/)。
        
    -   [什么是传统型负载均衡CLB](https://help.aliyun.com/zh/slb/classic-load-balancer/product-overview/what-is-clb/)。
        
-   如果您未使用过负载均衡产品，您可参考[快速入门](https://help.aliyun.com/zh/slb/getting-started)。
    
-   负载均衡产品计费相关文档汇总页可参考[负载均衡产品计费](https://help.aliyun.com/zh/slb/product-overview/billing-for-load-balancing-products)。
 
| 维度 | CLB（传统型/经典型） | ALB（应用型） | NLB（网络型） |
  |---|---|---|---|
  | **层级** | 四层 + 七层 | 七层（HTTP/HTTPS/gRPC） | 四层（TCP/UDP/TLS） |
  | **性能** | 中（弹性，上限不如后两者） | 高（弹性） | 极高（单实例千万并发） |
  | **主要调度算法** | 轮询、加权轮询、加权最小连接数、一致性哈希 | 轮询、加权轮询、加权最小连接数 | 加权最小连接数 |
  | **是否支持 EIP 绑定** | 支持 | 不支持 | 支持（每个可用区一个固定 IP） |
  | **有固定 IP 吗** | 需要搭配 | 无固定 IP | ✅ 有（每个可用区一个） |
  | **典型场景** | 传统架构，兼容存量老应用 | 微服务 / 容器 / 云原生 | 高性能 / 低延迟 / 长连接 |
  | **淘汰趋势** | 逐步被 ALB/NLB 取代 | 七层首选 | 四层首选 |
  | **SSL 卸载** | 支持 | 支持 | 支持 |
  | **健康检查** | TCP / HTTP / HTTPS | TCP / HTTP / HTTPS | TCP |