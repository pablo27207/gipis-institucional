from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor, iniciá sesión para acceder a esta página.'
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    
    from app.routes import main
    from app.routes import auth
    from app.routes import admin
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(admin.bp)

    from flask import session
    from app.i18n import translate, format_date

    @app.context_processor
    def inject_i18n():
        lang = session.get('lang', 'es')

        def loc(obj, field):
            """Contenido dinámico: versión _en si la interfaz está en inglés
            y existe traducción; si no, el original."""
            if lang == 'en':
                translated = getattr(obj, f'{field}_en', None)
                if translated:
                    return translated
            return getattr(obj, field)

        return {
            '_': lambda text: translate(text, lang),
            'current_lang': lang,
            'format_date': lambda dt, short=False: format_date(dt, lang, short),
            'loc': loc,
        }

    @app.errorhandler(413)
    def request_too_large(e):
        from flask import request, flash, redirect
        flash('El archivo es demasiado grande (máximo 10 MB). '
              'Reducí el tamaño de la imagen o PDF e intentá de nuevo.', 'error')
        return redirect(request.referrer or '/'), 303
    
    with app.app_context():
        db.create_all()
    
    return app
