"""
Migración: rol de usuario, producción personal (member_works) y
red de colaboración (partners).
"""
import sqlite3
import os

DB_PATH = os.environ.get('DATABASE_PATH', 'instance/gipis.db')

# Organizaciones que estaban hardcodeadas en cooperacion.xhtml
INITIAL_PARTNERS = [
    ('Universidad de Alcalá', 1),
    ('CONICET', 2),
    ('CIT Golfo San Jorge', 3),
    ('ANPCyT', 4),
]


def migrate():
    if not os.path.exists(DB_PATH):
        print(f"Base de datos no encontrada en {DB_PATH}. Nada que migrar.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("ALTER TABLE members ADD COLUMN role VARCHAR(20) DEFAULT 'member'")
        print("  ✓ Columna 'role' agregada.")
    except sqlite3.OperationalError as e:
        if "duplicate column" in str(e).lower():
            print("  - Columna 'role' ya existe, saltando.")
        else:
            raise

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS member_works (
            id INTEGER PRIMARY KEY,
            member_id INTEGER NOT NULL REFERENCES members(id),
            kind VARCHAR(30) NOT NULL DEFAULT 'publication',
            title VARCHAR(500) NOT NULL,
            authors VARCHAR(500),
            year VARCHAR(10),
            detail TEXT,
            source VARCHAR(20) DEFAULT 'manual',
            shared_item_id INTEGER REFERENCES research_items(id)
        )
    """)
    print("  ✓ Tabla 'member_works' verificada.")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS partners (
            id INTEGER PRIMARY KEY,
            name VARCHAR(200) NOT NULL,
            url VARCHAR(255),
            "order" INTEGER DEFAULT 0
        )
    """)
    print("  ✓ Tabla 'partners' verificada.")

    cursor.execute("SELECT COUNT(*) FROM partners")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            'INSERT INTO partners (name, "order") VALUES (?, ?)', INITIAL_PARTNERS
        )
        print(f"  ✓ {len(INITIAL_PARTNERS)} partners iniciales cargados.")

    conn.commit()
    conn.close()
    print("Migración de roles/producción/partners completada.")


if __name__ == "__main__":
    migrate()
