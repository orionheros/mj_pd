
CREATE TABLE IF NOT EXISTS pd_models (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS pd_opening_pressure (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    value INT NOT NULL
);

CREATE TABLE IF NOT EXISTS pd (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_id INTEGER NOT NULL,
    washer1_thickness REAL NOT NULL,
    washer2_thickness REAL NOT NULL,
    spring_length REAL NOT NULL,
    final_pressure REAL NOT NULL,
    opening_pressure_id INTEGER NOT NULL,
    FOREIGN KEY (model_id) REFERENCES pd_models(id) ON DELETE CASCADE,
    FOREIGN KEY (opening_pressure_id) REFERENCES pd_opening_pressure(id) ON DELETE CASCADE
);