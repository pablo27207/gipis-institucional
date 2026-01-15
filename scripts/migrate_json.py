"""
Script para migrar datos de database.json a SQLite.
Ejecutar una vez para poblar la base de datos inicial.
"""
import json
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import Category, Member, ResearchSection, ResearchItem, SiteContent


def migrate_data():
    """Migra los datos de la web vieja a SQLite."""
    
    # Cargar JSON
    json_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'database.json'
    )
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("Cargando datos de database.json...")
    
    # Crear app context
    app = create_app()
    with app.app_context():
        # Limpiar tablas existentes
        db.drop_all()
        db.create_all()
        
        # === MIGRAR MIEMBROS ===
        print("\nMigrando miembros del grupo...")
        group_data = data.get('group', {})
        members_data = group_data.get('members', {})
        categories_data = group_data.get('categories', [])
        
        # Crear categorías
        category_map = {}
        for idx, cat_data in enumerate(categories_data):
            if cat_data.get('name'):
                category = Category(
                    name=cat_data['name'],
                    order=idx
                )
                db.session.add(category)
                db.session.flush()
                category_map[cat_data['name']] = category
                
                # Agregar miembros de esta categoría
                for member_order, member_slug in enumerate(cat_data.get('members', [])):
                    member_info = members_data.get(member_slug, {})
                    if member_info:
                        # Extraer nombre del archivo de foto
                        photo_path = member_info.get('pic', '')
                        photo_file = os.path.basename(photo_path) if photo_path else None
                        
                        member = Member(
                            slug=member_slug,
                            name=member_info.get('name', 'Sin nombre'),
                            degree=member_info.get('degree', ''),
                            position=member_info.get('position', ''),
                            bio=member_info.get('desc', ''),
                            email=member_info.get('contact', {}).get('email', ''),
                            linkedin=member_info.get('contact', {}).get('linkedin', ''),
                            photo=photo_file,
                            order=member_order,
                            category_id=category.id
                        )
                        db.session.add(member)
                        print(f"  + {member.name}")
        
        # === MIGRAR INVESTIGACIÓN ===
        print("\nMigrando secciones de investigación...")
        research_data = data.get('research', {})
        sections_data = research_data.get('sections', [])
        items_data = research_data.get('items', {})
        
        for idx, section_data in enumerate(sections_data):
            if section_data.get('title'):
                section = ResearchSection(
                    slug=section_data.get('id', f'section_{idx}'),
                    title=section_data['title'],
                    order=idx
                )
                db.session.add(section)
                db.session.flush()
                print(f"  Sección: {section.title}")
                
                # Agregar items de esta sección
                for item_slug in section_data.get('content', []):
                    item_info = items_data.get(item_slug, {})
                    if item_info:
                        links = item_info.get('links', [])
                        item = ResearchItem(
                            slug=item_slug,
                            title=item_info.get('title', 'Sin título'),
                            authors=item_info.get('authors', ''),
                            year=item_info.get('year', ''),
                            abstract=item_info.get('desc', ''),
                            links=json.dumps(links) if links else None,
                            section_id=section.id
                        )
                        db.session.add(item)
        
        # === MIGRAR CONTENIDO DEL SITIO ===
        print("\nMigrando contenido del sitio...")
        home_data = data.get('home', {})
        for section in home_data.get('sections', []):
            if section.get('title') == 'Misión':
                site_content = SiteContent(
                    key='mission',
                    title='Misión',
                    content=section.get('content', '')
                )
                db.session.add(site_content)
                print("  + Misión")
        
        # Guardar todo
        db.session.commit()
        print("\n✓ Migración completada exitosamente!")
        print(f"  - {Category.query.count()} categorías")
        print(f"  - {Member.query.count()} miembros")
        print(f"  - {ResearchSection.query.count()} secciones de investigación")
        print(f"  - {ResearchItem.query.count()} items de investigación")
        print(f"  - {SiteContent.query.count()} contenidos del sitio")


if __name__ == '__main__':
    migrate_data()
