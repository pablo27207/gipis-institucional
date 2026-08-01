"""
Migración: columna 'source' en news (origen de la novedad: manual o red social).
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
        cursor.execute("ALTER TABLE news ADD COLUMN source VARCHAR(20) DEFAULT 'manual'")
        print("  ✓ Columna 'source' agregada a news.")
    except sqlite3.OperationalError as e:
        if "duplicate column" in str(e).lower():
            print("  - Columna 'source' ya existe en news, saltando.")
        else:
            raise

    conn.commit()
    conn.close()
    print("Migración de origen de novedades completada.")


if __name__ == "__main__":
    migrate()
