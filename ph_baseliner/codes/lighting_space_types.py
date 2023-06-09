# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Equivalence map between PHPP-space-type-names and Code-space-type-names."""

# -- TABLE C405.3.2(1) INTERIOR LIGHTING POWER ALLOWANCES: BUILDING AREA METHOD
# -- PHPP-Space-Type-Name : Code-Space-Type-Name
space_type_map = {
    "Single office": "Office",
    "Group office": "Office",
    "Open-plan office": "Office",
    "Meeting": "Office",
    "Counter area": "Retail",
    "Retail": "Retail",
    "Retail/department store with refrigerated products": "Retail",
    "Classroom": "School/University",
    "University auditorium": "School/University",
    "Bedroom": "Dormitory",
    "Hotel room": "Hotel/Motel",
    "Canteen": "Dining: cafeteria/fast food",
    "Restaurant": "Dining: family",
    "Kitchen in non-residential building": "Dining: family",
    "Kitchen, Storage, Preparation": "Dining: family",
    "WC, Sanitary": "Office",
    "Other habitable rooms": "Office",
    "Secondary areas": "Office",
    "Circulation area": "Office",
    "Storage, Services": "Office",
    "Server room": "Office",
    "Workshop (standing activity)": "Workshop",
    "Workshop (predominantly standing activity)": "Workshop",
    "Workshop (predominantly sedentary activity)": "Workshop",
    "Theatre auditorium": "Performing arts theater",
    "Theatre foyer": "Performing arts theater",
    "Theatre stage": "Performing arts theater",
    "Fair, Congress": "Courthouse",
    "Exhibition": "Museum",
    "Library reading room": "Library",
    "Open access library": "Library",
    "Library repository":"Library",
    "Sports hall": "Sports arena",
    "Parking garage": "Parking garage",
    "Public parking garage": "Parking garage",
    "Sauna area": "Exercise center",
    "Exercise room": "Exercise center",
    "Laboratory": "Health care clinic",
    "Examination/treatment rooms": "Health care clinic",
    "Special care areas": "Health care clinic",
    "Corridors of the general care area": "Health care clinic",
    "Medical/therapeutic practices": "Health care clinic",
    "Warehouses": "Warehouse",
}
