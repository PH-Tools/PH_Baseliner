import pathlib
import pytest
from ph_baseliner.codes.model import BaselineCode
from ph_baseliner.codes.options import ClimateZones, Use_Groups, PF_Groups


def test_get_all_window_shgcs():
    baseline_code_file_path = pathlib.Path(
        ".", "ph_baseliner", "codes", "ECCCNYS_2020.json"
    )
    baseline_code_model: BaselineCode = BaselineCode.parse_file(baseline_code_file_path)
    all_shgcs = baseline_code_model.get_window_shgcs()
    assert hasattr(all_shgcs, "CZ4")
    assert hasattr(all_shgcs, "CZ5")
    assert hasattr(all_shgcs, "CZ6")


def test_get_shgcs_for_PF():
    baseline_code_file_path = pathlib.Path(
        ".", "ph_baseliner", "codes", "ECCCNYS_2020.json"
    )
    baseline_code_model: BaselineCode = BaselineCode.parse_file(baseline_code_file_path)
    all_shgcs = baseline_code_model.get_window_shgcs()
    cz_shgcs = all_shgcs.get_shgcs_for_climate(ClimateZones.CZ4)
    assert cz_shgcs.get_shgc_for_pf(PF_Groups.pf_under_20) >= 0.0
    assert cz_shgcs.get_shgc_for_pf(PF_Groups.pf_20_to_50) >= 0.0
    assert cz_shgcs.get_shgc_for_pf(PF_Groups.pf_over_50) >= 0.0


def test_get_valid_shgc_by_climate_and_pf():
    baseline_code_file_path = pathlib.Path(
        ".", "ph_baseliner", "codes", "ECCCNYS_2020.json"
    )
    baseline_code_model: BaselineCode = BaselineCode.parse_file(baseline_code_file_path)
    all_u_values = baseline_code_model.get_window_u_values()
    cz_u_values = all_u_values.get_u_value_for_climate(ClimateZones.CZ4)
    assert cz_u_values.get_u_values_for_use_group(Use_Groups.group_r) == 2.5552188603
