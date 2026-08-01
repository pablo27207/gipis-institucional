import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///gipis.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB max upload

    # Cookies de sesión: SameSite mitiga CSRF en los POST; Secure solo
    # fuera de desarrollo (en local no hay HTTPS)
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_DEBUG') != '1'
    
    # Email SMTP (Gmail)
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'gipis.unp@gmail.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '')  # App Password de Gmail
    MAIL_DEFAULT_SENDER = ('GIPIS - Contacto Web', os.environ.get('MAIL_USERNAME', 'gipis.unp@gmail.com'))
    
    # Umami Analytics
    UMAMI_WEBSITE_ID = os.environ.get('UMAMI_WEBSITE_ID', '')
    UMAMI_SCRIPT_URL = os.environ.get('UMAMI_SCRIPT_URL', '/umami/script.js')
