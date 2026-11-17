"""Tests for the package itself — what importing it loads.

Module under test: src/neuralbrewery/__init__.py
Layer: Package structure

WHY these tests exist: Python runs a package's __init__.py before any of
its modules. When it imported the routers, every tool that needed a
single module of core loaded the features too: Alembic
at each migration, a script that reads the settings, a test.
"""

import json
import subprocess
import sys
import textwrap
import tomllib
from pathlib import Path

# Imports every module of core, then lists the modules of features and
# adapters it loaded.
IMPORT_ALL_OF_CORE = textwrap.dedent(
    """
    import pkgutil
    import sys

    import neuralbrewery.core as core

    for module in pkgutil.walk_packages(core.__path__, "neuralbrewery.core."):
        __import__(module.name)

    loaded = sorted(sys.modules)
    print([
        name
        for name in loaded
        if name.startswith(("neuralbrewery.features", "neuralbrewery.adapters"))
    ])
    """
)


class TestImportCore:
    def test_core_loads_no_feature_and_no_adapter(self, tmp_path):
        """[EC] Importing any module of core loads no feature and no adapter.

        WHY: core must not depend on features nor on adapters. import-linter reads the
        import statements of each module, but not what a package's
        __init__.py pulls in. In a subprocess, because in this one
        conftest.py has already imported the whole app.
        """
        result = subprocess.run(
            [sys.executable, "-c", IMPORT_ALL_OF_CORE],
            cwd=tmp_path,  # no .env in this directory
            capture_output=True,
            text=True,
            check=False,
        )

        assert result.returncode == 0, result.stderr
        assert result.stdout.strip() == "[]"


PYPROJECT = Path(__file__).parent.parent / "pyproject.toml"

# Imports every module of the domain of each feature that has one, then
# prints the domains and every module loaded.
IMPORT_ALL_DOMAINS = textwrap.dedent(
    """
    import importlib
    import json
    import os
    import pkgutil
    import sys

    import neuralbrewery.features as features

    domains = []
    for feature in pkgutil.iter_modules(features.__path__, features.__name__ + "."):
        # Looked for on disk: importing a feature to ask would run its
        # __init__.py, and features/health/__init__.py imports its router
        folder = os.path.join(feature.module_finder.path, feature.name.split(".")[-1])
        if not os.path.isdir(os.path.join(folder, "domain")):
            continue  # a feature with no domain layer, such as health
        name = feature.name + ".domain"
        domain = importlib.import_module(name)
        for module in pkgutil.walk_packages(domain.__path__, name + "."):
            importlib.import_module(module.name)
        domains.append(name)

    print(json.dumps({"domains": domains, "loaded": sorted(sys.modules)}))
    """
)


def domain_contract() -> dict:
    """The import-linter contract of the business layers, in pyproject.toml."""
    importlinter = tomllib.loads(PYPROJECT.read_text())["tool"]["importlinter"]
    for contract in importlinter["contracts"]:
        if contract.get("source_modules") == ["neuralbrewery.features.*.domain"]:
            return contract
    raise AssertionError("pyproject.toml has no import contract for the domains")


class TestImportDomain:
    def test_the_business_layer_loads_no_framework(self, tmp_path):
        """[EC] The domains load none of the packages their contract forbids.

        WHY: the domain of a feature is plain Python. Its contract reads the
        import statements, not what an __init__.py pulls in: the exceptions
        of core imported fastapi.status, and with them FastAPI and Starlette.
        """
        forbidden = domain_contract()["forbidden_modules"]

        result = subprocess.run(
            [sys.executable, "-c", IMPORT_ALL_DOMAINS],
            cwd=tmp_path,  # no .env in this directory
            capture_output=True,
            text=True,
            check=False,
        )

        assert result.returncode == 0, result.stderr
        report = json.loads(result.stdout)
        assert "neuralbrewery.features.approvals.domain" in report["domains"]
        assert [
            name
            for name in report["loaded"]
            if any(
                name == module or name.startswith(f"{module}.") for module in forbidden
            )
        ] == []


# Imports every module of the simulated plant, then prints every module loaded.
IMPORT_ALL_OF_PLANT_SIM = textwrap.dedent(
    """
    import importlib
    import json
    import pkgutil
    import sys

    import neuralbrewery.adapters.plant_sim as plant_sim

    prefix = plant_sim.__name__ + "."
    for module in pkgutil.walk_packages(plant_sim.__path__, prefix):
        importlib.import_module(module.name)

    print(json.dumps(sorted(sys.modules)))
    """
)


def plant_sim_contract() -> dict:
    """The import-linter contract of the simulated plant, in pyproject.toml."""
    importlinter = tomllib.loads(PYPROJECT.read_text())["tool"]["importlinter"]
    for contract in importlinter["contracts"]:
        if contract.get("source_modules") == ["neuralbrewery.adapters.plant_sim"]:
            return contract
    raise AssertionError("pyproject.toml has no import contract for plant_sim")


class TestImportPlantSim:
    def test_the_contract_forbids_the_frameworks(self):
        """[EC] FastAPI, httpx and SQLAlchemy are all in the contract.

        WHY: the simulated plant is plain Python (AGENTS.md). A name taken
        off the list would leave every check green.
        """
        forbidden = plant_sim_contract()["forbidden_modules"]

        assert {"fastapi", "httpx", "sqlalchemy"} <= set(forbidden)

    def test_the_simulated_plant_loads_no_framework(self, tmp_path):
        """[EC] The plant loads none of the packages its contract forbids.

        WHY: tests and evals run the plant in process, with no service around
        it. The contract reads the import statements, not what an __init__.py
        pulls in on the way to adapters/plant_sim.
        """
        forbidden = plant_sim_contract()["forbidden_modules"]

        result = subprocess.run(
            [sys.executable, "-c", IMPORT_ALL_OF_PLANT_SIM],
            cwd=tmp_path,  # no .env in this directory
            capture_output=True,
            text=True,
            check=False,
        )

        assert result.returncode == 0, result.stderr
        assert [
            name
            for name in json.loads(result.stdout)
            if any(
                name == module or name.startswith(f"{module}.") for module in forbidden
            )
        ] == []
