本快速入门教程为您介绍如何在RAM中创建访问密钥AccessKey（AK），查看并获取访问AccessKey信息，并以阿里云CLI为例为您演示如何在程序或服务中使用AccessKey来访问阿里云资源。

**重要**

根据阿里云的最佳实践，程序或服务应尽可能避免直接使用AccessKey来访问阿里云资源。具体请参见：[程序身份最佳实践](https://help.aliyun.com/zh/ram/product-overview/best-practices-for-identity-and-access-control#0dfa54dde248n)。

## 什么是AccessKey

**访问密钥（AccessKey）** 是一个由 AccessKey ID 和 AccessKey Secret 组成的密钥对。AccessKey主要用于应用程序或服务调用阿里云API时向RAM验证身份。

AccessKey与一个具体的 RAM 用户关联，属于长期访问凭证。**因其长期有效性，一旦泄露将带来极高的安全风险。**

## **配置流程**

1.  [创建AccessKey](#5be3fd3deb0lc)：为指定的RAM用户生成AccessKey。
    
2.  [使用AccessKey调用API](#242916084fpyt)：配置阿里云CLI，并使用AccessKey直接或间接调用API。
    
3.  [清理资源](#5cdaf03bcb87y)：清理本地凭证配置，禁用并删除AccessKey，
    

## **准备工作**

-   已创建 RAM 用户。如果未创建，请参考[快速入门：创建RAM用户并授权](https://help.aliyun.com/zh/ram/product-overview/create-and-authorize-a-ram-user)进行创建。**请勿使用主账号来进行创建AccessKey的操作**。
    
-   具备操作权限。创建并查看AccessKey需要相应的RAM权限。建议为操作用户授予RAM管理员（`AliyunRAMFullAccess`）系统策略，然后在完成本教程后移除权限。
    
-   安装阿里云CLI，具体方法请参见[快速使用 CLI](https://help.aliyun.com/zh/cli/quickly-start-using-alibaba-cloud-cli#d689301388gc5)。
    

## **创建AccessKey**

1.  登录[RAM控制台](https://ram.console.aliyun.com/)，在左侧导航栏选择**身份管理** > **用户**。
    
2.  在用户列表中，找到目标 **RAM 用户**，单击其名称。
    
3.  在**AccessKey**页签中，单击**创建AccessKey**。
    
    **说明**
    
    每个 **RAM 用户**最多允许创建 2 个 **AccessKey**。一个正常使用，另一个在需要轮转时才创建，用于替换旧的AccessKey。如果当前用户已达到上限，建议为其他RAM用户创建，或在确认安全的情况下删除不再使用的AccessKey。
    
4.  在弹出的确认对话框中，选择**CLI**并勾选**我确认必须创建AccessKey**，单击**继续创建**。
    
5.  根据界面提示，完成安全验证（MFA）。
    
6.  在**创建AccessKey**对话框，单击**下载CSV文件**以保存**AccessKey ID**和**AccessKey Secret**，然后单击**确定**。
    
    **重要**
    
    **AccessKey Secret** 只在创建时显示一次，后续无法查看。请务必妥善保管。
    

## **使用AccessKey调用API**

**说明**

本教程使用阿里云CLI作为使用AccessKey的范例。如果您希望知道如何在代码中使用AK，请参见：

-   [使用Credential工具管理访问凭证-AK](https://help.aliyun.com/zh/sdk/developer-reference/v2-manage-python-access-credentials#49b9ce814b4r5)
    
-   [使用Credential工具管理访问凭证-AK及RamRoleArn](https://help.aliyun.com/zh/sdk/developer-reference/v2-manage-python-access-credentials#87d4cd004bvxe)
    

### **直接使用AccessKey**

此方法将AccessKey直接配置在客户端，操作简单，但存在密钥硬编码和权限过大的风险。生产环境中不推荐使用。

1.  为持有AccessKey的RAM用户授予RAM只读权限`AliyunRAMReadOnlyAccess`。
    
    1.  登录[RAM控制台](https://ram.console.aliyun.com/)，进入 **身份管理** > **用户** 页面。
        
    2.  找到目标 **RAM 用户**，单击 **操作** 列的 **新增授权**。
        
    3.  在 **新增授权** 步骤中，搜索并选中 `AliyunRAMReadOnlyAccess` 系统策略，然后单击 **确认新增授权**。
        
    4.  回到用户列表，单击目标**RAM用户**名称。在**权限管理** > **个人权限**页签下，确认可以看到`AliyunRAMReadOnlyAccess`权限。
        

2.  打开本地终端并执行以下命令，通过交互式配置身份凭证。
    
    ```
    aliyun configure --profile AkProfile
    ```
    
3.  根据命令行交互提示，依次输入在[创建AccessKey](#5be3fd3deb0lc)步骤中保存的 **AccessKey ID** 和 **AccessKey Secret**，并设置地域和语言。
    
    ```
    Configuring profile 'AkProfile' in 'AK' authenticate mode...
    Access Key Id []: <yourAccessKeyID>
    Access Key Secret []: <yourAccessKeySecret>
    Default Region Id []: cn-shanghai
    Default Output Format [json]: json (Only support json)
    Default Language [zh|en] en: en
    Saving profile[AkProfile] ...Done.
    ```
    
4.  如果AccessKey信息和其他配置正确，您将会在终端看到如下返回结果。如果遇到报错，请[删除缓存的阿里云CLI凭证配置](#fa8fc514a6i8d)，检查配置后再次执行[步骤2](#066309943fr63)中的命令。
    
    ```
    Configure Done!!!
    ..............888888888888888888888 ........=8888888888888888888D=..............
    ...........88888888888888888888888 ..........D8888888888888888888888I...........
    .........,8888888888888ZI: ...........................=Z88D8888888888D..........
    .........+88888888 ..........................................88888888D..........
    .........+88888888 .......Welcome to use Alibaba Cloud.......O8888888D..........
    .........+88888888 ............. ************* ..............O8888888D..........
    .........+88888888 .... Command Line Interface(Reloaded) ....O8888888D..........
    .........+88888888...........................................88888888D..........
    ..........D888888888888DO+. ..........................?ND888888888888D..........
    ...........O8888888888888888888888...........D8888888888888888888888=...........
    ............ .:D8888888888888888888.........78888888888888888888O ..............
    ```
    
5.  执行以下命令，测试API调用。
    
    ```
    aliyun ram ListUsers --profile AkProfile
    ```
    
    如果一切正常，命令将返回RAM用户列表。类似：
    
    ```
    {
      "IsTruncated": false,
      "RequestId": "B3CDEF9E-A3F4-58B0-80BE-54576991****",
      "Users": {
        "User": [
          {
            "Comments": "",
            "CreateDate": "2025-10-29T02:47:52Z",
            "DisplayName": "username",
            "UpdateDate": "2025-10-29T02:47:52Z",
            "UserId": "20376656170607****",
            "UserName": "username"
          },
          ...
        ]
      }
    }
    ```
    

### **间接使用AccessKey**

此方法通过AccessKey获取有时效性的STS Token，再使用STS Token调用API。该方式配置相对复杂，但降低了长期AccessKey的暴露风险，并通过角色实现了权限的动态授予和分离，是更安全的使用方式。

1.  为持有AccessKey的RAM用户授予调用STS服务AssumeRole接口的权限`AliyunSTSAssumeRoleAccess`。
    
    1.  登录[RAM控制台](https://ram.console.aliyun.com/)，进入 **身份管理** > **用户** 页面。
        
    2.  找到目标 **RAM 用户**，单击 **操作** 列的 **新增授权**。
        
    3.  在 **新增授权** 步骤中，搜索并选中 `AliyunSTSAssumeRoleAccess` 系统策略，然后单击 **确认新增授权**。
        
    4.  回到用户列表，单击目标**RAM用户**名称。在**权限管理** > **个人权限**页签下，确认可以看到`AliyunSTSAssumeRoleAccess`权限。
        
2.  创建RAM角色，获取角色ARN。
    
    1.  在RAM控制台，进入 **身份管理** > **角色** 页面。
        
    2.  在**角色**页面，单击**创建角色**。
        
    3.  在**创建角色**页面，选择**信任主体类型**为**云账号**，然后设置具体的阿里云账号，单击**确定**。
        
    4.  在**创建角色**页面，输入角色名称`cli-test-role`。单击**确定**。
        
    5.  在角色详情页，找到**基本信息**区域下的ARN属性，点击**复制**并保存以备后续使用。
        
3.  为RAM角色授予RAM只读权限`AliyunRAMReadOnlyAccess`。
    
    进入 **身份管理** > **角色** 页面，单击 **操作** 列的 **新增授权**并添加权限，方法与[步骤1](#46bef3992fkdw)相同。
    
4.  打开本地终端并执行以下命令，通过交互式配置身份凭证。
    
    ```
    aliyun configure --profile RamRoleArnProfile --mode RamRoleArn
    ```
    
5.  根据命令行交互提示，输入在[创建AccessKey](#5be3fd3deb0lc)步骤中保存的 **AccessKey ID** 和 **AccessKey Secret**、以及在[步骤2](#2df0785691xty)中获取的RAM角色ARN。其余配置可参考如下示例。
    
    ```
    Configuring profile 'RamRoleArnProfile' in 'RamRoleArn' authenticate mode...
    Access Key Id []: <yourAccessKeyID>
    Access Key Secret []: <yourAccessKeySecret>
    Sts Region []: cn-shanghai
    Ram Role Arn []: acs:ram::012345678910****:role/cli-test-role
    Role Session Name []: cli-test-role
    External ID []: abcd1234
    Expired Seconds [900]: 900
    Default Region Id []: cn-shanghai
    Default Output Format [json]: json (Only support json)
    Default Language [zh|en] en: en
    Saving profile[RamRoleArnProfile] ...Done.
    ```
    
6.  如果AccessKey信息和其他配置正确，您将会在终端看到如下返回结果。如果遇到报错，请[删除缓存的阿里云CLI凭证配置](#fa8fc514a6i8d)，检查配置后再次执行[步骤4](#77e4fddf1a7pm)中的命令。
    
    ```
    Configure Done!!!
    ..............888888888888888888888 ........=8888888888888888888D=..............
    ...........88888888888888888888888 ..........D8888888888888888888888I...........
    .........,8888888888888ZI: ...........................=Z88D8888888888D..........
    .........+88888888 ..........................................88888888D..........
    .........+88888888 .......Welcome to use Alibaba Cloud.......O8888888D..........
    .........+88888888 ............. ************* ..............O8888888D..........
    .........+88888888 .... Command Line Interface(Reloaded) ....O8888888D..........
    .........+88888888...........................................88888888D..........
    ..........D888888888888DO+. ..........................?ND888888888888D..........
    ...........O8888888888888888888888...........D8888888888888888888888=...........
    ............ .:D8888888888888888888.........78888888888888888888O ..............
    ```
    
7.  执行以下命令，测试API调用。
    
    ```
    aliyun ram ListUsers --profile RamRoleArnProfile
    ```
    
    如果一切正常，命令将返回RAM用户列表。类似如下：
    
    ```
    {
      "IsTruncated": false,
      "RequestId": "B3CDEF9E-A3F4-58B0-80BE-54576991****",
      "Users": {
        "User": [
          {
            "Comments": "",
            "CreateDate": "2025-10-29T02:47:52Z",
            "DisplayName": "username",
            "UpdateDate": "2025-10-29T02:47:52Z",
            "UserId": "20376656170607****",
            "UserName": "username"
          },
          ...
        ]
      }
    }
    ```
    

## **清理资源**

### **删除缓存的阿里云CLI凭证配置**

在终端内，执行以下命令删除缓存的凭证配置。

-   如果您是按照[直接使用AccessKey](#a68eb74091wsu)步骤进行的配置，请执行以下命令：
    
    ```
    aliyun configure delete --profile AkProfile 
    ```
    
-   如果您是按照[间接使用AccessKey](#d03080c188xk6)步骤进行的配置，请执行以下命令：
    
    ```
    aliyun configure delete --profile RamRoleArnProfile
    ```
    

### **禁用和删除AccessKey**

1.  登录[RAM控制台](https://ram.console.aliyun.com/)，在左侧导航栏选择**身份管理** > **用户**。
    
2.  找到在上述创建 AccessKey 中的 目标**RAM 用户**，单击其名称。
    
3.  **禁用AccessKey**：在**AccessKey**页签中，单击目标AccessKey**操作**列的**禁用**。在弹出的**禁用**对话框中，单击**禁用**。
    
4.  **将AccessKey移入回收站**：单击目标AccessKey**操作**列的**删除**。在弹出的确认对话框中，输入当前AccessKey ID，然后单击**移入回收站**。
    
5.  **彻底删除AccessKey**：在用户详情页的**AccessKey回收站**区域，找到目标AccessKey，单击**操作**列的**删除**。在弹出的确认对话框中，输入目标AccessKey ID，然后单击**删除**，将其彻底删除。
    

## **相关文档**

您可以通过以下文档，了解更多相关信息：

-   [轮转RAM用户的AccessKey](https://help.aliyun.com/zh/ram/user-guide/rotate-accesskey-pairs-of-ram-users)
    
-   [调用AssumeRole接口获取扮演角色的临时身份凭证](https://help.aliyun.com/zh/ram/developer-reference/api-sts-2015-04-01-assumerole)
    
-   [在阿里云CLI中配置身份凭证](https://help.aliyun.com/zh/cli/configure-credentials/)
    
-   [使用访问凭据访问阿里云OpenAPI最佳实践](https://help.aliyun.com/zh/ram/use-cases/best-practices-for-programmatic-access-to-alibaba-cloud)