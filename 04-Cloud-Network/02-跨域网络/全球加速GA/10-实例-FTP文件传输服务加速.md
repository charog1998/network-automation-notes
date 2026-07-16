全球加速 GA（Global Accelerator）服务当前支持四层与七层协议的加速，其中包括FTP协议。本文为您介绍FTP协议的相关要点，并以当前主流的服务端vsftpd和客户端FileZilla为例，介绍如何使用全球加速服务加速FTP服务。

## 背景信息

FTP（File Transfer Protocol）是一种文件传输协议，基于客户端和服务器架构，支持以下两种工作模式：

主动模式的工作流程如下：

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9087647771/CAEQQRiBgMDvkbSZ9xgiIGIwOTQ5NGRjMTA3ZDQzZjNiOTBjMWEyMDI0YTZiZWNh3963382_20230830144006.372.svg)

| **序号** | **流程描述** |
| --- | --- |
| ①   | 客户端向21端口发送控制连接请求，建立控制连接。 |
| ②   | 客户端向21端口报告可以用于数据传输的端口2100。 |
| ③   | 服务端20端口主动连接客户端的2100端口，进行数据传输。 |
| ④   | 数据传输完成后，服务端主动关闭连接。 |

被动模式的工作流程如下：

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9087647771/CAEQQRiBgMDXqruZ9xgiIDlkNTVmNzk5MjUxNTQ4MGE4OTQwMWUwNThiNzY3OGQy3963382_20230830144006.372.svg)

| **序号** | **流程描述** |
| --- | --- |
| ①   | 客户端向21端口发送控制连接请求，建立控制连接。 |
| ②   | 服务端告知客户端数据传输端口为2120。 |
| ③   | 客户端重新开启一个端口连接服务端的数据传输端口2120，并进行数据传输。 |
| ④   | 数据传输完成后，服务端主动关闭连接。 |

GA不支持服务端主动发起连接，因此只能支持FTP的被动模式。

FTP支持以下三种认证模式：

## 前提条件

-   FTP服务器安全组已放通入方向21和2100~2120端口。
    
-   FTP服务器已拥有公网IP地址。
    

**说明**

本文以阿里云服务器ECS（Elastic Compute Service）作为FTP服务器。关于阿里云ECS如何配置安全组和公网IP，请参见[安全组操作导航](https://help.aliyun.com/zh/ecs/user-guide/work-with-security-groups#concept-2556610)和[EIP 快速上手](https://help.aliyun.com/zh/eip/product-overview/getting-started#task-2102958)。

## **使用限制**

如果您的GA实例无法加速FTP服务，可能是由于实例版本不支持。如需使用，请向商务经理申请升级实例。

## 配置步骤

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9087647771/CAEQQRiBgMCLp76Z9xgiIGM5MTI5Y2MzODFlZDQ3NDRhZGM0MzI1MDdjOWNiNmY24210981_20240213143608.814.svg)

**说明**

本文以按量付费的标准型全球加速实例为例，为您介绍如何配置全球加速以实现FTP文件传输服务加速。创建按量付费的标准型全球加速实例前，请先了解以下信息：

-   按量付费全球加速实例采用**按流量**的带宽计费方式，无需绑定带宽包。接入全球加速网络产生的流量费用统一由云数据传输 CDT（Cloud Data Transfer）结算出账。更多信息，请参见[流量计费](https://help.aliyun.com/zh/ga/product-overview/pay-by-data-transfer#concept-2261223)。
    
-   首次使用按量付费GA实例，您需要在[服务开通](https://common-buy.aliyun.com/?commodityCode=ga_afterpay_public_cn)页面根据提示开通按量付费全球加速服务。
    

## 步骤一：安装FTP软件并配置FTP服务器

以下步骤介绍如何在操作系统为Alibaba Cloud Linux 3的ECS实例上安装并配置vsftpd。当您使用不同操作系统和vsftpd软件版本时，可能需要根据实际情况调整命令和参数配置。

1.  执行以下命令安装vsftpd。
    
    ```
    yum install -y vsftpd
    ```
    
2.  使用本地用户模式进行认证，创建FTP用户。
    
    ```
    # 创建linux用户ftpdemo
    adduser ftpdemo
    # 修改用户ftpdemo的密码
    passwd ftpdemo
    # 创建一个供FTP服务使用的文件目录
    mkdir /var/ftp/demo
    # ftpdemo用户拥有此目录
    chown -R ftpdemo:ftpdemo /var/ftp/demo
    ```
    
3.  配置vsftpd。
    
    ```
    vim /etc/vsftpd/vsftpd.conf
    ```
    
4.  修改配置文件如下：
    
    ```
    # 除下面提及的参数外，其他参数保持默认值即可
    # 修改下列参数的值
    # 禁止匿名登录FTP服务器
    anonymous_enable=NO
    # 允许本地用户登录FTP服务器
    local_enable=YES
    # 监听IPv4 sockets
    listen=YES
    # 关闭监听IPv6 sockets
    # listen_ipv6=NO
    # 添加下列参数
    # 设置本地用户登录后所在目录
    local_root=/var/ftp/demo
    # 开启被动模式
    pasv_enable=YES
    # 关闭安全检查，需配置为YES，否则FTP客户端不能上传文件到FTP服务器
    pasv_promiscuous=YES
    # 设置被动模式下，建立数据传输可使用的端口范围的最小值
    pasv_min_port=2100
    # 设置被动模式下，建立数据传输可使用的端口范围的最大值
    pasv_max_port=2120
    ```
    
5.  按Esc退出编辑模式，然后输入`:wq`并回车以保存并关闭文件。
    
6.  执行以下命令查看或启动vsftpd服务。
    
    ```
    # 重启vsftpd服务
    systemctl restart vsftpd.service
    # 查看vsftpd服务的状态
    systemctl status vsftpd
    ```
    

## 步骤二：配置实例基础信息

1.  登录[全球加速管理控制台](https://ga.console.aliyun.com/list)。
    
2.  在**实例列表**页面，单击**创建标准型按量付费实例**。
    
3.  在**实例基础配置**向导页面，根据以下信息进行配置，然后单击**下一步**。
    
    | **配置** | **说明** |
    | --- | --- |
    | **全球加速实例名称** | 输入全球加速实例名称。 |
    | **实例计费方式** | 默认为**按量付费**。 使用按量付费的标准型全球加速实例，产生的费用包括：实例费、性能容量单位CU费和流量费。 - 关于实例费、性能容量单位CU费的更多信息，请参见[按量付费全球加速实例计费](https://help.aliyun.com/zh/ga/product-overview/billing-of-pay-as-you-go-ga-instances)。 - 关于流量费，请参见[流量计费](https://help.aliyun.com/zh/ga/product-overview/pay-by-data-transfer)。 |
    | **资源组** | 选择标准型全球加速实例所属的资源组。 该资源组为当前阿里云账号在资源管理中创建的资源组。更多信息，请参见[创建资源组](https://help.aliyun.com/zh/resource-management/resource-group/user-guide/create-a-resource-group#task-xpl-kjm-4fb)。 |
    

## **步骤三：配置加速区域**

为全球加速实例配置加速区域，指定可以加速访问后端服务的用户所在的地域并为其分配加速带宽。

在**配置加速区域**向导页面，根据以下信息配置加速区域，然后单击**下一步**。

| **配置** | **说明** |
| --- | --- |
| **加速区域** | 在下拉列表中选中需要进行访问加速的一个地域或多个地域，然后单击**添加至列表**。 本文选中**中国（香港）**地域。 |
| **分配带宽** |   |
| **带宽峰值** | 设置加速地域的带宽。每个加速地域支持分配的带宽范围为2~10000 Mbps。 此处带宽峰值仅作限速，产生的流量费用统一由CDT结算出账。 本文保持默认值**200** Mbps。 **重要** 如果带宽峰值设置过低，可能出现限速从而导致流量被丢弃，请合理规划带宽峰值，确保和业务需求匹配。 |
| **IP地址协议** | 选择接入全球加速服务的IP地址协议。 本文保持默认值**IPv4**。 |
| **公网质量类型** | 选择接入全球加速服务的公网质量类型。 本文选择**BGP（多线）**。 |

## **步骤四：配置监听**

监听负责检查连接请求，根据您指定的端口和协议处理来自客户端的入站连接。每个监听都关联一个终端节点组，通过指定要分发流量的地域，将终端节点组与监听关联。关联后，全球加速会将流量分配到与监听关联的终端节点组内的最佳终端节点。

在**配置监听**向导页面，配置监听，然后单击**下一步**。

此处仅介绍本文强相关的配置项，其余配置项可保持默认配置。更多信息，请参见[添加和管理智能路由类型监听](https://help.aliyun.com/zh/ga/user-guide/add-and-manage-intelligent-routing-listeners#section-ncm-izu-muk)。

| **配置** | **说明** |
| --- | --- |
| **监听名称** | 输入监听的名称。 |
| **路由类型** | 选择路由类型。 本文选择**智能路由**。 |
| **协议** | 选择监听的协议类型。 本文选择**TCP**。 |
| **端口** | 指定用来接收请求并向终端节点进行转发的监听端口，端口取值范围：**1-65499**。 本文输入21,2100-2120。2100-2120为[步骤一：安装FTP软件并配置FTP服务器](#section-tay-z8t-7oq)中FTP服务器中vsftpd.conf配置文件的pasv\\_min\\_port~pasv\\_max\\_port。 |
| **客户端亲和性** | 选择是否保持客户端亲和性。保持客户端亲和性，即客户端访问有状态的应用程序时，可以将来自同一客户端的所有请求都定向到同一终端节点。 本文选择**源 IP**。 |

## **步骤五：配置终端节点组和终端节点**

1.  在****配置终端节点组****配置向导页面，根据以下信息配置终端节点组和终端节点，然后单击**下一步**。
    
    此处仅介绍本文场景强相关配置项，关于终端节点配置项更多信息，请参见[添加和管理智能路由类型监听的终端节点组](https://help.aliyun.com/zh/ga/user-guide/create-and-manage-the-endpoint-groups-of-intelligent-routing-listeners)。
    
    **说明**
    
    FTP协议在客户端和服务器之间建立了两条通信链路、分别是控制链路和数据链路。其中，控制链路负责FTP会话过程中FTP命令的发送和接收。数据链路则负责数据的传输。
    
    在服务所在地域（终端节点组所属地域），GA实例有多个终端节点出公网IP，但部分FTP服务器配置了连接检查，要求控制链路和数据链路的客户端IP必须相同，这时需要关闭FTP服务端的源IP检查，或者需要您联系客户经理开通GA源一致性。
    
    | **配置** | **说明** |
    | --- | --- |
    | ****地域**** | 选择终端节点组所属的地域。 本文选择**美国（硅谷）**。 |
    | **终端节点配置** | 终端节点是客户端请求访问的目标主机。您可以根据以下信息配置终端节点： - **后端服务类型**：选择**阿里云公网 IP**。 - **后端服务**：输入要加速的后端服务的IP地址。本文输入FTP服务器的公网IP。 - **权重**：输入终端节点的权重，权重取值范围：0~255。全球加速根据您配置的权重按比例将流量路由到终端节点。 本文保持默认值**255**。 **警告** 如果某个终端节点的权重设置为0，全球加速将终止向该终端节点分发流量，请您谨慎操作。 |
    | **保持客户端源IP** | 选择是否保持客户端源IP。 选择保持客户端源IP，后端服务器可以通过该功能获取客户端源IP。更多信息，请参见[保持客户端源IP](https://help.aliyun.com/zh/ga/user-guide/preserve-client-ip-addresses#task-2416386)。 本文保持默认配置**不保持**。 |
    
2.  在**配置审核**向导页面，确认信息，然后单击**提交**。
    
    **说明**
    
    创建GA实例预计耗时3~5分钟，请您耐心等待。
    
3.  **可选：**创建任务完成后，在创建任务详情列表下方，单击**进入实例详情**，然后在实例详情页，可选择**实例信息**、**监听**、**加速区域**等页签查看实例配置信息。
    

## 步骤六：客户端访问测试

本文以Windows Server 2022系统的本地主机作为FTP客户端，使用FileZilla进行文件传输。

1.  远程连接Windows实例。
    
    具体操作，请参见[使用远程桌面/Windows App远程连接Windows实例](https://help.aliyun.com/zh/ecs/user-guide/connect-to-a-windows-instance-by-using-a-username-and-password#concept-n31-wyx-wdb)。
    
2.  启动FileZilla软件。
    
    您可以访问[FileZilla官网](https://www.filezilla.cn/)下载安装FileZilla软件。
    
3.  在顶部菜单栏，选择**文件 > 站点管理器**。
    
4.  在**站点管理器**对话框，单击**新站点**，在**选择记录**区域设置站点名称，并在右侧**常规**区域配置传输信息。
    
    本文中站点名称设置为**GA加速**。
    
    ![FTP管理软件 zh.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5986799171/p757678.png)
    
    | **配置** | **说明** |
    | --- | --- |
    | **协议** | 选择**FTP-文件传输协议**。 |
    | **主机** | 输入FTP登录主机地址，即全球加速的加速IP。 |
    | **用户** | 输入FTP登录用户名ftpdemo。 |
    | **密码** | 输入FTP登录密码。 |
    
    表格中未提到的配置项可保持默认。
    
5.  单击**连接**，即可连接到FTP服务器。
    
    连接成功后，您可以对网站文件进行上传、下载、新建和删除等操作。FileZilla工具界面如下图所示。
    
    ![FTP服务上传文件 zh.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5986799171/p757682.png)
    
    各区域的作用如下表：
    
    | **序号** | **说明** |
    | --- | --- |
    | ①   | 显示命令、FTP连接状态和任务执行结果。 |
    | ②   | 本地区域，即本地硬盘。 |
    | ③   | 远程区域，即站点区域。双击目录图标可进入相关目录。 |
    | ④   | 记录区域，可查看FTP任务的队列信息和日志信息。 |
    
6.  打开命令行窗口，执行以下命令，查看数据包延迟情况。
    
    ```
    curl -o /dev/null -s -w "time_connect: %{time_connect}\ntime_starttransfer: %{time_starttransfer}\ntime_total: %{time_total}\n" ftp://<GA加速IP>/<文件路径> --user <username>:<password>
    ```
    
    其中：
    
    -   time\_connect：连接时间，从开始到建立TCP连接完成所用的时间，单位为秒。
        
    -   time\_starttransfer：开始传输时间。在客户端发出请求后，到后端服务器响应第一个字节所用的时间，单位为秒。
        
    -   time\_total：连接总时间。客户端发出请求后，到后端服务器响应会话所用的时间，单位为秒。
        
    
    经测试，使用全球加速后，降低了中国香港FTP客户端访问美国（硅谷）FTP服务器的延迟。
    
    图 1. 加速前的访问延迟情况
    
    ![FTP服务加速前.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5986799171/p758827.png)
    
    图 2. 加速后的访问延迟情况
    
    ![FTP服务加速后.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5986799171/p758829.png)
    
    **说明**
    
    使用全球加速服务加速FTP客户端访问FTP服务器的加速效果以您的实际业务测试为准。