#!/usr/bin/env bash
# Runner for pmd on the MVN build. Exit contract: 0 ran / 1 failed / 3 skipped-cannot-run / 4 not-installed.
#
# Identical on the monolith and multi-module branches: "compile" runs in the same Maven build so sibling
# modules resolve, and the tools/ folder is passed explicitly (-Dtools.dir).
set -u
cd "$(dirname "$0")/../.." || exit 1
ROOT="$PWD"
command -v mvn >/dev/null 2>&1 || exit 4
mvn -q -o -Dtools.dir="$ROOT/tools" compile pmd:pmd
rc=$?
[ $rc -eq 0 ] && exit 0
exit 1
