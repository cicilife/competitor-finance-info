"""关闭编辑模式：删除 EDIT/SAVE 按钮、edit-status 指示器、body edit-mode、
   所有 contenteditable 与 .editable class、editor JS、相关 CSS。
"""
import re, sys
from pathlib import Path

src = Path(r"c:\Users\CICI\Documents\trae_projects\competitor_finance_info\网页报告\Section 1-项目回顾.html")
text = src.read_text(encoding="utf-8")
original_len = len(text)

# 1. body class 移除 edit-mode
text = re.sub(r'<body class="[^"]*\bedit-mode\b[^"]*">', '<body>', text)
text = re.sub(r'<body class="edit-mode">', '<body>', text)
text = re.sub(r' class="[^"]*\bedit-mode\b[^"]*"', '', text)

# 2. 删除 edit-controls 整个 block（含 </div> 结束标签）
text = re.sub(
    r'<div class="edit-controls">.*?</div>\s*',
    '',
    text,
    flags=re.DOTALL,
)

# 3. 删除 edit-status 整个 block
text = re.sub(
    r'<div class="edit-status">.*?</div>\s*',
    '',
    text,
    flags=re.DOTALL,
)

# 4. 移除 contenteditable="true" 属性
text = re.sub(r'\s+contenteditable="true"', '', text)
text = re.sub(r'\s+contenteditable="false"', '', text)
text = re.sub(r'\s+contenteditable="plaintext-only"', '', text)

# 5. 移除 class 中的 editable (但不删其他 class)
def strip_editable_in_class(m):
    cls = m.group(1)
    parts = [p for p in cls.split() if p != 'editable']
    if not parts:
        return ''
    return f' class="{" ".join(parts)}"'
text = re.sub(r' class="([^"]*)"', strip_editable_in_class, text)

# 6. 删除 CSS 中 .editable / .edit-mode / .edit-controls / .edit-btn / .edit-status
css_rules_to_remove = [
    r'\.editable:hover[^{]*\{[^}]*\}\s*',
    r'\.edit-mode [^{]*\{[^}]*\}\s*',
    r'\.edit-mode[^{]*\{[^}]*\}\s*',
    r'\.edit-controls[^{]*\{[^}]*\}\s*',
    r'\.edit-btn[^{]*\{[^}]*\}\s*',
    r'\.edit-btn:hover[^{]*\{[^}]*\}\s*',
    r'\.edit-status[^{]*\{[^}]*\}\s*',
    r'@keyframes pulse\s*\{[^}]*\}\s*',
    r'@keyframes pulse\s*\{[^}]*\{[^}]*\}\s*',
]
for pat in css_rules_to_remove:
    text = re.sub(pat, '', text, flags=re.DOTALL)

# 7. 删除 JS 中的 editor 相关
#    整段 editor = { ... }
text = re.sub(
    r'const editor = \{[\s\S]*?\n\s*\};?\s*',
    '',
    text,
)
#    saveHTML 函数
text = re.sub(
    r'(function|const|let|var)\s+saveHTML\s*=\s*function\s*\([\s\S]*?\n\s*\};?\s*',
    '',
    text,
)
#    saveHTML 简化形式
text = re.sub(
    r'function\s+saveHTML\s*\(\)\s*\{[\s\S]*?\n\s*\}\s*',
    '',
    text,
)
#    toggleEdit 函数
text = re.sub(
    r'function\s+toggleEdit\s*\(\)\s*\{[\s\S]*?\n\s*\}\s*',
    '',
    text,
)
#    编辑按钮事件监听 (editBtn / saveBtn)
text = re.sub(
    r"document\.getElementById\(['\"]editBtn['\"]\)\.addEventListener[\s\S]*?\}\s*\)\s*;?",
    '',
    text,
)
text = re.sub(
    r"document\.getElementById\(['\"]saveBtn['\"]\)\.addEventListener[\s\S]*?\}\s*\)\s*;?",
    '',
    text,
)
#    Ctrl+S / E key 监听
text = re.sub(
    r"document\.addEventListener\(['\"]keydown['\"][\s\S]*?\}\s*\)\s*;?",
    '',
    text,
)

# 8. SlidePresentation 构造函数中如果有 contenteditable 跳过逻辑，删除
text = re.sub(
    r'if \(el\.hasAttribute\([\'"]contenteditable[\'"]\)\) continue;\s*',
    '',
    text,
)
text = re.sub(
    r'el\.getAttribute\([\'"]contenteditable[\'"]\)[\s\S]*?continue;\s*',
    '',
    text,
)
text = re.sub(
    r'if \(el\.isContentEditable\) continue;\s*',
    '',
    text,
)

# 清理空行（连续 3+ 空行压缩为 1 行）
text = re.sub(r'\n{3,}', '\n\n', text)

src.write_text(text, encoding="utf-8")
print(f"[OK] 编辑模式已关闭  原大小={original_len}  新大小={len(text)}  减少={original_len-len(text)} 字节")
