"""Run local batch and real-time inference simulation workflows."""

from __future__ import annotations

from pathlib import Path

from risk_platform.inference.batch_inference import write_batch_inference_artifacts
from risk_platform.inference.realtime_simulator import write_realtime_simulation_artifacts


def run_inference_artifacts() -> dict[str, Path]:
    """Run all local inference workflows."""
    artifacts = {}
    artifacts.update(write_batch_inference_artifacts())
    artifacts.update(write_realtime_simulation_artifacts())
    return artifacts


def main() -> None:
    """CLI entry point for local inference workflows."""
    artifacts = run_inference_artifacts()
    for artifact_name, artifact_path in artifacts.items():
        print(f"Wrote {artifact_name}: {artifact_path}")


if __name__ == "__main__":
    main()
