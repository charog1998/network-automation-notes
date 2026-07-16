共享带宽提供地域级带宽共享和复用功能。创建共享带宽实例后，您可以将同地域下的EIP添加到共享带宽实例中，复用共享带宽中的带宽，统一管理公网出口，节省公网带宽使用成本。您可以将EIP绑定到云服务器ECS、公网NAT网关、传统型负载均衡CLB等，绑定后这些产品也可以使用共享带宽。本文为您介绍ECS实例如何通过共享带宽实现公网出口统一。

## **无公网IP的**ECS**实例**使用共享带宽

您可以在创建EIP的同时将EIP添加到共享带宽中，然后将EIP绑定到无公网IP的ECS实例，统一管理公网出口。具体实现流程如下：

1.  在ECS实例所属地域购买共享带宽实例。具体操作，请参见[创建共享带宽实例](https://help.aliyun.com/zh/internet-shared-bandwidth/user-guide/create-an-internet-shared-bandwidth-instance)。
    
2.  购买EIP并添加到共享带宽。
    
    -   如果您在ECS实例所属地域下没有可用的EIP，请选择**购买EIP并添加到带宽包**方式。
        
    -   如果您在ECS实例所属地域下有可用的EIP，请选择**从已有EIP列表选取**方式。
        
    
    具体操作，请参见[添加EIP](https://help.aliyun.com/zh/internet-shared-bandwidth/user-guide/associate-eips-with-an-internet-shared-bandwidth-instance)。
    
3.  将EIP绑定到ECS实例。具体操作，请参见[绑定云资源](https://help.aliyun.com/zh/internet-shared-bandwidth/user-guide/associate-an-eip-with-a-cloud-instance#steps-wwr-584-zps)。
    

## **已绑定EIP的**ECS**实例**使用共享带宽

您可以直接将ECS实例所绑定的EIP添加到共享带宽中。具体实现流程如下：

1.  在ECS实例所属地域购买共享带宽实例。具体操作，请参见[创建共享带宽实例](https://help.aliyun.com/zh/internet-shared-bandwidth/user-guide/create-an-internet-shared-bandwidth-instance)。
    
2.  将ECS实例所绑定的EIP添加到共享带宽中。
    
    此时，请选择**从已有EIP列表选取**方式。具体操作，请参见[添加EIP](https://help.aliyun.com/zh/internet-shared-bandwidth/user-guide/associate-eips-with-an-internet-shared-bandwidth-instance)。
    

## **使用固定公网IP的**ECS**实例**使用共享带宽

您可以先将ECS实例的固定公网IP转换为EIP，然后再将该EIP加入到共享带宽中，统一管理公网出口。具体实现流程如下：

1.  在ECS实例所属地域购买共享带宽实例。具体操作，请参见[创建共享带宽实例](https://help.aliyun.com/zh/internet-shared-bandwidth/user-guide/create-an-internet-shared-bandwidth-instance)。
    
2.  将ECS实例的将固定公网IP转换为EIP。具体操作及相关限制，请参见[专有网络ECS实例的固定公网IP转换为EIP](https://help.aliyun.com/zh/eip/convert-an-automatically-assigned-public-ip-address-to-an-eip-for-a-vpc-connected-ecs-instance)。
    
3.  将已绑定ECS实例的EIP加入共享带宽。
    
    此时，请选择**从已有EIP列表选取**方式。具体操作，请参见[添加EIP](https://help.aliyun.com/zh/internet-shared-bandwidth/user-guide/associate-eips-with-an-internet-shared-bandwidth-instance)。
    

## **经典网络中的**ECS**实例**使用共享带宽

经典网络中的ECS实例使用共享带宽，需先将ECS实例迁移至专有网络。具体实现流程如下：

1.  在ECS实例所属地域购买共享带宽实例。具体操作，请参见[创建共享带宽实例](https://help.aliyun.com/zh/internet-shared-bandwidth/user-guide/create-an-internet-shared-bandwidth-instance)。
    
2.  将ECS实例从经典网络迁移至专有网络。具体操作，请参见[ECS实例从经典网络迁移到专有网络](https://help.aliyun.com/zh/vpc/use-cases/migrate-ecs-instances-from-classic-network-to-vpc#task-1512598)。
    
3.  根据及以下信息，使ECS实例可以使用共享带宽中的带宽。
    
    -   如果迁移至专有网络的ECS实例没有公网IP，您可以将加入共享带宽的EIP绑定到ECS实例。具体操作，请参见[无公网IP的ECS实例使用共享带宽](#5350d4804debf)。
        
    -   如果迁移至专有网络的ECS实例使用了固定公网IP，您可以固定公网IP转换为EIP，然后将EIP添加到共享带宽。具体操作，请参见[使用固定公网IP的ECS实例使用共享带宽](#e98a78c04dgau)。