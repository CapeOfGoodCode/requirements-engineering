#!/usr/bin/env python3
"""Fail the build when the poster no longer fits on its single A1 page.

The poster is a fixed 2245x3179 px canvas with `overflow: hidden`, so anything
that outgrows a column is silently cut off rather than pushed into view. A font
substitution or an added paragraph therefore breaks the print deliverable
without producing any error. This script renders the built page in the same
headless Chrome that generates the PDF, measures it from inside the document,
and exits non-zero on the first sign of a clipped layout.

Usage: check-poster-layout.py <chrome-binary> <built-html>
"""

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

# Measured inside the page: column capacity versus what each column needs, plus
# every SVG label's box against its own viewBox. Both are checked in poster
# coordinates, so the browser window size does not matter.
PROBE = """
<div id="probe" style="display:none"></div>
<script>
window.addEventListener('load', function () {
  var stage = document.querySelector('.stage');
  var k = new DOMMatrix(getComputedStyle(stage).transform).a || 1;
  var problems = [];

  var cap = document.querySelector('.cols').getBoundingClientRect().height / k;
  [].forEach.call(document.querySelectorAll('.col'), function (col, i) {
    var need = 24 * (col.children.length - 1);
    [].forEach.call(col.children, function (block) {
      need += block.querySelector('.bh').getBoundingClientRect().height / k;
      [].forEach.call(block.querySelectorAll('.panel'), function (p) {
        need += p.getBoundingClientRect().height / k;
      });
    });
    if (need > cap) {
      problems.push('column ' + (i + 1) + ' needs ' + Math.round(need) +
                    'px but has ' + Math.round(cap) + 'px');
    }
  });

  [].forEach.call(document.querySelectorAll('svg.dia'), function (svg, i) {
    var vb = svg.viewBox.baseVal;
    var sr = svg.getBoundingClientRect();
    var scale = sr.width / vb.width;
    [].forEach.call(svg.querySelectorAll('text'), function (t) {
      var r = t.getBoundingClientRect();
      var x0 = (r.left - sr.left) / scale, x1 = (r.right - sr.left) / scale;
      var y0 = (r.top - sr.top) / scale,  y1 = (r.bottom - sr.top) / scale;
      if (x0 < -0.5 || y0 < -0.5 || x1 > vb.width + 0.5 || y1 > vb.height + 0.5) {
        problems.push('diagram ' + (i + 1) + ' label out of bounds: "' +
                      t.textContent.trim().slice(0, 40) + '"');
      }
    });
  });

  var poster = document.querySelector('.poster');
  if (poster.scrollHeight - poster.clientHeight > 1) {
    problems.push('poster content is ' + (poster.scrollHeight - poster.clientHeight) +
                  'px taller than the page');
  }

  document.getElementById('probe').textContent =
    'PROBE' + JSON.stringify({problems: problems}) + 'ENDPROBE';
});
</script>
"""


def main(argv):
    if len(argv) != 3:
        sys.stderr.write(__doc__)
        return 2

    chrome, built = argv[1], Path(argv[2])
    html = built.read_text(encoding="utf-8")

    # The probe has to run inside the real built page, so append it to a copy
    # rather than to the deployed file.
    with tempfile.TemporaryDirectory() as tmp:
        probe_file = Path(tmp) / "probe.html"
        probe_file.write_text(html.replace("</body>", PROBE + "\n</body>"),
                              encoding="utf-8")
        dom = subprocess.run(
            [chrome, "--headless=new", "--disable-gpu", "--no-sandbox",
             "--window-size=1600,1000", "--virtual-time-budget=6000",
             "--dump-dom", probe_file.as_uri()],
            capture_output=True, text=True, timeout=180).stdout

    match = re.search(r"PROBE(\{.*?\})ENDPROBE", dom, re.S)
    if not match:
        print("check-poster-layout: the probe never ran - the page failed to load")
        return 1

    problems = json.loads(match.group(1))["problems"]
    if problems:
        print("check-poster-layout: the poster no longer fits on one A1 page")
        for problem in problems:
            print("  - " + problem)
        return 1

    print("check-poster-layout: layout fits, no clipped labels")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
