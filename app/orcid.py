"""
Cliente de la API pública de ORCID (pub.orcid.org, sin autenticación).

Se usa para importar la producción de un miembro a partir de su ORCID iD.
Flujo: fetch_orcid_works() devuelve una lista de dicts con la misma forma
que produce el parser de SIGEVA (kind, title, authors, year, detail, group),
así la pantalla de revisión e importación comparten el mismo patrón.
"""
import json
import re
import urllib.request
import urllib.error

API_BASE = 'https://pub.orcid.org/v3.0'
TIMEOUT = 20
BULK_CHUNK = 50  # la API acepta hasta 100 put-codes por pedido

ORCID_RE = re.compile(r'(\d{4})-?(\d{4})-?(\d{4})-?(\d{3}[\dXx])')

# Tipos de trabajo de ORCID → etiqueta legible para agrupar en la revisión
TYPE_LABELS = {
    'journal-article': 'Artículos en revistas',
    'conference-paper': 'Trabajos en congresos',
    'conference-abstract': 'Trabajos en congresos',
    'conference-poster': 'Trabajos en congresos',
    'book': 'Libros y capítulos',
    'book-chapter': 'Libros y capítulos',
    'edited-book': 'Libros y capítulos',
    'dissertation-thesis': 'Tesis',
    'supervised-student-publication': 'Direcciones de estudiantes',
    'report': 'Informes técnicos',
    'working-paper': 'Documentos de trabajo',
    'preprint': 'Preprints',
    'software': 'Software',
    'data-set': 'Conjuntos de datos',
}

# Tipos que se importan como 'thesis' en MemberWork; el resto como 'publication'
THESIS_TYPES = {'dissertation-thesis', 'supervised-student-publication'}


class OrcidError(Exception):
    """Error recuperable al consultar ORCID (mensaje apto para mostrar)."""


def normalize_orcid_id(raw):
    """Extraer y validar un ORCID iD desde texto libre (URL o iD suelto).

    Devuelve el iD canónico 0000-0000-0000-0000 o None si no es válido.
    """
    if not raw:
        return None
    match = ORCID_RE.search(raw.strip())
    if not match:
        return None
    digits = ''.join(match.groups()).upper()
    if not _valid_checksum(digits):
        return None
    return '-'.join([digits[0:4], digits[4:8], digits[8:12], digits[12:16]])


def _valid_checksum(digits16):
    """Dígito verificador ORCID (ISO 7064 11,2): último carácter."""
    total = 0
    for ch in digits16[:-1]:
        total = (total + int(ch)) * 2
    result = (12 - total % 11) % 11
    expected = 'X' if result == 10 else str(result)
    return digits16[-1] == expected


def _get_json(path):
    url = f'{API_BASE}/{path}'
    req = urllib.request.Request(url, headers={
        'Accept': 'application/json',
        'User-Agent': 'GIPIS-institucional/1.0 (gipis.unp.edu.ar)',
    })
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise OrcidError('No existe un registro ORCID con ese iD.')
        raise OrcidError(f'ORCID respondió con un error (HTTP {e.code}). '
                         'Probá de nuevo en unos minutos.')
    except urllib.error.URLError:
        raise OrcidError('No se pudo conectar con ORCID. '
                         'Revisá la conexión e intentá de nuevo.')


def _value(node, *keys):
    """Navegar dicts anidados de la API tolerando None en el camino."""
    for key in keys:
        if not isinstance(node, dict):
            return None
        node = node.get(key)
    return node


def _work_to_item(work):
    title = _value(work, 'title', 'title', 'value')
    if not title:
        return None

    work_type = work.get('type') or 'other'
    year = _value(work, 'publication-date', 'year', 'value')

    contributors = _value(work, 'contributors', 'contributor') or []
    names = [_value(c, 'credit-name', 'value') for c in contributors]
    authors = '; '.join(n for n in names if n)

    detail_parts = []
    journal = _value(work, 'journal-title', 'value')
    if journal:
        detail_parts.append(journal)
    doi = None
    for ext in _value(work, 'external-ids', 'external-id') or []:
        if ext.get('external-id-type') == 'doi':
            doi = _value(ext, 'external-id-url', 'value') or \
                f"https://doi.org/{ext.get('external-id-value')}"
            break
    url = doi or _value(work, 'url', 'value')
    if url:
        detail_parts.append(url)

    return {
        'kind': 'thesis' if work_type in THESIS_TYPES else 'publication',
        'title': title.strip(),
        'authors': authors or None,
        'year': str(year) if year else None,
        'detail': ' · '.join(detail_parts) or None,
        'group': TYPE_LABELS.get(work_type, 'Otros trabajos'),
    }


def fetch_orcid_works(orcid_id):
    """Traer los trabajos públicos de un ORCID iD ya normalizado.

    Devuelve {'name': str|None, 'items': [dict, ...]}.
    """
    data = _get_json(f'{orcid_id}/works')

    put_codes = []
    for group in data.get('group') or []:
        summaries = group.get('work-summary') or []
        if summaries:
            put_codes.append(str(summaries[0].get('put-code')))

    items = []
    for start in range(0, len(put_codes), BULK_CHUNK):
        chunk = put_codes[start:start + BULK_CHUNK]
        bulk = _get_json(f'{orcid_id}/works/{",".join(chunk)}')
        for entry in bulk.get('bulk') or []:
            item = _work_to_item(entry.get('work') or {})
            if item:
                items.append(item)

    name = None
    try:
        person = _get_json(f'{orcid_id}/personal-details')
        given = _value(person, 'name', 'given-names', 'value') or ''
        family = _value(person, 'name', 'family-name', 'value') or ''
        name = f'{given} {family}'.strip() or None
    except OrcidError:
        pass  # el nombre es solo informativo

    return {'name': name, 'items': items}
