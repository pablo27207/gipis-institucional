from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Category(db.Model):
    """Categorías de miembros (Investigadores, Becarios, Colaboradores, etc.)"""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    order = db.Column(db.Integer, default=0)
    
    members = db.relationship('Member', backref='category', lazy='dynamic')
    
    def __repr__(self):
        return f'<Category {self.name}>'


class Member(UserMixin, db.Model):
    """Miembros del grupo de investigación (también usuarios del sistema)"""
    __tablename__ = 'members'
    
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    degree = db.Column(db.String(100))
    position = db.Column(db.String(200))
    bio = db.Column(db.Text)
    email = db.Column(db.String(150), unique=True)
    personal_email = db.Column(db.String(150))
    personal_email_public = db.Column(db.Boolean, default=False)
    institutional_email = db.Column(db.String(150))
    institutional_email_public = db.Column(db.Boolean, default=False)
    phone = db.Column(db.String(50))
    phone_public = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(256))
    linkedin = db.Column(db.String(255))
    orcid = db.Column(db.String(19))  # iD canónico 0000-0000-0000-0000
    photo = db.Column(db.String(255))
    order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    role = db.Column(db.String(20), default='member')  # 'admin' | 'member'

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    works = db.relationship('MemberWork', backref='member', lazy='dynamic',
                            cascade='all, delete-orphan')

    @property
    def is_admin(self):
        return self.role == 'admin'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<Member {self.name}>'


@login_manager.user_loader
def load_user(id):
    return Member.query.get(int(id))




class ResearchSection(db.Model):
    """Secciones de investigación (Publicaciones, Proyectos, Tesis, etc.)"""
    __tablename__ = 'research_sections'
    
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    title = db.Column(db.String(150), nullable=False)
    order = db.Column(db.Integer, default=0)
    
    items = db.relationship('ResearchItem', backref='section', lazy='dynamic',
                            order_by='ResearchItem.year.desc()')
    
    def __repr__(self):
        return f'<ResearchSection {self.title}>'


class ResearchItem(db.Model):
    """Items de investigación (publicaciones, proyectos, tesis, etc.)"""
    __tablename__ = 'research_items'
    
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    title = db.Column(db.String(500), nullable=False)
    authors = db.Column(db.String(500))
    year = db.Column(db.String(10))
    abstract = db.Column(db.Text)
    links = db.Column(db.Text)  # JSON string de links
    
    section_id = db.Column(db.Integer, db.ForeignKey('research_sections.id'))
    
    def __repr__(self):
        return f'<ResearchItem {self.title[:50]}>'


class ResearchLine(db.Model):
    """Líneas de investigación"""
    __tablename__ = 'research_lines'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50))  # Nombre del icono
    order = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return f'<ResearchLine {self.title}>'


class MemberWork(db.Model):
    """Producción personal de un miembro (importada de SIGEVA o cargada a mano).
    Puede compartirse al sitio creando un ResearchItem vinculado."""
    __tablename__ = 'member_works'

    KINDS = {
        'publication': 'Publicaciones',
        'project': 'Proyectos',
        'thesis': 'Tesis y becarios dirigidos',
    }

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)
    kind = db.Column(db.String(30), nullable=False, default='publication')
    title = db.Column(db.String(500), nullable=False)
    authors = db.Column(db.String(500))
    year = db.Column(db.String(10))
    detail = db.Column(db.Text)
    source = db.Column(db.String(20), default='manual')  # 'manual' | 'sigeva'
    shared_item_id = db.Column(db.Integer, db.ForeignKey('research_items.id'))

    shared_item = db.relationship('ResearchItem')

    @property
    def kind_label(self):
        return self.KINDS.get(self.kind, self.kind)

    def __repr__(self):
        return f'<MemberWork {self.title[:50]}>'


class Partner(db.Model):
    """Organizaciones de la Red de Colaboración (página Cooperación)"""
    __tablename__ = 'partners'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(255))
    order = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Partner {self.name}>'


class News(db.Model):
    """Novedades/Noticias"""
    __tablename__ = 'news'
    
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    title = db.Column(db.String(300), nullable=False)
    excerpt = db.Column(db.String(500))
    content = db.Column(db.Text)
    image = db.Column(db.String(255))
    category = db.Column(db.String(100))
    published_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<News {self.title[:50]}>'


class SiteContent(db.Model):
    """Contenido estático del sitio (misión, textos de secciones, etc.)"""
    __tablename__ = 'site_content'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    title = db.Column(db.String(200))
    content = db.Column(db.Text)
    
    def __repr__(self):
        return f'<SiteContent {self.key}>'
