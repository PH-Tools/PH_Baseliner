import pathlib

import pytest

from ph_baseliner.codes.model import BaselineCode
from ph_baseliner.codes.options import ClimateZones, Use_Groups, PF_Groups
from ph_baseliner.phpp import windows


def test_get_baseline_windows_u_value():
    baseline_code_file_path = pathlib.Path(
        ".", "ph_baseliner", "codes", "ECCCNYS_2020.json"
    )
    baseline_code_model: BaselineCode = BaselineCode.parse_file(baseline_code_file_path)
    u_value = windows.get_baseline_window_u_value(
        baseline_code_model, ClimateZones.CZ4, Use_Groups.group_r
    )
    assert u_value == 2.5552188603


def test_get_baseline_windows_shgc():
    baseline_code_file_path = pathlib.Path(
        ".", "ph_baseliner", "codes", "ECCCNYS_2020.json"
    )
    baseline_code_model: BaselineCode = BaselineCode.parse_file(baseline_code_file_path)
    shgc = windows.get_baseline_window_SHGC(
        baseline_code_model, ClimateZones.CZ4, PF_Groups.pf_20_to_50
    )
    assert shgc == 0.43
    shgc = windows.get_baseline_window_SHGC(
        baseline_code_model, ClimateZones.CZ5, PF_Groups.pf_20_to_50
    )
    assert shgc == 0.46
    shgc = windows.get_baseline_window_SHGC(
        baseline_code_model, ClimateZones.CZ6, PF_Groups.pf_20_to_50
    )
    assert shgc == 0.48
