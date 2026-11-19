#!/usr/bin/env python3
"""SUÇÜSTÜ! sayfalarını doğrulama aracı.

Kontroller:
1. docs/sucustu/ içindeki yeni sayfalar (index.html, privacy/index.html, support/index.html, terms/index.html) mevcut mu?
2. Her sayfanın doctype'ı var mı?
3. Her sayfada <html lang="..."> var mı?
4. Her sayfada viewport meta etiketi var mı?
5. Her sayfada <title> var mı ve dolu mu?
6. Her sayfada hem #tr hem #en bölümleri var mı?
7. Her dil bölümünde (#tr ve #en) tam olarak bir adet <h1> var mı?
8. Tüm göreli bağlantılar ve çıpalar (anchors) mevcut dosya ve kimliklere (ids) çözümleniyor mu?
9. Dış kaynaklı (off-site) <script src=...> var mı?
10. docs/sucustu.html ve docs/sucustu/ altında hiçbir yerde "nazartesi.com" geçiyor mu?
11. docs/sitemap.xml 4 yeni URL'yi içeriyor mu?
"""
import sys
import os
import re
import pathlib
import urllib.parse
from html.parser import HTMLParser

class SimpleDOMParser(HTMLParser):
    VOID_TAGS = {
        'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
        'link', 'meta', 'param', 'source', 'track', 'wbr'
    }

    class Element:
        def __init__(self, tag, attrs, parent=None):
            self.tag = tag.lower()
            self.attrs = {k.lower(): v for k, v in attrs}
            self.parent = parent
            self.children = []
            self.text = ""

        def find_by_id(self, elem_id):
            if self.attrs.get('id') == elem_id:
                return self
            for child in self.children:
                res = child.find_by_id(elem_id)
                if res:
                    return res
            return None

        def find_all(self, tag):
            results = []
            if self.tag == tag.lower():
                results.append(self)
            for child in self.children:
                results.extend(child.find_all(tag))
            return results

        def get_all_ids(self):
            ids = set()
            if 'id' in self.attrs:
                ids.add(self.attrs['id'])
            for child in self.children:
                ids.update(child.get_all_ids())
            return ids

    def __init__(self):
        super().__init__()
        self.root = self.Element('root', [])
        self.stack = [self.root]
        self.all_elements = []

    def handle_starttag(self, tag, attrs):
        elem = self.Element(tag, attrs, self.stack[-1])
        self.stack[-1].children.append(elem)
        self.all_elements.append(elem)
        if tag.lower() not in self.VOID_TAGS:
            self.stack.append(elem)

    def handle_endtag(self, tag):
        tag_l = tag.lower()
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag_l:
                self.stack = self.stack[:i]
                break

    def handle_data(self, data):
        if self.stack:
            self.stack[-1].text += data


def parse_html_file(file_path):
    parser = SimpleDOMParser()
    content = file_path.read_text(encoding='utf-8')
    parser.feed(content)
    return parser, content


def main():
    repo_root = pathlib.Path(__file__).resolve().parent.parent
    docs_dir = repo_root / "docs"

    errors = []

    new_pages = [
        docs_dir / "sucustu" / "index.html",
        docs_dir / "sucustu" / "privacy" / "index.html",
        docs_dir / "sucustu" / "support" / "index.html",
        docs_dir / "sucustu" / "terms" / "index.html",
    ]

    print(f"Checking {len(new_pages)} SUÇÜSTÜ! pages...")

    # Cache parsed files for link target verification
    parsed_cache = {}

    for page_path in new_pages:
        rel_path = page_path.relative_to(repo_root)
        print(f"\n--- Checking {rel_path} ---")

        # 1. Page exists
        if not page_path.is_file():
            errors.append(f"Missing file: {rel_path}")
            continue

        parser, content = parse_html_file(page_path)
        parsed_cache[str(page_path.resolve())] = parser

        # 2. Doctype check
        if not re.search(r'^\s*<!doctype\s+html', content, re.IGNORECASE):
            errors.append(f"{rel_path}: Missing <!doctype html> declaration at start")

        # 3. Lang attribute check
        html_elems = parser.root.find_all('html')
        if not html_elems or not html_elems[0].attrs.get('lang'):
            errors.append(f"{rel_path}: <html> tag missing 'lang' attribute")

        # 4. Viewport check
        meta_elems = parser.root.find_all('meta')
        has_viewport = any(m.attrs.get('name', '').lower() == 'viewport' and m.attrs.get('content') for m in meta_elems)
        if not has_viewport:
            errors.append(f"{rel_path}: Missing <meta name='viewport' content='...'>")

        # 5. Title check
        title_elems = parser.root.find_all('title')
        if not title_elems or not title_elems[0].text.strip():
            errors.append(f"{rel_path}: Missing or empty <title>")

        # 6. Both #tr and #en sections exist
        tr_elem = parser.root.find_by_id('tr')
        en_elem = parser.root.find_by_id('en')

        if not tr_elem:
            errors.append(f"{rel_path}: Missing section with id='tr'")
        if not en_elem:
            errors.append(f"{rel_path}: Missing section with id='en'")

        # 7. Exactly one <h1> per language section
        if tr_elem:
            tr_h1s = tr_elem.find_all('h1')
            if len(tr_h1s) != 1:
                errors.append(f"{rel_path}: Section #tr must have exactly 1 <h1>, found {len(tr_h1s)}")
        if en_elem:
            en_h1s = en_elem.find_all('h1')
            if len(en_h1s) != 1:
                errors.append(f"{rel_path}: Section #en must have exactly 1 <h1>, found {len(en_h1s)}")

        # 8. All relative links/anchors resolve to files or ids
        page_ids = parser.root.get_all_ids()
        link_elems = parser.root.find_all('a')
        for a in link_elems:
            href = a.attrs.get('href', '').strip()
            if not href:
                continue

            # Skip mailto, tel, javascript
            if href.startswith(('mailto:', 'tel:', 'javascript:')):
                continue

            parsed_url = urllib.parse.urlparse(href)

            # Check if it's an external url
            if parsed_url.scheme in ('http', 'https'):
                if parsed_url.netloc == 'buyukkol.com':
                    # Local absolute URL
                    target_rel = parsed_url.path.lstrip('/')
                    if not target_rel or target_rel.endswith('/'):
                        target_file = docs_dir / target_rel / "index.html"
                    else:
                        target_file = docs_dir / target_rel
                        if not target_file.exists() and (docs_dir / target_rel / "index.html").exists():
                            target_file = docs_dir / target_rel / "index.html"
                    if not target_file.exists():
                        errors.append(f"{rel_path}: Link '{href}' resolves to non-existent file {target_file}")
                    elif parsed_url.fragment:
                        # Check fragment in target file
                        tf_str = str(target_file.resolve())
                        if tf_str not in parsed_cache:
                            p, _ = parse_html_file(target_file)
                            parsed_cache[tf_str] = p
                        if parsed_url.fragment not in parsed_cache[tf_str].root.get_all_ids():
                            errors.append(f"{rel_path}: Link '{href}' fragment #{parsed_url.fragment} not found in {target_file}")
                continue

            # Same-page anchor
            if href.startswith('#'):
                frag = href[1:]
                if frag not in page_ids:
                    errors.append(f"{rel_path}: Anchor '{href}' target id '{frag}' not found on page")
                continue

            # Relative / root-relative URL
            path_part = parsed_url.path
            frag_part = parsed_url.fragment

            if path_part.startswith('/'):
                # Root-relative: relative to docs_dir
                target = docs_dir / path_part.lstrip('/')
            else:
                # Relative to current page's parent directory
                target = page_path.parent / path_part

            # If path ends with / or is directory, look for index.html
            if path_part.endswith('/') or target.is_dir():
                target_file = target / "index.html" if target.is_dir() else (target / "index.html" if not target.name.endswith('.html') else target)
            else:
                target_file = target

            # In case target is directory without trailing slash
            if target_file.is_dir():
                target_file = target_file / "index.html"

            if not target_file.exists():
                errors.append(f"{rel_path}: Link '{href}' points to non-existent file: {target_file.relative_to(repo_root) if target_file.is_relative_to(repo_root) else target_file}")
            elif frag_part:
                # Check fragment in target
                tf_str = str(target_file.resolve())
                if tf_str not in parsed_cache:
                    p, _ = parse_html_file(target_file)
                    parsed_cache[tf_str] = p
                if frag_part not in parsed_cache[tf_str].root.get_all_ids():
                    errors.append(f"{rel_path}: Link '{href}' fragment #{frag_part} not found in {target_file}")

        # 9. No <script src= pointing off-site
        script_elems = parser.root.find_all('script')
        for s in script_elems:
            src = s.attrs.get('src', '').strip()
            if not src:
                continue
            if src.startswith(('http://', 'https://', '//')):
                errors.append(f"{rel_path}: Off-site <script src='{src}'> is not allowed")
            else:
                # Verify local script exists
                if src.startswith('/'):
                    script_file = docs_dir / src.lstrip('/')
                else:
                    script_file = page_path.parent / src
                if not script_file.exists():
                    errors.append(f"{rel_path}: Local <script src='{src}'> not found on disk: {script_file}")

    # 10. Check no 'nazartesi.com' anywhere in docs/sucustu.html or docs/sucustu/
    print("\n--- Checking for forbidden 'nazartesi.com' ---")
    files_to_scan = [docs_dir / "sucustu.html"]
    sucustu_dir = docs_dir / "sucustu"
    if sucustu_dir.exists():
        files_to_scan.extend(sucustu_dir.rglob("*"))

    for f in files_to_scan:
        if f.is_file():
            try:
                text = f.read_text(encoding='utf-8')
                if "nazartesi.com" in text:
                    errors.append(f"Found 'nazartesi.com' in {f.relative_to(repo_root)}")
            except Exception as e:
                errors.append(f"Could not read {f.relative_to(repo_root)}: {e}")

    # 11. Check sitemap contains the 4 URLs
    print("\n--- Checking docs/sitemap.xml ---")
    sitemap_file = docs_dir / "sitemap.xml"
    if not sitemap_file.exists():
        errors.append("docs/sitemap.xml is missing")
    else:
        sitemap_content = sitemap_file.read_text(encoding='utf-8')
        expected_urls = [
            "https://buyukkol.com/sucustu/",
            "https://buyukkol.com/sucustu/privacy/",
            "https://buyukkol.com/sucustu/support/",
            "https://buyukkol.com/sucustu/terms/",
        ]
        for expected in expected_urls:
            loc_tag = f"<loc>{expected}</loc>"
            if loc_tag not in sitemap_content:
                errors.append(f"sitemap.xml missing required URL: {expected}")
            else:
                print(f"  ✓ Found {expected}")

    # Final result
    print("\n" + "=" * 50)
    if errors:
        print(f"FAILED: {len(errors)} error(s) detected:")
        for err in errors:
            print(f"  ✗ {err}")
        sys.exit(1)
    else:
        print("SUCCESS: All SUÇÜSTÜ! page checks passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()
