"""
Migración: agregar columnas de email personal/institucional al modelo Member.
Ejecutar una sola vez si la base de datos ya existe.
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
        ("personal_email", "VARCHAR(150)"),
        ("personal_email_public", "BOOLEAN DEFAULT 0"),
        ("institutional_email", "VARCHAR(150)"),
        ("institutional_email_public", "BOOLEAN DEFAULT 0"),
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
    print("Migración completada.")

if __name__ == "__main__":
    migrate()
