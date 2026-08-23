# frogbot-py-demo-scan-pr

Sample Python project used to showcase **`frogbot scan-pull-request`**.

`scan-pull-request` scans the PR's source branch, compares it against the target
branch, and comments the result on the pull request. The interesting part of
this demo is therefore the *diff* between the two branches.

## The app

The same tiny "orders service" as
[`frogbot-py-demo-scan-repo`](../frogbot-py-demo-scan-repo), built on three
major Python libraries:

| Component      | Used by |
|----------------|---------|
| `aiohttp`      | `orders/server.py` — the HTTP surface |
| `cryptography` | `orders/tokens.py` — receipt signing |
| `urllib3`      | `orders/client.py` — the catalog client |

## The demo diff

`main` pins all three components to **very old** versions. The
`bump-dependencies` branch (PR #1) upgrades all three, but deliberately not all
the way:

| Component      | `main` (very old) | `bump-dependencies` (the PR) | Outcome |
|----------------|-------------------|------------------------------|---------|
| `aiohttp`      | `3.7.4`           | `3.9.0`                      | Newer, **still vulnerable** |
| `cryptography` | `2.3`             | `41.0.0`                     | Newer, **still vulnerable** |
| `urllib3`      | `1.24.1`          | `2.7.0`                      | Latest, **no known CVEs** |

That is the story you usually want to demo: an upgrade that genuinely reduces
risk, where two of the three bumps still leave known CVEs on the table and one
component is fully remediated.

Dependencies are declared twice on purpose — in
[`requirements.txt`](requirements.txt) and in
[`pyproject.toml`](pyproject.toml) — so both the static SCA path (which parses
manifests) and the install-based path (which builds a real dependency tree)
resolve the same three components on either side of the comparison.

> These pins are for *scanning*, not for running. Versions this old do not build
> against a current CPython/OpenSSL, which is fine: Frogbot's static SCA reads
> the manifests and never installs them.

## Frogbot configuration

[`.frogbot/frogbot-config.yml`](.frogbot/frogbot-config.yml) declares a single
pip project at the repository root:

```yaml
params:
  git:
    repoName: frogbot-py-demo-scan-pr
    branches:
      - main
  scan:
    includeAllVulnerabilities: true
    failOnSecurityIssues: false
    projects:
      - installCommandName: pip
        installCommandArgs: ["install", "-r", "requirements.txt"]
        workingDirs:
          - .
```

## Running the scan locally

`scan-pull-request` needs an open pull request, and it reads the PR id from the
environment rather than from the working directory:

```bash
export JF_URL=https://<your-instance>.jfrog.io
export JF_ACCESS_TOKEN=<platform-token>
export JF_GIT_PROVIDER=github
export JF_GIT_OWNER=BiggieFudge
export JF_GIT_REPO=frogbot-py-demo-scan-pr
export JF_GIT_TOKEN=<github-token>
export JF_GIT_BASE_BRANCH=main
export JF_GIT_PULL_REQUEST_ID=1

frogbot scan-pull-request
```

> If your local `pip` is pointed at an Artifactory PyPI repository that blocks
> these old versions (curation, or a repo that simply does not proxy them), add
> `PIP_INDEX_URL=https://pypi.org/simple` so the install-based path can resolve
> them.
