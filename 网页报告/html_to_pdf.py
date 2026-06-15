"""Section 1-项目回顾.html → PDF (v3)
A4 横向 16:9 (297mm x 167mm)，每页 1 张 slide
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

HTML = Path(r"c:\Users\CICI\Documents\trae_projects\competitor_finance_info\网页报告\Section 1-项目回顾.html").absolute()
OUT  = Path(r"c:\Users\CICI\Documents\trae_projects\competitor_finance_info\网页报告\Section 1-项目回顾.pdf").absolute()

PRINT_CSS = """
* { animation: none !important; transition: none !important; }

html, body {
    width: 297mm !important;
    background: #f4f1ea !important;
    margin: 0 !important;
    padding: 0 !important;
    overflow: visible !important;
}

body {
    min-height: auto !important;
    height: auto !important;
    position: static !important;
    display: block !important;
}

.deck-viewport {
    position: static !important;
    inset: auto !important;
    width: 297mm !important;
    height: auto !important;
    min-height: auto !important;
    max-height: none !important;
    overflow: visible !important;
    background: #f4f1ea !important;
    display: block !important;
    transform: none !important;
}

.deck-stage {
    position: static !important;
    width: 297mm !important;
    height: auto !important;
    min-height: auto !important;
    max-height: none !important;
    transform: none !important;
    overflow: visible !important;
    display: block !important;
    background: #f4f1ea !important;
}

.slide {
    position: relative !important;
    inset: auto !important;
    width: 297mm !important;
    height: 167mm !important;
    min-height: 167mm !important;
    max-height: 167mm !important;
    margin: 0 !important;
    visibility: visible !important;
    opacity: 1 !important;
    pointer-events: auto !important;
    z-index: 1 !important;
    transform: none !important;
    page-break-after: always !important;
    page-break-inside: avoid !important;
    break-after: page !important;
    break-inside: avoid !important;
    display: block !important;
    overflow: hidden !important;
    box-shadow: 0 2px 10px rgba(0,0,0,0.10) !important;
    background: var(--bg) !important;
}

.slide:last-of-type {
    page-break-after: auto !important;
    break-after: auto !important;
}

.top-strip, .bottom-strip { position: absolute !important; }
.edit-controls, .edit-status, .edit-btn { display: none !important; }

@page {
    size: 297mm 167mm;
    margin: 0;
}
"""

with sync_playwright() as pw:
    browser = pw.chromium.launch()
    context = browser.new_context(
        viewport={"width": 1122, "height": 631},  # 297mm x 167mm at 96dpi
        device_scale_factor=2,
    )
    page = context.new_page()
    page.goto(f"file:///{HTML}".replace("\\", "/"), wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(2500)

    page.add_style_tag(content=PRINT_CSS)
    page.wait_for_timeout(1500)

    slide_count = page.evaluate("document.querySelectorAll('.slide').length")
    print(f"Total slides: {slide_count}")

    visible = page.evaluate("""
        Array.from(document.querySelectorAll('.slide')).map(s => ({
            h: s.offsetHeight, w: s.offsetWidth,
            vis: getComputedStyle(s).visibility,
            op:  getComputedStyle(s).opacity,
        }))
    """)
    for i, v in enumerate(visible, 1):
        print(f"  slide {i:2d}: {v['w']}x{v['h']} vis={v['vis']} op={v['op']}")

    body_h = page.evaluate("document.body.scrollHeight")
    print(f"Body scrollHeight: {body_h}px")

    page.pdf(
        path=str(OUT),
        width="297mm",
        height="167mm",
        margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        print_background=True,
        prefer_css_page_size=True,
    )
    print(f"OK  {OUT}")
    print(f"    size = {OUT.stat().st_size:,} bytes ({OUT.stat().st_size / 1024 / 1024:.2f} MB)")

    browser.close()
