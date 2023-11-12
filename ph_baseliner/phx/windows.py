# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to set baseline PHX Model windows."""

from typing import Callable, Dict

from PHX.model.project import PhxProject
from PHX.model.components import PhxComponentAperture
from PHX.model.constructions import PhxConstructionWindow

from ph_baseliner.codes.model import BaselineCode
from ph_baseliner.codes.options import ClimateZones, PF_Groups, Use_Groups


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
    _phx_project: PhxProject,
    _baseline_code: BaselineCode,
    _climate_zone: ClimateZones,
    _pf_group: PF_Groups,
    _use_group: Use_Groups,
    _output: Callable = print,
) -> PhxProject:
    # -- Get the baseline values for U-Value and SHGC
    u_value = get_baseline_window_u_value(_baseline_code, _climate_zone, _use_group)
    _output(f"Using baseline window U-Value: {u_value :.3f} for all windows.")

    shgc = get_baseline_window_SHGC(_baseline_code, _climate_zone, _pf_group)
    _output(f"Using baseline window SHGC: {shgc :.2f} for all windows.")
    

    # -----------------------------------------------------------------------------------
    # -- Collect all the unique 'PhxComponentAperture' types in the PHX project
    _output(f"Collecting the unique '{PhxComponentAperture.__name__}' types in the PHX-Project: '{_phx_project.name}'.")
    unique_aperture_types: Dict[str, PhxComponentAperture] = {}
    for variant in _phx_project.variants:
        for ap in variant.building.aperture_components:
            unique_aperture_types[ap.unique_key] = ap


    # -----------------------------------------------------------------------------------
    # -- Create a new baseline 'PhxConstructionWindow' for each of the unique 'PhxComponentAperture' types
    _output(f"Creating a new baseline '{PhxConstructionWindow.__name__}' for each unique '{PhxComponentAperture.__name__}' type.")
    for i, unique_window_type_key in enumerate(unique_aperture_types.keys(), start=1):
        window_type = unique_aperture_types[unique_window_type_key]
        baseline_phx_window = PhxConstructionWindow.from_total_u_value(
            u_value, shgc, f"BASELINE: WINDOW {i :03}"
        )
        baseline_phx_window.id_num_shade = window_type.shade_type_id_num

        # -- Add the new baseline window construction to the PHX project
        _phx_project.add_new_window_type(
            baseline_phx_window, _key=unique_window_type_key
        )


    # -----------------------------------------------------------------------------------
    # -- Set the baseline PhxComponentAperture's 'PhxConstructionWindow'
    _output(f"Setting all '{PhxConstructionWindow.__name__}' to the baseline types.")
    for variant in _phx_project.variants:
        for ap in variant.building.aperture_components:
            baseline_phx_window_type = _phx_project.get_window_type(
                ap.unique_key
            )
            ap.set_window_type(baseline_phx_window_type)

    return _phx_project


def set_baseline_window_area(
    _phx_project: PhxProject, _baseline_code: BaselineCode, _output: Callable = print
) -> PhxProject:
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
    current_gross_wall_area = _phx_project.get_total_gross_wall_area()
    maximum_aperture_area = current_gross_wall_area * maximum_wwr
    current_aperture_area = _phx_project.get_total_wall_aperture_area()
    current_wwr = current_aperture_area / current_gross_wall_area

    _output(f"Current wall aperture area = {current_aperture_area :.1f}")
    _output(f"Current gross wall area = {current_gross_wall_area:.1f}")
    _output(
        f"Wall aperture area limit = {maximum_aperture_area:.1f} [{current_gross_wall_area :.1f} x {maximum_wwr :.0%}]"
    )

    if current_wwr < maximum_wwr:
        _output(
            f"Current WWR {current_wwr:.2%} is less than baseline maximum of {maximum_wwr:.0%}."
        )
        return _phx_project

    aperture_area_reduction_required = current_aperture_area - maximum_aperture_area
    _output(
        f"Wall aperture area reduction required = {aperture_area_reduction_required:.1f}"
    )

    # -- Figure out the right scale factor to use
    area_scale_factor = 1 - (aperture_area_reduction_required / current_aperture_area)
    geometric_scale_factor = (area_scale_factor) ** 0.5
    _output(
        f"Scaling wall apertures down to {area_scale_factor :.1%} of original size."
    )

    # -- Scale all the Aperture components
    for variant in _phx_project.variants:
        variant.building.scale_all_wall_aperture_components(geometric_scale_factor)

    return _phx_project


def set_baseline_skylight_area(
    _phx_project: PhxProject, _baseline_code: BaselineCode, output: Callable = print
) -> PhxProject:
    maximum_srr = _baseline_code.get_baseline_max_srr()
    current_gross_roof_area = _phx_project.get_total_gross_roof_area()
    maximum_aperture_area = current_gross_roof_area * maximum_srr
    current_aperture_area = _phx_project.get_total_roof_aperture_area()
    current_srr = current_aperture_area / current_gross_roof_area

    output(f"Current roof aperture area = {current_aperture_area :.1f}")
    output(f"Current gross roof area = {current_gross_roof_area:.1f}")
    output(
        f"Roof aperture area limit = {maximum_aperture_area:.1f} [{current_gross_roof_area :.1f} x {maximum_srr :.0%}]"
    )

    if current_srr < maximum_srr:
        output(
            f"Current SRR {current_srr:.2%} is less than baseline maximum of {maximum_srr:.0%}."
        )
        return _phx_project

    aperture_area_reduction_required = current_aperture_area - maximum_aperture_area
    output(
        f"Roof aperture area reduction required = {aperture_area_reduction_required :.1f}"
    )

    # -- Figure out the right scale factor to use
    area_scale_factor = 1 - (aperture_area_reduction_required / current_aperture_area)
    geometric_scale_factor = (area_scale_factor) ** 0.5
    output(f"Scaling roof apertures down to {area_scale_factor :.1%} of original size.")

    # -- Scale all the Aperture components
    for variant in _phx_project.variants:
        variant.building.scale_all_roof_aperture_components(geometric_scale_factor)

    return _phx_project
