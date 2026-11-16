"""Tests for docker/dashboard.Dockerfile, the image of the brewer's dashboard.

WHY these tests exist: Streamlit brings about 300 MB that the API never
imports (numpy, pandas, pyarrow), measured on 15 November 2026. So the
dashboard has an image of its own, and the image of the API, with its
scan, stays as it was. This one follows the rules of the API's: the same
base image and uv, the lock checked, a user who owns nothing. And
Streamlit sends nothing out: no usage statistics, and no request to a
service on the internet for the machine's public address, which it makes
to print it unless told the address of the browser.
"""

import importlib.metadata
import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).parent.parent
DASHBOARD = ROOT / "docker" / "dashboard.Dockerfile"
API = ROOT / "docker" / "Dockerfile"
CODE = ROOT / "src" / "neuralbrewery" / "dashboard"
UV_IMAGE = re.compile(r"COPY --from=ghcr\.io/astral-sh/uv:(\S+) ")


def instructions(path: Path) -> list[str]:
    """The instructions, one per line: comments out, continuations joined."""
    joined = re.sub(r"\\\n\s*", " ", path.read_text())
    return [
        line.strip()
        for line in joined.splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]


def base_images(path: Path) -> list[str]:
    return [i.split()[1] for i in instructions(path) if i.startswith("FROM ")]


def runtime(path: Path = DASHBOARD) -> list[str]:
    steps = instructions(path)
    start = next(i for i, step in enumerate(steps) if " AS runtime" in step)
    return steps[start:]


def apt(path: Path) -> list[str]:
    """The steps of the runtime stage that run apt-get."""
    return [step for step in runtime(path) if "apt-get" in step]


def environment() -> str:
    return " ".join(step for step in runtime() if step.startswith("ENV "))


def normalized(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def third_party_imports() -> set[str]:
    """The top-level modules the dashboard imports, but its own and Python's."""
    names = set()
    for path in CODE.glob("*.py"):
        for match in re.finditer(r"^(?:from|import) (\w+)", path.read_text(), re.M):
            names.add(match.group(1))
    return {
        n for n in names if n != "neuralbrewery" and n not in sys.stdlib_module_names
    }


class TestBase:
    def test_the_same_base_image_as_the_api(self):
        """[HP] One base image to keep up to date, by tag and by digest."""
        assert len(base_images(DASHBOARD)) == 2
        assert set(base_images(DASHBOARD)) == set(base_images(API))

    def test_the_same_debian_upgrades_as_the_api(self):
        """[HP] Both runtimes upgrade the same Debian packages.

        WHY: one base, the same vulnerabilities: on 16 November 2026 both
        images had the two High of zlib1g. A fix in one image only would
        leave the other one red in its scan (tests/test_dockerfile.py).
        """
        assert apt(DASHBOARD)
        assert apt(DASHBOARD) == apt(API)

    def test_the_same_uv_as_the_api(self):
        """[HP] The uv that checks the lock in CI (tests/test_lockfile.py)."""
        dashboard = UV_IMAGE.search(DASHBOARD.read_text())
        api = UV_IMAGE.search(API.read_text())

        assert dashboard is not None and api is not None
        assert dashboard.group(1) == api.group(1)


class TestInstall:
    def test_only_the_dashboard_group_and_the_lock_checked(self):
        """[SEC] The group alone, as uv.lock says: no dependency of the API."""
        [install] = [i for i in instructions(DASHBOARD) if i.startswith("RUN uv sync")]

        assert "--locked" in install
        assert "--only-group dashboard" in install
        assert "--no-install-project" in install

    def test_the_group_brings_what_the_dashboard_imports(self):
        """[EC] Each module the dashboard imports comes with the group.

        WHY: the image installs the group alone, so a module the code
        imports and the group does not bring would fail only at the start
        of the container.
        """
        pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text())
        group = {
            normalized(re.match(r"[\w.-]+", spec).group(0))
            for spec in pyproject["dependency-groups"]["dashboard"]
            if isinstance(spec, str)
        }
        brought = set(group)
        for name in group:
            for requirement in importlib.metadata.requires(name) or []:
                if "extra ==" not in requirement:
                    brought.add(normalized(re.match(r"[\w.-]+", requirement).group(0)))
        owners = importlib.metadata.packages_distributions()

        missing = [
            module
            for module in third_party_imports()
            if not {normalized(d) for d in owners.get(module, [])} & brought
        ]

        assert third_party_imports() >= {"streamlit", "httpx"}
        assert missing == []

    def test_copies_only_the_dashboard(self):
        """[HP] The empty __init__.py of the package, and the dashboard."""
        copies = [i for i in runtime() if i.startswith("COPY ") and "src" in i]

        assert copies == [
            "COPY src/neuralbrewery/__init__.py src/neuralbrewery/__init__.py",
            "COPY src/neuralbrewery/dashboard src/neuralbrewery/dashboard",
        ]


class TestRuntime:
    def test_the_user_owns_nothing(self):
        """[SEC] As in the API's image: the code belongs to root."""
        steps = runtime()

        assert [step for step in steps if "chown" in step] == []
        assert "USER appuser" in steps

    def test_streamlit_sends_nothing_out(self):
        """[SEC] No usage statistics, no lookup of the public address."""
        env = environment()

        assert "STREAMLIT_BROWSER_GATHER_USAGE_STATS=false" in env
        assert "STREAMLIT_BROWSER_SERVER_ADDRESS=localhost" in env

    def test_starts_the_page_and_probes_it(self):
        """[HP] streamlit run on the page; the probe asks Streamlit's health."""
        steps = runtime()

        assert (
            steps[-1]
            == 'CMD ["streamlit", "run", "src/neuralbrewery/dashboard/app.py"]'
        )
        assert (CODE / "app.py").exists()
        assert any("/_stcore/health" in s for s in steps if s.startswith("HEALTHCHECK"))
