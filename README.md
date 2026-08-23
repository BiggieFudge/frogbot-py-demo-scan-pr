# frogbot-py-demo-scan-pr

Sample Python project used to showcase **`frogbot scan-pull-request`**.

`scan-pull-request` scans the PR's source branch, compares it against the target
branch, and comments the result on the pull request. That makes the interesting
part of this demo the *diff* between the two branches.

## The app

The same tiny "orders service" as
[`frogbot-py-demo-scan-repo`](../frogbot-py-demo-scan-repo), built on three
well-known Python libraries:

| Component  | Used by |
|------------|---------|
| `Django`   | `orders/settings.py`, `orders/urls.py`, `orders/views.py` |
| `PyYAML`   | `orders/config.py` |
| `requests` | `orders/client.py` |

## The demo diff

`main` pins all three components to **very old** versions. The
`bump-dependencies` branch upgrades all three, but deliberately not all the way:

| Component  | `main` (very old) | `bump-dependencies` (the PR) | Outcome |
|------------|-------------------|------------------------------|---------|
| `Django`   | `1.11`            | `3.2.5`                      | Newer, **still vulnerable** |
| `PyYAML`   | `3.12`            | `5.3.1`                      | Newer, **still vulnerable** |
| `requests` | `2.19.1`          | `2.32.5`                     | Latest, **no known CVEs** |

So the PR comment tells the story you usually want to demo: an upgrade that
genuinely reduces risk, while two of the three bumps still leave known CVEs on
the table and one component is fully remediated.

All six versions are real, resolvable releases with usable wheels, so
`pip install -r requirements.txt` succeeds on both branches and Frogbot can
build a full dependency tree on each side of the comparison.

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

`scan-pull-request` needs an open pull request to scan, and it reads the PR id
from the environment rather than from the working directory:

```bash
export JF_URL=https://<your-instance>.jfrog.io
export JF_ACCESS_TOKEN=<platform-token>
export JF_GIT_PROVIDER=github
export JF_GIT_OWNER=BiggieFudge
export JF_GIT_REPO=frogbot-py-demo-scan-pr
export JF_GIT_TOKEN=<github-token>
export JF_GIT_BASE_BRANCH=main
export JF_GIT_PULL_REQUEST_ID=<pr-number>

frogbot scan-pull-request
```

> If your local `pip` is pointed at an Artifactory PyPI repository that blocks
> these old versions (curation, or simply a repo that does not proxy them), add
> `PIP_INDEX_URL=https://pypi.org/simple` to the environment so the install step
> can resolve them.
