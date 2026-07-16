当服务部署在中国香港或其他海外地域、服务对象为中国内地用户时，公网绕行导致访问时延高。为服务绑定BGP（多线）\_精品线路EIP，可通过运营商专属线路直连，降低中国内地用户访问时延。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8373260871/CAEQYxiBgMDCvdD6yxkiIGYzYmM5ZjI5MDAzYTQyMzJhOWM1ZmI4ZWNmMjhkMGNm5734471_20250918154013.940.svg)

## 适用范围

不同付费模式下，支持的地域不同：

-   按量付费：中国香港、日本（东京）、新加坡、马来西亚（吉隆坡）、菲律宾（马尼拉）、印度尼西亚（雅加达）和泰国（曼谷）。
    
-   包年包月：中国香港。
    

## 创建并绑定精品 EIP

1.  创建 EIP：
    
    1.  前往[EIP控制台](https://vpc.console.aliyun.com/eip/cn-hangzhou/eips)，单击**创建弹性公网IP**。
        
    2.  配置EIP参数并完成购买。其余参数配置可参考[EIP 配置](https://help.aliyun.com/zh/eip/elastic-ip-address#64fa36953fqz4)。
        
        -   **付费模式**：优先结合业务部署地域选择。
            
        -   **地域和可用区**：选择云服务部署的地域。
            
        -   **线路类型**：选择**BGP（多线）\_精品**。
            
        -   **地址池**：已有[IP地址池](https://help.aliyun.com/zh/eip/ip-address-pools)的情况下，可以选择从已有 IP 地址池中分配EIP。
            
        
2.  绑定云资源：
    
    1.  前往[弹性公网IP](https://vpc.console.aliyun.com/eip/cn-hangzhou/eips)页面，在顶部菜单栏选择 EIP 所属地域。
        
    2.  单击目标 EIP **操作**列的**绑定资源**，选择实例类型后，选择绑定的实例。
        

## 验证网络质量

公网质量受运营商公网质量影响，请以实际业务测试为准。

以部署在华东1（杭州）的 ECS 访问部署在菲律宾（马尼拉）的两个 ECS（分别绑定 BGP（多线）线路 EIP 和 BGP（多线）\_精品线路 EIP）为例。

1.  为菲律宾（马尼拉）ECS 均配置 Nginx 服务。
    
    ```
    sudo yum install nginx -y
    sudo systemctl start nginx
    ```
    
2.  测试华东1（杭州）ECS 的访问时延。
    
    > 确保菲律宾（马尼拉）ECS 放通华东1（杭州）ECS 的公网 IP。
    
    ```
    {
    echo "=== Starting EIP Comparison Test ==="
    echo "BGP (Multi-ISP) EIP:"
    curl -w "Connect Time: %{time_connect}s Total Time: %{time_total}s\n" -o /dev/null -s http://<BGP_Multi_ISP_EIP>
    echo "BGP (Multi-ISP) Pro EIP:"
    curl -w "Connect Time: %{time_connect}s Total Time: %{time_total}s\n" -o /dev/null -s http://<BGP_Multi_ISP_Pro_EIP>
    }
    ```
    
    ```
    [root@iZbp xxx Z ~]# {
    echo "=== Starting EIP Comparison Test ==="
    echo "BGP (Multi-ISP) EIP:"
    curl -w "Connect Time: %{time_connect}s Total Time: %{time_total}s\n" -o /dev/null -s http://8.xxx.xxx.155
    echo "BGP (Multi-ISP) Pro EIP:"
    curl -w "Connect Time: %{time_connect}s Total Time: %{time_total}s\n" -o /dev/null -s http://8.xxx.xxx.233
    }
    === Starting EIP Comparison Test ===
    BGP (Multi-ISP) EIP:
    Connect Time: 0.228865s Total Time: 0.458878s
    BGP (Multi-ISP) Pro EIP:
    Connect Time: 0.079525s Total Time: 0.159364s
    ```
    

## 计费说明

BGP（多线）\_精品 EIP 与BGP（多线）EIP 计费单价不同，可参考[按量付费](https://help.aliyun.com/zh/eip/pay-as-you-go/)和[包年包月](https://help.aliyun.com/zh/eip/subscription)。

## 常见问题

### **BGP（多线）EIP是否支持转换为BGP（多线）\_精品EIP？**

不支持。EIP 的线路类型仅在创建时可选，创建完成后不支持转换线路类型。