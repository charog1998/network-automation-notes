#!/usr/bin/env python3
"""
实时 Markdown 文档服务器
将备考文档文件夹以文档站形式通过 HTTP 共享，支持侧边栏导航、实时 MD→HTML 渲染。

启动: python doc_server.py
访问: http://localhost:8888
"""

import http.server
import json
import re
import sys
import io
import os
import urllib.parse
from pathlib import Path
from markdown import markdown

# 修复 Windows Git Bash GBK 编码
try:
    if hasattr(sys.stdout, 'buffer'):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
except Exception:
    pass

# ========== 配置 ==========
DOC_ROOT = Path(r"D:\阿里云ACP\docs")
HOST = "0.0.0.0"
PORT = 9999
TITLE = "阿里云 ACP 备考笔记"
SUBTITLE = "云计算架构师高级认证（ACP）"

# ========== 工具函数 ==========
def strip_order_prefix(name):
    return re.sub(r'^\d{2,3}[-_]', '', name)

def natural_sort_key(name):
    m = re.match(r'^(\d{2,3})', name)
    return (0, int(m.group(1)), name) if m else (1, 0, name)

# ========== 目录树 ==========
def build_tree():
    items = []
    dirs = sorted([d for d in DOC_ROOT.iterdir() if d.is_dir()],
                  key=lambda d: natural_sort_key(d.name))
    for part_dir in dirs:
        part_node = {"name": strip_order_prefix(part_dir.name), "type": "folder", "children": []}
        subdirs = sorted([d for d in part_dir.iterdir() if d.is_dir()],
                        key=lambda d: natural_sort_key(d.name))
        md_files = sorted([f for f in part_dir.iterdir()
                          if f.is_file() and f.suffix == '.md'],
                         key=lambda f: natural_sort_key(f.name))
        if subdirs:
            for chap_dir in subdirs:
                chap_node = {"name": strip_order_prefix(chap_dir.name), "type": "folder", "children": []}
                files = sorted([f for f in chap_dir.iterdir()
                               if f.is_file() and f.suffix == '.md'],
                              key=lambda f: natural_sort_key(f.name))
                for f in files:
                    chap_node["children"].append({
                        "name": strip_order_prefix(f.stem),
                        "type": "file",
                        "path": str(f.relative_to(DOC_ROOT)).replace('\\', '/')
                    })
                if chap_node["children"]:
                    part_node["children"].append(chap_node)
            if md_files:
                for f in md_files:
                    part_node["children"].append({
                        "name": strip_order_prefix(f.stem),
                        "type": "file",
                        "path": str(f.relative_to(DOC_ROOT)).replace('\\', '/')
                    })
        elif md_files:
            for f in md_files:
                part_node["children"].append({
                    "name": strip_order_prefix(f.stem),
                    "type": "file",
                    "path": str(f.relative_to(DOC_ROOT)).replace('\\', '/')
                })
        if part_node["children"]:
            items.append(part_node)
    return items

def count_files(nodes):
    n = 0
    for node in nodes:
        if node["type"] == "file":
            n += 1
        if "children" in node:
            n += count_files(node["children"])
    return n

# ========== Markdown 渲染 ==========
def render_md_to_html(md_text):
    return markdown(
        md_text,
        extensions=['markdown.extensions.tables', 'markdown.extensions.fenced_code',
                     'markdown.extensions.codehilite', 'markdown.extensions.toc',
                     'markdown.extensions.sane_lists'],
        extension_configs={'markdown.extensions.codehilite': {'guess_lang': True, 'css_class': 'highlight'}}
    )

# ========== HTML 页面 ==========
def build_page():
    tree = build_tree()
    tree_json = json.dumps(tree, ensure_ascii=False)
    total = count_files(tree)
    stats = "{} 个模块 · {} 篇文档".format(len(tree), total)

    # 使用 HTML 文件分离方式——读外部模板
    # 这里把 CSS/JS/HTML 全部内联以保持单文件可移植性
    # 关键：不使用 .format() 避免花括号冲突，用 replace 注入变量

    html = get_page_html()
    html = html.replace('__TITLE__', TITLE)
    html = html.replace('__SUBTITLE__', SUBTITLE)
    html = html.replace('__STATS__', stats)
    html = html.replace('__TREE_JSON__', tree_json)
    html = html.replace('__PORT__', str(PORT))
    return html

def get_page_html():
    # CSS 和 JS 都硬写在下面，花括号无需转义
    return '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__TITLE__</title>
<link rel="stylesheet"
  href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github.min.css">
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --sidebar-w: 300px;
  --accent: #1677ff;
  --accent-light: #e6f4ff;
  --bg: #ffffff;
  --bg-sidebar: #f7f8fa;
  --text: #1a1a2e;
  --text-muted: #6b7280;
  --border: #e5e7eb;
  --code-bg: #f6f8fa;
  --table-stripe: #f9fafb;
  --table-header-bg: #f0f5ff;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC",
               "Microsoft YaHei", "Noto Sans SC", sans-serif;
  font-size: 15px; line-height: 1.7; color: var(--text); background: var(--bg);
  display: flex; min-height: 100vh;
}

/* === 侧边栏 === */
.sidebar {
  width: var(--sidebar-w); min-width: var(--sidebar-w); height: 100vh;
  position: fixed; top: 0; left: 0; background: var(--bg-sidebar);
  border-right: 1px solid var(--border); overflow-y: auto; overflow-x: hidden;
  z-index: 100; display: flex; flex-direction: column;
  transition: transform 0.3s ease;
}
.sidebar-header {
  padding: 20px 18px 14px; border-bottom: 1px solid var(--border);
  background: var(--bg-sidebar); position: sticky; top: 0; z-index: 10;
}
.sidebar-header h1 { font-size: 1.15em; color: #1a1a2e; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.sidebar-header .subtitle { font-size: 0.75em; color: var(--text-muted); }
.sidebar-header .stats { font-size: 0.7em; color: #9ca3af; margin-top: 6px; }

.search-box {
  padding: 10px 14px; border-bottom: 1px solid var(--border);
  background: var(--bg-sidebar); position: sticky; top: 0; z-index: 10;
}
.search-box input {
  width: 100%; padding: 7px 12px; border: 1px solid var(--border);
  border-radius: 6px; font-size: 0.85em; outline: none; background: #fff; color: var(--text);
}
.search-box input:focus { border-color: var(--accent); box-shadow: 0 0 0 2px var(--accent-light); }

.tree { flex: 1; padding: 8px 0; user-select: none; }
.tree-item {
  cursor: pointer; display: flex; align-items: center;
  padding: 5px 14px 5px 0; font-size: 0.88em; color: var(--text);
  text-decoration: none; transition: background 0.15s; white-space: nowrap;
}
.tree-item:hover { background: #eef1f5; }
.tree-item.active { background: var(--accent-light); color: var(--accent); font-weight: 600; }
.tree-item.folder { font-weight: 600; color: #374151; }
.tree-icon {
  width: 18px; height: 18px; margin: 0 6px 0 0; flex-shrink: 0;
  display: flex; align-items: center; justify-content: center;
  font-size: 0.7em; color: #9ca3af; transition: transform 0.2s;
}
.tree-item.folder.open > .tree-icon { transform: rotate(90deg); }
.tree-children { display: none; }
.tree-children.open { display: block; }
.tree-children .tree-item { padding-left: 14px; }
.tree-children .tree-children .tree-item { padding-left: 28px; }

.sidebar-toggle {
  display: flex; align-items: center; justify-content: center;
  position: fixed; top: 12px; left: 12px; z-index: 200;
  background: var(--accent); color: #fff; border: none; width: 36px; height: 36px;
  border-radius: 8px; font-size: 1.2em; cursor: pointer;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  transition: background 0.2s, left 0.3s ease;
}
.sidebar-toggle:hover { opacity: 0.9; }
.sidebar-overlay { display: none; }

/* === 主内容 === */
.main { margin-left: var(--sidebar-w); flex: 1; min-width: 0; max-width: 960px; padding: 40px 48px 80px; transition: margin-left 0.3s ease; }

.welcome { text-align: center; padding: 80px 20px 40px; }
.welcome h2 { font-size: 1.8em; color: #1a1a2e; margin-bottom: 12px; }
.welcome p { color: var(--text-muted); font-size: 1.05em; max-width: 520px; margin: 0 auto 24px; line-height: 1.8; }
.welcome .hint {
  display: inline-block; background: var(--accent-light); color: var(--accent);
  padding: 6px 16px; border-radius: 20px; font-size: 0.9em;
}

/* 内容排版 */
.content h1 { font-size: 1.8em; color: #1a1a2e; border-bottom: 2px solid var(--accent); padding-bottom: 8px; margin: 0 0 1em; }
.content h2 { font-size: 1.4em; color: #1f2937; margin: 1.6em 0 0.6em; padding-bottom: 6px; border-bottom: 1px solid var(--border); }
.content h3 { font-size: 1.2em; color: #374151; margin: 1.4em 0 0.5em; }
.content h4 { font-size: 1.05em; color: #4b5563; margin: 1.2em 0 0.4em; }
.content h5, .content h6 { font-size: 1em; color: var(--text-muted); margin: 1em 0 0.3em; }
.content p { margin: 0.75em 0; text-align: justify; }
.content a { color: var(--accent); }
.content strong { color: #111827; }
.content ul, .content ol { padding-left: 2em; margin: 0.6em 0; }
.content li { margin: 0.35em 0; }
.content li > ul, .content li > ol { margin: 0.2em 0; }

.content table {
  width: 100%; border-collapse: collapse; margin: 1.2em 0; font-size: 0.9em;
}
.content thead th {
  background: var(--table-header-bg); font-weight: 600; text-align: left;
  padding: 10px 14px; border: 1px solid #d1d5db;
}
.content tbody td {
  padding: 8px 14px; border: 1px solid var(--border); vertical-align: top;
}
.content tbody tr:nth-child(even) { background: var(--table-stripe); }
.content tbody tr:hover { background: #f0f4ff; }

.content code {
  font-family: "Cascadia Code", "Fira Code", "JetBrains Mono", Consolas, monospace;
  font-size: 0.88em; background: var(--code-bg); padding: 0.15em 0.45em;
  border-radius: 4px; color: #d63384;
}
.content pre {
  background: #f8f9fb; border: 1px solid var(--border); border-radius: 8px;
  padding: 16px 20px; overflow-x: auto; margin: 1em 0; line-height: 1.55;
}
.content pre code { background: none; padding: 0; color: inherit; font-size: 0.85em; }

.content blockquote {
  border-left: 4px solid var(--accent); margin: 1em 0; padding: 0.6em 1.2em;
  background: #f8faff; color: #4b5563; border-radius: 0 6px 6px 0;
}
.content img { max-width: 100%; height: auto; display: block; margin: 1.2em auto; border-radius: 6px; }
.content hr { border: none; border-top: 1px solid var(--border); margin: 2em 0; }

.breadcrumb {
  font-size: 0.85em; color: var(--text-muted); margin-bottom: 20px;
  padding-bottom: 12px; border-bottom: 1px dashed var(--border);
}
.breadcrumb span { color: var(--text); font-weight: 500; }

.loading { text-align: center; padding: 60px 20px; color: var(--text-muted); }
.spinner {
  display: inline-block; width: 32px; height: 32px;
  border: 3px solid var(--border); border-top-color: var(--accent);
  border-radius: 50%; animation: spin 0.6s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* 桌面端：侧边栏可折叠（非 overlay，内容区跟随伸展） */
@media (min-width: 769px) {
  body.sidebar-hidden .sidebar {
    transform: translateX(calc(-1 * var(--sidebar-w)));
  }
  body.sidebar-hidden .main {
    margin-left: 0;
    max-width: none;
  }
  body.sidebar-hidden .sidebar-toggle {
    background: var(--text-muted);
  }
  body.sidebar-hidden .sidebar-toggle:hover {
    background: var(--accent);
  }
}

/* 响应式 */
@media (max-width: 768px) {
  .sidebar { transform: translateX(-100%); }
  .sidebar.open { transform: translateX(0); }
  .sidebar-overlay { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.35); z-index: 99; }
  .sidebar-overlay.open { display: block; }
  .main { margin-left: 0; padding: 60px 20px 40px; }
  .sidebar-toggle { left: 12px; }
}
@media (max-width: 480px) {
  .main { padding: 56px 14px 40px; }
  .content h1 { font-size: 1.4em; }
  .content h2 { font-size: 1.2em; }
  .content table { font-size: 0.78em; }
  .content pre { padding: 12px 14px; font-size: 0.8em; }
}
</style>
</head>
<body>

<button class="sidebar-toggle" onclick="toggleSidebar()" title="目录">&#9776;</button>
<div class="sidebar-overlay" onclick="toggleSidebar()"></div>

<aside class="sidebar" id="sidebar">
  <div class="sidebar-header">
    <h1>__TITLE__</h1>
    <div class="subtitle">__SUBTITLE__</div>
    <div class="stats">__STATS__</div>
  </div>
  <div class="search-box">
    <input type="text" id="searchInput" placeholder="搜索文档..." oninput="filterTree()">
  </div>
  <nav class="tree" id="tree"></nav>
</aside>

<main class="main" id="main">
  <div class="welcome">
    <h2>&#128214; __TITLE__</h2>
    <p>__SUBTITLE__</p>
    <p>点击左侧目录浏览文档，支持代码高亮、表格、图片。</p>
    <div class="hint">&#8592; 从左侧目录选择一篇文档开始阅读</div>
  </div>
</main>

<script>
var treeData = __TREE_JSON__;
var currentPath = null;
var expandedFolders = new Set();

function renderTree(nodes, container, depth) {
  depth = depth || 0;
  nodes.forEach(function(node) {
    if (node.type === 'folder') {
      var isOpen = depth < 1 ? true : expandedFolders.has(node.name);
      if (isOpen) expandedFolders.add(node.name);
      var div = document.createElement('div');
      div.className = 'tree-item folder' + (isOpen ? ' open' : '');
      div.innerHTML = '<span class="tree-icon">&#9654;</span><span class="item-name">' + escHtml(node.name) + '</span>';
      div.onclick = function(e) { toggleFolder(div, node.name); e.stopPropagation(); };
      var childDiv = document.createElement('div');
      childDiv.className = 'tree-children' + (isOpen ? ' open' : '');
      container.appendChild(div);
      container.appendChild(childDiv);
      renderTree(node.children, childDiv, depth + 1);
    } else {
      var a = document.createElement('a');
      a.className = 'tree-item file';
      a.href = '#' + node.path;
      a.setAttribute('data-path', node.path);
      a.setAttribute('data-name', node.name.toLowerCase());
      a.innerHTML = '<span class="tree-icon" style="font-size:0.65em">&#9679;</span><span class="item-name">' + escHtml(node.name) + '</span>';
      a.onclick = function(e) { e.preventDefault(); loadDoc(node.path, a); };
      container.appendChild(a);
    }
  });
}

function toggleFolder(el, name) {
  var childDiv = el.nextElementSibling;
  var isOpen = childDiv.classList.contains('open');
  if (isOpen) { childDiv.classList.remove('open'); el.classList.remove('open'); expandedFolders.delete(name); }
  else { childDiv.classList.add('open'); el.classList.add('open'); expandedFolders.add(name); }
}

function escHtml(s) { var d = document.createElement('div'); d.textContent = s; return d.innerHTML; }

function filterTree() {
  var q = document.getElementById('searchInput').value.toLowerCase();
  var allItems = document.querySelectorAll('.tree-item.file');
  var allFolders = document.querySelectorAll('.tree-item.folder');
  if (!q) {
    allItems.forEach(function(el) { el.style.display = ''; });
    allFolders.forEach(function(el) { el.style.display = ''; });
    document.querySelectorAll('.tree-children').forEach(function(el) { el.classList.remove('open'); });
    document.querySelectorAll('.tree-item.folder').forEach(function(el) { el.classList.remove('open'); });
    document.querySelectorAll('#tree > .tree-children').forEach(function(el) { el.classList.add('open'); });
    document.querySelectorAll('#tree > .tree-item.folder').forEach(function(el) { el.classList.add('open'); });
    return;
  }
  allItems.forEach(function(el) {
    var name = el.getAttribute('data-name');
    if (name.indexOf(q) > -1) {
      el.style.display = '';
      var parent = el.parentElement;
      while (parent && parent.classList.contains('tree-children')) {
        parent.classList.add('open');
        var folder = parent.previousElementSibling;
        if (folder && folder.classList.contains('tree-item')) { folder.classList.add('open'); }
        parent = parent.parentElement;
      }
    } else { el.style.display = 'none'; }
  });
  allFolders.forEach(function(el) {
    var childDiv = el.nextElementSibling;
    if (childDiv && childDiv.classList.contains('tree-children')) {
      var allHidden = true;
      childDiv.querySelectorAll('.tree-item.file').forEach(function(f) {
        if (f.style.display !== 'none') allHidden = false;
      });
      el.style.display = allHidden ? 'none' : '';
    }
  });
}

function loadDoc(path, el) {
  currentPath = path;
  document.querySelectorAll('.tree-item.active').forEach(function(item) { item.classList.remove('active'); });
  if (el) {
    el.classList.add('active');
    var parent = el.parentElement;
    while (parent && parent.classList.contains('tree-children')) {
      parent.classList.add('open');
      var folder = parent.previousElementSibling;
      if (folder && folder.classList.contains('tree-item')) {
        folder.classList.add('open');
        expandedFolders.add(folder.querySelector('.item-name').textContent);
      }
      parent = parent.parentElement;
    }
  }
  if (window.innerWidth <= 768) { toggleSidebar(); }
  var main = document.getElementById('main');
  main.innerHTML = '<div class="loading"><div class="spinner"></div><p>加载中...</p></div>';
  fetch('/api/content?path=' + encodeURIComponent(path))
    .then(function(r) { return r.json(); })
    .then(function(data) {
      if (data.error) {
        main.innerHTML = '<div class="welcome"><h2>出错了</h2><p>' + escHtml(data.error) + '</p></div>';
        return;
      }
      var bc = data.breadcrumb.map(function(b) { return escHtml(b); }).join(' &raquo; ');
      main.innerHTML = '<div class="breadcrumb">' + bc + '</div><div class="content">' + data.html + '</div>';
      if (typeof hljs !== 'undefined') {
        main.querySelectorAll('pre code').forEach(function(block) { hljs.highlightElement(block); });
      }
      main.scrollTop = 0; window.scrollTo(0, 0);
      if (history.pushState) { history.pushState(null, '', '#' + path); }
    })
    .catch(function(err) {
      main.innerHTML = '<div class="welcome"><h2>加载失败</h2><p>' + escHtml(err.message) + '</p></div>';
    });
}

function toggleSidebar() {
  var sidebar = document.getElementById('sidebar');
  var overlay = document.querySelector('.sidebar-overlay');
  if (window.innerWidth <= 768) {
    // 移动端：overlay 模式
    var isOpen = sidebar.classList.toggle('open');
    overlay.classList.toggle('open', isOpen);
    // 确保 sidebar 在 DOM 顺序上 open 和 overlay 同步
    if (isOpen) {
      overlay.classList.add('open');
    } else {
      overlay.classList.remove('open');
    }
  } else {
    // 桌面端：推入/推出模式
    document.body.classList.toggle('sidebar-hidden');
    try {
      localStorage.setItem('sidebar-hidden', document.body.classList.contains('sidebar-hidden'));
    } catch(e) {}
  }
  updateToggleIcon();
}

function updateToggleIcon() {
  var btn = document.querySelector('.sidebar-toggle');
  var sidebar = document.getElementById('sidebar');
  if (!btn) return;
  var isOpen;
  if (window.innerWidth <= 768) {
    isOpen = sidebar.classList.contains('open');
  } else {
    isOpen = !document.body.classList.contains('sidebar-hidden');
  }
  btn.innerHTML = isOpen ? '&#10005;' : '&#9776;';
  btn.title = isOpen ? '关闭侧边栏' : '打开侧边栏';
}

document.addEventListener('DOMContentLoaded', function() {
  renderTree(treeData, document.getElementById('tree'), 0);
  document.querySelectorAll('#tree > .tree-children').forEach(function(el) { el.classList.add('open'); });
  document.querySelectorAll('#tree > .tree-item.folder').forEach(function(el) { el.classList.add('open'); });

  // 恢复侧边栏状态
  if (window.innerWidth > 768) {
    try {
      if (localStorage.getItem('sidebar-hidden') === 'true') {
        document.body.classList.add('sidebar-hidden');
      }
    } catch(e) {}
  }
  updateToggleIcon();

  // 窗口大小变化时清理跨断点状态
  window.addEventListener('resize', function() {
    if (window.innerWidth > 768) {
      // 从移动端切回桌面端：移除 overlay 类
      document.getElementById('sidebar').classList.remove('open');
      document.querySelector('.sidebar-overlay').classList.remove('open');
    } else {
      // 从桌面端切到移动端：桌面折叠类不影响移动端 overlay 逻辑
    }
    updateToggleIcon();
  });

  document.addEventListener('keydown', function(e) {
    if (e.key === '/' && document.activeElement !== document.getElementById('searchInput')) {
      e.preventDefault(); document.getElementById('searchInput').focus();
    }
    if (e.key === 'Escape') {
      document.getElementById('searchInput').value = ''; filterTree();
      document.getElementById('searchInput').blur();
      // Esc 关闭侧边栏（如果打开中）
      if (window.innerWidth <= 768 && document.getElementById('sidebar').classList.contains('open')) {
        toggleSidebar();
      }
    }
  });

  if (window.location.hash) {
    var hashPath = window.location.hash.substring(1);
    var el = document.querySelector('[data-path="' + hashPath + '"]');
    if (el) { loadDoc(hashPath, el); }
  }
});

window.addEventListener('hashchange', function() {
  var hashPath = window.location.hash.substring(1);
  if (hashPath && hashPath !== currentPath) {
    var el = document.querySelector('[data-path="' + hashPath + '"]');
    if (el) loadDoc(hashPath, el);
  }
});
</script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
</body>
</html>'''


# ========== HTTP 处理 ==========
class DocHandler(http.server.BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        # 简化日志输出，不做复杂格式化
        if args:
            try:
                msg = format % args
            except TypeError:
                msg = format + ' ' + str(args)
        else:
            msg = format
        print("[{}] {}".format(self.client_address[0], msg))

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        qs = urllib.parse.parse_qs(parsed.query)

        try:
            if path == '/' or path == '/index.html':
                self.serve_index()
            elif path == '/api/tree':
                self.serve_tree()
            elif path == '/api/content':
                self.serve_content(qs)
            else:
                self.send_error(404)
        except Exception as e:
            self.send_json({"error": str(e)})

    def serve_index(self):
        html = build_page()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

    def serve_tree(self):
        tree = build_tree()
        self.send_json(tree)

    def serve_content(self, qs):
        rel_path = qs.get("path", [None])[0]
        if not rel_path:
            self.send_json({"error": "缺少 path 参数"})
            return
        abs_path = (DOC_ROOT / rel_path).resolve()
        if not str(abs_path).startswith(str(DOC_ROOT.resolve())):
            self.send_json({"error": "非法的文件路径"})
            return
        if not abs_path.exists() or not abs_path.is_file():
            self.send_json({"error": "文件不存在: {}".format(rel_path)})
            return
        try:
            with open(abs_path, 'r', encoding='utf-8') as f:
                md_text = f.read()
        except Exception as e:
            self.send_json({"error": "读取失败: {}".format(str(e))})
            return

        html_body = render_md_to_html(md_text)
        breadcrumb = [strip_order_prefix(p) for p in rel_path.replace('\\', '/').split('/')[:-1]]
        breadcrumb.append(strip_order_prefix(Path(rel_path).stem))

        self.send_json({"html": html_body, "breadcrumb": breadcrumb, "path": rel_path})

    def send_json(self, data):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(body)


def main():
    print("=" * 60)
    print("  {}  文档服务器".format(TITLE))
    print("  文档目录: {}".format(DOC_ROOT))
    print("=" * 60)
    print()
    print("  服务器已启动: http://localhost:{}".format(PORT))
    print("  按 Ctrl+C 停止")
    print()

    server = http.server.HTTPServer((HOST, PORT), DocHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n服务器已停止")
        server.server_close()


if __name__ == '__main__':
    main()
