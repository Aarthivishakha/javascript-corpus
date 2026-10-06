#!/usr/bin/env python3
"""Merge per-module report files into one repo-level report.

A multi-module Maven build writes one report per module (<module>/target/...), while a monolith writes a
single target/... report. The runners call this helper so both layouts end up with the same repo-level file.

usage: _merge_reports.py <checkstyle|spotbugs> <out-file> <module-report> [<module-report> ...]
"""
import sys
import xml.etree.ElementTree as ET


def merge_checkstyle(out, paths):
    root = ET.Element("checkstyle")
    root.set("version", ET.parse(paths[0]).getroot().get("version", ""))
    for p in paths:
        for f in ET.parse(p).getroot().findall("file"):
            root.append(f)
    ET.ElementTree(root).write(out, encoding="utf-8", xml_declaration=True)


def merge_spotbugs(out, paths):
    trees = [ET.parse(p) for p in paths]
    base = trees[0]
    root = base.getroot()
    idx = len(list(root))
    for i, child in enumerate(list(root)):
        if child.tag in ("Errors", "FindBugsSummary"):
            idx = i
            break
    for t in trees[1:]:
        for bug in t.getroot().findall("BugInstance"):
            root.insert(idx, bug)
            idx += 1
    summary = root.find("FindBugsSummary")
    if summary is not None:
        summary.set("total_bugs", str(len(root.findall("BugInstance"))))
    base.write(out, encoding="utf-8", xml_declaration=True)


def main(argv):
    if len(argv) < 4:
        print(__doc__)
        return 2
    kind, out, paths = argv[1], argv[2], argv[3:]
    {"checkstyle": merge_checkstyle, "spotbugs": merge_spotbugs}[kind](out, paths)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
