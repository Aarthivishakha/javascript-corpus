# javascript-combos

Single GitHub repo for the JavaScript white-box combo corpus.

Previously each Node version was split across four repos (`javascript-n12-001-016`, `017-032`, …). Every combo is now a **branch** in this repo.

## Branch naming

`CE-N{version}-{id}`

- **version:** 12, 14, 16, 18, 20, 21, 22, 24, 26
- **id:** `001`–`064` (bundler × package manager × architecture)

Example:

```bash
git clone https://github.com/BENNYameen/javascript-combos.git
cd javascript-combos
git checkout CE-N12-001
```

Direct URL: `https://github.com/BENNYameen/javascript-combos/tree/CE-N12-001`

## Combo grid (64 per Node version)

| IDs | Bundler | Package managers | Architecture |
| --- | --- | --- | --- |
| 001–008 | esbuild | npm, yarn (Berry), pnpm, bun | Monolith / Microservices |
| 009–016 | Vite (built as esbuild) | same | same |
| 017–024 | Webpack | same | same |
| 025–032 | Rollup | same | same |
| 033–040 | Rspack | same | same |
| 041–048 | Parcel | same | same |
| 049–056 | Turbopack | same | same |
| 057–064 | SWC | same | same |

Full index: [COMBOS.csv](COMBOS.csv) (576 rows).

## Notes

- Node **20** had no split GitHub repos yet. Those 64 branches exist here as placeholders from `main` until the stacks are filled in.
- Other versions were copied from the original `javascript-n{ver}-001-016` … `049-064` repos.
