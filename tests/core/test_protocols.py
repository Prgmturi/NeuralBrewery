"""Tests for protocols — runtime_checkable verification.

Module under test: src/neuralbrewery/core/protocols.py
Layer: Pure domain (structural typing verification)

WHY these tests exist: runtime_checkable protocols enable isinstance checks.
If @runtime_checkable is accidentally removed, isinstance() calls silently
return False. These tests detect that at test time.
"""

from neuralbrewery.core.protocols import HealthCheckable


class TestCoreProtocols:
    """Verify runtime_checkable decorators work for core protocols."""

    def test_health_checkable_is_runtime_checkable(self):
        """[CT] HealthCheckable supports isinstance()."""

        class _Impl:
            async def health_check(self) -> bool:
                return True

        assert isinstance(_Impl(), HealthCheckable)
