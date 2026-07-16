您可以使用高速通道、VPN网关产品，实现阿里云VPC与用户本地数据中心、办公终端或其他云厂商网络互通。

## **VPC连接本地数据中心**

### **选择连接方案**

常见的有如下两种连接方案：

-   专线：通过运营商物理专线将本地数据中心网络连接到阿里云接入点机房。在物理专线两端距离很远的情况下，仍可以提供低时延、低丢包率和高带宽的内网级通信质量。
    
-   VPN：通过建立公网加密隧道的方式，实现本地数据中心与阿里云VPC之间建立安全可靠的网络连接。VPN连接质量会受到公网网络质量的影响。
    

| **连接方式** | **专线** | **VPN** |
| --- | --- | --- |
| 网络时延 | 低   | 中   |
| 建设周期 | 长   | 短   |
| 总体成本 | 高   | 低   |
| 安全性 | 高   | 中   |
| 扩展便捷性 | 低   | 高   |

### **使用专线连接**

本地数据中心使用专线连接到阿里云，您需要使用到[高速通道](https://help.aliyun.com/zh/express-connect/product-overview/what-is-express-connect/)产品。

连接过程中您需要进行的操作：

1.  申请物理专线端口，并完成您本地数据中心设备到阿里云接入点机房设备的[物理专线连接](https://help.aliyun.com/zh/express-connect/user-guide/what-is-a-physical-connection/)。物理专线类型分为独享专线和共享专线，会涉及到运营商工勘、专线铺设、布线施工等工作，整个施工周期预计按月为单位，建议您提前做好时间与预算规划。
    
    1.  独享专线：运营商从您的本地数据中心机房，新增一条专线并连接到阿里云接入点机房，整个施工周期预计需要1至3个月。该条专线及对应端口为您独有。
        
    2.  共享专线：部分运营商会预先与阿里云接入点建立连接，使用共享专线需要运营商从运营商的接入点新增专线，并连接到您的本地数据中心机房，整个施工周期一般在1个月内。在这种连接方式下，运营商接入点和阿里云接入点之间的连接是多租户共享。
        
2.  配置[边界路由器VBR](https://help.aliyun.com/zh/express-connect/user-guide/what-is-a-virtual-border-router/)、[专线网关ECR](https://help.aliyun.com/zh/express-connect/user-guide/ecr/)实例，并完成与VPC的连接。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7002994571/CAEQWhiBgIC9yJXSvhkiIDQ0YjkxYTI4NTQ5NDQ3NTM5M2JhNTBhODI0NjVjNDlm5274221_20250627113930.173.svg)

其他建议：

1.  为了避免单条物理专线可能因外界不可抗力导致网络中断（例如专线某处被误挖断），您可以通过双专线、双接入点的方式，提升物理专线链路可靠性。对于非核心业务，您可考虑[使用专线+VPN做主备](https://help.aliyun.com/zh/cloud-network-well-architected-design/dedicated-line-to-build-hybrid-cloud-multi-cloud-network#b47123fe77xk2)，降低总体成本。
    
2.  由于专线流量本身没有加密机制，而部分行业又因安全合规政策，要求敏感数据即使通过专线传输也需要进行加密，此时您可以参考：[通过私网VPN网关实现物理专线加密通信](https://help.aliyun.com/zh/cloud-network-well-architected-design/build-a-branch-to-cloud-network-by-ipsec-vpn#18797162c8xki)。
    
3.  实际生产环境中，通常有多个VPC需要与本地数据中心互通，同时VPC之间也需要互通，人工配置路由相对繁琐，您可以考虑更加便捷的组网方式。您可以通过将专有网络VPC与专线网关ECR均连接至[转发路由器TR](https://help.aliyun.com/zh/cen/product-overview/how-transit-routers-work)，结合BGP动态路由实现全网高效互联。动态路由能够根据网络拓扑的变化自动调整路由表，减少人工配置的工作量，降低组网配置复杂度。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7002994571/CAEQWhiBgIDA37SRvxkiIDY1MTc4ZTk2MDYwOTQ5YjZhY2JlZTcxMGYzMGYwMThl5274221_20250627113930.173.svg)
    

### **使用VPN连接**

本地数据中心使用VPN连接到阿里云，推荐您使用[IPsec-VPN](https://help.aliyun.com/zh/vpn/sub-product-ipsec-vpn/product-overview/what-is-ipsec-vpn)产品。

IPsec-VPN有2种使用方式，主要区别如下：

| **使用方式** | **绑定VPN网关** | **绑定转发路由器TR** |
| --- | --- | --- |
| 应用场景 | 本地数据中心仅能与VPN网关实例所在的VPC互通。 | 本地数据中心可以通过[转发路由器TR](https://help.aliyun.com/zh/cen/product-overview/how-transit-routers-work)实例与[云企业网CEN](https://help.aliyun.com/zh/cen/product-overview/what-is-cen/)内的任意VPC、其他本地数据中心互通。 |
| 双隧道时实现高可用链路的方式 | 主备链路 | ECMP链路 > ECMP（Equal-Cost Multipath Routing）通过多路径同时分担流量，实现负载均衡和链路备份，提升网络效率和可靠性。 |
| IPsec连接带宽是否可扩充 | 否   | 是。可以创建多个IPsec连接，通过ECMP链路同时传输流量，从而间接实现带宽扩充。 |

## 绑定VPN网关

IPsec连接绑定VPN网关场景下，两条隧道一主一备。在一条隧道故障后，可以切换至另一条隧道进行传输。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7002994571/CAEQWhiBgMDtqrmjvxkiIDMxYzg5ZTQ4ZWM0NjQyZWRiMjEzNGU1M2M3MGQyMWRl5274221_20250627113930.173.svg)

实际生产环境中，部分企业在进行网络设计时往往会设计单独的DMZ VPC，用于统一公网出入口管控、安全隔离公网流量。您可参考该方案设计VPN上云：[通过VPN网关连接到DMZ VPC方式（主备隧道）](https://help.aliyun.com/zh/cloud-network-well-architected-design/build-a-branch-to-cloud-network-by-ipsec-vpn#28526b1963ehl)。

## 绑定转发路由器TR

IPsec连接绑定转发路由器TR场景下，两条隧道自动形成ECMP链路，本地网关设备也开启ECMP时，两条隧道均传输流量。在一条隧道故障后，可以切换至另一条隧道进行传输。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7002994571/CAEQWhiBgMDJv7ijvxkiIDU1ZTNjZDg5YTBmNDQ4Y2JhNWFjZTgzNDc1Y2IxYjU15274221_20250627113930.173.svg)

## **VPC连接其他云（多云）**

VPC连接其他云，与[VPC连接本地数据中心](#523f526526ogz)类似。您可以将其他云视为“特殊的本地数据中心”，使用专线或IPsec-VPN进行连接，构建多云环境。

以阿里云VPC与AWS VPC进行互通为例。

## 专线连接多云

建议双专线、双接入点等方式，提升专线链路可靠性。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7002994571/CAEQWhiBgMCwma2ivxkiIDQ5NDYxYmNiNjU3NjQ3NzFiYjgzZTUyNDJiMmY0Njdi5274221_20250627113930.173.svg)

多云环境下，往往有多个VPC需要互通，人工配置路由相对繁琐，您可以通过将专有网络VPC与专线网关ECR均连接至[转发路由器TR](https://help.aliyun.com/zh/cen/product-overview/how-transit-routers-work)，结合BGP动态路由实现全网高效互联。动态路由能够根据网络拓扑的变化自动调整路由表，减少人工配置的工作量，降低组网配置复杂度。

![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=)

## IPsec-VPN连接多云

阿里云和AWS平台下的IPsec-VPN连接均支持双隧道模式，但由于AWS平台的两条隧道默认关联至同一个客户网关，而阿里云侧两条隧道拥有不同的IP地址，导致AWS平台和阿里云侧的两条隧道无法做到一一对应建立连接。

为确保阿里云侧IPsec-VPN连接下两条隧道同时启用，您需要在AWS平台创建两个站点到站点的VPN连接，每个站点到站点VPN连接关联不同的客户网关。

![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=)

多云环境下，往往有多个VPC需要互通，人工配置路由相对繁琐，您可以通过将IPsec连接绑定至[转发路由器TR](https://help.aliyun.com/zh/cen/product-overview/how-transit-routers-work)，结合BGP动态路由实现全网高效互联。动态路由能够根据网络拓扑的变化自动调整路由表，减少人工配置的工作量，降低组网配置复杂度。

> 阿里云IPsec-VPN绑定转发路由器TR时，默认开启ECMP，建议您在AWS侧也开启ECMP。如果AWS侧未开启ECMP，则AWS流向阿里云的流量需要指定连接，阿里云流向AWS的流量则会根据ECMP自动选择隧道。

![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=)

## **办公终端连接VPC**

办公终端使用VPN连接到阿里云VPC，推荐您使用[SSL-VPN](https://help.aliyun.com/zh/vpn/sub-product-ssl-vpn/product-overview/what-is-ssl-vpn)产品。

SSL-VPN支持市场主流的桌面客户端（Windows、Linux、macOS）和移动客户端（Android、iOS）接入。

![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=)

如果企业一部分应用同时部署在本地数据中心，您可以为VPN网关实例一并开启IPsec-VPN和SSL-VPN功能，同时连接本地数据中心和客户端。

连接建立后，客户端和本地数据中心均可以访问VPC，且客户端和本地数据中心之间可以互相通信。

![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=)