"""Transparent, preliminary structural screening calculations.

This module deliberately does not claim to replace a licensed structural design
or a validated CFD/FEA solver. It supplies traceable first-pass calculations
and a stable API that can later be backed by OpenSees, CalculiX or CFD workers.
"""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np
import pandas as pd


@dataclass(frozen=True)
class TwinInputs:
    floors: int = 4
    bays_x: int = 4
    bays_y: int = 3
    bay_m: float = 6.0
    storey_m: float = 3.6
    concrete_mpa: float = 35.0
    column_mm: int = 500
    beam_mm: int = 350
    wind_mps: float = 18.0
    rainfall_mm_h: float = 15.0
    flood_m: float = 0.0
    live_load_kpa: float = 3.0


def wind_pressure_kpa(speed_mps: float) -> float:
    """Dynamic wind pressure, q=0.613 V² (N/m²), reported as kPa."""
    return 0.613 * speed_mps**2 / 1000


def screening_results(i: TwinInputs) -> dict[str, float | str]:
    # Tributary-area axial screening for an interior lower-storey column.
    area = i.bay_m * i.bay_m
    gravity_kN = (6.0 + i.live_load_kpa) * area * i.floors
    column_area = (i.column_mm / 1000) ** 2
    axial_mpa = gravity_kN / column_area / 1000
    capacity_mpa = 0.40 * i.concrete_mpa
    # Simply supported beam screening under service gravity loading.
    line_kN_m = (6.0 + i.live_load_kpa) * i.bay_m
    moment = line_kN_m * i.bay_m**2 / 8
    # conservative simplified section-modulus stress indicator
    section_modulus = (i.beam_mm / 1000) ** 3 / 6
    flexural_mpa = moment / section_modulus / 1000
    wind_kpa = wind_pressure_kpa(i.wind_mps)
    flood_kpa = 9.81 * i.flood_m
    utilization = max(axial_mpa / capacity_mpa, flexural_mpa / (0.6 * i.concrete_mpa))
    return {
        "gravity_kN": gravity_kN,
        "axial_mpa": axial_mpa,
        "flexural_mpa": flexural_mpa,
        "wind_kpa": wind_kpa,
        "flood_kpa": flood_kpa,
        "utilization": utilization,
        "status": "Review required" if utilization >= 0.8 else "Screening pass",
    }


def frame_nodes(i: TwinInputs) -> pd.DataFrame:
    rows = []
    for z in range(i.floors + 1):
        for x in range(i.bays_x + 1):
            for y in range(i.bays_y + 1):
                rows.append((x * i.bay_m, y * i.bay_m, z * i.storey_m))
    return pd.DataFrame(rows, columns=["x", "y", "z"])


def frame_members(i: TwinInputs) -> list[tuple[tuple[float, float, float], tuple[float, float, float], str]]:
    members = []
    for x in range(i.bays_x + 1):
        for y in range(i.bays_y + 1):
            for z in range(i.floors):
                members.append(((x*i.bay_m, y*i.bay_m, z*i.storey_m), (x*i.bay_m, y*i.bay_m, (z+1)*i.storey_m), "column"))
    for z in range(1, i.floors + 1):
        for y in range(i.bays_y + 1):
            for x in range(i.bays_x):
                members.append(((x*i.bay_m, y*i.bay_m, z*i.storey_m), ((x+1)*i.bay_m, y*i.bay_m, z*i.storey_m), "beam"))
        for x in range(i.bays_x + 1):
            for y in range(i.bays_y):
                members.append(((x*i.bay_m, y*i.bay_m, z*i.storey_m), (x*i.bay_m, (y+1)*i.bay_m, z*i.storey_m), "beam"))
    return members


def telemetry(hours: int = 168, seed: int = 19) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    index = pd.date_range(end=pd.Timestamp.now().floor("h"), periods=hours, freq="h")
    thermal = 25 + 6*np.sin(np.linspace(0, 8*np.pi, hours)) + rng.normal(0, .45, hours)
    wind = np.clip(8 + 5*np.sin(np.linspace(0, 5*np.pi, hours)) + rng.normal(0, 2, hours), 0, None)
    strain = 165 + thermal*1.2 + wind*2.3 + rng.normal(0, 6, hours)
    return pd.DataFrame({"time": index, "strain_µε": strain, "tilt_mrad": .15 + wind*.012 + rng.normal(0, .02, hours), "temperature_°C": thermal, "wind_mps": wind})
