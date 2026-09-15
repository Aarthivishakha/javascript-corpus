# TypeScript Order Platform -- Microservices (TS_V20_VITE_BUN_MICRO)

Tool-evaluation repository for **Node 20**, bundled with **vite**,
managed with **bun**, in a **Microservices** layout.

This is branch **TS_V20_VITE_BUN_MICRO** of the consolidated `typescript-corpus` repository, which holds all 216 TypeScript branches across every Node version, bundler, package manager and architecture combination in this corpus.

## Project type

- **Language:** TypeScript 5.9.3
- **Runtime:** Node 20 (verified against 20.20.2)
- **Scenario:** 2 - Microservices
- **Architecture:** Microservices
- **Module layout:** workspace
- **Bundler:** Vite 2.9.18 (Rollup linker + its own esbuild 0.14.54 transform)
- **Package manager:** bun 1.3.13
- **Source root:** `packages/domain/src`

Node 12 is end-of-life, and that is deliberate: it pins the entire toolchain to
the last release of each tool that still supports it. Every version in this
repository was resolved against the live npm registry and then executed on a
real Node 20.20.2 interpreter. None was written from memory.

## Supported tools

26 tool families are wired. Each has a folder under `tools/` containing a
`trigger.yaml` manifest, a runner, and its configuration.

| Family | Pinned | Family | Pinned |
|---|---|---|---|
| TypeScript (tsc) | 5.0.4 | ts-morph | 18.0.0 |
| vite | 8.2.2 | ts-prune | 0.10.3 |
| mocha | 9.2.2 | madge | 5.0.2 |
| c8 (coverage, primary) | 8.0.1 | dependency-cruiser | 11.18.0 |
| nyc + ts-node (cross-check) | 15.1.0 | Stryker | 5.6.1 |
| eslint | 8.57.1 | fast-check | 4.9.0 |
| @typescript-eslint | 5.62.0 | cdxgen | 8.6.3 |
| eslint-plugin-sonarjs | 0.15.0 | ORT (cdxgen licence proxy) | n/a |
| eslint-plugin-security | 2.1.1 | npm-check-updates | 12.5.12 |
| eslint-scope | 7.2.2 | bun audit / ls | 1.3.13 |
| jscpd | 3.2.1 | OpenTelemetry sdk-node | 0.29.2 |
| Grype | v0.110.0 (binary) | Lizard | pip |
| pydriller | pip | GitHub Advisories + API | REST |

### Tools deliberately NOT wired

Skipping these is a finding, not an omission. See [`dataset.json`](dataset.json).

| Tool | Reason |
|---|---|
| knip | no published version supports Node 12 |
| vitest + @vitest/coverage-v8 | no published version supports Node 12 |
| @biomejs/biome | oldest published version already requires Node >=14.21.3 |
| OSV-Scanner | `api.osv.dev` unreachable -- 403 at the egress proxy |
| npm downloads API | `api.npmjs.org` unreachable -- 403 at the egress proxy |
| npm-check-updates 19.6.6 | requires Node >=18; 12.5.12 is pinned instead |

Declaring any of these would have produced a metric that cannot be computed.

## Build

```bash
# bun is a standalone binary, not an npm package -- see tools/npm-audit/run_npm_audit.sh
bun install --frozen-lockfile
make build
```

`make build` type-checks with `tsc --noEmit`, emits CommonJS + declarations to
`dist/`, then bundles with **Vite 2.9.18 (Rollup linker + its own esbuild 0.14.54 transform)** and **executes the bundle**.
Emitting is not proof; running it is.

## Run

```bash
node dist/packages/domain/src/index.js
```

Each service is independently runnable:

```bash
node dist/services/gateway-service/src/index.js
node dist/services/pricing-service/src/index.js
```

## Test

```bash
make test        # mocha over tests/
make coverage    # c8 (primary) AND nyc + ts-node (cross-check)
```

Both coverage tools must report non-zero. They deliberately disagree: c8 reads
V8 coverage of the emitted output and remaps it, while nyc instruments the
TypeScript AST directly through `ts-node/register`. Identical numbers would mean
one of them is not an independent second opinion.

`nyc` here never reports through a source-map remap. Doing so silently yields
0% -- the file is remapped to `.ts`, an `--include` written against `dist/**`
stops matching, and the report empties while the process still exits 0.

## Architecture

**Microservices.** Three independently deployable services over a shared domain
package, wired through a workspace root.

```
packages/
  domain/         @orderkit/domain     -- models, services, analysis fixtures
  contracts/      @orderkit/contracts  -- inter-service message types
services/
  gateway-service/    accepts payloads, emits order.submitted
  order-service/      validates and prices, emits order.priced / order.rejected
  pricing-service/    owns tier and volume rates (leaf -- calls no one)
```

Each service has its own `package.json`, its own `src/index.ts` entry point and
its own start script. The workspace root lists them under `workspaces`.

**Documented inter-service call path:**

```
http.request -> gateway-service -> order.submitted
                order-service   -> pricing.quote -> pricing-service
                pricing-service -> pricing.rate  -> order-service
                order-service   -> order.priced | order.rejected
```

This matters because of what the JavaScript corpus got wrong: FlintAtlas's sheet
said `Microservices` while the repository was a flat monolith with no
workspaces, and its own README and `dataset.json` both said "monolith". Nothing
in that repo compared the two. Here `tools/full_check.ts` fails the build if the
declared architecture and the actual layout disagree.


## Planted fixtures

Nothing in `packages/domain/src/analysis/` is production code. Each file exists so exactly one
tool family has something real to find, **using the committed configuration,
with no extra flags**.

| Fixture | Found by |
|---|---|
| `packages/domain/src/services/retail-order-processor.ts` + `wholesale-order-processor.ts` | jscpd -- a duplicate pair, at default thresholds |
| [`packages/domain/src/analysis/complexity-sample.ts`](packages/domain/src/analysis/complexity-sample.ts) | eslint + sonarjs -- cyclomatic 27, cognitive 74 |
| [`packages/domain/src/analysis/sast-fixture.ts`](packages/domain/src/analysis/sast-fixture.ts) | eslint-plugin-security |
| [`packages/domain/src/analysis/taint-fixture.ts`](packages/domain/src/analysis/taint-fixture.ts) | 4 taint flows + 1 sanitised control |
| [`packages/domain/src/analysis/dead-code.ts`](packages/domain/src/analysis/dead-code.ts) | ts-prune, eslint-scope |
| [`packages/domain/src/analysis/call-graph-sample.ts`](packages/domain/src/analysis/call-graph-sample.ts) | madge, dependency-cruiser -- depth 5, fan-out 6 |
| Five pinned dependencies | npm audit, Grype, GitHub Advisories -- see [`tools/grype/PLANTED-CVES.md`](tools/grype/PLANTED-CVES.md) |

The duplicate pair sits in real service code, not in `analysis/`, because
duplication inside a fixtures folder is trivially dismissed.

## Tool entry points

```bash
ts-node tools/tool_integration.ts             # wiring banner
ts-node tools/tool_integration.ts --list      # machine-readable list
ts-node tools/tool_integration.ts --verify    # folder + manifest + runner for every tool
ts-node tools/tool_integration.ts --run jscpd # one tool
ts-node tools/tool_integration.ts --run-all   # every tool, in order
ts-node tools/full_check.ts                   # cross-file consistency audit
```

Every tool can also be run directly: `bash tools/<tool>/run_<tool>.sh`.

CI runs **every one of these runners** and uploads their output as artifacts.
A CI file that only installs and tests would leave the declared tools unproven.

## Layout

```
typescript-corpus/  (TS_V20_VITE_BUN_MICRO)
|-- .github/  (1 files)
|-- packages/  (18 files)
|-- services/  (6 files)
|-- tests/  (5 files)
|-- tools/  (68 files)
|-- .editorconfig
|-- .gitignore
|-- .jscpd.json
|-- .madgerc
|-- .npmrc
|-- .nvmrc
|-- Makefile
|-- biome.json
|-- bunfig.toml
|-- dataset.json
|-- eslint.config.mjs
|-- knip.json
|-- package.json
|-- tsconfig.build.json
|-- tsconfig.json
|-- vite.config.mts
|-- vitest.config.ts
```

## Verification

Every claim in this README is checked by `ts-node tools/full_check.ts`, which
reads its expectations **from the repository** rather than from a hard-coded
list -- including that `.nvmrc`, `package.json` engines, `dataset.json`, the CI
workflow and all 26 `trigger.yaml` manifests agree on the Node version, the
branch, and the architecture.
