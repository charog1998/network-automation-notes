### Paramiko
Paramiko 是一个用于 Python 的 SSHv2 协议库，实现了 SSH 客户端与服务器的核心功能。它提供了安全的远程连接、命令执行、文件传输（SFTP）等功能，是自动化运维和远程管理的常用工具。

主要特点：
- **安全连接**：支持密钥认证和密码认证。
- **SFTP 客户端/服务器**：实现安全的文件传输。
- **远程命令执行**：通过 SSH 通道运行命令。
- **端口转发**：支持本地和远程端口转发。

适用于自动化部署、批量服务器管理等场景。

#### 常用类
- **Channel类**：包含执行命令，请求X11会话，发送数据，打开交互式会话等方法。通常这些来自Channel类的常用方法已包装在了SSHClient类中。
- **Message类**：包含向流中写入字节，提取字节等方法。
- **Packetizer类**：包含检查握手，获取channel ID等方法。
- **Transport类**：包含公钥认证，打开channel通道等方法。
- **SSHClient类**：包含建立连接，打开交互式会话等方法。SSHClient类是与SSH服务器会话的**高级表示**。该类集成了Transport、Channel和SFTPClient类。
- **SFTPClient类**：包含文件上传、下载等SFTP的方法。

#### Paramiko使用流程
由于**SSHClient类**集成了Transport、Channel和SFTPClient类，理论上来说整个SSH会话都可由这一个类实现，但还是要简单了解下其他类是如何工作的：

##### paramiko.Transport
主要负责建立连接
```py
Transport((主机名,端口)) # 建立连接
connect(username="",password="",pkey=None) # 建立连接并使用密码或私钥认证
close() # 关闭会话
```

##### Key-handling
主要负责读取私钥
```py
paramiko.RSAKey.from_private_key_file(filename) # 从文件中读取RSA私钥
paramiko.DSSKey.from_private_key_file(filename) # 从文件中读取DSS私钥
```

##### SFTPClient
```py
sftp = paramiko.SFTPClient.from_transport(一个Transport实例,window_size,max_packet_size) # 建立SFTP连接，可设置窗口大小，最大数据包大小
sftp.get()
sftp.put()
```

##### SSHClient
```py
client=paramiko.client.SSHClient() # 实例化一个类
client.connect(hostname,port,username,password) # 建立连接
client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy()) # 设置访问没有已知主机密钥时的策略 WarningPolicy警告并接受、RejectPolicy自动拒绝
client.load_system_host_keys() # 从系统文件中加载主机密钥
exec_command() # 远程执行命令
invoke_shell() # 启动交互式shell会话
open_sftp() # 创建SFTP通道
```

### 实战

**实验环境**
- **服务端**：华三HCL云实验室，MSR36-20设备，软件版本Comware 7.1.064
- **客户端**：Win10系统，Python 3.11.3

#### 实验一
**实验目标**：通过SSH连接到目标路由器并通过`show current-configuration`命令获取设备当前运行配置

**实验原理**
- 利用`paramiko.client.SSHClient().connect()`建立连接
- 利用`client.invoke_shell()`打开一个可交互的SHELL环境

**实验步骤**
一、MSR设备初始化配置
```
# Version 7.1.064，Release 0427P22
system-view

# 创建本地用户
local-user zzy class manage
 password simple 123456qwer
 service-type ssh
 authorization-attribute user-role network-admin

# SSH相关配置
ssh server enable
ssh user zzy service-type all authentication-type password

# VTY线路配置
user-interface vty 0 15
 authentication-mode scheme
 protocol inbound ssh
 user-role network-admin
 quit

# 接口配置
interface GigabitEthernet0/0
 ip address 192.168.56.123 255.255.255.0
```

二、编写Python脚本并运行
```python
import paramiko
import time

with paramiko.client.SSHClient() as client:
    client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
    client.connect("192.168.56.123", 22, "zzy", "123456qwer")
    with client.invoke_shell() as shell:
        shell.send("screen-length disable\n")
        shell.send("show current-configuration\n")
        time.sleep(2)
        output = shell.recv(65535).decode('utf-8')
        print(output)
```

三、实验结果
```sh
PS F:\network-automation-labs\Paramiko> python .\ssh_connect.py
screen-length disable
show current-configuration

 ******************************************************************************
* Copyright (c) 2004-2021 New H3C Technologies Co., Ltd. All rights reserved.*
* Without the owner's prior written consent,                                 *
* no decompiling or reverse-engineering shall be allowed.                    *
******************************************************************************

 <H3C>screen-length disable
<H3C>show current-configuration
#
 version 7.1.064, Release 0427P22
#
 sysname H3C
#
 system-working-mode standard
 xbar load-single
 password-recovery enable
...
```

**实验要点**
- 由于**OpenSSH**会把用户访问过每个计算机的公钥都记录在`~/.ssh/known_hosts`。当下次访问相同计算机时，OpenSSH会核对公钥。如果公钥不同，OpenSSH会发出警告，避免用户受到中间人攻击等。代码中需要用`client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())`设置自动把未知公钥添加到`~/.ssh/known_hosts`文件中的策略
- 利用`screen-length disable`命令让运行结果可以一次性输出多屏
- 在接收结果前利用`time.sleep(2)`等待路由器输出完毕

#### 实验二
**实验目标**：通过SFTP连接到目标路由器并下载设备的`startup.cfg`配置，然后再上传为`test.cfg`

**实验原理**
- 利用`paramiko.Transport.connect()`建立连接
- 利用`paramiko.SFTPClient.from_transport()`建立一个SFTP客户端
- 利用GET和PUT方法操作文件

**实验步骤**
一、MSR设备初始化配置（同实验一）
二、编写Python脚本并运行
```python
import paramiko

tran = paramiko.Transport(('192.168.56.123', 22))
tran.connect(username='zzy', password='123456qwer')
sftp = paramiko.SFTPClient.from_transport(tran)

sftp.get('/startup.cfg', 'startup.cfg')
sftp.put('startup.cfg', '/test.cfg')

tran.close()
```
三、实验结果

**客户端**可以看到运行后在本地目录新增了`startup.cfg`文件：
```bash
PS F:\network-automation-labs\Paramiko> dir
    目录: F:\network-automation-labs\Paramiko
Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----         2026/1/15     14:30                device-config
-a----         2026/1/15     15:09            267 sftp_connect.py
-a----         2026/1/15     14:47            452 ssh_connect.py

PS F:\network-automation-labs\Paramiko> python .\sftp_connect.py
PS F:\network-automation-labs\Paramiko> dir
    目录: F:\network-automation-labs\Paramiko
Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----         2026/1/15     14:30                device-config
-a----         2026/1/15     15:09            267 sftp_connect.py
-a----         2026/1/15     14:47            452 ssh_connect.py
-a----         2026/1/15     15:49           3185 startup.cfg
```

**服务端**可以看到SFTP登陆时的系统日志，并且在脚本运行后设备上也新增了一个`test.cfg`文件
```bash
<H3C>dir
Directory of flash: (VFAT)
   0 drw-           - Jan 15 2026 11:14:50   diagfile
...
  10 -rw-        3185 Jan 15 2026 12:43:52   startup.cfg
...
1046512 KB total (1046324 KB free)

%Jan 15 15:49:12:010 2026 H3C SSHS/6/SSHS_LOG: Accepted password for zzy from 192.168.56.1 port 50308.
%Jan 15 15:49:12:012 2026 H3C SSHS/6/SSHS_LOG: Subsystem request for sftp.
%Jan 15 15:49:13:016 2026 H3C SSHS/6/SSHS_CONNECT: SSH user zzy (IP: 192.168.56.1) connected to the server successfully.
%Jan 15 15:49:13:018 2026 H3C SSHS/6/SSHS_LOG: Session opened for local user zzy from [192.168.56.1].
%Jan 15 15:49:13:020 2026 H3C SSHS/6/SSHS_SFTP_OPER: User zzy at 192.168.56.1 requested operation: open "flash:/startup.cfg" (attribute code 0666) in READ mode.%Jan 15 15:49:13:029 2026 H3C SSHS/6/SSHS_LOG: Closed "flash:/startup.cfg". 3185 bytes read, 0 bytes written.
%Jan 15 15:49:13:034 2026 H3C SSHS/6/SSHS_SFTP_OPER: User zzy at 192.168.56.1 requested operation: open "flash:/test.cfg" (attribute code 0666) in WRITE,CREATE,TRUNCATE mode.
%Jan 15 15:49:13:036 2026 H3C SSHS/6/SSHS_LOG: Closed "flash:/test.cfg". 0 bytes read, 3185 bytes written.
%Jan 15 15:49:13:042 2026 H3C SSHS/6/SSHS_LOG: User zzy logged out from 192.168.56.1 port 50308.
%Jan 15 15:49:13:044 2026 H3C SSHS/6/SSHS_DISCONNECT: SSH user zzy (IP: 192.168.56.1) disconnected from the server.
%Jan 15 15:49:13:044 2026 H3C SSHS/6/SSHS_LOG: Session closed for local user zzy from [192.168.56.1].

<H3C>dir
Directory of flash: (VFAT)
   0 drw-           - Jan 15 2026 11:14:50   diagfile
...
  10 -rw-        3185 Jan 15 2026 12:43:52   startup.cfg
  11 -rw-       52936 Jan 15 2026 12:43:52   startup.mdb
  12 -rw-        3185 Jan 15 2026 15:49:13   test.cfg

1046512 KB total (1046320 KB free)
```