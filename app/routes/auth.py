import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.models import Member

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

