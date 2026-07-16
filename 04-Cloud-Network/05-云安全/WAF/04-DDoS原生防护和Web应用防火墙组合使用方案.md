本文介绍了为网站类业务同时部署DDoS原生防护和Web应用防火墙的配置方法。该方案适用于为网站业务同时防御四层DDoS攻击和七层Web攻击、CC攻击的场景。

## 前提条件

-   已创建ECS实例并部署了业务相关的应用，ECS实例拥有公网IP地址且网站有域名。
    
    **说明**
    
    如果网站用于在中国内地提供服务，则网站域名必须已经完成ICP备案，否则将不能接入中国内地的Web应用防火墙实例进行防护。更多信息，请参见[ICP备案流程](https://help.aliyun.com/zh/icp-filing/basic-icp-service/user-guide/icp-filing-application-overview#task-2038407)。
    
-   已购买DDoS原生防护。更多信息，请参见[购买DDoS原生防护实例](https://help.aliyun.com/zh/anti-ddos/anti-ddos-origin/getting-started/purchase-an-anti-ddos-origin-enterprise-instance#task561)。
    
    **说明**
    
    您在购买原生防护实例时，需要选择资源所在地域。该地域必须与ECS实例一致。
    
-   已购买Web应用防火墙3.0。更多信息，请参见[购买WAF 3.0包年包月实例](https://help.aliyun.com/zh/waf/web-application-firewall-3-0/user-guide/purchase-a-subscription-waf-3-0-instance)。
    

## 背景信息

为网站类业务开启DDoS原生防护时，如果业务本身除了需要防御DDoS攻击，还需要防御Web攻击、CC攻击，建议您为网站同时开启Web应用防火墙，由Web应用防火墙帮助业务防御常见的Web攻击、CC攻击。关于Web应用防火墙（WAF）的详细介绍，请参见[什么是Web应用防火墙](https://help.aliyun.com/zh/waf/web-application-firewall-3-0/product-overview/what-is-waf)。

同时使用DDoS原生防护和Web应用防火墙时，您需要先将网站业务接入Web应用防火墙进行防护，然后将WAF实例的IP地址添加为DDoS原生防护实例的防护对象。完成上述部署后，所有业务流量先经过WAF进行安全清洗，攻击流量（包括DDoS攻击、Web攻击、CC攻击）被丢弃，只有正常的业务流量被转发到源站服务器。

## 操作步骤

登录[Web应用防火墙3.0控制台](https://yundunnext.console.aliyun.com/?p=wafnew)。在顶部菜单栏，选择WAF实例的资源组和地域（**中国内地**、**非中国内地**）。在左侧导航栏，单击**接入管理**，然后在**CNAME接入**页签单击**接入**。

### **步骤一：配置监听**

1.  填写**域名**，仅支持填写一个需防护的域名，包括精确域名（如`www.aliyundoc.com`）或通配符域名（如`*.aliyundoc.com`）。
    
    -   **通配符域名匹配规则**：
        
        -   仅能匹配同级别子域名。例如`*.aliyundoc.com`能够匹配`www.aliyundoc.com`、`example.aliyundoc.com`等，但不能匹配`www.example.aliyundoc.com`。
            
        -   当通配符应用于二级域名（如`*.aliyundoc.com`）时，能够匹配二级域名本身（即`aliyundoc.com`）。
            
        -   当通配符应用于三级域名（如`*.example.aliyundoc.com`）时，不能匹配三级域名本身（即`example.aliyundoc.com`）。
            
    -   **优先级规则**：当精确域名和通配符域名同时接入，且需防护的域名同时匹配这两者时，系统优先应用精确域名的防护规则。
        
    
    为确认域名所有权，需完成归属权验证。若填写域名后系统提示需验证，请从以下两种验证方式中任选其一进行验证。
    
    -   **DNS解析验证**：在域名解析服务商处，手动添加WAF提供的TXT记录。推荐采用此方式。
        
    -   **文件验证**：将WAF提供的验证文件上传至域名源站服务器的指定根目录。需具备源站服务器操作权限，并配置安全组策略，允许所有IP访问，以确保WAF可从公网验证该文件。
        
    
    ### **DNS解析验证**
    
    1.  在验证提示区域，单击**方法1：DNS解析验证**页签。
        
    2.  根据WAF控制台提供的**记录类型**、**主机记录**、**记录值**，在您的域名解析服务商添加TXT记录。
        
        若使用阿里云云解析DNS，请参考以下步骤操作；若使用其他域名解析服务商，请在其系统中进行类似配置。
        
        1.  在[公网权威解析](https://dns.console.aliyun.com/)页面，找到目标主域名，并单击右侧的**解析设置**。
            
        2.  单击**添加记录**，填写以下参数后，单击**确定**。其余未提及参数保持默认即可。
            
            -   **记录类型**：选择**TXT**。
                
            -   **主机记录**：复制并填写域名的前缀，例如`verification`。
                
            -   **记录值**：复制并填写WAF生成的记录值，例如`verify_8fca29dec226****`
                
    3.  等待TXT解析生效。域名首次配置TXT解析记录后将实时生效，但修改TXT解析记录通常将在10分钟后生效（生效时间取决于域名DNS解析配置的TTL时长，默认为10分钟）。
        
    4.  返回WAF控制台，单击“**点击验证**”。
        
        -   显示**验证成功**：域名归属权验证完成。
            
        -   显示**验证失败**：请按以下步骤排查：
            
            1.  **检查TXT记录**：确保添加的主机记录和记录值与WAF控制台提供的信息完全一致。如有差异，请删除错误记录并重新添加，然后重新验证。
                
            2.  **等待DNS生效**：DNS记录配置后可能不会立即生效，生效时间取决于域名服务器中设置的TTL缓存时间。建议等待10分钟后重新验证。
                
            3.  **更换验证方式**：如多次尝试仍无法通过验证，建议使用"**方法2: 文件验证**"。
                
    
    ### **文件验证**
    
    1.  在验证提示区域，单击**方法2: 文件验证**页签。
        
    2.  单击下载验证文件链接，下载验证文件。将下载的验证文件上传至域名根目录。在**协议类型**区域选择**HTTP**或**HTTPS**。上传完成后，选中**已上传**，单击**点击验证**。
        
        **重要**
        
        -   验证文件仅在下载后的3天内有效，若逾期未完成文件验证，则需要重新下载。
            
        -   请勿对验证文件执行任何修改操作，例如编辑、重命名等。
            
        -   WAF将根据选择的协议类型访问源站服务器，请确保源站服务器放行了对应的安全组或防火墙规则：
            
            -   选择**HTTP**时，需要放行入方向TCP协议80端口，访问来源为0.0.0.0/0。
                
            -   选择**HTTPS**时，需要放行入方向TCP协议443端口，访问来源为0.0.0.0/0。
                
        
    3.  手动将验证文件上传至域名源站服务器（例如ECS、OSS、CVM、COS、EC2等）网页的根目录。
        
        **说明**
        
        若添加的域名为通配符域名，例如`*.aliyun.com`，则需要将验证文档上传到`aliyun.com`的根目录。
        
        上传完成后，可以参考如下方法，查看验证文档是否上传成功。
        
        #### **Windows**
        
        在指定根目录，查看验证文件。在 Windows Server 的 IIS 网站根目录（如 `C:\inetpub\域名目录\wwwroot`）下，确认已上传的域名验证文件（文件名形如 `verify_xxxxxxxxxx`，HTML 格式）是否存在。
        
        #### **Linux**
        
        执行如下命令，查看验证文档。
        
        ```
        [root@xxx html]# pwd
        /usr/share/nginx/html
        [root@xxx html]# ls -al verify_4017759d36784d6e8b54d0b98928xxx.html
        -rw-r--r-- 1 root root 42 Jun 13 14:17 verify_4017759d36784d6e8b54d0b98928xxx.html
        [root@xxx html]# curl -ki "https://v205.xxx.cn/verify_4017759d36784d6e8b54d0b98928xxx.html"
        HTTP/1.1 200 OK
        Server: nginx/1.18.0
        Date: Tue, 13 Jun 2023 07:15:09 GMT
        Content-Type: text/html
        Content-Length: 42
        Last-Modified: Tue, 13 Jun 2023 06:17:26 GMT
        Connection: keep-alive
        ETag: "648809f6-2a"
        Access-Control-Allow-Credentials: true
        Access-Control-Allow-Origin: http://v205.xxx.cn
        Accept-Ranges: bytes
        ```
        
    4.  返回WAF控制台，单击“**点击验证**”。
        
        -   显示**验证成功**：域名归属权验证完成。
            
        -   显示**验证失败**：请根据报错信息进行排查：
            
            | **问题描述** | **解决方案** |
            | --- | --- |
            | 无法访问域名 | 1. 检查域名 DNS 解析，确保存在指向源站服务器的解析记录。以阿里云云解析DNS为例，操作请参见[添加解析记录](https://help.aliyun.com/zh/dns/add-a-dns-record)。 2. 检查源站服务器安全组或防火墙规则，确保放行公网访问请求。以ECS安全组为例，操作请参见[添加安全组规则](https://help.aliyun.com/zh/ecs/user-guide/manage-security-group-rules#36d9b82ad5xev)。 |
            | 验证文件不存在 | 重新在域名源站服务器中上传验证文件。 |
            | 文件内容不正确 | 1. 前往您域名的源站服务器，删除不正确的验证文件。 2. 重新上传验证文件。 |
            
    5.  由于允许所有IP访问的安全组规则存在安全风险，若源站服务器初始安全组配置中未包含0.0.0.0/0规则，建议在完成所有权验证后，删除用于验证而添加的安全组规则。
        
    
2.  选择网站**协议类型**（HTTP或HTTPS），并填写相应配置信息，可同时配置两种协议。
    
    **说明**
    
    WAF 共享虚拟主机定制版不支持 HTTPS。
    
    #### **HTTP**
    
    **HTTP端口**
    
    填写用户访问网站时使用的端口，建议HTTP协议使用80端口。如需自定义端口，支持在[端口范围](https://help.aliyun.com/zh/waf/web-application-firewall-3-0/user-guide/view-supported-ports#concept-2164031)内进行修改，每输入一个端口，按回车确认。
    
    #### **HTTPS**
    
    1.  **HTTPS端口**
        
        填写用户访问网站时使用的端口，建议HTTPS协议使用443端口。如需自定义端口，支持在[端口范围](https://help.aliyun.com/zh/waf/web-application-firewall-3-0/user-guide/view-supported-ports#concept-2164031)内进行修改，每输入一个端口，按回车确认。
        
    2.  **HTTPS** **证书上传方式**
        
        为使WAF能够监听并防护网站的HTTPS业务流量，需将域名关联的SSL证书上传至WAF。可选项：
        
        -   **手动上传**：适用于证书未上传至阿里云数字证书管理服务（原 SSL 证书）的场景。
            
        -   **选择已有证书**：从阿里云数字证书管理服务（原 SSL 证书）中选择已签发或已上传的证书。
            
        -   **申请新证书：**如未持有该域名的SSL证书，需先完成证书购买，等待证书签发后再接入WAF。
            
        
        #### **手动上传**
        
        -   **证书名称**：为证书设置一个唯一的名称，不能与已上传的证书名称重复。
            
        -   **证书文件**：请使用文本编辑器打开并粘贴 **PEM、CER、CRT 格式**的证书文本内容。
            
            格式示例：`-----BEGIN CERTIFICATE-----......-----END CERTIFICATE-----`
            
            -   格式转换：若证书是 PFX、P7B 等格式，请使用[证书工具](https://help.aliyun.com/zh/ssl-certificate/use-the-certificate-toolkit#section-7pl-isf-owk)将其转换为 PEM 格式。
                
            -   证书链：若包含中间证书，请按照 “服务器证书、中间证书” 的顺序拼接后粘贴。
                
        -   **私钥文件**：请使用文本编辑器打开并粘贴 PEM 格式的私钥文本内容。
            
            -   RSA：`-----BEGIN RSA PRIVATE KEY-----......-----END RSA PRIVATE KEY-----`
                
            -   ECC：`-----BEGIN EC PRIVATE KEY-----......-----END EC PRIVATE KEY-----`
                
        
        #### **选择已有证书**
        
        从证书下拉列表中选择要上传到WAF的证书。
        
        **说明**
        
        若WAF控制台提示“**证书链完整性校验失败，使用该证书可能会影响您的业务访问**”，表示证书链存在完整性问题。请检查证书内容的正确性与完整性后，在数字证书管理服务控制台重新上传。具体操作，请参见[上传、同步和共享SSL证书](https://help.aliyun.com/zh/ssl-certificate/upload-an-ssl-certificate#concept-g5c-3xn-yfb)。
        
        #### **申请新证书**
        
        还没有购买证书时，需参见[购买正式证书](https://help.aliyun.com/zh/ssl-certificate/purchase-an-ssl-certificate)进行购买，可单击**立即申请**阅读申请证书的相关文档。
        
    

### **步骤二：配置转发**

1.  在**服务器地址**区域，根据服务器类型填写源站服务器IP或域名。WAF通过此配置转发正常业务请求至源站服务器。
    
2.  确定源站服务器类型后，完成以下配置。
    
    ##### **IP**
    
    -   **回源端口**：即网站使用的端口。用户通过步骤一中配置的**HTTP/HTTPS端口**访问网站，WAF通过此处的**回源端口**访问源站服务器。
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2815729771/CAEQYhiBgIDJoJuTyBkiIDJhYWQ2MjIzNGY1YzQxM2Y4Y2IwNjI3ODA3NjFkOTVj5597349_20250821104239.602.svg)
        -   默认与上一步**协议类型**中配置的**HTTP/HTTPS端口**保持一致，支持在[端口范围](https://help.aliyun.com/zh/waf/web-application-firewall-3-0/user-guide/view-supported-ports#concept-2164031)内自定义回源端口，适用于需指定WAF以特定端口回源的场景。
            
    -   **回源IP**：填写源站服务器IP地址。
        
        -   必须为可访问的公网IP地址。
            
        -   支持填写多个IP地址。每填写一个IP地址，按回车进行确认。最多支持添加20个源站服务器IP。如果填写了多个IP地址，WAF会根据您在负载均衡算法中的配置转发回源请求。
            
        -   支持配置 IPv4 和 IPv6 地址，可单独或同时配置。如需配置IPv6地址，必须确保在**配置监听**时，开启IPv6防护。
            
    
    ##### **域名（如CNAME）**
    
    -   **回源端口**：即网站使用的端口。用户通过步骤一中配置的**HTTP/HTTPS端口**访问网站，WAF通过此处的**回源端口**访问源站服务器。
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2815729771/CAEQYhiBgIDJoJuTyBkiIDJhYWQ2MjIzNGY1YzQxM2Y4Y2IwNjI3ODA3NjFkOTVj5597349_20250821104239.602.svg)
        -   默认与上一步**协议类型**中配置的端口保持一致，支持在[端口范围](https://help.aliyun.com/zh/waf/web-application-firewall-3-0/user-guide/view-supported-ports#concept-2164031)内自定义回源端口，适用于需指定WAF以特定端口回源的场景。
            
    -   **回源域名**：填写源站服务器域名地址。
        
        -   WAF仅支持将客户端请求转发至该域名解析出的IPv4地址。对于IPv6网站，请选择IP方式接入。
            
    
    **重要**
    
    如网站对应的源站服务器地址变更，请及时修改此处的服务器地址。
    
3.  如需自定义配置**负载均衡算法**、**备链路回源**、**HTTP回源**、**回源SNI**、**请求头字段配置**、**流量标记**、**回源超时时间**、**回源重试**、**回源长连接**，**国密HTTPS**、**HTTP2**、**HTTPS强制跳转**、**TLS协议版本**、**HTTPS加密套件**、**WAF前存在七层代理（如CDN）**、**IPv6**、**独享IP**、**WAF集群智能负载均衡**等高级配置，请参见[进阶配置](https://help.aliyun.com/zh/waf/web-application-firewall-3-0/user-guide/add-a-domain-name-to-waf-in-cname-record-mode#39d46d25d2h3i)。若无需自定义，保持其余配置项默认即可，单击**提交**。
    

### **步骤三：切换流量**

在WAF控制台完成以上配置后，**必须**执行以下操作将流量切换至WAF，否则WAF防护将不会生效。

1.  **放行WAF回源IP段**：若源站服务器上配置了**安全组规则、防火墙规则**等访问控制策略，或使用了安全狗、云锁等安全软件，则**必须**在源站服务器设置放行WAF回源IP段，否则WAF回源流量可能被拦截，导致业务中断。
    
    **说明**
    
    建议配置源站服务器**仅**放行WAF回源IP段，确保仅有WAF能与源站服务器建立通信，避免攻击者访问源站服务器公网IP，绕过WAF发起攻击。
    
    1.  在**接入完成**向导页右上角，单击**WAF IP 地址**。
        
    2.  在**回源IP段**对话框，单击**复制**，将所有WAF回源IP复制到剪贴板。
        
        **说明**
        
        复制的回源IP段之间以英文逗号（,）分隔。其中包含类似 2408:400a:3c:xxxx::/56 的地址，此类地址属于 IPv6 地址段。
        
    3.  在服务器防火墙等位置放行以上IP段。例如当源站服务器是阿里云ECS实例时，需要在ECS安全组中放行，更多安全组的操作，请参见[添加安全组规则](https://help.aliyun.com/zh/ecs/user-guide/manage-security-group-rules#36d9b82ad5xev)。
        
        1.  在 ECS 实例详情页面，单击**安全组** > **安全组列表**，选择目标安全组并进入其详情页。
            
        2.  在安全组详情页的**入方向**下，单击**增加规则**。
            
        3.  由于安全组规则无法在单条规则中同时包含IPv4和IPv6地址，需要分两步操作：
            
            1.  **添加IPv4规则：**在**新建安全组规则**面板的**访问来源**区域，粘贴上一步复制的IP段，并手动删除其中的IPv6地址，将**访问目的（本实例）**设置为在步骤二中配置的回源端口，其余参数保持默认值，单击**提交**即可。
                
            2.  **添加IPv6规则：**再次单击**增加规则**，参照上一步添加IPv6地址段，在**访问来源**区域选择**IPv6**。
                
2.  **本地验证WAF配置正确性**：建议在修改域名DNS解析设置前，先通过修改本地`hosts`文件映射域名进行验证。可防止因配置错误导致业务中断。
    
    1.  在**接入完成**向导页，单击**复制CNAME**获取WAF提供的CNAME地址。
        
    2.  打开[网络诊断分析](https://boce.aliyun.com/home)，选择**网络诊断分析**，输入复制的CNAME地址，如`xxx.c.yundunwaf2.com`，单击**立即检测**。
        
    3.  复制**DNS服务商解析结果**的IP地址。修改本地计算机`hosts`文件。
        
        #### **Windows**
        
        1.  使用记事本打开`C:\Windows\System32\drivers\etc\hosts`文件，在末尾添加以下记录并保存。
            
            ```
            <上一步骤c复制的IP地址> <当前在WAF添加的域名>
            ```
            
        2.  打开`cmd`，执行`ping <当前在WAF添加的域名>`命令，若输出的IP地址与添加的IP地址一致，表示hosts修改已生效；否则请执行`ipconfig /flushdns`刷新DNS缓存后重新执行ping命令。
            
        3.  打开浏览器，在地址栏输入被防护域名进行访问。
            
            -   如果网站能够正常访问，说明WAF域名配置正确。可以进行下一步的DNS解析修改。
                
            -   如果网站访问异常，可能说明WAF域名配置错误。建议检查上述配置，修复问题后重新进行本地验证。
                
        4.  完成本地验证后，重新修改hosts文件至原始状态。
            
        
        #### **macOS**
        
        1.  通过`Command + 空格键`搜索并打开`终端`。
            
        2.  输入`sudo vim /etc/hosts`，打开`hosts`文件。
            
        3.  在文件末尾添加以下记录并保存。
            
            ```
            <上一步骤c复制的IP地址> <当前在WAF添加的域名>
            ```
            
        4.  执行`ping <当前在WAF添加的域名>`命令，若输出的IP地址与添加的IP地址一致，表示hosts修改已生效；否则请执行`sudo killall -HUP mDNSResponder`刷新DNS缓存后重新执行ping命令。
            
        5.  打开浏览器，在地址栏输入被防护域名进行访问。
            
            -   如果网站能够正常访问，说明WAF域名配置正确。可以进行下一步的DNS解析修改。
                
            -   如果网站访问异常，可能说明WAF域名配置错误。建议检查上述配置，修复问题后重新进行本地验证。
                
        6.  完成本地验证后，重新修改hosts文件至原始状态。
            
        
3.  **修改域名DNS解析：**将域名DNS解析指向WAF提供的CNAME地址，以确保域名的Web请求解析到WAF进行安全防护。
    
    **说明**
    
    建议于业务低峰期执行此操作以降低业务影响。
    
    1.  在**接入完成**向导页，单击**复制CNAME**获取WAF提供的CNAME地址。
        
    2.  将域名的DNS解析地址设置为上一步复制的地址。若域名解析托管在阿里云云解析DNS，请按以下步骤操作；若使用其他服务商的DNS服务，请在其系统中进行类似配置。
        
        1.  在[公网权威解析](https://dns.console.aliyun.com/#/dns/domainList)页面，定位到要设置的域名，单击其**操作**列下的**解析设置**。
            
        2.  在**解析设置**页面，定位到要设置的**主机记录**，单击其**操作**列下的**修改**。例如接入WAF的域名为`www.aliyundoc.com`，那么此处需定位到主域名`aliyundoc.com`下，主机记录为`www`的条目进行修改。
            
        3.  在**编辑记录**面板，选择**记录类型**为**CNAME**，修改**记录值**为WAF提供的CNAME地址，其余设置保持不变。
            
            修改DNS解析记录时：
            
            -   对于同一个主机记录，CNAME解析记录值只能填写一个，需要将其修改为WAF CNAME地址。
                
            -   同一主机记录下，CNAME记录与A、MX、TXT等其他记录类型存在冲突。需要先删除存在冲突的记录，再添加新的CNAME记录。
                
                **警告**
                
                在DNS变更的空窗期内，可能出现部分用户访问中断的情况。因此删除原解析记录后必须立即新增CNAME记录。
                
        4.  单击**确定**，完成解析设置修改，等待修改后的DNS解析记录生效。
            
            **说明**
            
            由于DNS解析记录生效需要一定时间，如果修改后网站访问失败，请等待10分钟后刷新页面重新访问。
            

### **步骤四：添加防护对象**

1.  登录[流量安全产品控制台](https://yundun.console.aliyun.com/?p=ddos)。
    
2.  在左侧导航栏，选择**网络安全** > **DDoS原生防护** > **防护对象**。
    
3.  在顶部菜单栏左上角处，选择实例所在资源组，地域选择**全球**。
    
4.  单击**添加防护对象**，在**从资产中添加**页签的**待选择对象**区域，选择**WAF**，将WAF资产移入**已选择对象**中，单击**确认**。具体操作，请参见[防护对象](https://help.aliyun.com/zh/anti-ddos/anti-ddos-origin/user-guide/add-an-object-for-protection)。
    

添加防护对象后，WAF实例将享有DDoS原生防护实例的DDoS攻击[全力防护](https://help.aliyun.com/zh/anti-ddos/anti-ddos-pro-and-premium/product-overview/terms#section-iet-6rf-8p9)能力，在业务遭受DDoS攻击时，自动触发流量清洗，防御DDoS攻击。