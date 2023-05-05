# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Allowable options for the Baseline Codes."""

from enum import Enum
from typing import List


class ClimateZones(Enum):
    """The climate zones that are available for the PH Baseliner."""

    CZ4 = "CZ4 (Except Marine 4)"
    CZ5 = "CZ5 (and Marine 4)"
    CZ6 = "CZ6"

    @classmethod
    def as_list(cls) -> List[str]:
        """Return a list of the Enum values as strings."""
        return [_.value for _ in cls]


class BaselineCodes(Enum):
    """The baseline codes that are available for the PH Baseliner."""

    ECCCNYS_2020 = "ECC of NYS 2020"

    @classmethod
    def as_list(cls) -> List[str]:
        """Return a list of the Enum values as strings."""
        return [_.value for _ in cls]


class PF_Groups(Enum):
    """The Projection Factor groups that are available for the PH Baseliner."""

    pf_under_20 = "Under 0.2"
    pf_20_to_50 = "0.2 to 0.5"
    pf_over_50 = "Over 0.5"

    @classmethod
    def as_list(cls) -> List[str]:
        """Return a list of the Enum values as strings."""
        return [_.value for _ in cls]


class Use_Groups(Enum):
    """The Use groups that are available for the PH Baseliner."""

    group_r = "Group R"
    all_other = "All Other"

    @classmethod
    def as_list(cls) -> List[str]:
        """Return a list of the Enum values as strings."""
        return [_.value for _ in cls]
