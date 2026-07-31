import os
import re
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.models import Member, MemberWork, ResearchSection, ResearchItem

bp = Blueprint('auth', __name__, url_prefix='/auth')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_upload_folder():
    upload_folder = os.path.join(current_app.static_folder, 'img', 'profiles')
    os.makedirs(upload_folder, exist_ok=True)
    return upload_folder


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login para miembros"""
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        member = Member.query.filter_by(email=email).first()
        
        if member and member.check_password(password):
            login_user(member)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('auth.dashboard'))
        else:
            flash('Email o contraseña incorrectos', 'error')
    
    return render_template('auth/login.xhtml')


@bp.route('/logout')
@login_required
def logout():
    """Cerrar sesión"""
    logout_user()
    return redirect(url_for('main.home'))


@bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard del miembro - editar perfil"""
    return render_template('auth/dashboard.xhtml')


@bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Editar perfil del miembro"""
    if request.method == 'POST':
        current_user.name = request.form.get('name', current_user.name)
        current_user.degree = request.form.get('degree', current_user.degree)
        current_user.position = request.form.get('position', current_user.position)
        current_user.bio = request.form.get('bio', current_user.bio)
        current_user.linkedin = request.form.get('linkedin', current_user.linkedin)
        
        # Manejar emails con visibilidad
        current_user.personal_email = request.form.get('personal_email', current_user.personal_email)
        current_user.personal_email_public = 'personal_email_public' in request.form
        current_user.institutional_email = request.form.get('institutional_email', current_user.institutional_email)
        current_user.institutional_email_public = 'institutional_email_public' in request.form
        current_user.phone = request.form.get('phone', current_user.phone)
        current_user.phone_public = 'phone_public' in request.form
        
        # Manejar foto de perfil
        photo = request.files.get('photo')
        if photo and photo.filename and allowed_file(photo.filename):
            ext = photo.filename.rsplit('.', 1)[1].lower()
            filename = f"{current_user.slug}.{ext}"
            filepath = os.path.join(get_upload_folder(), filename)
            
            # Eliminar foto anterior si tiene otra extensión
            if current_user.photo and current_user.photo != filename:
                old_path = os.path.join(get_upload_folder(), current_user.photo)
                if os.path.exists(old_path):
                    os.remove(old_path)
            
            photo.save(filepath)
            current_user.photo = filename
        elif photo and photo.filename and not allowed_file(photo.filename):
            flash('Formato de imagen no permitido. Usá PNG, JPG o WebP.', 'error')
            return redirect(url_for('auth.edit_profile'))
        
        # Manejar eliminación de foto
        if request.form.get('remove_photo') == '1':
            if current_user.photo:
                old_path = os.path.join(get_upload_folder(), current_user.photo)
                if os.path.exists(old_path):
                    os.remove(old_path)
                current_user.photo = None
        
        # Manejar cambio de contraseña
        new_password = request.form.get('new_password')
        if new_password:
            current_user.set_password(new_password)
        
        db.session.commit()
        flash('Perfil actualizado correctamente', 'success')
        return redirect(url_for('auth.dashboard'))

    return render_template('auth/edit_profile.xhtml')


# ==========================================
# Mi producción (trabajos personales)
# ==========================================

# Sección sugerida al compartir, por tipo de trabajo
KIND_DEFAULT_SECTION = {
    'publication': 'publications',
    'project': 'projects',
    'thesis': 'doctoral',
}


@bp.route('/works', methods=['GET', 'POST'])
@login_required
def works():
    """Producción personal del miembro"""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        if not title:
            flash('El título es obligatorio.', 'error')
            return redirect(url_for('auth.works'))

        kind = request.form.get('kind', 'publication')
        if kind not in MemberWork.KINDS:
            kind = 'publication'

        db.session.add(MemberWork(
            member_id=current_user.id,
            kind=kind,
            title=title,
            authors=request.form.get('authors', '').strip() or None,
            year=request.form.get('year', '').strip() or None,
            detail=request.form.get('detail', '').strip() or None,
        ))
        db.session.commit()
        flash('Trabajo agregado a tu producción.', 'success')
        return redirect(url_for('auth.works'))

    my_works = current_user.works.order_by(
        MemberWork.kind, MemberWork.year.desc()).all()
    sections = ResearchSection.query.order_by(ResearchSection.order).all()
    return render_template('auth/works.xhtml', works=my_works, sections=sections,
                           kinds=MemberWork.KINDS, default_sections=KIND_DEFAULT_SECTION)


def _own_work_or_404(work_id):
    work = MemberWork.query.get_or_404(work_id)
    if work.member_id != current_user.id:
        from flask import abort
        abort(403)
    return work


@bp.route('/works/<int:work_id>/edit', methods=['POST'])
@login_required
def edit_work(work_id):
    work = _own_work_or_404(work_id)
    work.title = request.form.get('title', work.title).strip() or work.title
    work.authors = request.form.get('authors', '').strip() or None
    work.year = request.form.get('year', '').strip() or None
    work.detail = request.form.get('detail', '').strip() or None
    kind = request.form.get('kind')
    if kind in MemberWork.KINDS:
        work.kind = kind
    # Si está compartido, reflejar los cambios en el ítem del sitio
    if work.shared_item:
        work.shared_item.title = work.title
        work.shared_item.authors = work.authors
        work.shared_item.year = work.year
        work.shared_item.abstract = work.detail
    db.session.commit()
    flash('Trabajo actualizado.', 'success')
    return redirect(url_for('auth.works'))


def _release_shared_item(work):
    """Quitar el ítem del sitio solo si ningún otro miembro lo comparte"""
    item = work.shared_item
    work.shared_item_id = None
    if item:
        others = MemberWork.query.filter(
            MemberWork.shared_item_id == item.id,
            MemberWork.id != work.id,
        ).count()
        if others == 0:
            db.session.delete(item)


@bp.route('/works/<int:work_id>/delete', methods=['POST'])
@login_required
def delete_work(work_id):
    work = _own_work_or_404(work_id)
    _release_shared_item(work)
    db.session.delete(work)
    db.session.commit()
    flash('Trabajo eliminado.', 'success')
    return redirect(url_for('auth.works'))


@bp.route('/works/<int:work_id>/share', methods=['POST'])
@login_required
def share_work(work_id):
    """Publicar un trabajo personal en la sección de Investigación elegida"""
    work = _own_work_or_404(work_id)
    if work.shared_item:
        flash('Este trabajo ya está compartido en el sitio.', 'error')
        return redirect(url_for('auth.works'))

    section = ResearchSection.query.get(request.form.get('section_id', type=int))
    if not section:
        flash('Elegí una sección válida.', 'error')
        return redirect(url_for('auth.works'))

    # Evitar duplicados: mismo título (sin distinguir mayúsculas) en la sección
    existing = ResearchItem.query.filter(
        ResearchItem.section_id == section.id,
        db.func.lower(ResearchItem.title) == work.title.lower(),
    ).first()
    if existing:
        work.shared_item_id = existing.id
        db.session.commit()
        flash('Ya existía un ítem igual en esa sección; se vinculó tu trabajo a ese ítem.', 'success')
        return redirect(url_for('auth.works'))

    slug_base = re.sub(r'[^a-z0-9]+', '-', work.title.lower()).strip('-')[:40] or 'item'
    slug = slug_base
    counter = 2
    while ResearchItem.query.filter_by(slug=slug).first():
        slug = f"{slug_base}-{counter}"
        counter += 1

    item = ResearchItem(
        slug=slug,
        title=work.title,
        authors=work.authors,
        year=work.year,
        abstract=work.detail,
        section_id=section.id,
    )
    db.session.add(item)
    db.session.flush()
    work.shared_item_id = item.id
    db.session.commit()
    flash(f'Trabajo publicado en "{section.title}".', 'success')
    return redirect(url_for('auth.works'))


# ==========================================
# Importación desde SIGEVA
# ==========================================

@bp.route('/sigeva/parse', methods=['POST'])
@login_required
def sigeva_parse():
    """Analizar el PDF de SIGEVA y mostrar la pantalla de revisión"""
    pdf = request.files.get('pdf')
    if not pdf or not pdf.filename.lower().endswith('.pdf'):
        flash('Subí un archivo PDF exportado de SIGEVA.', 'error')
        return redirect(url_for('auth.works'))

    try:
        from app.sigeva import parse_sigeva
        result = parse_sigeva(pdf.stream)
    except Exception:
        current_app.logger.exception('Error parseando PDF de SIGEVA')
        flash('No se pudo leer el PDF. ¿Es el CV exportado de SIGEVA?', 'error')
        return redirect(url_for('auth.works'))

    if not result['items'] and not result['profile']:
        flash('No se encontró información reconocible en el PDF.', 'error')
        return redirect(url_for('auth.works'))

    # Marcar los que ya existen en la producción del miembro para no preseleccionarlos
    existing = {w.title.lower() for w in current_user.works}
    for item in result['items']:
        item['duplicate'] = item['title'].lower() in existing

    groups = {}
    for idx, item in enumerate(result['items']):
        groups.setdefault(item['group'], []).append((idx, item))

    import json
    return render_template(
        'auth/sigeva_review.xhtml',
        profile=result['profile'],
        groups=groups,
        payload=json.dumps({'profile': result['profile'], 'items': result['items']}),
    )


@bp.route('/sigeva/import', methods=['POST'])
@login_required
def sigeva_import():
    """Guardar los elementos seleccionados en la revisión"""
    import json
    try:
        payload = json.loads(request.form.get('payload', '{}'))
    except ValueError:
        flash('Datos de importación inválidos. Volvé a subir el PDF.', 'error')
        return redirect(url_for('auth.works'))

    items = payload.get('items', [])
    selected = {int(i) for i in request.form.getlist('item') if i.isdigit()}

    existing = {w.title.lower() for w in current_user.works}
    imported = skipped = 0
    for idx in sorted(selected):
        if idx >= len(items):
            continue
        item = items[idx]
        title = (item.get('title') or '').strip()
        if not title:
            continue
        if title.lower() in existing:
            skipped += 1
            continue
        kind = item.get('kind')
        if kind not in MemberWork.KINDS:
            kind = 'publication'
        db.session.add(MemberWork(
            member_id=current_user.id,
            kind=kind,
            title=title[:500],
            authors=(item.get('authors') or '')[:500] or None,
            year=(item.get('year') or '')[:10] or None,
            detail=item.get('detail') or None,
            source='sigeva',
        ))
        existing.add(title.lower())
        imported += 1

    profile = payload.get('profile', {})
    profile_updates = []
    if request.form.get('profile_degree') and profile.get('degree'):
        current_user.degree = profile['degree'][:100]
        profile_updates.append('título')
    if request.form.get('profile_bio') and profile.get('bio'):
        current_user.bio = profile['bio']
        profile_updates.append('biografía')

    db.session.commit()

    parts = [f'{imported} trabajos importados']
    if skipped:
        parts.append(f'{skipped} ya existían')
    if profile_updates:
        parts.append(f'perfil actualizado ({", ".join(profile_updates)})')
    flash('. '.join(parts) + '.', 'success')
    return redirect(url_for('auth.works'))


@bp.route('/works/<int:work_id>/unshare', methods=['POST'])
@login_required
def unshare_work(work_id):
    work = _own_work_or_404(work_id)
    if work.shared_item:
        _release_shared_item(work)
        db.session.commit()
        flash('El trabajo ya no se muestra en la página de Investigación.', 'success')
    return redirect(url_for('auth.works'))

