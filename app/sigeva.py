"""
Parser de CVs exportados de SIGEVA (PDF).

Extrae publicaciones, proyectos, tesistas/becarios dirigidos y datos de
perfil. El resultado se muestra en una pantalla de revisión donde el
usuario elige qué importar, así que el parseo prioriza no perder entradas
por sobre la precisión perfecta de cada campo.
"""
import html
import re
from pypdf import PdfReader

# Subsecciones del PDF de SIGEVA que nos interesan
PUBLICATION_HEADERS = [
    'PUBLICACIONES - Artículos publicados en revistas:',
    'PUBLICACIONES - Trabajos en eventos c-t publicados:',
    'PUBLICACIONES - Libros:',
    'PUBLICACIONES - Capítulos de libros:',
]
PROJECT_HEADER = 'FINANCIAMIENTO CYT - Proyectos I+D:'
RRHH_HEADERS = {
    'FORMACION DE RRHH EN CYT - Becarios:': ('Beca', 'Becarios dirigidos'),
    'FORMACION DE RRHH EN CYT - Tesistas:': ('Tesis', 'Tesistas dirigidos'),
}

YEAR_RE = re.compile(r'\b(?:19|20)\d{2}\b')

# Autores estilo SIGEVA: "APELLIDO, NOMBRE; PEREZ, JUAN; ... ROSALES, PABLO."
# Requiere al menos un ';' para no confundirse con títulos en mayúsculas.
_AUTHOR_TOKEN = r"[A-ZÁÉÍÓÚÑÜ][A-ZÁÉÍÓÚÑÜa-záéíóúñü.,'\- ]{1,70}?"
AUTHOR_RUN = re.compile(
    rf"(?:{_AUTHOR_TOKEN}\s*;\s*)+{_AUTHOR_TOKEN}\s*\.")


def extract_text(pdf_file):
    """Texto completo del PDF sin encabezados/pies de página repetidos."""
    reader = PdfReader(pdf_file)
    lines = []
    for page in reader.pages:
        # El modo layout preserva la relación etiqueta→valor de los
        # formularios en dos columnas de SIGEVA.
        text = page.extract_text(extraction_mode='layout') or ''
        for line in text.splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith('CONSEJO NACIONAL DE INVESTIGACIONES'):
                continue
            if stripped.startswith(('Curriculum vitae', 'Currículum vitae')):
                continue
            if stripped.startswith('Fecha de impresión:'):
                continue
            if re.match(r'^Página \d+ de \d+$', stripped):
                continue
            lines.append(stripped)
    return '\n'.join(lines)


def _header_re(header):
    """Regex tolerante a espacios múltiples del modo layout."""
    return re.compile(r'\s+'.join(re.escape(w) for w in header.split()))


def _is_section_break(line):
    """¿La línea es el encabezado de otra (sub)sección?
    Encabezados: 'SECCION EN MAYUSCULAS - Detalle:' (a veces sin ':' final
    si el título sigue en la línea siguiente) o 'SERVICIOS:' a secas.
    Las instituciones en mayúsculas no llevan ':' final ni ' - '."""
    stripped = line.strip()
    if ';' in stripped:
        # Filas de tablas de instituciones ('FAC. INGENIERIA - SEDE X ; ...')
        return False
    if ' - ' in stripped:
        head, tail = stripped.split(' - ', 1)
        # En un encabezado real el detalle va en minúsculas ('- Becarios:');
        # las instituciones siguen en mayúsculas ('- SEDE COMODORO').
        if not any(c.islower() for c in tail):
            return False
    elif stripped.endswith(':'):
        head = stripped[:-1]
    else:
        return False
    head = head.strip()
    if not head or not any(c.isalpha() for c in head):
        return False
    return head.upper() == head


def _section_body(text, header):
    """Contenido entre un encabezado y el siguiente encabezado de subsección."""
    match = _header_re(header).search(text)
    if not match:
        return ''
    body_lines = []
    for line in text[match.end():].splitlines():
        if _is_section_break(line):
            break
        body_lines.append(line)
    return '\n'.join(body_lines).strip()


def _owner_line(text):
    """Línea 'APELLIDO, NOMBRE' del dueño del CV (se repite en cada página)."""
    match = re.search(r'^([A-ZÁÉÍÓÚÑÜ ]+,\s*[A-ZÁÉÍÓÚÑÜ ]+)$', text, re.MULTILINE)
    return match.group(1).strip() if match else None


def _strip_owner_name(text, owner_line):
    if not owner_line:
        return text
    return '\n'.join(
        line for line in text.splitlines() if line.strip() != owner_line
    )


# ==========================================
# Publicaciones
# ==========================================

def parse_publications(text):
    results = []
    for header in PUBLICATION_HEADERS:
        body = _section_body(text, header)
        if not body:
            continue
        flowing = html.unescape(' '.join(body.split()))
        for entry in _split_entries(flowing):
            parsed = _parse_citation(entry)
            if parsed:
                parsed['kind'] = 'publication'
                parsed['group'] = header.split(' - ')[1].rstrip(':')
                results.append(parsed)
    return results


def _upper_word(word):
    letters = [c for c in word if c.isalpha()]
    if len(letters) <= 1 or not all(c.isupper() for c in letters):
        return False
    # Excluir numeración romana (XII Jornadas, XX Coloquio, etc.)
    return not all(c in 'IVXLCDM' for c in letters)


def _mostly_upper(run):
    letters = [c for c in run if c.isalpha()]
    return bool(letters) and sum(c.isupper() for c in letters) / len(letters) > 0.8


def _split_entries(flowing):
    """Cada entrada empieza con una corrida de autores 'X; Y; Z.'"""
    starts = []
    for m in AUTHOR_RUN.finditer(flowing):
        # El regex puede arrastrar el final de la entrada anterior
        # (ej: '...XX Coloquio de Oceanografía. CONICET MARCOS ZARATE; ...').
        # Probar cada palabra en mayúsculas del span como inicio hasta que
        # la corrida resultante sea un listado de autores plausible.
        span = m.group(0)
        pos = 0
        for word in span.split():
            idx = span.find(word, pos)
            pos = idx + len(word)
            if not _upper_word(word):
                continue
            cm = AUTHOR_RUN.match(flowing[m.start() + idx:])
            if cm and _mostly_upper(cm.group(0)):
                starts.append(m.start() + idx)
                break
    if not starts:
        return [flowing] if len(flowing) > 30 else []
    entries = []
    for i, s in enumerate(starts):
        e = starts[i + 1] if i + 1 < len(starts) else len(flowing)
        chunk = flowing[s:e].strip()
        if len(chunk) > 30:
            entries.append(chunk)
    return entries


def _parse_citation(entry):
    """De 'AUTORES. Título. resto...' extraer autores, título, año y detalle."""
    authors = None
    rest = entry
    m = AUTHOR_RUN.match(entry)
    if m:
        authors = m.group(0).rstrip('.').strip()
        rest = entry[m.end():].strip()

    tm = re.match(r'^(.{10,300}?)\.\s', rest)
    title = tm.group(1).strip() if tm else rest[:200].strip()

    after_title = rest[len(title):]
    ym = YEAR_RE.search(after_title) or YEAR_RE.search(rest)
    return {
        'title': title,
        'authors': authors,
        'year': ym.group(0) if ym else None,
        'detail': entry.strip()[:2000],
    }


# ==========================================
# Proyectos I+D
# ==========================================

def parse_projects(text):
    body = _section_body(text, PROJECT_HEADER)
    if not body:
        return []
    results = []
    blocks = re.split(r'Tipo de actividad de I\+D:', body)
    for block in blocks[1:]:
        title = _field(block, 'Denominación del proyecto:',
                       stop=r'Tipo de proyecto:|Código de identificación:|Fecha desde:')
        if not title:
            continue
        desc = _field(block, 'Descripción del proyecto:',
                      stop=r'Campo aplicación:|Área del conocimiento:|Moneda:')
        date_from = _field(block, 'Fecha desde:',
                           stop=r'Fecha hasta:|Descripción')
        ym = YEAR_RE.search(date_from or '') or YEAR_RE.search(block[:300])
        results.append({
            'kind': 'project',
            'group': 'Proyectos I+D',
            'title': title,
            'authors': None,
            'year': ym.group(0) if ym else None,
            'detail': (desc or '')[:2000] or None,
        })
    return results


# ==========================================
# Becarios y tesistas dirigidos
# ==========================================

def parse_rrhh(text):
    results = []
    for header, (label, group) in RRHH_HEADERS.items():
        body = _section_body(text, header)
        if not body:
            continue
        blocks = re.split(r'Año desde:', body)
        for block in blocks[1:]:
            first_name = _field(block, 'Nombre/s:', stop=r'Apellido/s:|Institución')
            last_name = _field(block, 'Apellido/s:', stop=r'Institución|Tipo de|Nombre/s:')
            if not first_name and not last_name:
                continue
            person = f"{first_name or ''} {last_name or ''}".strip()
            work_type = (_field(block, 'Tipo de beca:', stop=r'Función|Año')
                         or _field(block, 'Tipo de trabajo dirigido:', stop=r'Función|Año')
                         or label)
            ym = YEAR_RE.search(block)
            role = (_field(block, 'Función desempañada:', stop=r'Año desde:|Nombre/s:')
                    or _field(block, 'Función desempeñada:',
                              stop=r'Calificación|Año desde:|Nombre/s:'))
            results.append({
                'kind': 'thesis',
                'group': group,
                'title': f"{label}: {person} ({work_type})",
                'authors': person,
                'year': ym.group(0) if ym else None,
                'detail': f"Función: {role}." if role else None,
            })
    return results


# ==========================================
# Perfil
# ==========================================

def parse_profile(text):
    profile = {}

    resumen = _field(text, 'Resumen:',
                     stop=r'Areas de Actuación|Áreas de Actuación')
    if resumen:
        profile['bio'] = resumen[:2000]

    # Título académico: posgrado completo > grado
    for level_header in ('FORMACION ACADEMICA - Nivel Universitario de Posgrado/Doctorado:',
                         'FORMACION ACADEMICA - Nivel Universitario de Grado:'):
        body = _section_body(text, level_header)
        if not body:
            continue
        situation = _field(body, 'Situación del nivel:', stop=r'Fecha|Instituciones')
        degree = _field(body, 'Título:',
                        stop=r'Número de resolución:|Instituciones|Título de la tesis')
        if not degree:
            continue
        completed = situation and 'completo' in situation.lower() \
            and 'incompleto' not in situation.lower()
        if completed:
            profile['degree'] = degree
            break
        if 'Grado' in level_header and 'degree' not in profile:
            profile['degree'] = degree
    return profile


def _field(block, label, stop):
    """Valor de un campo 'Etiqueta: valor' hasta el próximo campo conocido."""
    match = _header_re(label).search(block)
    if not match:
        return None
    rest = block[match.end():]
    m = re.search(stop, rest) if stop else None
    value = rest[:m.start()] if m else rest
    value = ' '.join(value.split()).strip()
    return value or None


def parse_sigeva(pdf_file):
    """Punto de entrada: dict con 'profile' y lista de 'items'."""
    text = extract_text(pdf_file)
    text = _strip_owner_name(text, _owner_line(text))

    items = []
    items.extend(parse_publications(text))
    items.extend(parse_projects(text))
    items.extend(parse_rrhh(text))

    return {
        'profile': parse_profile(text),
        'items': items,
    }
