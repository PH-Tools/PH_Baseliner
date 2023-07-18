# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Data model of the Baseline Building Code."""

from pydantic import BaseModel, validator
from typing import Dict

from ph_units.converter import convert
from ph_baseliner.codes.options import ClimateZones, Use_Groups, PF_Groups

# -----------------------------------------------------------------------------


class TableMaximumUFactor_Values(BaseModel):
    group_r: float
    all_other: float

    @classmethod
    def convert_units(cls, v: "TableMaximumUFactor_Values", **kwargs):
        for field in v.__fields__:
            val = getattr(v, field)
            val = convert(val, kwargs["units"], "W/m2K")
            setattr(v, field, val)
        return v

    def get_u_values_for_use_group(self, _use_group: Use_Groups) -> float:
        """Return the U-value for the given use group name.

        Args:
            _use_group: Use_Groups:
                The use group to return the U-value for.
        """

        try:
            return getattr(self, _use_group.name)
        except Exception as e:
            allowed_use_group_names = [_ for _ in self.__fields__]
            msg = (
                f"Use Group: '{_use_group.name}' is not supported. "
                f"Supported groups include only: {allowed_use_group_names}"
            )
            raise ValueError(msg, e)


class TableMaximumCFactor_Values(BaseModel):
    group_r: float
    all_other: float

    @classmethod
    def convert_units(cls, v: "TableMaximumCFactor_Values", **kwargs):
        for field in v.__fields__:
            val = getattr(v, field)
            val = convert(val, kwargs["units"], "W/m2K")
            setattr(v, field, val)
        return v

    def get_c_factor_for_use_group(self, _use_group: Use_Groups) -> float:
        """Return the C-Factor for the given use group name.

        Args:
            _use_group: Use_Groups:
                The name of the use group to return the C-Factor for.
        """

        try:
            return getattr(self, _use_group.name)
        except Exception as e:
            allowed_use_group_names = [_ for _ in self.__fields__]
            msg = (
                f"Use Group: '{_use_group.name}' is not supported. "
                f"Supported groups include only: {allowed_use_group_names}"
            )
            raise ValueError(msg, e)


class TableMaximumFFactor_Values(BaseModel):
    group_r: float
    all_other: float

    @classmethod
    def convert_units(cls, v: "TableMaximumFFactor_Values", **kwargs):
        for field in v.__fields__:
            val = getattr(v, field)
            val = convert(val, kwargs["units"], "W/m2K")
            setattr(v, field, val)
        return v

    def get_f_factor_for_use_group(self, _use_group: Use_Groups) -> float:
        """Return the F-Factor for the given use group name.

        Args:
            _use_group: Use_Groups
                The name of the use group to return the F-Factor for.
        """

        try:
            return getattr(self, _use_group.name)
        except Exception as e:
            allowed_use_group_names = [_ for _ in self.__fields__]
            msg = (
                f"Use Group: '{_use_group.name}' is not supported. "
                f"Supported groups include only: {allowed_use_group_names}"
            )
            raise ValueError(msg, e)


class TableMaximumSHGC_Values(BaseModel):
    pf_under_20: float
    pf_20_to_50: float
    pf_over_50: float

    @classmethod
    def convert_units(cls, v: "TableMaximumSHGC_Values", **kwargs):
        return v

    def get_shgc_for_pf(self, _pf_group: PF_Groups) -> float:
        """Return the SHGC value for the given PF group name.

        Args:
            _pf_group: PF_Groups:
                The PF group to return the SHGC for.
        """

        try:
            return getattr(self, _pf_group.name)
        except Exception as e:
            allowed_pf_group_names = [_ for _ in self.__fields__]
            msg = (
                f"Climate Zone: '{_pf_group.name}' is not supported. "
                f"Supported zones include only: {allowed_pf_group_names}"
            )
            raise ValueError(msg, e)


# -----------------------------------------------------------------------------


class TableMaximumUFactor_ClimateZones(BaseModel):
    CZ4: TableMaximumUFactor_Values
    CZ5: TableMaximumUFactor_Values
    CZ6: TableMaximumUFactor_Values

    @classmethod
    def convert_units(cls, v: "TableMaximumUFactor_ClimateZones", **kwargs):
        for field_name in v.__fields__:
            field_type = getattr(v, field_name)
            field_type.convert_units(field_type, **kwargs)
        return v

    def get_u_value_for_climate(
        self, _climate_zone: ClimateZones
    ) -> "TableMaximumUFactor_Values":
        """Return the U-Values for the given climate zone name.

        Args:
            _climate_zone: ClimateZones:
                The name of the climate zone to return the U-Values for.
        """

        try:
            return getattr(self, _climate_zone.name)
        except Exception as e:
            allowed_climate_zone_names = [_ for _ in self.__fields__]
            msg = (
                f"Climate Zone: '{_climate_zone.name}' is not supported. "
                f"Supported zones include only: {allowed_climate_zone_names}"
            )
            raise ValueError(msg, e)


class TableMaximumCFactor_ClimateZones(BaseModel):
    CZ4: TableMaximumCFactor_Values
    CZ5: TableMaximumCFactor_Values
    CZ6: TableMaximumCFactor_Values

    @classmethod
    def convert_units(cls, v: "TableMaximumCFactor_ClimateZones", **kwargs):
        for field_name in v.__fields__:
            field_type = getattr(v, field_name)
            field_type.convert_units(field_type, **kwargs)
        return v

    def get_c_factor_for_climate(
        self, _climate_zone: ClimateZones
    ) -> "TableMaximumCFactor_Values":
        """Return the C-Factors for the given climate zone name.

        Args:
            _climate_zone: ClimateZones
                The name of the climate zone to return the C-Factors for.
        """

        try:
            return getattr(self, _climate_zone.name)
        except Exception as e:
            allowed_climate_zone_names = [_ for _ in self.__fields__]
            msg = (
                f"Climate Zone: '{_climate_zone.name}' is not supported. "
                f"Supported zones include only: {allowed_climate_zone_names}"
            )
            raise ValueError(msg, e)


class TableMaximumFFactor_ClimateZones(BaseModel):
    CZ4: TableMaximumFFactor_Values
    CZ5: TableMaximumFFactor_Values
    CZ6: TableMaximumFFactor_Values

    @classmethod
    def convert_units(cls, v: "TableMaximumFFactor_ClimateZones", **kwargs):
        for field_name in v.__fields__:
            field_type = getattr(v, field_name)
            field_type.convert_units(field_type, **kwargs)
        return v

    def get_f_factor_for_climate(
        self, _climate_zone: ClimateZones
    ) -> "TableMaximumFFactor_Values":
        """Return the F-Factors for the given climate zone name.

        Args:
            _climate_zone: ClimateZones
                The name of the climate zone to return the F-Factors for.
        """

        try:
            return getattr(self, _climate_zone.name)
        except Exception as e:
            allowed_climate_zone_names = [_ for _ in self.__fields__]
            msg = (
                f"Climate Zone: '{_climate_zone.name}' is not supported. "
                f"Supported zones include only: {allowed_climate_zone_names}"
            )
            raise ValueError(msg, e)


class TableMaximumSHGC_ClimateZones(BaseModel):
    CZ4: TableMaximumSHGC_Values
    CZ5: TableMaximumSHGC_Values
    CZ6: TableMaximumSHGC_Values

    @classmethod
    def convert_units(cls, v: "TableMaximumSHGC_ClimateZones", **kwargs):
        return v

    def get_shgcs_for_climate(
        self, _climate_zone: ClimateZones
    ) -> TableMaximumSHGC_Values:
        """Get the SHGC values for a given climate zone.

        Args:
            climate_zone: ClimateZones:
                The name of the climate zone.
        """
        try:
            return getattr(self, _climate_zone.name)
        except Exception as e:
            allowed_climate_zone_names = [_ for _ in self.__fields__]
            msg = (
                f"Climate Zone: '{_climate_zone.name}' is not supported. "
                f"Supported zones include only: {allowed_climate_zone_names}"
            )
            raise ValueError(msg, e)


# -----------------------------------------------------------------------------


class TableMaximumUFactorRoofs(BaseModel):
    insulation_above_deck: TableMaximumUFactor_ClimateZones
    metal_building: TableMaximumUFactor_ClimateZones
    attic_and_other: TableMaximumUFactor_ClimateZones

    @classmethod
    def convert_units(cls, v: "TableMaximumUFactorRoofs", **kwargs):
        for field_name in v.__fields__:
            field_type = getattr(v, field_name)
            field_type.convert_units(field_type, **kwargs)
        return v


class TableMaximumUFactorWalls(BaseModel):
    mass: TableMaximumUFactor_ClimateZones
    metal_building: TableMaximumUFactor_ClimateZones
    metal_framed: TableMaximumUFactor_ClimateZones
    wood_framed_and_other: TableMaximumUFactor_ClimateZones
    below_grade: TableMaximumCFactor_ClimateZones

    @classmethod
    def convert_units(cls, v: "TableMaximumUFactorWalls", **kwargs):
        for field_name in v.__fields__:
            field_type = getattr(v, field_name)
            field_type.convert_units(field_type, **kwargs)
        return v


class TableMaximumUFactorFloors(BaseModel):
    mass: TableMaximumUFactor_ClimateZones
    joist_framed: TableMaximumUFactor_ClimateZones
    unheated_slab: TableMaximumFFactor_ClimateZones
    heated_slab: TableMaximumUFactor_ClimateZones

    @classmethod
    def convert_units(cls, v: "TableMaximumUFactorFloors", **kwargs):
        for field_name in v.__fields__:
            field_type = getattr(v, field_name)
            field_type.convert_units(field_type, **kwargs)
        return v


class TableMaximumUFactorFenestration(BaseModel):
    u_factors: TableMaximumUFactor_ClimateZones
    shgc: TableMaximumSHGC_ClimateZones

    @classmethod
    def convert_units(cls, v: "TableMaximumUFactorFenestration", **kwargs):
        for field_name in v.__fields__:
            field_type = getattr(v, field_name)
            field_type.convert_units(field_type, **kwargs)
        return v


# -----------------------------------------------------------------------------


class TableEnvelopeMaximumUFactors(BaseModel):
    name: str
    section: str
    units: str
    roofs: TableMaximumUFactorRoofs
    walls: TableMaximumUFactorWalls
    floors: TableMaximumUFactorFloors

    @validator("roofs", "walls", "floors", pre=False)
    @classmethod
    def convert_units(cls, v: "TableEnvelopeMaximumUFactors", values: Dict):
        return type(v).convert_units(v, **values)


class TableFenestrationMaximumUFactors(BaseModel):
    name: str
    section: str
    units: str
    fixed_windows: TableMaximumUFactorFenestration
    operable_windows: TableMaximumUFactorFenestration
    entrance_doors: TableMaximumUFactorFenestration
    skylights: TableMaximumUFactorFenestration

    @validator(
        "fixed_windows", "operable_windows", "entrance_doors", "skylights", pre=False
    )
    @classmethod
    def convert_units(cls, v: "TableFenestrationMaximumUFactors", values: Dict):
        return type(v).convert_units(v, **values)


class TableLightingLPDAreaMethod(BaseModel):
    name: str
    section: str
    units: str
    LPD: dict

    @validator("LPD", pre=False)
    @classmethod
    def convert_units(cls, v: Dict, values: Dict):
        units = values["units"]
        for key, val in v.items():
            v[key] = convert(val, units, "W/M2")
        return v


# -----------------------------------------------------------------------------


class SectionMaximumFenestrationArea(BaseModel):
    source_url: str
    name: str
    section: str
    maximum_skylight_percent_of_roof: float
    maximum_window_percent_of_wall: float


# -----------------------------------------------------------------------------


class BaselineCodeTables(BaseModel):
    maximum_u_factors: TableEnvelopeMaximumUFactors
    fenestration_u_factors: TableFenestrationMaximumUFactors
    lighting_area_method: TableLightingLPDAreaMethod


class BaselineCodeSections(BaseModel):
    maximum_fenestration_area: SectionMaximumFenestrationArea


class BaselineCode(BaseModel):
    """Pydantic BaselineCode model."""

    name: str
    state: str
    year: str
    source_url: str
    tables: BaselineCodeTables
    sections: BaselineCodeSections

    def get_window_shgcs(self) -> TableMaximumSHGC_ClimateZones:
        """Return the TableMaximumSHGC_ClimateZones with the window SHGC values.

        Returns:
            * TableMaximumSHGC_ClimateZones: The SHGC values for windows.
        """
        return self.tables.fenestration_u_factors.operable_windows.shgc

    def get_window_u_values(self) -> TableMaximumUFactor_ClimateZones:
        """Return the TableMaximumUFactor_ClimateZones with the window U-values.

        Returns:
            * TableMaximumUFactor_ClimateZones: The U-values for windows.
        """
        return self.tables.fenestration_u_factors.operable_windows.u_factors

    def get_roof_u_values(self) -> TableMaximumUFactor_ClimateZones:
        """Get the roof groups from the baseline code."""
        return self.tables.maximum_u_factors.roofs.insulation_above_deck

    def get_exposed_wall_u_values(self) -> TableMaximumUFactor_ClimateZones:
        """Get the exposed wall groups from the baseline code."""
        return self.tables.maximum_u_factors.walls.metal_framed

    def get_ground_wall_c_factors(self) -> TableMaximumCFactor_ClimateZones:
        """Get the ground wall groups from the baseline code."""
        return self.tables.maximum_u_factors.walls.below_grade

    def get_exposed_floor_u_values(self) -> TableMaximumUFactor_ClimateZones:
        """Get the exposed floor groups from the baseline code."""
        return self.tables.maximum_u_factors.floors.mass

    def get_ground_floor_f_factors(self) -> TableMaximumFFactor_ClimateZones:
        """Get the ground floor groups from the baseline code."""
        return self.tables.maximum_u_factors.floors.unheated_slab

    def get_baseline_max_wwr(self) -> float:
        """Get the maximum window-to-wall ratio from the baseline code."""
        return self.sections.maximum_fenestration_area.maximum_window_percent_of_wall

    def get_baseline_max_srr(self) -> float:
        """Get the maximum skylight-to-roof ratio from the baseline code."""
        return self.sections.maximum_fenestration_area.maximum_skylight_percent_of_roof

    def get_baseline_roof_u_value(self, _cz: ClimateZones, _ug: Use_Groups) -> float:
        """Get the maximum roof U-value from the baseline code for a climate/use-group."""
        all_roof_u_values = self.get_roof_u_values()
        cz_roof_u_values = all_roof_u_values.get_u_value_for_climate(_cz)
        roof_u_value = cz_roof_u_values.get_u_values_for_use_group(_ug)
        return roof_u_value

    def get_baseline_exposed_wall_u_value(
        self, _cz: ClimateZones, _ug: Use_Groups
    ) -> float:
        """Get the maximum exposed wall U-value from the baseline code for a climate/use-group."""
        all_exposed_wall_u_values = self.get_exposed_wall_u_values()
        cz_exposed_wall_u_values = all_exposed_wall_u_values.get_u_value_for_climate(
            _cz
        )
        exposed_wall_u_value = cz_exposed_wall_u_values.get_u_values_for_use_group(_ug)
        return exposed_wall_u_value

    def get_baseline_ground_wall_c_factor(
        self, _cz: ClimateZones, _ug: Use_Groups
    ) -> float:
        """Get the maximum ground wall C-Factor from the baseline code for a climate/use-group."""
        all_ground_wall_c_factors = self.get_ground_wall_c_factors()
        cz_ground_wall_c_factors = all_ground_wall_c_factors.get_c_factor_for_climate(
            _cz
        )
        ground_wall_c_factor = cz_ground_wall_c_factors.get_c_factor_for_use_group(_ug)
        return ground_wall_c_factor

    def get_baseline_exposed_floor_u_value(
        self, _cz: ClimateZones, _ug: Use_Groups
    ) -> float:
        """Get the maximum exposed floor U-value from the baseline code for a climate/use-group."""
        all_exposed_floor_u_values = self.get_exposed_floor_u_values()
        cz_exposed_floor_u_values = all_exposed_floor_u_values.get_u_value_for_climate(
            _cz
        )
        exposed_floor_u_value = cz_exposed_floor_u_values.get_u_values_for_use_group(
            _ug
        )
        return exposed_floor_u_value

    def get_baseline_ground_floor_f_factor(
        self, _cz: ClimateZones, _ug: Use_Groups
    ) -> float:
        """Get the maximum ground floor F-Factor from the baseline code for a climate/use-group."""
        all_ground_floor_f_factors = self.get_ground_floor_f_factors()
        cz_ground_floor_f_factors = all_ground_floor_f_factors.get_f_factor_for_climate(
            _cz
        )
        ground_floor_f_factor = cz_ground_floor_f_factors.get_f_factor_for_use_group(
            _ug
        )
        return ground_floor_f_factor
