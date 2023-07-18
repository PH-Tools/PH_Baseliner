# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to set baseline PHPP lighting."""

from typing import Optional

from PHX.PHPP.phpp_app import PHPPConnection

from ph_baseliner.codes.model import BaselineCode
from ph_baseliner.codes.lighting_space_types import space_type_map


def find_lighting_installed_power(
    _baseline_code: BaselineCode, _program_name: str
) -> Optional[float]:
    """Find the baseline lighting installed power density for a given PHPP space.

    Arguments:
    ----------
        * _baseline_code: BaselineCode
            The BaselineCode object
        * _program_name: str
            The PHPP space type name

    Returns:
    --------
        * code_LPD: Optional[float]
            The baseline lighting installed power density for the given PHPP space type
    """

    # -- First, find the building-code name which corresponds to the PHPP space type
    code_name = space_type_map.get(_program_name.upper().strip(), None)

    if (
        not code_name
        or code_name not in _baseline_code.tables.lighting_area_method.LPD.keys()
    ):
        msg = (
            f"> Warning: The PHPP Space-Type: '{_program_name}' does not have a corresponding "
            "building-code lighting-space-type? Cannot set electric lighting baseline. "
            "You should set the electric lighting installer power density manually on the "
            "PHPP 'Electricity non-res' worksheet."
        )
        print(msg)
        return None

    # -- Then, find the lighting installed power density for that building-code name
    return _baseline_code.tables.lighting_area_method.LPD[code_name]


def set_baseline_lighting_installed_power_density(
    _phpp_conn: PHPPConnection, _baseline_code: BaselineCode
) -> None:
    """Set the PHPP 'Electricity non-res' worksheet baseline lighting installed power density.

    Arguments:
    ----------
        _phpp_conn: phpp_app.PHPPConnection
            The PHPPConnection object
        _baseline_code: BaselineCode
            The BaselineCode object
    """

    for row_num in _phpp_conn.elec_non_res.lighting.used_lighting_row_numbers:
        row_data = _phpp_conn.elec_non_res.lighting.get_lighting_row_data(row_num)
        code_LPD = find_lighting_installed_power(
            _baseline_code, row_data.utilization_profile_name
        )
        if not code_LPD:
            continue
        _phpp_conn.elec_non_res.lighting.set_lighting_power_density(
            row_num, code_LPD, "W/M2"
        )
