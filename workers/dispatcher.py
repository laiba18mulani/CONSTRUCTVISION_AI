"""Worker dispatch policy; production deployments invoke this from a durable queue."""
from __future__ import annotations

import shutil

SUPPORTED = {
    "RECONSTRUCTION": ("colmap", "COLMAP photogrammetry"),
    "STRUCTURAL_FEA": ("OpenSees", "OpenSees finite-element solver"),
    "CFD": ("simpleFoam", "OpenFOAM CFD solver"),
    "FLOOD": ("simpleFoam", "OpenFOAM shallow-water/CFD solver"),
}


def solver_readiness(kind: str) -> dict[str, str | bool]:
    executable, label = SUPPORTED[kind]
    available = shutil.which(executable) is not None
    return {
        "solver": label,
        "executable": executable,
        "available": available,
        "state": "READY" if available else "BLOCKED",
        "message": "Worker can execute this job." if available else f"Install {label} and attach a worker; no result has been fabricated.",
    }
