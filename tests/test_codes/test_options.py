from ph_baseliner.codes.options import (
    ClimateZones,
    BaselineCodes,
    PF_Groups,
    Use_Groups,
)


def test_climate_zones():
    assert len(ClimateZones.as_list()) == 3


def test_climate_zones_invalid():
    assert "CZ_NOT_VALID" not in ClimateZones.as_list()


def test_baseline_codes():
    assert len(BaselineCodes.as_list()) == 1


def test_baseline_codes_invalid():
    assert "ECCCNYS_2020_NOT_VALID" not in BaselineCodes.as_list()


def test_pf_groups():
    assert len(PF_Groups.as_list()) == 3


def test_pf_groups_invalid():
    assert "pf_not_valid" not in PF_Groups.as_list()


def test_use_groups():
    assert len(Use_Groups.as_list()) == 2


def test_use_groups_invalid():
    assert "use_not_valid" not in Use_Groups.as_list()
