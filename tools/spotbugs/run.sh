#!/usr/bin/env bash
# Runner for spotbugs on the MVN build. Exit contract: 0 ran / 1 failed / 3 skipped-cannot-run / 4 not-installed.
#
# Identical on the monolith and multi-module branches:
#  - "compile" runs in the same Maven build, so SpotBugs always has classes to analyse and sibling modules resolve;
#  - the tools/ folder is passed explicitly (-Dtools.dir);
#  - a multi-module build writes one target/spotbugsXml.xml per module, so the module reports are merged into the
#    repo-level target/spotbugsXml.xml (the same file the monolith writes).
set -u
cd "$(dirname "$0")/../.." || exit 1
ROOT="$PWD"
command -v mvn >/dev/null 2>&1 || exit 4

mvn -q -o -Dtools.dir="$ROOT/tools" compile spotbugs:spotbugs
rc=$?
[ $rc -eq 0 ] || exit 1

# merge module reports (nothing to do on a single-module build)
reports=$(find . -mindepth 3 -maxdepth 3 -path '*/target/spotbugsXml.xml' | sort)
if [ -n "$reports" ]; then
  PY=""
  for c in python3 python "py -3"; do $c -c 'import sys' >/dev/null 2>&1 && PY=$c && break; done
  if [ -n "$PY" ]; then
    mkdir -p target
    $PY tools/_merge_reports.py spotbugs target/spotbugsXml.xml $reports || echo "spotbugs: report merge failed" >&2
  else
    echo "spotbugs: python not found, module reports left unmerged" >&2
  fi
fi
exit 0
