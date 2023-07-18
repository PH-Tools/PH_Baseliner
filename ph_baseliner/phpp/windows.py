# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to set baseline PHPP windows."""

from PHX.PHPP import phpp_app
from PHX.model.constructions import PhxConstructionWindow

from ph_baseliner.codes.model import BaselineCode
from ph_baseliner.codes.options import ClimateZones, PF_Groups, Use_Groups
from ph_baseliner.phpp.components import (
    add_new_baseline_window_glazing,
    add_new_baseline_window_frame,
)


def get_baseline_window_u_value(
    _baseline_code: BaselineCode, _climate_zone: ClimateZones, _use_group: Use_Groups
) -> float:
    """Get the baseline U-Value for the specified climate zone."""
    all_u_values = _baseline_code.get_window_u_values()
    cz_uvalues = all_u_values.get_u_value_for_climate(_climate_zone)
    u_value = cz_uvalues.get_u_values_for_use_group(_use_group)
    return u_value


def get_baseline_window_SHGC(
    _baseline_code: BaselineCode, _climate_zone: ClimateZones, _pf_group: PF_Groups
) -> float:
    """Get the baseline SHGC for the specified climate zone and Projection Factor group."""
    all_shgcs = _baseline_code.get_window_shgcs()
    cz_shgcs = all_shgcs.get_shgcs_for_climate(_climate_zone)
    pf_shgc = cz_shgcs.get_shgc_for_pf(_pf_group)
    return pf_shgc


def set_baseline_window_construction(
    _phpp_conn: phpp_app.PHPPConnection,
    _baseline_code: BaselineCode,
    _climate_zone: ClimateZones,
    _pf_group: PF_Groups,
    _use_group: Use_Groups,
) -> None:
    """Set the baseline window construction in the PHPP Windows Worksheet.

    Arguments:
    ----------
        phpp_conn: phpp_app.PHPPConnection
            The PHPPConnection object
        baseline_code: BaselineCode
            The BaselineCode object
    """

    # -- Get the baseline values for U-Value and SHGC
    u_value = get_baseline_window_u_value(_baseline_code, _climate_zone, _use_group)
    shgc = get_baseline_window_SHGC(_baseline_code, _climate_zone, _pf_group)

    # -- Create the new baseline window construction
    baseline_phx_window = PhxConstructionWindow.from_total_u_value(
        u_value, shgc, "BASELINE: WINDOW"
    )
    phpp_glazing_id = add_new_baseline_window_glazing(_phpp_conn, baseline_phx_window)
    phpp_frame_id = add_new_baseline_window_frame(_phpp_conn, baseline_phx_window)

    # -- Set the window constructions in the Windows Worksheet
    for row_num in _phpp_conn.windows.used_window_row_numbers:
        _phpp_conn.windows.set_single_window_construction_ids(
            row_num, phpp_glazing_id, phpp_frame_id
        )


def set_baseline_window_area(
    _phpp_conn: phpp_app.PHPPConnection, _baseline_code: BaselineCode
) -> None:
    """Set the maximum window-to-wall ratio in the PHPP Windows Worksheet.

    Arguments:
    ----------
        phpp_conn: phpp_app.PHPPConnection
            The PHPPConnection object
        baseline_code: BaselineCode
            The BaselineCode object
    """

    # -- As per NYS Code, C402.4.1 Maximum Area:
    #
    # > "The vertical fenestration area, not including opaque doors and
    # > opaque spandrel panels, shall be not greater than 30
    # > percent of the GROSS above-grade wall area."
    #
    # -- So be sure to use the GROSS wall area, BEFORE the windows
    # -- have been punched out of them.

    maximum_wwr = _baseline_code.get_baseline_max_wwr()
    current_net_wall_area = _phpp_conn.areas.get_total_net_wall_area()
    current_window_area = _phpp_conn.windows.get_total_window_area()
    total_gross_wall_area = current_net_wall_area + current_window_area
    current_wwr = current_window_area / total_gross_wall_area

    if current_wwr < maximum_wwr:
        print(
            f"Current WWR {current_wwr.value :.2%} is less than maximum {maximum_wwr :.0%}."
        )
        return None

    print(
        f"Current WWR {current_wwr.value :.2%} is greater than "
        f"maximum {maximum_wwr :.0%}. Scaling windows."
    )

    # -- Figure out the right scale factor
    scale_factor = maximum_wwr / current_wwr.value

    # -- Scale the window areas
    for row_num in _phpp_conn.windows.used_window_row_numbers:
        if not _phpp_conn.windows.row_is_window(row_num):
            continue

        _phpp_conn.windows.scale_window_size(row_num, scale_factor)


def set_baseline_skylight_area(
    _phpp_conn: phpp_app.PHPPConnection, _baseline_code: BaselineCode
) -> None:
    """Set the maximum skylight-to-roof ratio in the PHPP Windows Worksheet.

    Arguments:
    ----------
        phpp_conn: phpp_app.PHPPConnection
            The PHPPConnection object
        baseline_code: BaselineCode
            The BaselineCode object
    """
    maximum_srr = _baseline_code.get_baseline_max_srr()
    current_roof_area = _phpp_conn.areas.get_total_net_roof_area()
    current_skylight_area = _phpp_conn.windows.get_total_skylight_area()
    total_gross_roof_area = current_roof_area + current_skylight_area
    current_srr = current_skylight_area / total_gross_roof_area

    if current_srr < maximum_srr:
        print(
            f"Current SRR {current_srr.value :.2%} is less than maximum {maximum_srr :.0%}."
        )
        return None

    print(
        f"Current SRR {current_srr.value :.2%} is greater than "
        f"maximum {maximum_srr :.0%}. Scaling Skylights."
    )

    # -- Figure out the right scale factor
    scale_factor = maximum_srr / current_srr.value

    # -- Scale the window areas
    for row_num in _phpp_conn.windows.used_window_row_numbers:
        if not _phpp_conn.windows.row_is_skylight(row_num):
            continue

        _phpp_conn.windows.scale_window_size(row_num, scale_factor)
