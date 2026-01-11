#!/usr/bin/env python
# License: GPL v3 Copyright: 2026, Mateusz Jamróz
# pd/core/repositories.py

import sqlite3
from dataclasses import dataclass
from pd.core.models import PD, PDView

# washer1 = lower washer
# washer2 = upper washer

@dataclass(frozen=True)
class PDRecord:
    washer1: float
    spring: float
    washer2: float


class PDRepository:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def get_models(self):
        """
        Only models of pump units, like 0414720215, without duplicates
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, model_name FROM pd_models")
        return cursor.fetchall()
    
    def get_unit_by_pd_id(self, pd_id: str) -> PD | None:
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id, model_id, washer1_thickness, washer2_thickness, spring_length, final_pressure, opening_pressure_id FROM pd WHERE id = ?",
            (pd_id,)
        )
        row = cursor.fetchone()
        if row:
            return PD(*row)
        return None
    
    def update(self, pd: PD) -> None:
        self.conn.execute(
            """
            UPDATE pd
            SET model_id = ?,
                washer1_thickness = ?,
                washer2_thickness = ?,
                spring_length = ?,
                final_pressure = ?,
                opening_pressure_id = ?
            WHERE id = ?
            """,
            (
                pd.model_id,
                pd.washer1_thickness,
                pd.washer2_thickness,
                pd.spring_length,
                pd.final_pressure,
                pd.opening_pressure_id,
                pd.id
            )
        )
        self.conn.commit()
    
    def count_by_model(self, model_id: str) -> int:
        """
        Count number of pump units for a given model_id
        """
        cur = self.conn.cursor()
        cur.execute(
            "SELECT COUNT(*) FROM pd WHERE model_id = ?",
            (model_id,)
        )
        return cur.fetchone()[0]

    def get_opening_pressures(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, value FROM pd_opening_pressure")
        return cursor.fetchall()
    
    def get_opening_press_value(self, opening_pressure_id: int) -> float:
        cursor = self.conn.cursor()
        cursor.execute("SELECT value FROM pd_opening_pressure WHERE id = ?", (opening_pressure_id,))
        row = cursor.fetchone()
        return row[0] if row else None
    
    def get_wash1_2_spring_by_model(self, model_id: str) -> list[PDRecord]:
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT washer1_thickness, spring_length, washer2_thickness
            FROM pd
            WHERE model_id = ?
            """,
            (model_id,)
        )

        return [
            PDRecord(
                washer1=row[0],
                spring=row[1],
                washer2=row[2]
            )
            for row in cur.fetchall()
        ]
    
    def get_washers_by_model(self, model_id: str) -> tuple[list[float], list[float]]:
        cur = self.conn.cursor()
        cur.execute(
            "SELECT washer1_thickness, washer2_thickness FROM pd WHERE model_id = ?",
            (model_id,)
        )
        lower = []
        upper = []
        for row in cur.fetchall():
            lower.append(row[0])
            upper.append(row[1])
        return lower, upper
        
    def get_all(self) -> list[PD]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, model_id, washer1_thickness, washer2_thickness, spring_length, final_pressure, opening_pressure_id FROM pd")
        rows = cursor.fetchall()
        return [PD(*row) for row in rows]

    def get_all_with_name(self) -> list[PDView]:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT pd.id, pd.model_id, m.model_name, op.value, pd.washer1_thickness, pd.washer2_thickness, pd.spring_length, pd.final_pressure
            FROM pd
            LEFT JOIN pd_models m ON pd.model_id = m.id
            LEFT JOIN pd_opening_pressure op ON pd.opening_pressure_id = op.id
            """
        )
        rows = cursor.fetchall()
        return [PDView(*row) for row in rows]
    
    def add(self, pd: PD) -> None:
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO pd (model_id, washer1_thickness, washer2_thickness, spring_length, final_pressure, opening_pressure_id) VALUES (?, ?, ?, ?, ?, ?)",
            (
                pd.model_id,
                pd.washer1_thickness,
                pd.washer2_thickness,
                pd.spring_length,
                pd.final_pressure,
                pd.opening_pressure_id
            )
        )
        self.conn.commit()

    def insert(
        self,
        model_id,
        washer1,
        washer2,
        spring_length,
        final_pressure,
        opening_pressure
    ):
        self.conn.execute(
            """
            INSERT INTO pd (
                model_id,
                washer1_thickness,
                washer2_thickness,
                spring_length,
                final_pressure,
                opening_pressure_id
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                model_id,
                washer1,
                washer2,
                spring_length,
                final_pressure,
                opening_pressure
            )
        )
        self.conn.commit()

    def insert_model(self, model_name: str) -> None:
        self.conn.execute(
            "INSERT INTO pd_models (model_name) VALUES (?)",
            (model_name,)
        )
        self.conn.commit()

    def delete(self, pd_id: int) -> None:
        self.conn.execute(
            "DELETE FROM pd WHERE id = ?",
            (pd_id,)
        )
        self.conn.commit()