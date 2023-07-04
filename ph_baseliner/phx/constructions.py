# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions for creating and setting Baseline Constructions of a PHX model."""

from copy import copy
from typing import NamedTuple, Callable

from PHX.model.constructions import PhxConstructionOpaque

from ph_baseliner.codes.model import BaselineCode
from ph_baseliner.codes.options import ClimateZones, Use_Groups


class BaselinePHXConstructions(NamedTuple):
    """NamedTuple: The baseline PHX constructions for the PHPP U-Values Worksheet."""

    roof: PhxConstructionOpaque
    exposed_wall: PhxConstructionOpaque
    ground_wall: PhxConstructionOpaque
    exposed_floor: PhxConstructionOpaque
    ground_floor: PhxConstructionOpaque


class BaselineConstructionPHPPids(NamedTuple):
    """NamedTuple: Output of the add_baseline_constructions_to_phpp function."""

    roof: str
    exposed_wall: str
    ground_wall: str
    exposed_floor: str
    ground_floor: str


def create_baseline_constructions(
    baseline_code: BaselineCode,
    climate_zone: ClimateZones,
    use_group: Use_Groups,
    output: Callable = print,
) -> BaselinePHXConstructions:
    """Create the baseline constructions from the code baseline model."""

    # -- Roofs
    new_roof_phx_construction = PhxConstructionOpaque.from_total_u_value(
        baseline_code.get_baseline_roof_u_value(climate_zone, use_group),
        "BASELINE: ROOF",
    )

    # -- Exposed Walls (Above Grade)
    new_exposed_wall_phx_construction = PhxConstructionOpaque.from_total_u_value(
        baseline_code.get_baseline_exposed_wall_u_value(climate_zone, use_group),
        "BASELINE: EXPOSED WALL",
    )

    # -- Ground Walls (Below Grade)
    new_ground_wall_phx_construction = PhxConstructionOpaque.from_total_u_value(
        baseline_code.get_baseline_ground_wall_c_factor(climate_zone, use_group),
        "BASELINE: GROUND WALL",
    )

    # -- Exposed Floors
    new_exposed_floor_phx_construction = PhxConstructionOpaque.from_total_u_value(
        baseline_code.get_baseline_exposed_floor_u_value(climate_zone, use_group),
        "BASELINE: EXPOSED FLOOR",
    )

    # -- Ground Floors
    new_ground_floor_phx_construction = PhxConstructionOpaque.from_total_u_value(
        baseline_code.get_baseline_ground_floor_f_factor(climate_zone, use_group),
        "BASELINE: GROUND FLOOR",
    )

    return BaselinePHXConstructions(
        new_roof_phx_construction,
        new_exposed_wall_phx_construction,
        new_ground_wall_phx_construction,
        new_exposed_floor_phx_construction,
        new_ground_floor_phx_construction,
    )
