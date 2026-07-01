[TOC]
### 1、配置网络设置
将 node1 配置为具有以下网络配置： 
- 主机名： node1.domain250.example.com
- IP 地址： 172.25.250.100
- 子网掩码： 255.255.255.0
- 网关： 172.25.250.254
- DNS服务器： 172.25.250.254

#### 解法
```
nmcli con show # 查看网卡信息
nmcli con mod 'Wired connection 1' ipv4.method manual ipv4.addresses 172.25.250.100/24 ipv4.gateway 172.25.250.254 ipv4.dns 172.25.250.254 autoconnect yes
nmcli con up 'Wired connection 1' # 启用网卡
hostnamectl set-hostname node1.domain250.example.com # 设置主机名
```

#### 验证
```
ip a
hostname
```

#### 注
真正考试时做完node1的配置网络ip，就去破解node2的密码，然后返回做node1题目，按顺序做下面的题目

### 2、配置您的系统以使用默认存储库
- YUM 或者DNF存储库已可以从
  - http://content/rhel9.0/x86_64/dvd/BaseOS
  - http://content/rhel9.0/x86_64/dvd/AppStream 
- 使用配置您的系统，以将这些位置用作默认存储库

#### 解法
```
[root@node1 ~]# vim /etc/yum.repos.d/rhcsa.repo 
[Base]
name=Base
baseurl=http://content/rhel9.0/x86_64/dvd/BaseOS
enabled=1
gpgcheck=no
[App]
name=App
baseurl=http://content/rhel9.0/x86_64/dvd/AppStream
enabled=1
gpgcheck=no
```

#### 验证
```
[root@node1 ~]# yum repoinfo  
[root@node1 ~]# yum -y install vsftpd
```

#### 注
如果考试是DNF存储库，命令前部分更换为dnf即可
[root@node1 ~]# dnf -y install vsftpd

### 3、调试 SELinux
- 非标准端口 82 上运行的 Web 服务器在提供内容时遇到问题。根据需要调试并解决问题，使其满足以下条件：
  - 系统上的 Web 服务器能够提供 /var/www/html 中所有现有的 HTML ⽂件（注：不要删除或以其他方式改动现有的⽂件内容）
  - Web 服务器在端口 82 上提供此内容 Web 服务器在系统启动时自动启动
  - 确保SELinux机制运行在Enforcing模式

#### 解法
```
[root@node1 ~]# yum provides "*/semanage"  
[root@node1 ~]# yum -y install policycoreutils-python-utils 
[root@node1 ~]# semanage fcontext -m -t httpd_sys_content_t /var/www/html/file1
[root@node1 ~]# semanage port -a -t http_port_t -p tcp 82 
[root@node1 ~]# restorecon -Rv /var/www/html
# 也可以使用man semanage port，然后/EXAMPLE 
[root@node1 ~]# firewall-cmd --permanent --add-service=http 
[root@node1 ~]# firewall-cmd --permanent --add-port=82/tcp
[root@node1 ~]# firewall-cmd --reload
[root@node1 ~]# systemctl restart httpd 
[root@node1 ~]# systemctl enable --now httpd 
```

#### 实操
```
[root@node1 ~]# yum provides "*/semanage"  
Last metadata expiration check: 0:14:38 ago on Sun 15 Sep 2024 07:23:37 AM EDT.
policycoreutils-python-utils-3.3-6.el9_0.noarch : SELinux policy core python uti
Repo        : @System
Matched from:
Filename    : /usr/sbin/semanage
Filename    : /usr/share/bash-completion/completions/semanage

# 上面查出来的包名
[root@node1 ~]# yum -y install policycoreutils-python-utilsLast 

[root@node1 ~]# semanage fcontext -m -t httpd_sys_content_t /var/www/html/file1 

[root@node1 ~]# semanage port -a -t http_port_t -p tcp 82 

[root@node1 ~]# restorecon -Rv /var/www/html
Relabeled /var/www/html/file1 from unconfined_u:object_r:default_t:s0 to unconfined_u:object_r:httpd_sys_content_t:s0

[root@node1 ~]# firewall-cmd --permanent --add-service=http 
success
[root@node1 ~]# firewall-cmd --permanent --add-port=82/tcp
success
[root@node1 ~]# firewall-cmd --reload
success
[root@node1 ~]# systemctl restart httpd 
[root@node1 ~]# systemctl enable --now httpd
Created symlink /etc/systemd/system/multi-user.target.wants/httpd.service → /usr/lib/systemd/system/httpd.service.
```

#### 验证
```
[root@node1 ~]# curl http://node1.domain250.example.com:82/file1
[root@node1 ~]# curl http://node1.domain250.example.com:82/file2
[root@node1 ~]# curl http://node1.domain250.example.com:82/file3
```

#### 注
至于为什么只需要修改File1，因为只有File1的SELinux的上下文与另外两个不一致，可以通过ll -Z查看

### 4、创建用户帐户
创建下列用户、组和组成员资格： 
- 名为 sysmgrs 的组
- 用户 natasha ，作为次要组从属于 sysmgrs
- 用户 harry ，作为次要组还从属于 sysmgrs 
- 用户 sarah ，无权访问系统上的 交互式 shell 且不是 sysmgrs 的成员 
- natasha 、 harry 和 sarah 的密码应当都是 flectrag

#### 解法
```
[root@node1 ~]# groupadd sysmgrs 
[root@node1 ~]# useradd -G sysmgrs natasha 
[root@node1 ~]# useradd -G sysmgrs harry 
[root@node1 ~]# useradd -s /bin/false sarah 
```

#### 验证
```
[root@node1 ~]# echo flectrag |passwd --stdin natasha 
[root@node1 ~]# echo flectrag |passwd --stdin harry 
[root@node1 ~]# echo flectrag |passwd --stdin sarah
```

### 5、配置 cron 作业
以用户 harry 身份，每隔1分钟运行执行/usr/bin/echo hello
以用户 harry 身份，每天14:23分执行/usr/bin/echo hello

#### 解法
cron总计有5个表达式，也就是5个*
从左到右，分别代表：分、时、日、月、周
如果是每隔2分钟，例如：
*/2 * * * * 
其他同理，考试正常替换即可

```
[root@node1 ~]# systemctl status crond        ＃查看状态 
[root@node1 ~]# systemctl enable crond        ＃设置开机自启
[root@node1 ~]# crontab -e -u harry           ＃写入计划任务
*/1 * * * * /usr/bin/echo hello
23 14 * * * /usr/bin/echo hello
```

#### 验证
```
[root@node1 ~]# crontab -l -u harry
*/1 * * * * /usr/bin/echo hello
23 14 * * * /usr/bin/echo hello
```

#### 注
*/1: 每隔1分钟
,: 不同的时间段
-: 表示范围
星期0: 星期日

### 6、创建协作目录
创建具有以下特征的协作⽬录 /home/managers ：
- /home/managers 的组⽤权是 sysmgrs 
- 目录应当可被 sysmgrs 的成员读取、写⼊和访问，但任何其他用户不具这些权限。（当然，root 用户有权访问系统上的所有⽂件和目录） 
- /home/managers 中创建的⽂件⾃动将组所有权设置到 sysmgrs 组

#### 解法
```
[root@node1 ~]# mkdir /home/managers 
[root@node1 ~]# chgrp sysmgrs /home/managers 
[root@node1 ~]# chmod 2770 /home/managers # 2代表第三条要求，创建的文件默认属组
```

#### 验证
```
[root@node1 ~]# ll -Z /home
```

### 7、配置 NTP
- 配置您的系统，使其成为 materials.example.com 的 NTP 客户端。（注： materials.example.com 是 classroom.example.com 的 DNS 别名）

#### 解法
```
[root@node1 ~]# yum -y install chrony         ＃ NTP客户端
[root@node1 ~]# vim /etc/chrony.conf 
server materials.example.com iburst 
[root@node1 ~]# systemctl restart chronyd 
[root@node1 ~]# systemctl enable chronyd
```

#### 验证
把时间改走再同步试试
```
[root@node1 ~]# date -s "1982-1-1"  
[root@node1 ~]# systemctl restart chronyd  
# 隔3-5秒执行，太快了时间不会同步
[root@node1 ~]# date # 可以用watch date
```

### 8、配置 autofs
配置 autofs ，以按照如下所述自动挂载远程用户的主目录： 
- materials.example.com ( 172.25.254.254 ) NFS 导出 /rhome 到您的系统。此文件系统包含为用户 remoteuser1 预配置的主目录 
- remoteuser1 的主目录是 materials.example.com:/rhome/remoteuser1 
- remoteuser1 的主目录应自动挂载到本地 /rhome 下的 /rhome/remoteuser1 
- 主目录必须可供其用户 写⼊ 
- remoteuser1 的密码是 flectrag

#### 解法
```
# 暂时记做法，环境暂时没做出来
[root@node1 ~]# yum -y install nfs-utils 
[root@node1 ~]# yum -y install autofs 
# auto.master的/rhome /etc/auto.rhome这一行，/rhome后面是一个空格，不要用tab或者打多空格
[root@node1 ~]# vim /etc/auto.master 
/rhome /etc/auto.rhome 
[root@node1 ~]# vim /etc/auto.rhome 
remoteuser1 -rw materials.example.com:/rhome/remoteuser1
[root@node1 ~]# systemctl enable --now autofs ＃ 设置开机自启并现在启动
Created symlink /etc/systemd/system/multi-user.target.wants/autofs.service → /usr/lib/systemd/system/autofs.service.
```

#### 验证
```
[root@node1 ~]# ll /rhome/ 
[root@node1 ~]# ssh remoteuser1@localhost 
remoteuser1@localhost\'s password: `flectrag` 
$ pwd 
/rhome/remoteuser1 
$ touch my.file 
$ mount | grep rhome 
... 
materials.example.com:/rhome/remoteuser1 on /rhome/remoteuser1 type nfs4 
(`rw`,relatime,vers=4.2,rsize=131072,wsize=131072,namlen=255,hard,proto=tcp,timeo=600,r 
etrans=2,sec=sys,clientaddr=172.25.250.100,local_lock=none,addr=172.25.254.254)
```

### 9、 配置用户帐户
- 配置用户 manalo ，其用户 ID 为 3533 。此用户的密码应当为 flectrag 。

#### 解法
```
[root@node1 ~]# useradd -u 3533 manalo                    #创建用户指定uid为3533
[root@node1 ~]# echo flectrag | passwd --stdin manalo     #设置密码
```

#### 验证
```
tail -1 /etc/passwd #查看
```

### 10、查找文件
- 查找属于 jacques 用户所属文件，并拷贝到/root/findfiles 目录

#### 解法
```
[root@node1 ~]# mkdir /root/findfiles 
[root@node1 ~]# find / -user jacques 
[root@node1 ~]# find / -user jacques -exec cp -a {} /root/findfiles \;
#查找所属主和组是jacques的文件
```

#### 验证
```
[root@node1 ~]# ll /root/findfiles/
```