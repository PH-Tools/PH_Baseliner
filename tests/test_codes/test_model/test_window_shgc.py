import pathlib
import pytest
from ph_baseliner.codes.model import BaselineCode


def test_get_valid_shgc_by_climate_and_pf():
    baseline_code_file_path = pathlib.Path(
        ".", "ph_baseliner", "codes", "ECCCNYS_2020.json"
    )
    baseline_code_model = BaselineCode.parse_file(baseline_code_file_path)
    all_shgcs = baseline_code_model.get_window_shgcs()
    cz4_shgcs = all_shgcs.get_shgcs_for_climate("CZ4")
    assert cz4_shgcs.get_shgc_for_pf("pf_20_to_50") == 0.43


def test_get_invalid_shgc_by_climate_and_pf():
    baseline_code_file_path = pathlib.Path(
        ".", "ph_baseliner", "codes", "ECCCNYS_2020.json"
    )
    baseline_code_model = BaselineCode.parse_file(baseline_code_file_path)
    all_shgcs = baseline_code_model.get_window_shgcs()

    with pytest.raises(ValueError):
        cz4_shgcs = all_shgcs.get_shgcs_for_climate("CZ_NOT_VALID")
