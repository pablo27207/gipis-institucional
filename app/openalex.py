"""
Cliente de la API de OpenAlex (api.openalex.org, abierta y sin clave).

Se usa para descubrir publicaciones de un miembro a partir de su ORCID iD
(OpenAlex indexa trabajos aunque el autor no los haya cargado en ORCID).
Devuelve ítems con la misma forma que app/orcid.py para compartir la
pantalla de revisión e importación.
"""
import json
import urllib.request
import urllib.parse
import urllib.error

API_BASE = 'https://api.openalex.org'
TIMEOUT = 20
PER_PAGE = 100  # máximo aceptado por la API
MAX_PAGES = 5   # tope de seguridad (500 trabajos)

TYPE_LABELS = {
    'article': 'Artículos',
    'book': 'Libros y capítulos',
    'book-chapter': 'Libros y capítulos',
    'dissertation': 'Tesis',
    'preprint': 'Preprints',
    'dataset': 'Conjuntos de datos',
    'report': 'Informes técnicos',
}


class OpenAlexError(Exception):
    """Error recuperable al consultar OpenAlex (mensaje apto para mostrar)."""


def _get_json(path_and_query):
    url = f'{API_BASE}/{path_and_query}'
    req = urllib.request.Request(url, headers={
        'Accept': 'application/json',
        'User-Agent': 'GIPIS-institucional/1.0 (gipis.unp.edu.ar)',
    })
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise OpenAlexError('OpenAlex no tiene registros para ese ORCID iD.')
        raise OpenAlexError(f'OpenAlex respondió con un error (HTTP {e.code}). '
                            'Probá de nuevo en unos minutos.')
    except urllib.error.URLError:
        raise OpenAlexError('No se pudo conectar con OpenAlex. '
                            'Revisá la conexión e intentá de nuevo.')


def _work_to_item(work):
    title = (work.get('title') or '').strip()
    if not title:
        return None

    authors = '; '.join(
        name for name in (
            (a.get('author') or {}).get('display_name')
            for a in work.get('authorships') or []
        ) if name
    )

    detail_parts = []
    venue = ((work.get('primary_location') or {}).get('source') or {}).get('display_name')
    if venue:
        detail_parts.append(venue)
    doi = work.get('doi')  # viene como https://doi.org/...
    if doi:
        detail_parts.append(doi)

    year = work.get('publication_year')
    work_type = work.get('type') or 'article'

    return {
        'kind': 'thesis' if work_type == 'dissertation' else 'publication',
        'title': title[:500],
        'authors': authors[:500] or None,
        'year': str(year) if year else None,
        'detail': ' · '.join(detail_parts) or None,
        'group': TYPE_LABELS.get(work_type, 'Otros trabajos'),
        'citations': work.get('cited_by_count') or 0,
    }


def fetch_openalex_works(orcid_id):
    """Traer los trabajos indexados por OpenAlex para un ORCID iD.

    Devuelve {'items': [dict, ...]} ordenados por citas (desc).
    """
    items = []
    for page in range(1, MAX_PAGES + 1):
        query = urllib.parse.urlencode({
            'filter': f'author.orcid:{orcid_id}',
            'per-page': PER_PAGE,
            'page': page,
            'select': 'title,authorships,publication_year,type,doi,'
                      'primary_location,cited_by_count',
        })
        data = _get_json(f'works?{query}')
        results = data.get('results') or []
        for work in results:
            item = _work_to_item(work)
            if item:
                items.append(item)
        if len(results) < PER_PAGE:
            break

    items.sort(key=lambda i: -i['citations'])
    return {'items': items}


def fetch_citations_by_doi(dois):
    """Conteo de citas para una lista de DOIs (formato 10.xxxx/...).

    Devuelve {doi_lower: cited_by_count}. Errores → dict vacío (best effort).
    """
    counts = {}
    try:
        for start in range(0, len(dois), 50):
            chunk = dois[start:start + 50]
            query = urllib.parse.urlencode({
                'filter': 'doi:' + '|'.join(chunk),
                'per-page': 50,
                'select': 'doi,cited_by_count',
            })
            data = _get_json(f'works?{query}')
            for work in data.get('results') or []:
                doi = (work.get('doi') or '').replace('https://doi.org/', '').lower()
                if doi:
                    counts[doi] = work.get('cited_by_count') or 0
    except OpenAlexError:
        pass
    return counts
