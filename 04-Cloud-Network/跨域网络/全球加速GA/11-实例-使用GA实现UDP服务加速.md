UDP协议因其低延迟和无连接的特性，广泛应用于实时通信、在线游戏、视频流媒体等场景。然而，由于跨地域网络传输的复杂性，UDP数据包在传输过程中容易出现数据丢包、抖动和延迟等问题。全球加速服务支持UDP协议监听，并依托阿里云优质BGP带宽和全球传输网络，实现全球网络就近接入，可有效改善全球多地域终端用户的访问速度和体验。

## **场景示例**

某游戏公司新推出了一款在线小游戏，游戏服务器部署在德国（法兰克福）的阿里云上，并通过UDP端口4000对外提供服务。该游戏在测试阶段发现了以下问题：

-   用户量快速增长，主要集中在中国香港地域。
    
-   经常出现延迟、丢包、掉线频繁等问题，影响终端用户游戏体验。
    

为解决以上问题，该游戏公司部署了全球加速实例，使终端用户访问请求就近接入阿里云加速网络，有效提升了用户的游戏体验。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0178180871/CAEQUBiBgIDcx7_PlBkiIDcyNjA3MDA0YmI0NzRlNmU4YjUyM2Y2MzE2MWE2NTEx3963382_20230830144006.372.svg)

## 前提条件

-   您已经在德国（法兰克福）的服务器上部署了UDP 4000服务。
    
    本文以Alibaba Cloud Linux 3操作系统为例，并使用Socat部署UDP Echo服务，便于测试客户端到UDP服务端的时延。
    
    **参考示例：阿里云ECS部署UDP测试服务**
    
    ```
    # 安装Socat
    yum install socat
    # 启动Socat，端口为4000
    nohup socat -v UDP-LISTEN:4000,fork PIPE 2>/dev/null &
    ```
    
-   您已经在后端服务的访问策略（例如[安全组](https://help.aliyun.com/zh/ecs/user-guide/add-a-security-group-rule)）中，允许以下IP地址访问服务端口（本文场景为UDP 4000）：
    
    -   [终端节点出公网IP](https://help.aliyun.com/zh/ga/support/faq-about-endpoint-groups#section-dk6-kxp-j5m)：如果GA与后端服务通过[公网连接](https://help.aliyun.com/zh/ga/user-guide/overview-4/#5b9fd4756expi)时，请放通GA终端节点出公网IP。
        
    -   后端服务所属交换机网段：如果GA与后端服务通过[私网连接](https://help.aliyun.com/zh/ga/user-guide/overview-4/#5b9fd4756expi)时，请放通后端服务所属交换机网段。
        

## **操作步骤**

### **步骤一：配置实例基础信息**

本文以按量付费的标准型GA实例为例。

1.  在[全球加速控制台](https://ga.console.aliyun.com/list)的**标准型实例** > **实例列表**列表页面，单击**创建标准型按量付费实例**。
    
2.  在**实例基础配置**向导页面，配置基础信息，单击**下一步**。
    
    ![GA基础配置.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8676661371/p842361.png)
    

### 步骤二：**配置加速区域**

在**配置加速区域**向导页面，添加加速地域并为其分配带宽，然后单击**下一步**。

本文以中国香港地域为例，**加速区域**添加为**中国香港**，**公网质量类型**配置为**BGP(多线)**，[加速地域其他参数配置](https://help.aliyun.com/zh/ga/user-guide/add-and-manage-acceleration-areas)可保持默认值或根据实际情况修改。

**说明**

如果还存在中国内地地域客户端，您可以将**公网质量类型**配置为**BGP精品**。BGP精品线路在为中国内地客户端提供服务时，通过运营商精品公网直连中国内地，时延更低。

### 步骤三：**配置监听**

在**配置监听**配置向导页面，配置转发协议与端口，然后单击**下一步**。

本文场景中，**协议**配置为**UDP**，**端口**配置为**4000**，其他参数可保持默认值或根据实际情况修改。监听配置详细信息，请参见[添加和管理智能路由类型监听](https://help.aliyun.com/zh/ga/user-guide/add-and-manage-intelligent-routing-listeners)。

### 步骤四：**配置终端节点组与终端节点**

1.  在**配置终端节点组**配置向导页面，配置终端节点后端服务，然后单击**下一步**。
    
    本文场景中，**地域**选择**德国**，**后端服务类型**选择**ECS**，**后端服务**选择已部署UDP Echo服务的服务器，其他参数可保持默认值或根据实际情况修改。终端节点组配置详细信息，请参见[添加和管理智能路由类型监听的终端节点组](https://help.aliyun.com/zh/ga/user-guide/create-and-manage-the-endpoint-groups-of-intelligent-routing-listeners)。
    
    在**数据跨境合规承诺**区域，勾选**同意以上合规承诺**，然后单击**下一步**。
    
2.  在**配置审核**配置向导页面，确认全球加速的配置信息，然后单击**提交**。
    

### 步骤五：访问测试

本文以Alibaba Cloud Linux 3操作系统为例进行访问测试。

#### **测试连通性**

在接入地域（本文为中国香港地域）的电脑中打开命令行窗口，执行以下命令测试连通性。

```
echo "Hello, UDP!" | socat - UDP4:<服务IP>:4000
```

未使用全球加速时，使用后端服务器公网IP测试：

```
[root@iZbrxxx ~]# echo "Hello, UDP!" | socat - UDP4:47.91xxx:4000
Hello, UDP!
```

使用全球加速后，使用全球加速为中国香港加速地域分配的加速IP测试：

```
[root@iZbrxxx ~]# echo "Hello, UDP!" | socat - UDP4:47.98.xxx.xxx:4000
Hello, UDP!
```

经验证，使用全球加速后，UDP服务可正常访问。

#### **测试加速效果**

1.  在接入地域（本文为中国香港地域）的电脑中打开命令行窗口，执行以下命令部署UDPing工具。
    
    ```
    # 下载UDPing工具　
    wget https://networktools-public.oss-cn-hangzhou.aliyuncs.com/ga/udping/udping.py
    # 赋予UDPing工具执行权限
    chmod +x udping.py
    ```
    
2.  执行以下命令测试加速效果。
    
    ```
    ./udping.py <服务IP> <监听端口>
    ```
    
    未使用全球加速时，使用后端服务器公网IP测试：
    
    ```
    [root@iZbxxx ~]# ./udping.py 47.91.xxx.xxx 4000
    udping 47.91.xxx via port 4000 with 64 bytes of payload
    Reply from 47.91.xxx    seq=0 time=234.26 ms
    Reply from 47.91.xxx    seq=1 time=233.81 ms
    Reply from 47.91.xxx    seq=2 time=233.79 ms
    Reply from 47.91.xxx    seq=3 time=233.80 ms
    ^C
    --- ping statistics ---
    4 packets transmitted, 4 received, 0.00% packet loss
    ```
    
    使用全球加速后，使用全球加速为中国香港加速地域分配的加速IP测试：
    
    ```
    [root@iZbpxxx ~]# ./udping.py 47.98.xxx.xxx 4000
    udping 47.98.xxx.xxx via port 4000 with 64 bytes of payload
    Reply from 47.98.xxx.xxx seq=0 time=146.93 ms
    Reply from 47.98.xxx.xxx seq=1 time=146.05 ms
    Reply from 47.98.xxx.xxx seq=2 time=145.08 ms
    Reply from 47.98.xxx.xxx seq=3 time=145.02 ms
    ^C
    --- ping statistics ---
    4 packets transmitted, 4 received, 0.00% packet loss
    rtt min/avg/max = 145.02/145.77/146.93 ms
    ```
    
    加速效果对比如下：
    
    | **加速前平均时延（单位：ms）** | **加速后平均时延（单位：ms）** | **加速数据参考（百分比）** |
    | --- | --- | --- |
    | 233.915 | 145.77 | 速度提升约37.69% |
    

**说明**

本文示例与数据仅供参考。使用GA的加速效果以您的实际业务测试为准。

## **常见问题**

### UDP监听协议是否支持客户端亲和性和保持客户端源IP功能？

支持。

-   您可以在[创建GA实例](https://help.aliyun.com/zh/ga/user-guide/create-and-manage-standard-ga-instances)或为已有GA实例[添加UDP监听](https://help.aliyun.com/zh/ga/user-guide/add-and-manage-intelligent-routing-listeners#title-i0g-o2d-oy6)时配置客户端亲和性。
    
-   您可以在配置终端节点时，为UDP监听开启[保持客户端源IP](https://help.aliyun.com/zh/ga/user-guide/preserve-client-ip-addresses#100a8a573cosr)。
    

### **单个UDP监听是否可以添加多个端口？**

-   单个智能路由类型的UDP监听
    
    GA实例付费模式的不同，单个UDP监听可添加的端口数有所差别，默认最多可配置30个端口（或端口段）。详情请参见[智能路由类型监听端口](https://help.aliyun.com/zh/ga/user-guide/overview-2/#2c13383d757v0)。
    
    -   多个端口之间使用半角逗号（,）分隔，例如80,90,8080。
        
    -   多个连续的端口可以使用短划线（-）表示监听端口范围，例如80,81,82,83端口，可以使用80-83表示。
        
-   单个自定义路由类型的UDP监听
    
    在可配置端口范围内（1~65499）不作数量限制。更多信息，请参见[自定义路由类型监听端口](https://help.aliyun.com/zh/ga/user-guide/overview-2/#p-061-1xe-4y2)。
    

## **相关文档**

-   [CreateListener](https://help.aliyun.com/zh/ga/developer-reference/api-ga-2019-11-20-createlistener#doc-api-Ga-CreateListener) ：为全球加速实例创建UDP监听。
    
-   [UpdateListener](https://help.aliyun.com/zh/ga/developer-reference/api-ga-2019-11-20-updatelistener#doc-api-Ga-UpdateListener)：修改全球加速实例下指定监听的配置。
    
-   [DeleteListener](https://help.aliyun.com/zh/ga/developer-reference/api-ga-2019-11-20-deletelistener#doc-api-Ga-DeleteListener)：删除全球加速实例下指定的监听。