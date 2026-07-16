EIP 是可独立持有的公网 IP 资源。将 ECS 实例的固定公网 IP 转换为 EIP，提升 IP 地址的灵活性，有助于：

-   故障恢复：当 ECS 实例故障时，可将 EIP 快速切换至备用实例，保障业务连续性。
    
-   架构升级：支持将 EIP 切换绑定至负载均衡或公网 NAT 网关，平滑升级网络架构。
    

## 转换影响

-   **IP 地址不变：** 转换过程中，公网 IP 地址保持不变，现有网络连接不受影响。
    
-   **计费变更**：转换后，公网带宽计费方式和计费单价保持不变。EIP 独立产生账单，收取 EIP 配置费和公网网络费。
    
    > [不收取 EIP 配置费（公网 IP 保有费）的情况](https://help.aliyun.com/zh/eip/pay-as-you-go/#f9082b946e17t)。
    
-   **操作不可逆**：转换为 EIP 后，无法直接回退为固定公网 IP。如需绑定固定公网 IP，需要先解绑 EIP，再调整 ECS 公网带宽，为 ECS 重新分配一个新的固定公网 IP，IP 地址会发生变化。
    

## 适用范围

-   实例状态：
    
    -   ECS 实例处于**运行中**或者**已停止**状态。
        
    -   如果实例正在进行规格变更，请等待变更生效后再执行转换。
        
-   计费方式：
    
    -   按量付费 ECS 实例：账号欠费时，不支持转换。
        
    -   包年包月 ECS 实例：
        
        -   仅公网带宽计费方式为按使用流量计费，支持转换；按固定带宽计费的公网带宽需要转为按使用流量计费才可以转换。
            
            [固定公网IP切换为按使用流量计费后，再转换为EIP并切换为包年包月计费时，可能存在差价。](https://help.aliyun.com/zh/ecs/billing-item-faqs#section-q8n-xvj-tob)
            
        -   到期前 24 小时内，不支持转换。
            
-   地域与线路：中国香港地域的 BGP 精品（多线）线路的固定公网 IP 不支持转换。
    

## 转换为 EIP

### **控制台**

1.  前往[ECS控制台-实例](https://ecs.console.aliyun.com/server/region)页面。
    
2.  单击目标 ECS 实例 ID，在**全部操作**中选择**网络和安全组** > **公网 IP 转换为弹性公网 IP**。
    
3.  确认信息后，单击**确定**。转换完成后，**实例详情**页面的**公网 IP**不再显示内容，**弹性公网 IP**显示转换后的 EIP。
    

### **API**

调用[ConvertNatPublicIpToEip](https://help.aliyun.com/zh/ecs/api-convertnatpubliciptoeip#doc-api-Ecs-ConvertNatPublicIpToEip)将固定公网 IP 转换为 EIP。