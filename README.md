# network-notes

网络自动化学习笔记，涵盖网络协议、自动化运维、API 编程等方向的知识整理。

> 📦 本笔记仓库与实验仓库 **[network-labs](https://github.com/charog1998/network-labs)** 配套使用——笔记中涉及的大部分拓扑和实验均在 network-labs 中有对应的配置文件。

---

## 目录结构

| 目录 | 说明 |
|------|------|
| `00-Getting-Started/` | 环境搭建与入门指南（EVE-NG 等） |
| `01-Protocols-APIs/` | 网络协议与编程接口笔记 |
| `02-RFC-files/` | RFC 原文归档 |
| `03-Ansible/` | Ansible 自动化运维笔记与 RHCE 练习题 |
| `80-Ideas/` | 临时点子与项目灵感收集 |
| `98-Notebook-Images/` | 笔记引用的图片资源 |

### `01-Protocols-APIs/` 子目录

| 主题 | 内容 |
|------|------|
| **BGP** | BGP 协议基础 |
| **BFD** | 双向转发检测 |
| **DHCP** | DHCP 协议与中继 |
| **Firewall** | 防火墙技术 |
| **IPv6** | IPv6 基础 |
| **IS-IS** | IS-IS 路由协议 |
| **Management** | 设备带内/带外管理 |
| **Multicast** | 组播技术 |
| **NETCONF** | NETCONF 协议（概念 → XML → RPC 报文） |
| **OSPF** | OSPF 路由协议 |
| **Paramiko** | Python SSH/SFTP 实战 |
| **Routing-Policy** | 路由策略与路由控制 |
| **Scripts** | 实用脚本（设备基础配置等） |
| **Security** | 常见安全策略 |
| **SNMP** | SNMP 协议实战 |
| **Switching** | RSTP/MSTP、堆叠与集群 |
| **Telemetry** | 流式遥测（Dial-out 模式实战） |
| **Traffic-Engineering** | 流量过滤与转发路径控制 |
| **VPN** | VPN 技术 |
| **VRF** | VRF 技术 |
| **VRRP** | VRRP 协议 |
| **WLAN** | 无线局域网 |
| **YANG** | YANG 数据建模（概念 → 约束 → 引用与增强） |

### RFC 阅读器

`02-RFC-files/` 目录下附带了一个基于 [Textual](https://github.com/Textualize/textual) 的终端交互式 RFC 阅读器，支持自动分页、搜索高亮、目录导航、书签等功能。

```bash
pip install textual
python rfcview.py                 # 文件浏览器模式
python rfcview.py rfc4271.txt     # 直接打开指定 RFC
```

详细用法见 [`02-RFC-files/README.md`](02-RFC-files/README.md)。

---

## 相关仓库

| 仓库 | 说明 |
|------|------|
| 🧪 [network-labs](https://github.com/charog1998/network-labs) | 配套实验文件（拓扑、设备配置等） |
| 📝 [network-notes](https://github.com/charog1998/network-notes) | 本仓库——学习笔记与知识整理 |

---