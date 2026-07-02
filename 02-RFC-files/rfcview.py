#!/usr/bin/env python3
"""
RFC Page Viewer — 基于 Textual 的交互式 RFC 分页阅读器

利用 RFC 文档的标准页眉/页脚自动切割页面，在终端中逐页浏览原文。

用法：
  python rfcview.py rfc7348-vxlan.txt
  python rfcview.py rfc4271-bgp4.txt -p 50    # 从第 50 页开始
  textual run rfcview.py -- file.txt          # Dev 模式（热重载）
"""

import re
import os
import sys
from textwrap import dedent

from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Header, Footer, Static, Input


# ── RFC 文档解析 ────────────────────────────────────────

def parse_rfc(filepath: str) -> dict:
    """解析 RFC 文件，返回元信息和分页列表"""
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    # 提取 RFC 编号和标题
    basename = os.path.basename(filepath)
    m = re.search(r'rfc(\d+)', basename, re.IGNORECASE)
    rfc_num = m.group(1) if m else '????'

    # 从文件头部提取标题
    lines = content.split('\n')
    title = ''
    # 标题特征：位于 RFC 头部信息（作者、日期等）之后，是一行或两行居中/缩进的描述性文字
    # 策略：先找到日期行（Month Year），然后取之后第一个有内容的行
    date_seen = False
    for line in lines[:40]:
        s = line.strip()
        if not date_seen:
            if re.search(r'(^|\s)(January|February|March|April|May|June|July|'
                     r'August|September|October|November|December)\s+\d{4}', s):
                date_seen = True
            continue
        if not s:
            continue
        # 日期之后第一个有实质内容的行就是标题
        if len(s) > 10:
            title = s
            break

    # ── 按换页符切割页面 ──
    segments = content.split('\f')
    pages = []

    for seg in segments:
        seg_lines = seg.split('\n')
        cleaned = []
        for line in seg_lines:
            line = line.rstrip()
            # 去掉页脚：含 "[Page N]"
            if re.search(r'\[Page \d+\]', line):
                continue
            # 去掉页眉：以 "RFC NNNN" 开头且跟大量空格
            if re.match(r'^RFC \d+[ ]{2,}', line):
                continue
            cleaned.append(line)

        # 去掉顶部和底部的连续空行
        while cleaned and not cleaned[0].strip():
            cleaned.pop(0)
        while cleaned and not cleaned[-1].strip():
            cleaned.pop()

        if cleaned:
            pages.append(cleaned)

    # 构建 TOC（从目录页提取章节索引）
    toc = []
    for pi, page_lines in enumerate(pages):
        for li, line in enumerate(page_lines):
            s = line.strip()
            if s == 'Table of Contents':
                continue
            if '....' in s and re.search(r'\d+$', s):
                title_part = s.split('....')[0].strip()
                toc.append((title_part, pi))

    return {
        'rfc_num': rfc_num,
        'title': title or f'RFC {rfc_num}',
        'pages': pages,
        'total': len(pages),
        'toc': toc,
    }


# ── Modal 弹窗：跳转到指定页 ────────────────────────────

class GotoScreen(ModalScreen[int | None]):
    """输入页码后按 Enter 跳转"""

    BINDINGS = [
        Binding("escape", "dismiss_none", "取消", priority=True),
        Binding("enter", "submit", "确认"),
    ]

    def __init__(self, max_page: int):
        super().__init__()
        self.max_page = max_page

    def compose(self) -> ComposeResult:
        with VerticalScroll():
            yield Static(f'跳转到页 (1–{self.max_page})', id="goto-label")
            yield Input(placeholder='输入页码...', id="goto-input")

    def on_mount(self):
        self.query_one(Input).focus()

    @on(Input.Submitted)
    def _on_input_submit(self):
        """Input 内按 Enter 时触发"""
        self._do_go()

    def action_submit(self):
        """屏幕级 Enter 绑定（Input 失去焦点时的后备）"""
        self._do_go()

    def _do_go(self):
        inp = self.query_one(Input)
        try:
            n = int(inp.value)
            if 1 <= n <= self.max_page:
                self.dismiss(n)
            else:
                inp.value = ''
                self.app.clear_notifications()
                self.notify(f'页码范围: 1–{self.max_page}', severity='warning')
        except ValueError:
            inp.value = ''
            self.app.clear_notifications()
            self.notify('请输入数字', severity='warning')

    def action_dismiss_none(self):
        self.dismiss(None)


# ── Modal 弹窗：搜索 ────────────────────────────────────

class SearchScreen(ModalScreen[str | None]):
    """输入关键词后 Enter 搜索，实时高亮"""

    BINDINGS = [
        Binding("escape", "dismiss_none", "取消", priority=True),
    ]

    def compose(self) -> ComposeResult:
        with VerticalScroll():
            yield Static('搜索 (Enter 确认, Esc 取消)', id="search-label")
            yield Input(placeholder='输入关键词...', id="search-input")

    def on_mount(self):
        self.query_one(Input).focus()

    @on(Input.Submitted)
    def on_submit(self, event: Input.Submitted):
        if event.value.strip():
            self.dismiss(event.value.strip())
        else:
            self.dismiss(None)

    def action_dismiss_none(self):
        self.dismiss(None)


# ── 帮助屏 ──────────────────────────────────────────────

class HelpScreen(ModalScreen[None]):
    BINDINGS = [
        Binding("escape", "dismiss_help", "返回", priority=True),
    ]

    def compose(self) -> ComposeResult:
        with VerticalScroll():
            yield Static(dedent("""\
            [bold]RFC Viewer — 按键说明[/]

            [bold]导航[/]
              n / → / Space        下一页
              p / ← / Backspace    上一页
              PgDn                 前进 5 页
              PgUp                 后退 5 页
              Home                 第一页
              End                  最后一页

            [bold]功能[/]
              g                    跳转到指定页
              /                    搜索关键词
              h / ?                显示此帮助
              q / Esc              退出

            [bold]提示[/]
              搜索到的关键词在页面中会高亮显示。
              页面按 RFC 原文的换页符 (form feed) 切割。
            """), id="help-text")

    def action_dismiss_help(self):
        self.dismiss(None)


# ── 主应用 ──────────────────────────────────────────────

class RfcViewerApp(App):
    """RFC 分页查看器"""

    CSS = """
    Header {
        background: $primary;
        color: $text;
        text-style: bold;
    }

    Footer {
        background: $primary;
    }

    #page-content {
        padding: 0 1;
        width: 100%;
        height: auto;
    }

    /* ── Goto 弹窗 ── */
    GotoScreen {
        align: center middle;
    }
    GotoScreen > VerticalScroll {
        width: 40;
        height: auto;
        max-height: 12;
        background: $surface;
        border: thick $primary;
        padding: 1 2;
    }
    #goto-label {
        margin-bottom: 1;
        text-style: bold;
    }
    #goto-input {
        width: 100%;
    }

    /* ── Search 弹窗 ── */
    SearchScreen {
        align: center middle;
    }
    SearchScreen > VerticalScroll {
        width: 50;
        height: auto;
        max-height: 12;
        background: $surface;
        border: thick $primary;
        padding: 1 2;
    }
    #search-label {
        margin-bottom: 1;
        text-style: bold;
    }
    #search-input {
        width: 100%;
    }

    /* ── Help 弹窗 ── */
    HelpScreen {
        align: center middle;
    }
    HelpScreen > VerticalScroll {
        width: 50;
        height: auto;
        max-height: 28;
        background: $surface;
        border: thick $primary;
        padding: 1 2;
    }
    """

    BINDINGS = [
        Binding("n,right,space,j", "next_page", "下一页", show=True),
        Binding("p,left,backspace,k", "prev_page", "上一页", show=True),
        Binding("g", "goto_page", "跳转", show=True),
        Binding("slash", "search", "搜索", show=True),
        Binding("comma", "next_match", "下一匹配", show=False),
        Binding("period", "prev_match", "上一匹配", show=False),
        Binding("h,question_mark", "show_help", "帮助", show=True),
        Binding("pagedown", "next_5", "前进 5 页", show=False),
        Binding("pageup", "prev_5", "后退 5 页", show=False),
        Binding("home", "first_page", "首页", show=False),
        Binding("end", "last_page", "末页", show=False),
        Binding("q,escape", "quit", "退出", show=True),
    ]

    def __init__(self, filepath: str, start_page: int = 0):
        # 先解析数据（不涉及 reactive 属性）
        self._meta = parse_rfc(filepath)
        if not self._meta['pages']:
            print("错误：未能从文件中提取任何页面。")
            sys.exit(1)
        self._rfc_num = self._meta['rfc_num']
        self._rfc_title = self._meta['title']
        self._pages = self._meta['pages']
        self._total = self._meta['total']
        self._toc = self._meta['toc']
        self._current = max(0, min(start_page, self._total - 1))
        self._search_term: str = ''
        self._search_matches: list[int] = []
        self._match_idx: int = 0
        super().__init__()

    # ── 布局 ──

    def compose(self) -> ComposeResult:
        yield Header()
        with VerticalScroll(id="body"):
            self.content = Static('', id='page-content', markup=True)
            yield self.content
        yield Footer()

    def on_mount(self):
        self.title = f'RFC {self._rfc_num}: {self._rfc_title}'
        self.sub_title = f'Page {self._current + 1}/{self._total}'
        self.refresh_page()

    # ── 页面渲染 ──

    def refresh_page(self):
        """渲染当前页，处理搜索高亮"""
        lines = self._pages[self._current]
        text = '\n'.join(lines)

        if self._search_term:
            # 转义 Rich markup 中的 [
            text = text.replace('[', r'\[')
            text = text.replace(']', r'\]')
            # 对搜索词做高亮替换
            term = re.escape(self._search_term)
            highlighted = re.sub(
                term,
                lambda m: f'[bold reverse]{m.group()}[/]',
                text,
                flags=re.IGNORECASE,
            )
            self.content.update(highlighted)
            # 记录匹配行号（用于逐个跳转）
            self._search_matches = [
                i for i, line in enumerate(lines)
                if self._search_term.lower() in line.lower()
            ]
            self._match_idx = 0
        else:
            # 无搜索：转义方括号防止被 Rich 误解析
            text = text.replace('[', r'\[')
            text = text.replace(']', r'\]')
            self.content.update(text)

        self.sub_title = f'Page {self._current + 1}/{self._total}'

    # ── 翻页动作 ──

    def action_next_page(self):
        if self._current < self._total - 1:
            self._current += 1
            self.refresh_page()
        else:
            self.clear_notifications()
            self.notify('已是最后一页', severity='warning')

    def action_prev_page(self):
        if self._current > 0:
            self._current -= 1
            self.refresh_page()
        else:
            self.clear_notifications()
            self.notify('已是第一页', severity='warning')

    def action_next_5(self):
        self._current = min(self._current + 5, self._total - 1)
        self.refresh_page()

    def action_prev_5(self):
        self._current = max(self._current - 5, 0)
        self.refresh_page()

    def action_first_page(self):
        self._current = 0
        self.refresh_page()

    def action_last_page(self):
        self._current = self._total - 1
        self.refresh_page()

    # ── 搜索匹配跳转 ──

    def action_next_match(self):
        if not self._search_matches:
            return
        self._match_idx = (self._match_idx + 1) % len(self._search_matches)
        self._scroll_to_match()

    def action_prev_match(self):
        if not self._search_matches:
            return
        self._match_idx = (self._match_idx - 1) % len(self._search_matches)
        self._scroll_to_match()

    def _scroll_to_match(self):
        """滚动到当前匹配行"""
        line_no = self._search_matches[self._match_idx]
        try:
            self.query_one(VerticalScroll).scroll_to(
                y=line_no, animate=False
            )
        except Exception:
            pass

    # ── 弹窗：跳转 ──

    def action_goto_page(self):
        self.push_screen(GotoScreen(self._total), callback=self._on_goto)

    def _on_goto(self, page_num: int | None):
        if page_num is not None:
            self._current = page_num - 1
            self.refresh_page()

    # ── 弹窗：搜索 ──

    def action_search(self):
        self.push_screen(SearchScreen(), callback=self._on_search)

    def _on_search(self, term: str | None):
        if term:
            self._search_term = term
            self.refresh_page()
            self.notify(
                f'搜索 "{term}" — 当前页 '
                f'{len(self._search_matches)} 个匹配 '
                f'(按 , . 跳转匹配项)'
            )
        elif term is None:
            pass

    # ── 弹窗：帮助 ──

    def action_show_help(self):
        self.push_screen(HelpScreen())

    # ── 键盘：数字快速翻页比例（如按 5 跳到 50% 位置）──
    # 暂不实现，保留扩展空间


# ── 入口 ──────────────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description='RFC Page Viewer — 交互式 RFC 分页阅读器 (基于 Textual)')
    parser.add_argument('file', help='RFC .txt 文件路径')
    parser.add_argument('-p', '--page', type=int, default=1,
                        help='起始页码 (默认: 1)')
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f'文件不存在: {args.file}')
        sys.exit(1)

    app = RfcViewerApp(args.file, start_page=args.page - 1)
    app.run()


if __name__ == '__main__':
    main()
