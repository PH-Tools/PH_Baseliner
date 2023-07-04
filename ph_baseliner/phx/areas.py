# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions for setting the PHX Model envelope constructions to the baseline values. """

from typing import Callable

from PHX.model.enums.building import ComponentFaceType, ComponentExposureExterior
from PHX.model.project import PhxProject

from ph_baseliner.codes.model import BaselineCode
from ph_baseliner.codes.options import ClimateZones, Use_Groups
from ph_baseliner.phx.constructions import create_baseline_constructions


def set_baseline_envelope_constructions(
    _phx_project: PhxProject,
    baseline_code: BaselineCode,
    climate_zone: ClimateZones,
    use_group: Use_Groups,
    output: Callable = print,
) -> PhxProject:
    """Set the PHX Model envelope constructions to the baseline values."""

    baseline_constructions = create_baseline_constructions(
        baseline_code, climate_zone, use_group
    )

    (
        roof,
        exposed_wall,
        ground_wall,
        exposed_floor,
        ground_floor,
    ) = baseline_constructions

    # -- Add all the new baseline constructions to the PHX project
    for construction in baseline_constructions:
        _phx_project.add_assembly_type(construction, _key=construction.identifier)

    # -- Set each envelope surface to use the right baseline construction
    for variant in _phx_project.variants:
        for opaque_component in variant.building.opaque_components:
            face_type = opaque_component.face_type
            face_exposure = opaque_component.exposure_exterior

            if face_type == ComponentFaceType.WALL:
                if face_exposure == ComponentExposureExterior.EXTERIOR:
                    opaque_component.set_assembly_type(exposed_wall)
                elif face_exposure == ComponentExposureExterior.SURFACE:
                    opaque_component.set_assembly_type(exposed_wall)
                else:
                    opaque_component.set_assembly_type(ground_wall)
            elif face_type == ComponentFaceType.ROOF_CEILING:
                opaque_component.set_assembly_type(roof)
            elif face_type == ComponentFaceType.FLOOR:
                if face_exposure == ComponentExposureExterior.EXTERIOR:
                    opaque_component.set_assembly_type(exposed_floor)
                elif face_exposure == ComponentExposureExterior.SURFACE:
                    opaque_component.set_assembly_type(exposed_floor)
                else:
                    opaque_component.set_assembly_type(ground_floor)

    return _phx_project
