import re
import unicodedata
from functools import wraps

from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user

from app import db
from app.models import Member, Category, ResearchSection, ResearchItem, Partner

bp = Blueprint('admin', __name__, url_prefix='/auth/admin')


def admin_required(f):
    @wraps(f)
    @login_required
    def wrapped(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return wrapped


def slugify(name):
    """Generar slug único a partir del nombre (ej: 'Juan Pérez' -> 'jperez')"""
    normalized = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')
    parts = [p for p in re.sub(r'[^a-z ]', '', normalized.lower()).split() if p]
    if not parts:
        base = 'miembro'
    elif len(parts) == 1:
        base = parts[0]
    else:
        base = parts[0][0] + parts[-1]

    slug = base
    counter = 2
    while Member.query.filter_by(slug=slug).first():
        slug = f"{base}{counter}"
        counter += 1
    return slug


# ==========================================
# Miembros
# ==========================================

@bp.route('/members', methods=['GET', 'POST'])
@admin_required
def members():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        if not name or not email or not password:
            flash('Nombre, email y contraseña inicial son obligatorios.', 'error')
            return redirect(url_for('admin.members'))

        if Member.query.filter_by(email=email).first():
            flash(f'Ya existe un miembro con el email {email}.', 'error')
            return redirect(url_for('admin.members'))

        member = Member(
            slug=slugify(name),
            name=name,
            email=email,
            degree=request.form.get('degree', '').strip() or None,
            position=request.form.get('position', '').strip() or None,
            role=request.form.get('role', 'member'),
            category_id=request.form.get('category_id', type=int),
            order=request.form.get('order', type=int) or 0,
        )
        member.set_password(password)
        db.session.add(member)
        db.session.commit()
        flash(f'Miembro {name} creado. Puede ingresar con {email}.', 'success')
        return redirect(url_for('admin.members'))

    all_members = Member.query.order_by(Member.order, Member.name).all()
    categories = Category.query.order_by(Category.order).all()
    return render_template('admin/members.xhtml', members=all_members, categories=categories)


@bp.route('/members/<int:member_id>/role', methods=['POST'])
@admin_required
def toggle_role(member_id):
    member = Member.query.get_or_404(member_id)
    if member.id == current_user.id:
        flash('No podés cambiar tu propio rol.', 'error')
    else:
        member.role = 'member' if member.is_admin else 'admin'
        db.session.commit()
        flash(f'{member.name} ahora es {"administrador" if member.is_admin else "miembro"}.', 'success')
    return redirect(url_for('admin.members'))


@bp.route('/members/<int:member_id>/active', methods=['POST'])
@admin_required
def toggle_active(member_id):
    member = Member.query.get_or_404(member_id)
    if member.id == current_user.id:
        flash('No podés desactivar tu propia cuenta.', 'error')
    else:
        member.is_active = not member.is_active
        db.session.commit()
        flash(f'{member.name} {"activado" if member.is_active else "desactivado"}.', 'success')
    return redirect(url_for('admin.members'))


# ==========================================
# Investigación (secciones e items)
# ==========================================

@bp.route('/research')
@admin_required
def research():
    sections = ResearchSection.query.order_by(ResearchSection.order).all()
    return render_template('admin/research.xhtml', sections=sections)


@bp.route('/research/sections', methods=['POST'])
@admin_required
def add_section():
    title = request.form.get('title', '').strip()
    if not title:
        flash('El título de la sección es obligatorio.', 'error')
        return redirect(url_for('admin.research'))

    slug_base = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-') or 'seccion'
    slug = slug_base
    counter = 2
    while ResearchSection.query.filter_by(slug=slug).first():
        slug = f"{slug_base}-{counter}"
        counter += 1

    max_order = db.session.query(db.func.max(ResearchSection.order)).scalar() or 0
    db.session.add(ResearchSection(slug=slug, title=title, order=max_order + 1))
    db.session.commit()
    flash(f'Sección "{title}" creada.', 'success')
    return redirect(url_for('admin.research'))


@bp.route('/research/items', methods=['POST'])
@admin_required
def add_item():
    title = request.form.get('title', '').strip()
    section_id = request.form.get('section_id', type=int)
    if not title or not section_id:
        flash('Título y sección son obligatorios.', 'error')
        return redirect(url_for('admin.research'))

    db.session.add(ResearchItem(
        slug=_item_slug(title),
        title=title,
        authors=request.form.get('authors', '').strip() or None,
        year=request.form.get('year', '').strip() or None,
        abstract=request.form.get('abstract', '').strip() or None,
        section_id=section_id,
    ))
    db.session.commit()
    flash('Ítem agregado.', 'success')
    return redirect(url_for('admin.research'))


@bp.route('/research/items/<int:item_id>/edit', methods=['POST'])
@admin_required
def edit_item(item_id):
    item = ResearchItem.query.get_or_404(item_id)
    item.title = request.form.get('title', item.title).strip() or item.title
    item.authors = request.form.get('authors', '').strip() or None
    item.year = request.form.get('year', '').strip() or None
    item.abstract = request.form.get('abstract', '').strip() or None
    section_id = request.form.get('section_id', type=int)
    if section_id:
        item.section_id = section_id
    db.session.commit()
    flash('Ítem actualizado.', 'success')
    return redirect(url_for('admin.research'))


@bp.route('/research/items/<int:item_id>/delete', methods=['POST'])
@admin_required
def delete_item(item_id):
    item = ResearchItem.query.get_or_404(item_id)
    # Desvincular producción personal que apunte a este ítem
    from app.models import MemberWork
    MemberWork.query.filter_by(shared_item_id=item.id).update({'shared_item_id': None})
    db.session.delete(item)
    db.session.commit()
    flash('Ítem eliminado.', 'success')
    return redirect(url_for('admin.research'))


def _item_slug(title):
    slug_base = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')[:40] or 'item'
    slug = slug_base
    counter = 2
    while ResearchItem.query.filter_by(slug=slug).first():
        slug = f"{slug_base}-{counter}"
        counter += 1
    return slug


# ==========================================
# Red de Colaboración
# ==========================================

@bp.route('/partners', methods=['GET', 'POST'])
@admin_required
def partners():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if not name:
            flash('El nombre de la organización es obligatorio.', 'error')
            return redirect(url_for('admin.partners'))

        max_order = db.session.query(db.func.max(Partner.order)).scalar() or 0
        db.session.add(Partner(
            name=name,
            url=request.form.get('url', '').strip() or None,
            order=max_order + 1,
        ))
        db.session.commit()
        flash(f'"{name}" agregada a la Red de Colaboración.', 'success')
        return redirect(url_for('admin.partners'))

    all_partners = Partner.query.order_by(Partner.order).all()
    return render_template('admin/partners.xhtml', partners=all_partners)


@bp.route('/partners/<int:partner_id>/edit', methods=['POST'])
@admin_required
def edit_partner(partner_id):
    partner = Partner.query.get_or_404(partner_id)
    partner.name = request.form.get('name', partner.name).strip() or partner.name
    partner.url = request.form.get('url', '').strip() or None
    order = request.form.get('order', type=int)
    if order is not None:
        partner.order = order
    db.session.commit()
    flash('Organización actualizada.', 'success')
    return redirect(url_for('admin.partners'))


@bp.route('/partners/<int:partner_id>/delete', methods=['POST'])
@admin_required
def delete_partner(partner_id):
    partner = Partner.query.get_or_404(partner_id)
    db.session.delete(partner)
    db.session.commit()
    flash('Organización eliminada.', 'success')
    return redirect(url_for('admin.partners'))
