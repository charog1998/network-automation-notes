# 文档工具

将任意 Markdown 文档文件夹以文档站形式浏览，或打包为离线可用的静态 HTML。

## 文件

| 文件 | 作用 |
|------|------|
| `doc_server.py` | 实时服务器，边改边看 |
| `build_static.py` | 预渲染所有 MD，生成单文件离线页面 |
| `start_doc_server.ps1` | Windows 下双击启动服务器 + 自动打开浏览器 |

## 文档文件夹结构要求

```
文档根目录/
├── 00-分类A/
│   ├── 子主题1/            # 可选二级目录
│   │   ├── 00-概览.md
│   │   └── 01-详解.md
│   ├── 子主题2/
│   └── 顶层文档.md          # 也可直接在分类下放 .md
├── 01-分类B/
└── 02-分类C/
```

规则：
- 文件名：`<两位数>[_-]<标题>.md`，如 `03-配置向导.md`
- 文件夹名：`<两位数>-<分类名>`，如 `01-基础入门`
- 编码：UTF-8
- 层级不限，但侧边栏只展开一级比较好读
- 无数字前缀的文件/文件夹会正常显示，排序靠后，名称原样展示
- 三位数前缀（如 `123-`）也会被剥离，但排序位置可能不如预期

## 配置

两个 Python 脚本顶部都有硬编码的配置变量，按需修改：

```python
DOC_ROOT = Path(r"D:\阿里云ACP\docs")   # 文档根目录
HOST = "0.0.0.0"                        # 监听地址（仅 doc_server）
PORT = 9999                             # 监听端口（仅 doc_server）
TITLE = "阿里云 ACP 备考笔记"            # 页面标题
SUBTITLE = "云计算架构师高级认证（ACP）"   # 副标题
```

## 使用

### 实时预览（doc_server.py）

适合边写边看效果。

```bash
# 安装依赖
pip install markdown

# 启动
python doc_server.py

# 或 Windows 下双击
start_doc_server.ps1
```

浏览器打开 `http://localhost:9999`，修改 `.md` 后刷新即可看到效果。

### 离线打包（build_static.py）

适合分享、存档、放到 U 盘。

```bash
pip install markdown
python build_static.py
```

生成 `index.html`，一个约 2 MB 的单文件。双击用浏览器打开即可，无需服务器、无需 Python。

## 依赖

- Python 3.6+
- `markdown` 包（`pip install markdown`）

`build_static.py` 生成产物后，阅读端无需任何依赖。
