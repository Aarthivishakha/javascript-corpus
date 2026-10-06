#!/usr/bin/env bash
# Runner for checkstyle on the MVN build. Exit contract: 0 ran / 1 failed / 3 skipped-cannot-run / 4 not-installed.
#
# Identical on the monolith and multi-module branches:
#  - the tools/ folder is passed explicitly (-Dtools.dir) so the config file resolves from the repo root,
#    whatever directory Maven thinks the project root is;
#  - a multi-module build writes one target/checkstyle-result.xml per module, so the module reports are merged
#    into the repo-level target/checkstyle-result.xml (the same file the monolith writes).
set -u
cd "$(dirname "$0")/../.." || exit 1
ROOT="$PWD"
command -v mvn >/dev/null 2>&1 || exit 4

mvn -q -o -Dtools.dir="$ROOT/tools" checkstyle:check
rc=$?
[ $rc -eq 0 ] || exit 1

# merge module reports (nothing to do on a single-module build)
reports=$(find . -mindepth 3 -maxdepth 3 -path '*/target/checkstyle-result.xml' | sort)
if [ -n "$reports" ]; then
  PY=""
  for c in python3 python "py -3"; do $c -c 'import sys' >/dev/null 2>&1 && PY=$c && break; done
  if [ -n "$PY" ]; then
    mkdir -p target
    $PY tools/_merge_reports.py checkstyle target/checkstyle-result.xml $reports || echo "checkstyle: report merge failed" >&2
  else
    echo "checkstyle: python not found, module reports left unmerged" >&2
  fi
fi
exit 0
