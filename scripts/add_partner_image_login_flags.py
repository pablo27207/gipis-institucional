"""
Migración: logo en partners (columna image) y flags de email habilitado
para login en members.
"""
import sqlite3
import os

DB_PATH = os.environ.get('DATABASE_PATH', 'instance/gipis.db')

COLUMNS = [
    ('partners', "ALTER TABLE partners ADD COLUMN image VARCHAR(255)", 'image'),
    ('members', "ALTER TABLE members ADD COLUMN personal_email_login BOOLEAN DEFAULT 0",
     'personal_email_login'),
    ('members', "ALTER TABLE members ADD COLUMN institutional_email_login BOOLEAN DEFAULT 0",
     'institutional_email_login'),
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
    print("Migración de logos de partners y emails de login completada.")


if __name__ == "__main__":
    migrate()
