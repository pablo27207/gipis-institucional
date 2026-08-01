"""
Migración: columnas de traducción opcional al inglés (novedades y biografías).
"""
import sqlite3
import os

DB_PATH = os.environ.get('DATABASE_PATH', 'instance/gipis.db')

COLUMNS = [
    ('news', "ALTER TABLE news ADD COLUMN title_en VARCHAR(300)", 'title_en'),
    ('news', "ALTER TABLE news ADD COLUMN excerpt_en VARCHAR(500)", 'excerpt_en'),
    ('news', "ALTER TABLE news ADD COLUMN content_en TEXT", 'content_en'),
    ('members', "ALTER TABLE members ADD COLUMN bio_en TEXT", 'bio_en'),
]


def migrate():
    if not os.path.exists(DB_PATH):
        print(f"Base de datos no encontrada en {DB_PATH}. Nada que migrar.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for table, sql, column in COLUMNS:
        try:
            cursor.execute(sql)
            print(f"  ✓ Columna '{column}' agregada a {table}.")
        except sqlite3.OperationalError as e:
            if "duplicate column" in str(e).lower():
                print(f"  - Columna '{column}' ya existe en {table}, saltando.")
            else:
                raise

    conn.commit()
    conn.close()
    print("Migración de columnas de traducción completada.")


if __name__ == "__main__":
    migrate()
