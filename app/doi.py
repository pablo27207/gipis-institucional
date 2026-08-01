"""
Resolución de metadatos por DOI vía doi.org con content negotiation
(formato CSL JSON; cubre Crossref, DataCite y otros registradores).
"""
import json
import re
import urllib.request
import urllib.parse
import urllib.error

TIMEOUT = 15

DOI_RE = re.compile(r'(10\.\d{4,9}/[^\s"<>]+)', re.IGNORECASE)


class DoiError(Exception):
    """Error recuperable al resolver un DOI (mensaje apto para mostrar)."""


def normalize_doi(raw):
    """Extraer el DOI desde texto libre (URL de doi.org, 'doi:...' o suelto)."""
    if not raw:
        return None
    match = DOI_RE.search(raw.strip())
    return match.group(1).rstrip('.,;') if match else None


def fetch_bibtex(doi):
    """Traer la cita BibTeX de un DOI (content negotiation en doi.org)."""
    url = f'https://doi.org/{urllib.parse.quote(doi, safe="/")}'
    req = urllib.request.Request(url, headers={
        'Accept': 'application/x-bibtex',
        'User-Agent': 'GIPIS-institucional/1.0 (gipis.unp.edu.ar)',
    })
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return resp.read().decode('utf-8').strip()
    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise DoiError('No se encontró ese DOI.')
        raise DoiError(f'El servicio de DOI respondió con un error (HTTP {e.code}).')
    except urllib.error.URLError:
        raise DoiError('No se pudo consultar el DOI.')


def fetch_doi(doi):
    """Traer metadatos de un DOI ya normalizado.

    Devuelve {'title', 'authors', 'year', 'detail'} (todos str o None).
    """
    url = f'https://doi.org/{urllib.parse.quote(doi, safe="/")}'
    req = urllib.request.Request(url, headers={
        'Accept': 'application/vnd.citationstyles.csl+json',
        'User-Agent': 'GIPIS-institucional/1.0 (gipis.unp.edu.ar)',
    })
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            data = json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise DoiError('No se encontró ese DOI. Revisá que esté bien escrito.')
        raise DoiError(f'El servicio de DOI respondió con un error (HTTP {e.code}). '
                       'Probá de nuevo en unos minutos.')
    except (urllib.error.URLError, ValueError):
        raise DoiError('No se pudo consultar el DOI. Revisá la conexión '
                       'e intentá de nuevo.')

    title = data.get('title')
    if isinstance(title, list):
        title = title[0] if title else None

    authors = []
    for a in data.get('author') or []:
        given, family = a.get('given'), a.get('family')
        if family and given:
            authors.append(f'{family}, {given}')
        elif family or given or a.get('name'):
            authors.append(a.get('name') or family or given)

    year = None
    for key in ('issued', 'published-print', 'published-online', 'created'):
        parts = ((data.get(key) or {}).get('date-parts') or [[None]])[0]
        if parts and parts[0]:
            year = str(parts[0])
            break

    detail_parts = []
    container = data.get('container-title')
    if isinstance(container, list):
        container = container[0] if container else None
    if container:
        detail_parts.append(container)
    detail_parts.append(f'https://doi.org/{doi}')

    return {
        'title': title,
        'authors': '; '.join(authors) or None,
        'year': year,
        'detail': ' · '.join(detail_parts),
    }
