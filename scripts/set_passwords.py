"""Script para establecer contraseñas iniciales a los miembros existentes."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import Member

app = create_app()

# Contraseña por defecto (los usuarios deberán cambiarla)
DEFAULT_PASSWORD = "gipis2024"

with app.app_context():
    members = Member.query.all()
    
    if not members:
        print("No hay miembros en la base de datos.")
    else:
        print(f"Encontrados {len(members)} miembros.")
        print(f"Estableciendo contraseña por defecto: {DEFAULT_PASSWORD}")
        print("-" * 50)
        
        for member in members:
            if not member.password_hash:
                member.set_password(DEFAULT_PASSWORD)
                print(f"✅ Contraseña establecida para: {member.name} ({member.email})")
            else:
                print(f"⏭️  Ya tiene contraseña: {member.name}")
        
        db.session.commit()
        print("-" * 50)
        print("✅ Proceso completado.")
        print(f"\nLos miembros pueden ingresar con su email y la contraseña: {DEFAULT_PASSWORD}")
        print("Se recomienda que cambien la contraseña después de ingresar.")
