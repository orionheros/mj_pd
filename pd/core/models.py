#!/usr/bin/env python
# License: GPL v3 Copyright: 2026, Mateusz Jamróz
# pd/core/models.py

from dataclasses import dataclass

@dataclass
class PD:
    id: int
    model_id: str
    washer1_thickness: float
    washer2_thickness: float
    spring_length: float
    final_pressure: float
    opening_pressure_id: float

@dataclass
class PDView:
    id: int
    model_id: str
    model_name: str
    opening_pressure: float
    washer1: float
    washer2: float
    spring_length: float
    final_pressure: float

@dataclass
class PDModel:
    id: int
    model_name: str

@dataclass
class PDOpeningPressure:
    id: int
    value: int