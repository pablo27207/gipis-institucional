"""
Migración: columna 'content_en' en site_content + traducción de la misión.

La traducción solo se aplica si el texto en español es el original (se
verifica una huella) y todavía no hay traducción cargada.
"""
import sqlite3
import os

DB_PATH = os.environ.get('DATABASE_PATH', 'instance/gipis.db')

MISSION_EN = (
    "<p>This group seeks to strengthen the links between the scientific-"
    "technological system and the productive sector in the fields of "
    "informatics and telecommunications, in order to face the new challenges "
    "posed by digital transformation and thereby generate a positive impact "
    "on the activities of the San Jorge Gulf Basin.</p>"
    "<p>Its research lines focus on the digital signal processing used by "
    "sensor systems deployed in smart spaces, power grids and underwater "
    "environments to perceive the state of the surroundings and the entities "
    "they interact with.</p>"
    "<p>In the case of power grids, research focuses on signal processing for "
    "power line communication (PLC) systems, particularly frame "
    "synchronization and channel estimation techniques for orthogonal "
    "frequency-division multiplexing (OFDM) modulation schemes. This line "
    "also includes the design of pilot symbols that reduce computational "
    "complexity compared to current synchronization and estimation "
    "schemes.</p>"
    "<p>In the case of smart spaces and shallow underwater acoustic "
    "environments, research centers on the processing of coded acoustic "
    "signals. Efforts focus on designing coding schemes that provide "
    "robustness against noise, allow multiple users to coexist in the same "
    "environment, and increase the precision in determining signal arrival "
    "times. Such systems are used in underwater sensor networks for coastal "
    "monitoring, as well as by autonomous underwater vehicles (AUVs).</p>"
    "<p>Another research line is oriented toward developing solutions based "
    "on ICT tools (hardware and software) for oceanographic monitoring and "
    "the analysis of data obtained through different sensor systems, "
    "oceanographic campaigns and coastal surveys.</p>"
    "<p>In addition, the group's activities include the evaluation and "
    "implementation on programmable devices, such as FPGAs, of new "
    "state-of-the-art multicarrier modulation transceiver filter banks for "
    "PLC systems, as well as the aforementioned algorithms for the OFDM "
    "scheme with acoustic signals.</p>"
)


def migrate():
    if not os.path.exists(DB_PATH):
        print(f"Base de datos no encontrada en {DB_PATH}. Nada que migrar.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("ALTER TABLE site_content ADD COLUMN content_en TEXT")
        print("  ✓ Columna 'content_en' agregada a site_content.")
    except sqlite3.OperationalError as e:
        if "duplicate column" in str(e).lower():
            print("  - Columna 'content_en' ya existe, saltando.")
        else:
            raise

    cursor.execute(
        "UPDATE site_content SET content_en = ? "
        "WHERE key = 'mission' AND content_en IS NULL "
        "AND content LIKE '%fortalecer la vinculación%'",
        (MISSION_EN,))
    if cursor.rowcount:
        print("  ✓ Traducción de la misión cargada.")
    else:
        print("  - Misión sin cambios (ya traducida o texto modificado).")

    conn.commit()
    conn.close()
    print("Migración de contenido del sitio en inglés completada.")


if __name__ == "__main__":
    migrate()
