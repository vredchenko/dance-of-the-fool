# Versioning & Releases

This project uses a single version number of the form **`X.Y.Z`**, stored in the
root [`VERSION`](../VERSION) file, which is the **source of truth**.

## What the numbers mean

| Part | Bump when… | Examples |
|------|------------|----------|
| **X** — book | The **book content** changes | a re-translated chapter, corrected text, new translation version |
| **Y** — website | The **web reader** (`webui/`) changes | reader redesign, new reading feature, UI fix |
| **Z** — other | Anything else in the repo | tooling, build pipeline, docs, CI |

### Roll-over (semver-style resets)

A higher-priority bump **resets everything below it to `0`**:

- Book change → bump **X**, reset Y and Z → `1.4.2` → **`2.0.0`**
- Website change → bump **Y**, reset Z → `1.4.2` → **`1.5.0`**
- Other change → bump **Z** → `1.4.2` → **`1.4.3`**

This keeps versions sorting correctly and unambiguous. If a single release
contains several kinds of change, bump the **highest-priority** part that applies.

## Cutting a release

Releases are built and published automatically by
[`.github/workflows/release.yml`](../.github/workflows/release.yml) when a
`vX.Y.Z` tag is pushed. The tag **must** match the `VERSION` file (CI fails if
it doesn't).

```bash
# 1. Bump the version (source of truth)
echo "1.1.0" > VERSION

# 2. Keep package metadata in sync (optional but tidy)
#    - pyproject.toml  -> version = "1.1.0"
#    - webui/package.json -> "version": "1.1.0"

# 3. Commit on main
git add VERSION pyproject.toml webui/package.json
git commit -m "Release 1.1.0"
git push origin main

# 4. Tag and push the tag — this triggers the release build
git tag v1.1.0
git push origin v1.1.0
```

CI then builds and attaches these assets to the GitHub Release:

| Asset | Contents |
|-------|----------|
| `dance-of-the-fool.pdf` | Translation, clean |
| `dance-of-the-fool-annotated.pdf` | Translation + translator's notes |
| `dance-of-the-fool.epub` | Translation, clean |
| `dance-of-the-fool-annotated.epub` | Translation + translator's notes |
| `dance-of-the-fool-web.zip` | Static web reader bundle |

Asset names are **stable across releases**, so these always point at the newest
build:

```
https://github.com/vredchenko/dance-of-the-fool/releases/latest/download/dance-of-the-fool.pdf
https://github.com/vredchenko/dance-of-the-fool/releases/latest/download/dance-of-the-fool.epub
```

You can also trigger a release manually from the Actions tab
(**Release → Run workflow**) by entering the version — CI will create the tag
for you (the `VERSION` file must already match).
