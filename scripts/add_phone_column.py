"""
Migración: agregar columnas de teléfono al modelo Member.
"""
import sqlite3
import os

DB_PATH = os.environ.get('DATABASE_PATH', 'instance/gipis.db')

def migrate():
    if not os.path.exists(DB_PATH):
        print(f"Base de datos no encontrada en {DB_PATH}. Nada que migrar.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    columns_to_add = [
        ("phone", "VARCHAR(50)"),
        ("phone_public", "BOOLEAN DEFAULT 0"),
    ]

    for col_name, col_type in columns_to_add:
        try:
            cursor.execute(f"ALTER TABLE members ADD COLUMN {col_name} {col_type}")
            print(f"  ✓ Columna '{col_name}' agregada.")
        except sqlite3.OperationalError as e:
            if "duplicate column" in str(e).lower():
                print(f"  - Columna '{col_name}' ya existe, saltando.")
            else:
                raise

    conn.commit()
    conn.close()
    print("Migración de teléfono completada.")

if __name__ == "__main__":
    migrate()
