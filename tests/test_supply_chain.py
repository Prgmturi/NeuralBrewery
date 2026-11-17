"""Tests for what the project takes from others, and how it is checked.

WHY these tests exist: on 19 March 2026 an attacker moved 76 of the 77
tags of aquasecurity/trivy-action to code that stole the secrets of the
workflows using them. Every action here was named by a tag; nothing
scanned the image; nothing stopped a secret before the commit
(all checked on 25 October 2026). On 16 November 2026 the image of the
dashboard was built and never scanned, and the scan of the API's image was
red on master: a red scan said nothing of what it found, and its report
could not reach a private repository.
"""

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).parent.parent
WORKFLOWS = sorted((ROOT / ".github" / "workflows").glob("*.yml"))
CI_WORKFLOW = ROOT / ".github" / "workflows" / "ci.yml"
PRE_COMMIT = ROOT / ".pre-commit-config.yaml"
COMPOSE = ROOT / "compose.yaml"
# owner/repo[/path]@<commit SHA> # v<version>
PINNED = re.compile(r"[\w.-]+/[\w./-]+@[0-9a-f]{40} # v\d+(\.\d+)*")
SCAN = "anchore/scan-action@"
UPLOAD = "github/codeql-action/upload-sarif@"
# docker build -f <Dockerfile> -t <image> .
BUILD = re.compile(r"docker build -f (\S+) -t (\S+) \.")
# The names of a Dockerfile
DOCKERFILE_NAME = re.compile(r"dockerfile|containerfile", re.I)
# Folders that hold no file of the project, beside the hidden ones
NOT_THE_PROJECT = {"node_modules", "_reference"}


def uses() -> list[str]:
    """Every action the workflows run, with the comment after it."""
    return [
        match.group(1).strip()
        for path in WORKFLOWS
        for match in re.finditer(r"^\s*(?:- )?uses:\s*(.+)$", path.read_text(), re.M)
    ]


def ci_jobs() -> dict[str, dict]:
    return yaml.safe_load(CI_WORKFLOW.read_text())["jobs"]


def ci_steps(action: str) -> list[tuple[str, dict]]:
    """(job, step) for every step of ci.yml that runs the action."""
    return [
        (name, step)
        for name, job in ci_jobs().items()
        for step in job["steps"]
        if step.get("uses", "").startswith(action)
    ]


def builds() -> set[tuple[str, str, str]]:
    """(job, Dockerfile, image) for every docker build of ci.yml."""
    return {
        (name, *match.groups())
        for name, job in ci_jobs().items()
        for step in job["steps"]
        for match in BUILD.finditer(step.get("run", ""))
    }


def scan_of(job: str) -> dict:
    """The scan step of a job: one per job."""
    [scan] = [step for name, step in ci_steps(SCAN) if name == job]
    return scan


def report_of(job: str) -> str:
    """The expression that names the report of the job's scan."""
    return f"steps.{scan_of(job)['id']}.outputs.sarif"


def dockerfiles() -> list[Path]:
    """Every Dockerfile of the project.

    Hidden folders (.git, .venv, the caches) and NOT_THE_PROJECT are left
    out; a test module named after a Dockerfile, or its bytecode, is not one.
    """
    folders = [
        path
        for path in ROOT.iterdir()
        if path.is_dir()
        and path.name not in NOT_THE_PROJECT
        and not path.name.startswith(".")
    ]
    candidates = [
        *ROOT.iterdir(),
        *(p for folder in folders for p in folder.rglob("*")),
    ]
    return [
        path
        for path in candidates
        if path.is_file()
        and DOCKERFILE_NAME.search(path.name)
        and path.suffix not in {".py", ".pyc"}
    ]


class TestActions:
    def test_every_action_is_pinned_to_a_commit(self):
        """[SEC] owner/repo@<commit SHA> # v<version>, never a tag alone.

        WHY: a tag can be moved to other code, a commit cannot. The comment
        keeps the version readable, and an update moves both.
        """
        assert uses()
        assert [use for use in uses() if not PINNED.fullmatch(use)] == []


class TestImageScan:
    def test_every_image_ci_builds_is_scanned(self):
        """[SEC] Each Dockerfile is built in CI, and scanned in the same job.

        WHY: the dashboard's image was built only by the stack of the e2e
        job, never scanned. CI does not publish it, but compose.yaml runs
        it, with Streamlit, pyarrow, pandas and tornado: packages the API's
        scan never sees (16 November 2026).
        """
        built = {(job, image) for job, _, image in builds()}
        scanned = {(job, step["with"]["image"]) for job, step in ci_steps(SCAN)}

        assert {dockerfile for _, dockerfile, _ in builds()} == {
            path.relative_to(ROOT).as_posix() for path in dockerfiles()
        }
        assert scanned == built

    def test_the_scan_fails_on_a_fixable_high_and_ignores_nothing(self):
        """[SEC] High and Critical with a fix fail the build; no CVE is ignored.

        WHY only the fixable ones: on 25 October 2026 the image had 55 High
        in Debian packages with no fix. Failing on those would fail every
        build, with nothing to do about it. Exactly these inputs: config
        and vex would let a file decide which vulnerabilities count. The
        "user-provided ignore rules" of the log are only-fixed itself, which
        Grype turns into rules on the state of the fix (grype v0.118.0,
        cmd/grype/cli/commands/root.go).
        """
        scans = ci_steps(SCAN)

        assert scans
        assert [
            job
            for job, step in scans
            if step["with"]
            != {
                "image": step["with"]["image"],
                "only-fixed": True,
                "severity-cutoff": "high",
                "fail-build": True,
                "output-format": "sarif",
            }
            or "env" in step
        ] == []

    def test_no_grype_configuration_in_the_repository(self):
        """[SEC] Grype reads no file of ours that could ignore a CVE.

        WHY: without a config input, Grype looks in the folder it runs in
        for .grype.<ext> and .grype/config.<ext>, with any extension viper
        reads (anchore/fangs, finders.go), and takes GRYPE_* variables.
        """
        assert [path.name for path in ROOT.glob(".grype*")] == []
        assert "GRYPE_" not in CI_WORKFLOW.read_text()

    def test_a_failed_scan_says_what_it_found(self):
        """[HP] The High and Critical of each report go to the run's summary.

        WHY: the log of a failed scan says only "Failed minimum severity
        level", and a private repository has no Code scanning to read the
        report in: on 15 November 2026 the CVEs that failed master were
        found again by hand. Grype marks High and Critical "error" in the
        report (grype v0.118.0, grype/presenter/sarif/presenter.go).
        """
        for job, _ in ci_steps(SCAN):
            [summary] = [
                step
                for step in ci_jobs()[job]["steps"]
                if "GITHUB_STEP_SUMMARY" in step.get("run", "")
            ]

            assert "!cancelled()" in summary["if"]
            assert f"{report_of(job)} != ''" in summary["if"]
            assert summary["env"]["SARIF"] == f"${{{{ {report_of(job)} }}}}"
            assert 'select(.level == "error")' in summary["run"]

    def test_the_report_reaches_code_scanning_on_a_public_repository(self):
        """[HP] Each report goes to the Security tab, also when its scan fails.

        WHY only when public: on a private repository of a personal account
        there is no Code scanning, and the upload failed the job even with
        the scan green (15 November 2026). Made public, the repository gets
        it with no change here. One category per image: a report replaces
        the previous one of its category only.
        """
        uploads = ci_steps(UPLOAD)

        assert len(uploads) == len(ci_steps(SCAN))
        for job, upload in uploads:
            assert "!cancelled()" in upload["if"]
            assert "!github.event.repository.private" in upload["if"]
            assert ci_jobs()[job]["permissions"] == {
                "contents": "read",
                "security-events": "write",
            }
        assert len({upload["with"]["category"] for _, upload in uploads}) == len(
            uploads
        )

    def test_no_upload_without_a_report(self):
        """[EC] Without a scan there is no report, and no upload.

        WHY: when the image did not build, the upload ran anyway and failed
        with "Input required and not supplied: sarif_file", an error next to
        the real one (PR #53, 26 October 2026). scan-action sets its sarif
        output also when it fails the build, so a failed scan still reaches
        the Security tab. Each upload sends the report of its own job.
        """
        for job, upload in ci_steps(UPLOAD):
            assert f"{report_of(job)} != ''" in upload["if"]
            assert upload["with"]["sarif_file"] == f"${{{{ {report_of(job)} }}}}"


class TestSecretsHook:
    def test_gitleaks_runs_before_each_commit(self):
        """[SEC] gitleaks stops a secret before it leaves the machine.

        WHY: once pushed to a public repository a secret is public, even if
        the commit is removed later. Its revision is a commit, as for the
        actions.
        """
        config = yaml.safe_load(PRE_COMMIT.read_text())
        repo = next(
            r
            for r in config["repos"]
            if r["repo"] == "https://github.com/gitleaks/gitleaks"
        )

        assert re.fullmatch(r"[0-9a-f]{40}", repo["rev"])
        assert re.search(r"rev: [0-9a-f]{40}  # frozen: v\d+", PRE_COMMIT.read_text())
        assert [hook["id"] for hook in repo["hooks"]] == ["gitleaks"]

    def test_the_keycloak_database_url_is_not_taken_for_a_key(self):
        """[EC] A commit that moves or copies KC_DB_URL is not stopped.

        WHY: gitleaks' generic-api-key rule reads "keycloak-db" as the name
        of a key and "5432/keycloak" as its value, with an entropy of 3.55
        against a threshold of 3.5 (checked on 26 October 2026). The line
        says gitleaks:allow, which is safe while the URL holds no user name
        and no password: those stay in KC_DB_USERNAME and KC_DB_PASSWORD.
        """
        line = next(
            line for line in COMPOSE.read_text().splitlines() if "KC_DB_URL:" in line
        )

        assert line.endswith("  # gitleaks:allow")
        assert "@" not in line
