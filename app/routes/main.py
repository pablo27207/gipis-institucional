from flask import Blueprint, render_template
from app.models import Member, Category, ResearchLine, ResearchSection, ResearchItem, News, SiteContent

bp = Blueprint('main', __name__)


@bp.route('/')
def home():
    """Página principal"""
    mission = SiteContent.query.filter_by(key='mission').first()
    news = News.query.order_by(News.published_at.desc()).limit(3).all()
    return render_template('pages/home.xhtml', mission=mission, news=news)


@bp.route('/equipo')
def equipo():
    """Nuestro Equipo"""
    categories = Category.query.order_by(Category.order).all()
    return render_template('pages/equipo.xhtml', categories=categories)


@bp.route('/equipo/<slug>')
def miembro_detalle(slug):
    """Detalle de un miembro del equipo"""
    member = Member.query.filter_by(slug=slug).first_or_404()
    return render_template('pages/miembro.xhtml', member=member)


@bp.route('/investigacion')
def investigacion():
    """Líneas de Investigación"""
    lines = ResearchLine.query.order_by(ResearchLine.order).all()
    sections = ResearchSection.query.order_by(ResearchSection.order).all()
    return render_template('pages/investigacion.xhtml', lines=lines, sections=sections)


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
    return render_template('pages/cooperacion.xhtml', content=content)


@bp.route('/novedades')
def novedades():
    """Listado de novedades"""
    page = 1  # TODO: implementar paginación
    news = News.query.order_by(News.published_at.desc()).all()
    return render_template('pages/novedades.xhtml', news=news)


@bp.route('/novedades/<slug>')
def novedad_detalle(slug):
    """Detalle de una novedad"""
    news_item = News.query.filter_by(slug=slug).first_or_404()
    return render_template('pages/novedad.xhtml', news=news_item)


@bp.route('/contacto')
def contacto():
    """Página de contacto"""
    return render_template('pages/contacto.xhtml')
