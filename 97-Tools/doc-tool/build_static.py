#!/usr/bin/env python3
"""
静态 HTML 文档站生成器
读取所有 .md 文件，预渲染为 HTML，输出单一自包含 index.html。
打开 index.html 即可浏览，无需本地服务器。

用法: python build_static.py
输出: docs/index.html
"""

import json
import re
from pathlib import Path
from markdown import markdown

# ========== 配置 ==========
DOC_ROOT = Path(r"D:\阿里云ACP\docs")
OUTPUT = DOC_ROOT / "index.html"
TITLE = "阿里云 ACP 备考笔记"
SUBTITLE = "云计算架构师高级认证（ACP）"

# ========== 工具函数（与 doc_server.py 保持一致） ==========
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

# ========== 收集所有文件路径 ==========
def collect_files(nodes):
    """从目录树中提取所有文件路径"""
    paths = []
    for node in nodes:
        if node["type"] == "file":
            paths.append(node["path"])
        if "children" in node:
            paths.extend(collect_files(node["children"]))
    return paths

# ========== 构建内容数据 ==========
def build_content_data(tree):
    """遍历所有 MD 文件，渲染 HTML，返回 {path: {html, breadcrumb}} 的字典"""
    content = {}
    paths = collect_files(tree)
    total = len(paths)
    for i, rel_path in enumerate(paths):
        abs_path = DOC_ROOT / rel_path
        try:
            with open(abs_path, 'r', encoding='utf-8') as f:
                md_text = f.read()
        except Exception as e:
            print(f"  [跳过] {rel_path} — 读取失败: {e}")
            continue

        html_body = render_md_to_html(md_text)

        # 面包屑：路径各段 + 文件名，去掉数字前缀
        breadcrumb = [strip_order_prefix(p) for p in rel_path.replace('\\', '/').split('/')[:-1]]
        breadcrumb.append(strip_order_prefix(Path(rel_path).stem))

        content[rel_path] = {"html": html_body, "breadcrumb": breadcrumb}
        print(f"  [{i+1}/{total}] {rel_path}")

    return content

# ========== HTML 页面 ==========
def build_page(tree, content_data):
    tree_json = json.dumps(tree, ensure_ascii=False)
    content_json = json.dumps(content_data, ensure_ascii=False)
    total = count_files(tree)
    stats = "{} 个模块 · {} 篇文档".format(len(tree), total)

    html = get_page_html()
    html = html.replace('__TITLE__', TITLE)
    html = html.replace('__SUBTITLE__', SUBTITLE)
    html = html.replace('__STATS__', stats)
    html = html.replace('__TREE_JSON__', tree_json)
    html = html.replace('__CONTENT_JSON__', content_json)
    return html

def get_page_html():
    # 与 doc_server.py 基本一致，关键区别：
    # 1. loadDoc 从内嵌的 contentData 取数据，不走 AJAX
    # 2. 不加载 highlight.js（预渲染时 codehilite 已生成带 class 的 HTML）
    return '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__TITLE__</title>
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

/* 桌面端：侧边栏推入推出 */
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
    <p>静态独立页面，无需服务器，点击左侧目录直接浏览。</p>
    <div class="hint">&#8592; 从左侧目录选择一篇文档开始阅读</div>
  </div>
</main>

<script>
var treeData = __TREE_JSON__;
var contentData = __CONTENT_JSON__;   // {path: {html, breadcrumb}}
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

// ★ 关键变化：从内嵌 contentData 取内容，不再发起 HTTP 请求
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
  var data = contentData[path];
  if (!data) {
    main.innerHTML = '<div class="welcome"><h2>出错了</h2><p>内容未找到: ' + escHtml(path) + '</p></div>';
    return;
  }
  var bc = data.breadcrumb.map(function(b) { return escHtml(b); }).join(' &raquo; ');
  main.innerHTML = '<div class="breadcrumb">' + bc + '</div><div class="content">' + data.html + '</div>';
  main.scrollTop = 0; window.scrollTo(0, 0);
  if (history.pushState) { history.pushState(null, '', '#' + path); }
}

function toggleSidebar() {
  var sidebar = document.getElementById('sidebar');
  var overlay = document.querySelector('.sidebar-overlay');
  if (window.innerWidth <= 768) {
    var isOpen = sidebar.classList.toggle('open');
    overlay.classList.toggle('open', isOpen);
  } else {
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

  if (window.innerWidth > 768) {
    try {
      if (localStorage.getItem('sidebar-hidden') === 'true') {
        document.body.classList.add('sidebar-hidden');
      }
    } catch(e) {}
  }
  updateToggleIcon();

  window.addEventListener('resize', function() {
    if (window.innerWidth > 768) {
      document.getElementById('sidebar').classList.remove('open');
      document.querySelector('.sidebar-overlay').classList.remove('open');
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
</body>
</html>'''


# ========== 主流程 ==========
def main():
    print("=" * 60)
    print("  阿里云 ACP 静态文档站生成器")
    print("=" * 60)
    print()

    print("[1/3] 构建目录树...")
    tree = build_tree()
    total = count_files(tree)
    print(f"  找到 {len(tree)} 个模块，共 {total} 篇文档")

    print()
    print("[2/3] 渲染 Markdown → HTML...")
    content_data = build_content_data(tree)
    print(f"  完成，{len(content_data)} 篇渲染成功")

    print()
    print("[3/3] 生成静态页面...")
    page = build_page(tree, content_data)
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write(page)

    size_kb = OUTPUT.stat().st_size / 1024
    print(f"  输出: {OUTPUT}")
    print(f"  大小: {size_kb:.1f} KB")
    print()
    print("=" * 60)
    print("  生成完成！用浏览器打开 index.html 即可浏览。")
    print("=" * 60)


if __name__ == '__main__':
    main()
