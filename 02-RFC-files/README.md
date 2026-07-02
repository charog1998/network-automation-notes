## RFC 阅读器

基于 [Textual](https://github.com/Textualize/textual) 的终端交互式 RFC 阅读器，自动按换页符分页，支持搜索高亮和文件浏览器。

### 安装依赖

```bash
pip install textual
```

### 用法

```bash
# 文件浏览器模式（默认）—— 光标选择文件
python rfcview.py

# 直接打开指定文件
python rfcview.py 01-转发与控制/rfc4271-bgp4.txt

# 从第 50 页开始阅读
python rfcview.py rfc4271-bgp4.txt -p 50
```

### 按键说明

**文件浏览器**

| 按键 | 功能 |
|------|------|
| `↑` `↓` / `j` `k` | 上下移动光标 |
| `Enter` | 打开文件 / 进入目录 |
| `←` / `Backspace` | 返回上级目录 |
| `h` `?` | 帮助 |
| `q` `Esc` | 退出 |

**RFC 阅读器**

| 按键 | 功能 |
|------|------|
| `n` `→` `Space` `j` | 下一页 |
| `p` `←` `Backspace` `k` | 上一页 |
| `PgDn` / `PgUp` | 前进/后退 5 页 |
| `Home` / `End` | 首页 / 末页 |
| `g` | 跳转到指定页码 |
| `/` | 搜索关键词（高亮 + 逐匹配跳转） |
| `,` `.` | 上一匹配 / 下一匹配 |
| `h` `?` | 帮助 |
| `q` `Esc` | 退出（自动回到文件浏览器） |
