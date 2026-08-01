from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from app.models import Member, Category, ResearchLine, ResearchSection, ResearchItem, News, SiteContent, MemberWork, Partner
from app.i18n import LANGUAGES

bp = Blueprint('main', __name__)


@bp.route('/lang/<code>')
def set_language(code):
    """Cambiar el idioma de la interfaz (guardado en sesión)"""
    if code in LANGUAGES:
        session['lang'] = code
    return redirect(request.referrer or url_for('main.home'))


@bp.route('/')
def home():
    """Página principal"""
    mission = SiteContent.query.filter_by(key='mission').first()
    news = News.query.order_by(News.published_at.desc()).limit(3).all()
    return render_template('pages/home.xhtml', mission=mission, news=news)


@bp.route('/equipo')
def equipo():
    """Nuestro Equipo. Orden: primero quienes tienen foto (incentivo a subirla),
    luego por jerarquía del cargo (Member.position_rank) y alfabético por nombre."""
    categories = Category.query.order_by(Category.order).all()
    for category in categories:
        category.sorted_members = sorted(
            category.members.filter_by(is_active=True),
            key=lambda m: (0 if m.photo else 1, m.position_rank, m.name.lower()))
    return render_template('pages/equipo.xhtml', categories=categories)


@bp.route('/equipo/<slug>')
def miembro_detalle(slug):
    """Detalle de un miembro del equipo"""
    member = Member.query.filter_by(slug=slug).first_or_404()
    works = member.works.order_by(
        MemberWork.kind, MemberWork.year.desc().nullslast()).all()
    return render_template('pages/miembro.xhtml', member=member,
                           member_works=works, work_kinds=MemberWork.KINDS)


@bp.route('/equipo/<slug>/vcard')
def member_vcard(slug):
    """Generar vCard (.vcf) para un miembro"""
    import os
    import base64
    from flask import current_app, make_response
    
    member = Member.query.filter_by(slug=slug).first_or_404()
    
    # Separar nombre y apellido (aproximado)
    name_parts = member.name.split()
    first_name = name_parts[0] if name_parts else ''
    last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''
    
    lines = [
        'BEGIN:VCARD',
        'VERSION:3.0',
        f'N:{last_name};{first_name};;;',
        f'FN:{member.name}',
        'ORG:GIPIS - UNPSJB;Facultad de Ingeniería',
    ]
    
    if member.position:
        lines.append(f'TITLE:{member.position}')
    
    if member.institutional_email and member.institutional_email_public:
        lines.append(f'EMAIL;TYPE=WORK:{member.institutional_email}')
    
    if member.personal_email and member.personal_email_public:
        lines.append(f'EMAIL;TYPE=HOME:{member.personal_email}')
    
    if member.phone and member.phone_public:
        lines.append(f'TEL;TYPE=WORK:{member.phone}')
    
    if member.linkedin:
        lines.append(f'URL:{member.linkedin}')
    
    # Foto embebida como base64
    if member.photo:
        photo_path = os.path.join(current_app.static_folder, 'img', 'profiles', member.photo)
        if os.path.exists(photo_path):
            ext = member.photo.rsplit('.', 1)[1].upper() if '.' in member.photo else 'PNG'
            if ext == 'JPG':
                ext = 'JPEG'
            with open(photo_path, 'rb') as f:
                photo_data = base64.b64encode(f.read()).decode('ascii')
            # vCard 3.0 photo format with line folding
            photo_line = f'PHOTO;ENCODING=b;TYPE={ext}:{photo_data}'
            lines.append(photo_line)
    
    lines.append('END:VCARD')
    
    vcard_content = '\r\n'.join(lines)
    
    response = make_response(vcard_content)
    response.headers['Content-Type'] = 'text/vcard; charset=utf-8'
    response.headers['Content-Disposition'] = f'attachment; filename="{member.slug}.vcf"'
    return response


@bp.route('/investigacion')
def investigacion():
    """Líneas de Investigación"""
    lines = ResearchLine.query.order_by(ResearchLine.order).all()
    sections = ResearchSection.query.order_by(ResearchSection.order).all()
    return render_template('pages/investigacion.xhtml', lines=lines, sections=sections)


@bp.route('/investigacion/produccion')
def produccion():
    """Producción científica completa, con búsqueda y filtros en el cliente"""
    from app.doi import normalize_doi
    sections = ResearchSection.query.order_by(ResearchSection.order).all()
    years = set()
    for section in sections:
        for item in section.items:
            if item.year:
                years.add(item.year)
            # DOI detectado en el texto del ítem: habilita citas y "Citar"
            item.doi_norm = normalize_doi(
                f"{item.abstract or ''} {item.links or ''}")
    return render_template('pages/produccion.xhtml', sections=sections,
                           years=sorted(years, reverse=True))


@bp.route('/investigacion/produccion/<int:item_id>/bibtex')
def produccion_bibtex(item_id):
    """Cita BibTeX de un ítem (vía DOI si tiene; si no, generada básica)"""
    from flask import Response, abort
    from app.doi import normalize_doi, fetch_bibtex, DoiError
    from app.security import rate_limited

    # Este endpoint hace una consulta saliente a doi.org: limitar abuso
    if rate_limited('bibtex', limit=30, window_seconds=300):
        abort(429)

    item = ResearchItem.query.get_or_404(item_id)
    doi = normalize_doi(f"{item.abstract or ''} {item.links or ''}")
    bibtex = None
    if doi:
        try:
            bibtex = fetch_bibtex(doi)
        except DoiError:
            pass
    if not bibtex:
        first_author = (item.authors or 'GIPIS').split(';')[0].split(',')[0].strip()
        key = ''.join(c for c in first_author.lower() if c.isalnum()) or 'gipis'
        fields = [f'  title = {{{item.title}}}']
        if item.authors:
            fields.append(f'  author = {{{item.authors}}}')
        if item.year:
            fields.append(f'  year = {{{item.year}}}')
        bibtex = ('@misc{%s%s,\n' % (key, item.year or '')) + ',\n'.join(fields) + '\n}'
    return Response(bibtex, mimetype='text/plain; charset=utf-8')


@bp.route('/investigacion/<int:line_id>')
def linea_detalle(line_id):
    """Detalle de una línea de investigación"""
    line = ResearchLine.query.get_or_404(line_id)
    # Obtener items relacionados (por ahora todos)
    sections = ResearchSection.query.order_by(ResearchSection.order).all()
    return render_template('pages/linea.xhtml', line=line, sections=sections)


@bp.route('/cooperacion')
def cooperacion():
    """Cooperación Científica e Industrial"""
    content = SiteContent.query.filter_by(key='cooperacion').first()
    partners = Partner.query.order_by(Partner.order).all()
    return render_template('pages/cooperacion.xhtml', content=content, partners=partners)


@bp.route('/novedades')
def novedades():
    """Listado de novedades, paginado"""
    page = request.args.get('page', 1, type=int)
    pagination = News.query.order_by(News.published_at.desc()).paginate(
        page=page, per_page=9, error_out=False)
    return render_template('pages/novedades.xhtml',
                           news=pagination.items, pagination=pagination)


@bp.route('/novedades/<slug>')
def novedad_detalle(slug):
    """Detalle de una novedad"""
    news_item = News.query.filter_by(slug=slug).first_or_404()
    return render_template('pages/novedad.xhtml', news=news_item)


# ==========================================
# SEO: sitemap y robots
# ==========================================

@bp.route('/sitemap.xml')
def sitemap():
    """Sitemap XML para buscadores"""
    from flask import Response

    urls = []
    for endpoint in ('main.home', 'main.equipo', 'main.investigacion',
                     'main.produccion', 'main.cooperacion', 'main.novedades',
                     'main.contacto'):
        urls.append((url_for(endpoint, _external=True), None))

    for member in Member.query.filter(Member.is_active.is_(True),
                                      Member.category_id.isnot(None)).all():
        urls.append((url_for('main.miembro_detalle', slug=member.slug,
                             _external=True), None))

    for item in News.query.order_by(News.published_at.desc()).all():
        lastmod = item.published_at.strftime('%Y-%m-%d') if item.published_at else None
        urls.append((url_for('main.novedad_detalle', slug=item.slug,
                             _external=True), lastmod))

    entries = []
    for loc, lastmod in urls:
        entry = f'  <url>\n    <loc>{loc}</loc>\n'
        if lastmod:
            entry += f'    <lastmod>{lastmod}</lastmod>\n'
        entries.append(entry + '  </url>')

    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + '\n'.join(entries) + '\n</urlset>\n')
    return Response(xml, mimetype='application/xml')


@bp.route('/robots.txt')
def robots():
    from flask import Response
    body = (
        'User-agent: *\n'
        'Allow: /\n'
        'Disallow: /auth/\n'
        f'Sitemap: {url_for("main.sitemap", _external=True)}\n'
    )
    return Response(body, mimetype='text/plain')


@bp.route('/contacto', methods=['GET', 'POST'])
def contacto():
    """Página de contacto"""
    if request.method == 'POST':
        # Honeypot anti-spam: si este campo tiene valor, es un bot
        if request.form.get('website', ''):
            flash('¡Mensaje enviado correctamente! Nos pondremos en contacto a la brevedad.', 'success')
            return redirect(url_for('main.contacto'))

        from app.security import rate_limited
        if rate_limited('contacto', limit=3, window_seconds=600):
            flash('Enviaste varios mensajes seguidos. Esperá unos minutos '
                  'antes de volver a intentar.', 'error')
            return redirect(url_for('main.contacto'))

        nombre = request.form.get('nombre', '').strip()[:100]
        email = request.form.get('email', '').strip()[:150]
        asunto = request.form.get('asunto', '').strip()[:150]
        mensaje = request.form.get('mensaje', '').strip()[:5000]

        if not nombre or not email or not asunto or not mensaje:
            flash('Por favor, completá todos los campos.', 'error')
            return redirect(url_for('main.contacto'))

        import re as _re
        if not _re.fullmatch(r'[^@\s]+@[^@\s]+\.[^@\s]+', email):
            flash('El email ingresado no parece válido.', 'error')
            return redirect(url_for('main.contacto'))

        try:
            from flask_mail import Message
            from app import mail
            
            msg = Message(
                subject=f'[GIPIS Web] {asunto}',
                recipients=['gipis.unp@gmail.com'],
                reply_to=email
            )
            msg.body = (
                f"Nuevo mensaje desde el formulario de contacto del sitio web GIPIS\n"
                f"{'=' * 60}\n\n"
                f"Nombre: {nombre}\n"
                f"Email: {email}\n"
                f"Asunto: {asunto}\n\n"
                f"Mensaje:\n{mensaje}\n"
            )
            from markupsafe import escape
            msg.html = (
                f"<h2>Nuevo mensaje desde el sitio web GIPIS</h2>"
                f"<hr>"
                f"<p><strong>Nombre:</strong> {escape(nombre)}</p>"
                f"<p><strong>Email:</strong> <a href='mailto:{escape(email)}'>{escape(email)}</a></p>"
                f"<p><strong>Asunto:</strong> {escape(asunto)}</p>"
                f"<hr>"
                f"<p><strong>Mensaje:</strong></p>"
                f"<p>{str(escape(mensaje)).replace(chr(10), '<br>')}</p>"
            )
            mail.send(msg)
            flash('¡Mensaje enviado correctamente! Nos pondremos en contacto a la brevedad.', 'success')
        except Exception as e:
            print(f'Error enviando email de contacto: {e}')
            flash('Hubo un error al enviar el mensaje. Por favor, intentá nuevamente o escribinos directamente a gipis.unp@gmail.com.', 'error')
        
        return redirect(url_for('main.contacto'))
    
    return render_template('pages/contacto.xhtml')
