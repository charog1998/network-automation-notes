EIP 默认提供不超过 5Gbps 的[DDoS 基础防护](#276f43e09a37h)能力，当流量超过基础防护能力时，流量将会被黑洞处理，即所有入流量全部被屏蔽，可能导致服务完全中断。使用 DDoS 防护（增强版）EIP，可获得 Tbps 级的防护能力，保障业务连续性。

## **工作原理**

DDoS 防护（增强版）EIP 使用 [DDoS 原生防护](https://help.aliyun.com/zh/anti-ddos/anti-ddos-origin/product-overview/what-is-anti-ddos-origin#b09574f75ag5n) ，具备 Tbps 级的 DDoS 防护能力，适用于大型游戏、重大线上直播等对安全防护级别要求较高且时延较敏感的场景。

-   入方向：先经过 DDoS 原生防护检测并清洗，过滤攻击流量后，将正常流量转发至实例。
    
-   出方向：直接通过 EIP 访问公网。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2677856771/CAEQbBiBgIC1j6SM6RkiIDMzZTQyYTM5ZjNjZTQwYzA5NWM0ZDdlZjczZDg1YWJm5274221_20250627113930.173.svg)

## **适用范围**

-   线路类型：BGP（多线）。
    
-   计费方式：按量付费。
    
-   通过[IP地址池](https://help.aliyun.com/zh/eip/ip-address-pools)创建DDoS防护（增强版）EIP时，IP地址池也需要是 DDoS 防护（增强版）。
    
-   支持的地域：
    
    ## EIP
    
    -   亚太-中国：华北2（北京）、华东1（杭州）、华东2（上海）、中国香港
        
    -   亚太-其他：菲律宾（马尼拉）、日本（东京）、新加坡、马来西亚（吉隆坡）、印度尼西亚（雅加达）、韩国（首尔）、泰国（曼谷）
        
    -   其他：美国（弗吉尼亚）、美国（硅谷）、德国（法兰克福）、英国（伦敦）、墨西哥
        
    
    ## IP地址池
    
    -   亚太-中国：中国香港
        
    -   亚太-其他：菲律宾（马尼拉）、日本（东京）、新加坡、马来西亚（吉隆坡）、印度尼西亚（雅加达）、韩国（首尔）、泰国（曼谷）
        
    -   其他：美国（弗吉尼亚）、美国（硅谷）、德国（法兰克福）、英国（伦敦）、墨西哥
        
    

## **开启 DDoS 防护（增强版）**

确保已开通 DDoS原生防护（按量付费版）。开通服务并添加防护资产后，阿里云即认为您正式使用产品并开始[计费](https://help.aliyun.com/zh/anti-ddos/anti-ddos-origin/product-overview/pay-as-you-go)。该服务是按月开通产品，30天内不支持停用。

### **控制台**

前往[EIP购买页](https://common-buy.aliyun.com/?spm=5176.9843921.content.11.661e4882hCrvFj&commodityCode=eip&regionId=cn-hangzhou-dg-a01#/buy)。其他配置参考[弹性公网 IP](https://help.aliyun.com/zh/eip/elastic-ip-address)。

-   **付费模式**：**按量付费**。
    
-   **线路类型**：**BGP(多线)**。
    
-   **安全防护**：**DDoS防护（增强版）**。
    
-   **地址池**：
    
    -   保持默认：从阿里云公共 IP 地址池分配 DDoS 防护（增强版）EIP。
        
    -   指定 IP 地址池：必须指定 DDoS 防护（增强版）IP 地址池，从中分配 EIP。
        

创建完成后，可以登录[弹性公网IP管理控制台](https://vpc.console.aliyun.com/eip)，单击目标 EIP **安全防护**列的![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7572275771/p1031644.png)图标，查看 DDoS 安全防护的清洗阈值和黑洞阈值。

T日创建完成后，可在 T+1 日前往[流量安全产品控制台](https://yundun.console.aliyun.com/?p=ddos)，在**流量安全** > **网络安全** > **DDoS原生防护** > **账单中心**页面查询用量明细。单击**详细说明**，可以申请调整访问峰值带宽。

### **API**

调用[AllocateEipAddress](https://help.aliyun.com/zh/eip/developer-reference/api-vpc-2016-04-28-allocateeipaddress-eips)配置`SecurityProtectionTypes`为`AntiDDoS_Enhanced`，创建 DDoS 防护（增强版）EIP。

## 计费说明

仅按量付费的 EIP 支持 DDoS 防护（增强版）安全防护级别，计费项包括：

-   公网 IP 保有费和公网网络费：EIP 收取；
    
-   [DDoS 原生防护 2.0 费用](https://help.aliyun.com/zh/anti-ddos/anti-ddos-origin/product-overview/pay-as-you-go#task-2273180)：DDoS 防护收取。DDoS 防护（增强版）EIP 属于增强型云产品。
    

## 更多信息

### **DDoS 基础防护**

EIP 默认具备不超过 5Gbps 的 DDoS 基础防护能力。公网入方向流量首先经过阿里云 DDoS 基础防护，经检测符合 DDoS 攻击模型，且超过清洗阈值时，DDoS 基础防护将启动流量清洗，过滤恶意报文，将正常流量转发至 EIP。

-   流量清洗：
    
    -   清洗方法：过滤攻击报文、限制流量速度、限制数据包速度等。
        
    -   清洗触发：流量符合攻击模型特征，且流量达到 BPS（流量速率） 清洗阈值或 PPS （数据包速率）清洗阈值。DDoS 基础防护根据 EIP 带宽自动设定清洗阈值。
        
        -   BPS 清洗阈值：当 EIP 带宽 ≤ 300Mbps 时，为 450Mbps；EIP 带宽 ＞ 300Mbps 时，为`EIP 带宽值 × 1.5`Mbps。
            
        -   PPS 清洗阈值：当 EIP 带宽 ≤ 100Mbps 时，为 100000pps；EIP 带宽 ＞ 100Mbps 时，为`EIP 带宽值 × 1000`pps。
            
-   黑洞策略：当 DDoS 攻击流量超过 EIP 的黑洞阈值（即 5Gbps 的 DDoS 基础防护能力，具体为 5200Mbps）时，为避免对云产品产生更大损害，阿里云会执行黑洞策略，屏蔽 EIP 所有入方向流量，这将导致服务完全中断。默认黑洞自动解除时间是2.5小时。实际根据资产被攻击频率有差异。