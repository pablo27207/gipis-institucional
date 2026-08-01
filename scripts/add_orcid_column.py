"""
Migración: columna 'orcid' en members (integración ORCID).
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

    try:
        cursor.execute("ALTER TABLE members ADD COLUMN orcid VARCHAR(19)")
        print("  ✓ Columna 'orcid' agregada.")
    except sqlite3.OperationalError as e:
        if "duplicate column" in str(e).lower():
            print("  - Columna 'orcid' ya existe, saltando.")
        else:
            raise

    conn.commit()
    conn.close()
    print("Migración de ORCID completada.")


if __name__ == "__main__":
    migrate()
