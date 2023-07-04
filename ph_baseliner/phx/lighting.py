# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to set baseline PHX Model lighting."""

from typing import Callable

from PHX.model.project import PhxProject

from ph_baseliner.codes.model import BaselineCode
from ph_baseliner.codes.lighting_space_types import space_type_map


def set_baseline_lighting_installed_power_density(
    _phx_project: PhxProject, _baseline_code: BaselineCode, _output: Callable = print
) -> PhxProject:
    # TODO

    return _phx_project
