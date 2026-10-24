"""Extract the policy text from a .docx with the standard library only (headers, body, tables, footers).

Usage: python3 -I extrair_politica.py <politica.docx> > politica.txt
"""
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def paragraphs(xml: bytes):
    root = ET.fromstring(xml)
    for p in root.iter(W + "p"):
        text = "".join(t.text or "" for t in p.iter(W + "t"))
        if text.strip():
            yield text


def main(path: str) -> None:
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        for n in sorted(x for x in names if re.match(r"word/header\d*\.xml$", x)):
            for t in paragraphs(z.read(n)):
                print("[cab]", t)
        for t in paragraphs(z.read("word/document.xml")):
            print(t)
        for n in sorted(x for x in names if re.match(r"word/footer\d*\.xml$", x)):
            for t in paragraphs(z.read(n)):
                print("[rod]", t)
        if "docProps/core.xml" in names:
            core = z.read("docProps/core.xml").decode("utf-8", "replace")
            for tag in ("created", "modified"):
                m = re.search(rf"<dcterms:{tag}[^>]*>([^<]+)<", core)
                if m:
                    print(f"[core] {tag}: {m.group(1)}")


if __name__ == "__main__":
    main(sys.argv[1])
