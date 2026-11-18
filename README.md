# wow-addon-ci

Shared CI/CD for World of Warcraft addons: checks, changelog and version from conventional commits, packaging, GitHub release, CurseForge upload, and reminders for what to update by hand on GitHub and CurseForge.

## Use it in an addon

The addon repository needs:

- `src/<Addon>.toc` (plus optional `src/<Addon>_<Flavor>.toc`) and `src/<Addon>.tga`. Everything in `src/` ships.
- `CHANGELOG.md` with `## [Unreleased](<repo>/compare/<version>...<branch>)` and a tag for the latest version.
- `README.md` with `<!-- release:start -->` and `<!-- release:end -->` lines.
- `.luacheckrc` for the `lint` check.
- Secrets `CF_API_TOKEN` and `CF_PROJECT_ID`. `github-actions` must be allowed to push to the default branch.

`.github/workflows/pipeline.yml`:

```yaml
name: Pipeline
run-name: >-
  ${{ github.ref_type == 'tag' && format('Publish {0}', github.ref_name)
  || github.event_name == 'workflow_dispatch' && format('Run by hand on {0}', github.ref_name)
  || github.event.pull_request.title || github.event.head_commit.message }}

on:
  pull_request:
  push:
    branches: [main]
    tags: ["[0-9]+.[0-9]+.[0-9]+"]
  workflow_dispatch:
    inputs:
      bump:
        description: "On the default branch: auto follows the commits; patch, minor and major force at least that bump."
        type: choice
        options: [auto, patch, minor, major]
        default: auto

concurrency:
  group: pipeline-${{ github.ref }}
  cancel-in-progress: ${{ github.event_name == 'pull_request' }}

jobs:
  pipeline:
    uses: jordinbrouwer/wow-addon-ci/.github/workflows/addon.yml@v1
    permissions:
      actions: write
      contents: write
    with:
      addon: MyAddon
      bump: ${{ inputs.bump || 'auto' }}
    secrets: inherit
```

## The addon's own checks

Put extra checks in `.github/checks/` of the addon: `<name>.py` or `<name>.sh`. They run from the addon's root next to the shared checks, each as its own job. A check with the same name as a shared one (`lint`, `toc`, …) replaces it.

- Python checks can use the shared lib: `from lib import log, toc` (`toc.ADDON`, `toc.SRC`, `log.passed`, `log.fail`).
- Shell checks get `$ADDON` and `$LOG_PREFIX`. A check that needs a tool installs it itself (`sudo apt-get install -y shellcheck`).

See `fixture/.github/checks/` for one of each.

## Run the checks locally

Clone this repository next to the addon, then from the addon's root:

```sh
python3 ../wow-addon-ci/scripts/checks/run.py quick   # fast structural checks
python3 ../wow-addon-ci/scripts/checks/run.py         # everything CI runs
python3 ../wow-addon-ci/scripts/checks/run.py --help  # all modes
```

## Releasing a new version of this repository

Addons call `@v1`. Tag a release (`v1.2.0`) and move `v1` to it; breaking changes for addons get `v2`.

```sh
git tag v1.2.0 && git tag -f v1 && git push origin v1.2.0 && git push -f origin v1
```

`fixture/` is a tiny addon that the CI of this repository runs every check and test on.
