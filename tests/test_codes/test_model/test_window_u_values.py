import pathlib
import pytest
from ph_baseliner.codes.model import BaselineCode


def test_get_valid_shgc_by_climate_and_pf():
    baseline_code_file_path = pathlib.Path(
        ".", "ph_baseliner", "codes", "ECCCNYS_2020.json"
    )
    baseline_code_model = BaselineCode.parse_file(baseline_code_file_path)
    all_u_values = baseline_code_model.get_window_u_values()
    cz_u_values = all_u_values.get_u_value_for_climate("CZ4")
    assert cz_u_values.get_u_values_for_use_group("group_r") == 2.5552188603


def test_get_invalid_shgc_by_climate_and_pf():
    baseline_code_file_path = pathlib.Path(
        ".", "ph_baseliner", "codes", "ECCCNYS_2020.json"
    )
    baseline_code_model = BaselineCode.parse_file(baseline_code_file_path)
    all_u_values = baseline_code_model.get_window_shgcs()

    with pytest.raises(ValueError):
        cz_u_values = all_u_values.get_shgcs_for_climate("CZ_NOT_VALID")
