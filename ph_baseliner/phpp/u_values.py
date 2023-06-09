# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions for creating and setting Baseline Constructions on the PHPP U-Values worksheet."""

from copy import copy

from PHX.PHPP import phpp_app

from ph_baseliner.phx.constructions import (
    BaselinePHXConstructions,
    BaselineConstructionPHPPids,
)


def add_baseline_constructions_to_phpp(
    phpp_conn: phpp_app.PHPPConnection, baseline_constructions: BaselinePHXConstructions
) -> BaselineConstructionPHPPids:
    """Add the baseline constructions to the PHPP U-Values Worksheet."""
    roof_phpp_id = phpp_conn.u_values.add_new_phx_construction(
        baseline_constructions.roof
    )
    exposed_wall_phpp_id = phpp_conn.u_values.add_new_phx_construction(
        baseline_constructions.exposed_wall
    )
    ground_wall_phpp_id = phpp_conn.u_values.add_new_phx_construction(
        baseline_constructions.ground_wall
    )
    exposed_floor_phpp_id = phpp_conn.u_values.add_new_phx_construction(
        baseline_constructions.exposed_floor
    )
    ground_floor_phpp_id = phpp_conn.u_values.add_new_phx_construction(
        baseline_constructions.ground_floor
    )

    return BaselineConstructionPHPPids(
        roof_phpp_id,
        exposed_wall_phpp_id,
        ground_wall_phpp_id,
        exposed_floor_phpp_id,
        ground_floor_phpp_id,
    )


def replace_u_values_with_baseline_constructions(
    phpp_conn: phpp_app.PHPPConnection, baseline_constructions: BaselinePHXConstructions
) -> None:
    """Replace the existing U-Values with the baseline constructions."""

    def is_roof(_input: str):
        """Return True if the R_si type is a 'Roof'."""
        return "ROOF" in str(_input).upper()

    def is_wall(_input: str):
        """Return True if the R_si type is a 'Wall'."""
        return "WALL" in str(_input).upper()

    def is_floor(_input: str):
        """Return True if the R_si type is a 'Floor'."""
        return "FLOOR" in str(_input).upper()

    def is_below_grade(_input: str):
        """Return True if the R_se type is a 'Ground'."""
        return "GROUND" in str(_input).upper()

    for row_num in phpp_conn.u_values.used_constructor_start_rows:
        constructor_name = phpp_conn.u_values.get_constructor_name(row_num)
        r_si_type = phpp_conn.u_values.get_constructor_r_si_type(row_num)
        r_se_type = phpp_conn.u_values.get_constructor_r_se_type(row_num)

        if is_roof(r_si_type):
            _phx_const = copy(baseline_constructions.roof)
        elif is_wall(r_si_type) and is_below_grade(r_se_type):
            _phx_const = copy(baseline_constructions.ground_wall)
        elif is_wall(r_si_type) and not is_below_grade(r_se_type):
            _phx_const = copy(baseline_constructions.exposed_wall)
        elif is_floor(r_si_type) and is_below_grade(r_se_type):
            _phx_const = copy(baseline_constructions.ground_floor)
        elif is_floor(r_si_type) and not is_below_grade(r_se_type):
            _phx_const = copy(baseline_constructions.exposed_floor)
        else:
            continue

        _phx_const.display_name = constructor_name

        # -- Update the PHPP
        phpp_conn.u_values.clear_single_constructor_data(row_num, False)
        phpp_conn.u_values.write_single_PHX_construction(_phx_const, row_num)
