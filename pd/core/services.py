#!/usr/bin/env python
# License: GPL v3 Copyright: 2026, Mateusz Jamróz
# pd/core/services.py

from pd.core.models import PD
from pd.core.repositories import PDRepository
from pd.core.statistics import PDStats, compute_stats
from pd.core.models import PDView

class PDService:
    def __init__(self, repo: PDRepository):
        self.repo = repo

    def get_model_name(self, model_id: str) -> str:
        models = self.repo.get_models()
        for mid, name in models:
            if mid == model_id:
                return name
        return "Unknown Model"
    
    def unit_info(self, pd_id: str) -> PD | None:
        return self.repo.get_unit_by_pd_id(pd_id)
    
    def update_unit(self, pd: PD) -> None:
        self.repo.update(pd)
    
    def get_models(self):
        return self.repo.get_models()
    
    def get_model_stats(self, model_id: str) -> PDStats | None:
        records = self.repo.get_wash1_2_spring_by_model(model_id)
        return compute_stats(records)

    def get_opening_pressures(self):
        return self.repo.get_opening_pressures()
    
    def get_opening_press_value(self, opening_pressure_id: int) -> float:
        return self.repo.get_opening_press_value(opening_pressure_id)
    
    def list_models(self) -> list[PD]:
        return self.repo.get_all()
    
    def delete_unit(self, pd_id: int) -> None:
        self.repo.delete(pd_id)
    
    def washers_distribution(self, model_id: str) -> tuple[list[float], list[float]]:
        return self.repo.get_washers_by_model(model_id)
    
    def count_model(self, model_id: str) -> int:
        return self.repo.count_by_model(model_id)
    
    def create_model(
        self,
        model_id: str,
        washer1_thickness: float,
        washer2_thickness: float,
        spring_length: float,
        final_pressure: float,
        opening_pressure_id: int
    ) -> None:
        pd = PD(
            id=None,  # id zostanie nadane przez bazę
            model_id=model_id,
            washer1_thickness=washer1_thickness,
            washer2_thickness=washer2_thickness,
            spring_length=spring_length,
            final_pressure=final_pressure,
            opening_pressure_id=opening_pressure_id
        )
        if not all([
            model_id,
            washer1_thickness,
            washer2_thickness,
            spring_length,
            final_pressure,
            opening_pressure_id
        ]):
            raise ValueError("Wszystkie pola muszą być wypełnione.")
        self.repo.add(pd)

    def add_new(
        self,
        model_id: str,
        washer1: float,
        washer2: float,
        spring_length: float,
        final_pressure: float,
        opening_pressure: int,
    ):
        if not model_id:
            raise ValueError("Model ID is required.")
        
        self.repo.insert(
            model_id,
            washer1,
            washer2,
            spring_length,
            final_pressure,
            opening_pressure
        )

    def add_model(self, model_name: str) -> None:
        if not model_name:
            raise ValueError("Model name cannot be empty.")
        self.repo.insert_model(model_name)
    
    def list_models_with_name(self) -> list[PDView]:
        return self.repo.get_all_with_name()