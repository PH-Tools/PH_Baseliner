import pathlib
from ph_baseliner.codes.model import BaselineCode

def test_model_loads_properly():
    baseline_code_file_path = pathlib.Path(".", "ph_baseliner", "codes", "ECCCNYS_2020.json")
    baseline_code_model = BaselineCode.parse_file(baseline_code_file_path)
    assert baseline_code_model.year == "2020"
    assert baseline_code_model.name == "Energy Conservation Construction Code of New York State"
 
