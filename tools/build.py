"""src/ ve data/ içeriğini tek, bağımsız çalışan index.html dosyasına derler.

Kullanım:  python3 tools/build_questions.py && python3 tools/build.py
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
JS_ORDER = ["lessons.js", "core.js", "engine.js", "program.js", "logic.js", "views.js"]


def read(*p):
    with open(os.path.join(*p), encoding="utf-8") as f:
        return f.read()


def main():
    tpl = read(SRC, "index.template.html")
    bank = json.loads(read(ROOT, "data", "questions.json"))
    data = "window.QBANK = " + json.dumps(bank, ensure_ascii=False, separators=(",", ":")) + ";"
    js = "\n".join(f"/* ---- {name} ---- */\n" + read(SRC, name) for name in JS_ORDER)
    for s in (data, js):
        assert "</script" not in s.lower(), "gömülü betik '</script' içeremez"
    html = tpl.replace("/*__CSS__*/", read(SRC, "style.css")).replace("/*__DATA__*/", data).replace("/*__JS__*/", js)
    out = os.path.join(ROOT, "index.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"index.html yazıldı: {len(html.encode('utf-8')) / 1024:.0f} KB, {bank['meta']['count']} soru")


if __name__ == "__main__":
    main()
