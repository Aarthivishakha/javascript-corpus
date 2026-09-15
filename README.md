# Testable Java corpus — JV_V17_MAVEN_WAR_MICRO

Grid cell `MVN-WAR-S` of the 24-cell Java grid.

## Project type

Order pricing and risk domain. The domain layer is byte-identical across all 24 branches
in this family, so any difference in tool output is attributable to the branch variables
below and not to the code the tool was pointed at.

## Branches

This repository holds 432 orphan branches, one per grid cell across every Java version, build system and packaging combination in this corpus. `main` carries the title
only. See `dataset.json` for the machine-readable description of this branch.

## Branch variables

| Variable | Value |
|---|---|
| Java version | 17 |
| Host JDK | 17 |
| Build system | Maven |
| Packaging | WAR |
| Architecture | Microservices |

## Supported tools

| Tool | Pinned version | Metric block |
|---|---|---|
| Checkstyle | 12.3.1 | Lint / Rule Violations |
| PMD | 7.26.0 | Cognitive Complexity |
| CPD (PMD) | 7.26.0 | Code Duplication |
| SpotBugs + FindSecBugs | 4.10.3 / 1.14.0 | Static Vulnerabilities (SAST) |
| JaCoCo | 0.8.14 | Statement / Branch / Path Coverage |
| PIT | 1.30.0 | Mutation Score |
| OWASP Dependency-Check | 13.0.0 | Dependency Risk (SCA) |
| git | — | Code Churn |

Every pin is the newest release that runs on JDK 17, the host chosen for this
family so the toolchain rolls back with it. Checkstyle is held at 12.3.1
because 13.x requires JDK 21+. Gradle rolls to 9.x here (it requires JDK 17 to run) and
the shadow plugin to its 9.x line with it.

**Two tools change state in this family.** CK goes dark: CK 0.7.0 bundles Eclipse JDT
3.26.0, which parses only up to Java 16, so it cannot read this branch's records or sealed
types — its runner exits 3. Spoon becomes available for the first time: it requires JDK
17+, which this family satisfies. That swap is the "which tools go dark" measurement
producing an actual result.

## Build

```
mvn -B clean package
```

Main and test sources both compile at Java 17 (bytecode major version 61). The code
uses records, a sealed interface, pattern matching for `instanceof`, text blocks, switch
expressions and `Stream.toList`, so it fails to compile under `--release 11` in eleven
places — the version differentiation is real, not
declared.

Produces: `jv-054.war`

## Run

```
java -jar <artifact> O-1234
```

## Test

```
mvn -B test
```

## Workspace projects

- `jv-054-domain/`
- `jv-054-pricing/`
- `jv-054-risk/`
- `jv-054-catalog/`

## Tool entry points

Each tool has `tools/<tool>/trigger.yaml` and `tools/<tool>/run.sh`. Runners follow the
exit-code contract: 0 ran, 1 failed, 3 skipped-cannot-run, 4 not-installed.

## Planted CVE pins

| Dependency | Version |
|---|---|
| `commons-collections:commons-collections` | 3.2.1 |
| `org.apache.commons:commons-text` | 1.9 |
| `com.fasterxml.jackson.core:jackson-databind` | 2.9.10.1 |
| `log4j:log4j` | 1.2.17 |
| `org.yaml:snakeyaml` | 1.30 |

Deliberately vulnerable versions, so the SCA metrics have known true positives. Do not
upgrade them.
