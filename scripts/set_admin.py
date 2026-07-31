"""
Asignar (o quitar) rol de administrador a un miembro por email.

Uso:
    python scripts/set_admin.py usuario@dominio.com
    python scripts/set_admin.py usuario@dominio.com --revoke
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import Member


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    email = sys.argv[1]
    revoke = '--revoke' in sys.argv

    app = create_app()
    with app.app_context():
        member = Member.query.filter_by(email=email).first()
        if not member:
            print(f"No existe un miembro con email {email}")
            sys.exit(1)

        member.role = 'member' if revoke else 'admin'
        db.session.commit()
        print(f"{member.name} ahora tiene rol '{member.role}'.")


if __name__ == '__main__':
    main()
