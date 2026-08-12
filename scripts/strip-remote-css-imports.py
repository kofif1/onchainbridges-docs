#!/usr/bin/env python3
"""
Remove off-origin @import rules from the BUILT stylesheets.

Why this is a build step and not an edit.

The Google Fonts request on this site does not come from anything in this
repository. It is emitted by the jekyll-theme-cayman gem, at the top of its
compiled stylesheet:

    @import url("https://fonts.googleapis.com/css?family=Open+Sans:400,700&display=swap");

We do not own that file. Overriding it would mean reproducing the whole theme
stylesheet in this repo, which is both a copying problem and a maintenance one.
Removing the rule from the build output is the honest minimum: the theme stays
the theme, and the visitor's browser is not sent to a third party.

A CSS @import fetches when the stylesheet is parsed, with no action from the
visitor. That is why the two <link> tags removed earlier were not the whole
story: they were the visible half, and this is the half that was doing the work.

Effect on appearance, stated rather than hidden: Open Sans stops loading and the
theme's own fallback applies, which is "Helvetica Neue", Helvetica, Arial.
Visitors who have Open Sans installed locally still see it, with no request. If
the exact webfont is wanted back, self-host it; do not restore the import.

    python3 scripts/strip-remote-css-imports.py _site
"""

import os
import re
import sys

# Matches: @import url("https://x");  @import url(//x);  @import "https://x";
REMOTE_IMPORT = re.compile(
    r'''@import\s+(?:url\(\s*)?['"]?\s*(?:https?:)?//[^)'";]+['"]?\s*\)?\s*[^;]*;''',
    re.I,
)


def main(argv):
    root = argv[1] if len(argv) > 1 else '_site'
    if not os.path.isdir(root):
        print('no such directory: %s' % root)
        return 1

    removed_total = 0
    touched = []
    for dirpath, _dirs, files in os.walk(root):
        for name in files:
            if not name.lower().endswith(('.css', '.html', '.htm')):
                continue
            path = os.path.join(dirpath, name)
            try:
                text = open(path, encoding='utf-8', errors='replace').read()
            except OSError:
                continue
            hits = REMOTE_IMPORT.findall(text)
            if not hits:
                continue
            new = REMOTE_IMPORT.sub('', text)
            open(path, 'w', encoding='utf-8').write(new)
            rel = os.path.relpath(path, root)
            touched.append(rel)
            removed_total += len(hits)
            for h in hits:
                print('   removed from %-40s %s' % (rel, ' '.join(h.split())[:90]))

    if removed_total:
        print('removed %d remote @import rule(s) from %d file(s)'
              % (removed_total, len(touched)))
    else:
        print('no remote @import rules in the build output')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
