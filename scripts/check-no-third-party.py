#!/usr/bin/env python3
"""
Assert that the built site fetches nothing from a third party on page load.

This exists because onchainbridges.com/privacy.html clause 1.2 (d) and this
site's own footer both make that claim in published legal text. A claim like
that needs an instrument that keeps it true, not a person remembering to
re-check it after a theme bump.

WHAT COUNTS, AND WHY THE DISTINCTION MATTERS

A *resource* reference is fetched by the browser with no action from the
visitor: a stylesheet, script, image, font, iframe, preconnect, preload. That
fetch discloses the visitor's IP address and user agent to whoever is on the
other end. That is the thing being asserted about.

A *navigation* href is fetched only if the visitor clicks it. Clicking is the
visitor's own decision to go somewhere else. This site links out to GitHub and
to several block explorers, and those links are fine; the published wording is
"request no resources from any third party when loaded" precisely so it stays
true in their presence.

So this checker classifies by parsed tag and attribute, not by matching strings
anywhere in the file. It is the same classification used for the host
enumeration that was accepted as the evidence of record for the clause.

WHY NOT A DENYLIST

The first version of this check grepped for nine known hosts (Google Fonts and
some CDNs). That is narrower than the claim it guards: a resource loaded from
any host outside those nine would have kept the build green while making a
published legal statement false. This asserts the general property instead:
no absolute http(s) URL in a resource context, from any host at all.

    python3 scripts/check-no-third-party.py _site
    python3 scripts/check-no-third-party.py --self-test

--self-test runs the checker against fixtures that are supposed to fail. CI
runs it before the real check, so a checker that has been accidentally reduced
to a no-op fails the build instead of silently passing everything.
"""

import os
import re
import sys
from html.parser import HTMLParser

# Attributes the browser fetches without the visitor doing anything.
RESOURCE_ATTRS = {
    'script':  ['src'],
    'img':     ['src', 'srcset'],
    'iframe':  ['src'],
    'source':  ['src', 'srcset'],
    'embed':   ['src'],
    'object':  ['data'],
    'video':   ['src', 'poster'],
    'audio':   ['src'],
    'track':   ['src'],
    'input':   ['src'],
    'body':    ['background'],
    'table':   ['background'],
}

# <link rel=...> values that cause a fetch or a connection on load.
# Anything else (canonical, alternate, author, license) is metadata.
FETCHING_REL = {
    'stylesheet', 'preload', 'preconnect', 'dns-prefetch', 'prefetch',
    'prerender', 'icon', 'shortcut icon', 'apple-touch-icon', 'mask-icon',
    'manifest', 'modulepreload', 'preload stylesheet',
}

ABSOLUTE = re.compile(r'^\s*(https?:)?//', re.I)
CSS_URL = re.compile(r'''url\(\s*['"]?\s*((?:https?:)?//[^)'"\s]+)''', re.I)
CSS_IMPORT = re.compile(r'''@import\s+(?:url\()?\s*['"]?\s*((?:https?:)?//[^)'";\s]+)''', re.I)


def host_of(url):
    u = url.strip()
    if u.startswith('//'):
        u = 'https:' + u
    m = re.match(r'^https?://([^/?#]+)', u, re.I)
    return m.group(1).lower() if m else None


def srcset_urls(value):
    # "a.png 1x, b.png 2x" -> the URL is the first token of each entry
    for part in value.split(','):
        part = part.strip()
        if part:
            yield part.split()[0]


class ResourceFinder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.hits = []   # (tag, attr, url)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'link':
            rel = (a.get('rel') or '').lower().strip()
            href = a.get('href')
            if href and rel in FETCHING_REL:
                self._maybe(tag, 'rel=' + rel, href)
            return
        for attr in RESOURCE_ATTRS.get(tag, []):
            val = a.get(attr)
            if not val:
                continue
            if attr == 'srcset':
                for u in srcset_urls(val):
                    self._maybe(tag, attr, u)
            else:
                self._maybe(tag, attr, val)

    def _maybe(self, tag, attr, url):
        if ABSOLUTE.match(url or ''):
            self.hits.append((tag, attr, url.strip()))


def scan(root, allow_hosts):
    findings = []
    for dirpath, _dirs, files in os.walk(root):
        for name in files:
            ext = os.path.splitext(name)[1].lower()
            if ext not in ('.html', '.htm', '.css', '.xml'):
                continue
            path = os.path.join(dirpath, name)
            rel = os.path.relpath(path, root)
            try:
                text = open(path, encoding='utf-8', errors='replace').read()
            except OSError as e:
                findings.append((rel, 'file', 'unreadable', str(e)))
                continue
            if ext in ('.html', '.htm', '.xml'):
                p = ResourceFinder()
                try:
                    p.feed(text)
                except Exception as e:                      # malformed markup
                    findings.append((rel, 'parse', 'failed', str(e)))
                    continue
                for tag, attr, url in p.hits:
                    h = host_of(url)
                    if h and h not in allow_hosts:
                        findings.append((rel, '<%s %s>' % (tag, attr), h, url))
            # inline <style> blocks are inside the HTML text, so scanning the
            # raw text catches them as well as .css files
            for rx in (CSS_URL, CSS_IMPORT):
                for m in rx.finditer(text):
                    h = host_of(m.group(1))
                    if h and h not in allow_hosts:
                        findings.append((rel, 'css url()', h, m.group(1)))
    return findings


def self_test():
    """The gate must be able to fail. Prove it, every run."""
    import tempfile
    cases = {
        'google-font.html':
            '<html><head><link rel="preload" as="style" '
            'href="https://fonts.googleapis.com/css?family=Open+Sans"></head></html>',
        'unlisted-host.html':          # the case the old denylist missed
            '<html><head><script src="https://tracker.example.net/t.js"></script></head></html>',
        'protocol-relative.html':
            '<html><body><img src="//cdn.example.org/pixel.gif"></body></html>',
        'inline-css-font.html':
            '<html><head><style>@import url(https://fonts.example.com/x.css);</style></head></html>',
        'srcset.html':
            '<html><body><img srcset="https://img.example.com/a.png 2x"></body></html>',
        'stylesheet.css':
            'body{background:url("https://bg.example.com/x.png")}',
    }
    clean = {
        'ok-relative.html':
            '<html><head><link rel="stylesheet" href="/assets/css/style.css">'
            '<link rel="canonical" href="https://kofif1.github.io/onchainbridges-docs/">'
            '</head><body><a href="https://github.com/kofif1">GitHub</a>'
            '<a href="https://sepolia.etherscan.io/address/0x0">explorer</a>'
            '<script type="application/ld+json">{"@id":"https://schema.org/x"}</script>'
            '</body></html>',
    }
    ok = True
    with tempfile.TemporaryDirectory() as d:
        # every bad fixture must be caught, individually
        for name, body in cases.items():
            sub = os.path.join(d, 'bad', name.replace('.', '_'))
            os.makedirs(sub, exist_ok=True)
            open(os.path.join(sub, name), 'w').write(body)
            found = scan(sub, set())
            if found:
                print('   catches %-24s -> %s' % (name, found[0][2]))
            else:
                print('   MISSED  %-24s  <-- the gate cannot see this' % name)
                ok = False
        # and the clean fixture must NOT be caught, or the gate is useless noise
        sub = os.path.join(d, 'good')
        os.makedirs(sub, exist_ok=True)
        for name, body in clean.items():
            open(os.path.join(sub, name), 'w').write(body)
        found = scan(sub, set())
        if found:
            print('   FALSE POSITIVE on clean fixture: %r' % (found,))
            ok = False
        else:
            print('   clean fixture passes (canonical, nav links and JSON-LD ignored)')
    return ok


def main(argv):
    if '--self-test' in argv:
        print('SELF-TEST: the check must fail on these, and pass on the clean one')
        good = self_test()
        print('\nself-test', 'PASSED' if good else 'FAILED')
        return 0 if good else 1

    args = [a for a in argv[1:] if not a.startswith('--')]
    allow = set()
    for a in argv[1:]:
        if a.startswith('--allow-host='):
            allow.add(a.split('=', 1)[1].lower())
    root = args[0] if args else '_site'

    if not os.path.isdir(root):
        print('no such directory: %s' % root)
        return 1

    pages = sum(len([f for f in fs if f.lower().endswith(('.html', '.htm'))])
                for _, _, fs in os.walk(root))
    findings = scan(root, allow)

    if not findings:
        print('checked %d built pages: no third-party resource is requested on page load' % pages)
        if allow:
            print('(allowed hosts: %s)' % ', '.join(sorted(allow)))
        return 0

    print('Third-party resources are requested on page load:\n')
    for f in sorted(set(findings)):
        print('   %-46s %-22s %s' % (f[0], f[1], f[3] if len(f) > 3 else f[2]))
    print('')
    print('These fetch on load, with no action from the visitor, and disclose the')
    print("visitor's IP address and user agent to the host shown.")
    print('')
    print('onchainbridges.com/privacy.html clause 1.2 (d) and this site\'s footer')
    print('both state that this does not happen. Either remove the reference, or')
    print('tell the legal review channel that the published wording has to change.')
    print('Do not do neither.')
    return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
