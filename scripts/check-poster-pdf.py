#!/usr/bin/env python3
"""Fail the build when the rendered PDF does not actually cover its page.

Checking the page count and the page size is not enough: a poster that is
shifted off the paper still reports one correctly sized A1 page, while a third
of it hangs past the edge and is dropped. That is exactly how the first
generated PDF looked, and nothing in the pipeline noticed.

So this measures the ink. `pdftotext -bbox` reports every word's box in page
coordinates; if the text stops well short of an edge, or starts well past one,
the layout is not sitting on the page as intended.

Usage: check-poster-pdf.py <pdf>
"""

import re
import subprocess
import sys

# A1 is 1683.8 x 2383.9 pt. The poster's own margin is 70px top / 82px sides /
# 48px bottom, i.e. roughly 53/62/36 pt, and the outermost ink sits just inside
# that. These bounds allow generous slack while still catching a sheet that is
# cropped or pushed off the page.
PAGE_WIDTH = 1683.8
PAGE_HEIGHT = 2383.9
MAX_START = 120.0   # ink must begin within this distance of the left/top edge
MIN_REACH = 150.0   # and must reach within this distance of the right/bottom


def main(argv):
    if len(argv) != 2:
        sys.stderr.write(__doc__)
        return 2

    pdf = argv[1]
    xml = subprocess.run(["pdftotext", "-bbox", pdf, "-"],
                         capture_output=True, text=True, check=True).stdout

    boxes = re.findall(
        r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)"',
        xml)
    if not boxes:
        print("check-poster-pdf: the PDF contains no text at all")
        return 1

    x_min = min(float(b[0]) for b in boxes)
    y_min = min(float(b[1]) for b in boxes)
    x_max = max(float(b[2]) for b in boxes)
    y_max = max(float(b[3]) for b in boxes)
    print("check-poster-pdf: ink spans x %.0f..%.0f, y %.0f..%.0f "
          "on a %.0f x %.0f pt page" %
          (x_min, x_max, y_min, y_max, PAGE_WIDTH, PAGE_HEIGHT))

    problems = []
    if x_min > MAX_START:
        problems.append("starts %.0f pt from the left edge - the sheet is "
                        "shifted right" % x_min)
    if y_min > MAX_START:
        problems.append("starts %.0f pt from the top edge" % y_min)
    if PAGE_WIDTH - x_max > MIN_REACH:
        problems.append("stops %.0f pt short of the right edge - the sheet is "
                        "cropped or too narrow" % (PAGE_WIDTH - x_max))
    if PAGE_HEIGHT - y_max > MIN_REACH:
        problems.append("stops %.0f pt short of the bottom edge" %
                        (PAGE_HEIGHT - y_max))

    if problems:
        print("check-poster-pdf: the poster does not cover its page")
        for problem in problems:
            print("  - " + problem)
        return 1

    print("check-poster-pdf: the poster covers its page")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
