当您在多个VPC中部署了业务，需要通过内网共享资源时，可通过云企业网实现VPC之间的互通。

本文以同一个地域内的2个VPC互通为例，帮助您熟悉云企业网的使用方法，您可以由此扩展到更多VPC内网互通。

## **场景示例**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0807426771/CAEQUBiBgMDeuf_XlhkiIDU1NjEzNDYyYjllYTRiYWRiNmYyNThmNzUzZTk0N2I34729461_20241028200639.331.svg)

如图，假设您在华东1（杭州）地域已经创建了2个VPC：

-   VPC1
    
    -   IPv4网段：10.0.0.0/16
        
    -   交换机1，位于可用区J，网段： 10.0.0.0/24
        
    -   交换机2，位于可用区K，网段：10.0.1.0/24 （在2个不同的可用区分别创建交换机，用于多可用区容灾）
        
    -   ECS1地址：10.0.0.1 （ECS用于验证连通性）
        
-   VPC2
    
    -   IPv4网段：172.16.0.0/16
        
    -   交换机1，位于可用区J，网段：172.16.0.0/24
        
    -   交换机2，位于可用区K，网段：172.16.1.0/24
        
    -   ECS2地址：172.16.0.1
        

那么您可以将2个VPC连接到云企业网的转发路由器，实现内网互通。

**重要**

规划网络时，请确保要互通的VPC网段没有重叠。

## **开始配置**

### **1 创建云企业网**

| 1. 打开[云企业网控制台](https://cen.console.aliyun.com/cen)，在**云企业网实例**菜单下，点击**创建云企业网实例**。 | ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8087572371/p872314.png) |
| --- | --- |
| 2. 在**创建云企业网实例**页面，输入**名称**为`cen1`，点击**确认**。 | ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8087572371/p872316.png) |
| 3. 创建后页面显示**云企业网实例创建成功。**单击**进入云企业网实例详情**。 | ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8087572371/p872461.png) |

### **2 创建转发路由器**

| 1. 在云企业网实例详情页面，点击**创建转发路由器**。 | ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8087572371/p872483.png) |
| --- | --- |
| 2. 在**创建转发路由器**的弹窗中，选择地域为**华东1（杭州）**，其他选项保持默认，最后单击**确认**。 | ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) |
| 3. 创建后页面显示**转发路由器创建成功！**单击右上角X号关闭弹窗。 | ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) |
| 4. 在云企业网实例详情页面，您可以看到已创建的转发路由器。 | ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) |

### **3 将VPC连接到转发路由器**

| 1. 在转发路由器的**操作**列下，单击**创建网络实例连接** > **创建地域内连接**。 | ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) |
| --- | --- |
| 2. 在**创建地域内连接**页面： - **实例类型**选择**专有网络（VPC）** - **连接名称**填写`attach1` - **网络实例**选择`VPC1` 其他选项保持默认，单击**确定创建**按钮。 **说明** 为实现多可用区容灾，系统会帮您自动勾选当前VPC下的2个可用区。如果您的VPC下仅有1个交换机，需要您至少再创建1个交换机，且这2个交换机必须位于不同可用区。 | ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) |
| 3. 页面显示**连接创建成功**后，表明您已将VPC1连接到转发路由器。接下来您可以单击**继续创建连接**，按照同样的步骤，将`VPC2`连接到转发路由器，并将**连接名称**填写为`attach2`。 | ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) |
| 4. 将`VPC2`连接到转发路由器之后，点击**返回列表**。 | ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) |
| 5. 单击**华东1（杭州）**地域转发路由器的**实例ID**后，您可以看到刚刚在转发路由器上创建的2个**VPC连接**，分别为`attach1`和`attach2`。 | ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) |

### **4 测试验证**

**说明**

操作前，请确保2台ECS的安全组规则允许VPC资源互访。具体操作，请参见[查询安全组规则](https://help.aliyun.com/zh/ecs/user-guide/view-security-group-rules#task-1357273)和[添加安全组规则](https://help.aliyun.com/zh/ecs/user-guide/add-a-security-group-rule#concept-sm5-2wz-xdb)。

登录ECS1，执行`ping`命令访问ECS2：

```
ping 172.16.0.1
```

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8087572371/p872790.png)

如上图所示，如果能`ping`通，则说明`VPC1`和`VPC2`的网络已连通。

## **更多操作**

-   可视化[查看刚刚创建的云企业网拓扑](https://help.aliyun.com/zh/cen/user-guide/view-resource-topology)
    
-   实现[跨地域VPC内网互通](https://help.aliyun.com/zh/cen/getting-started/use-enterprise-edition-transit-routers-to-connect-vpcs-across-regions-and-accounts)
    
-   通过[流日志](https://help.aliyun.com/zh/cen/user-guide/configure-a-flow-log)分析流经转发路由器的流量