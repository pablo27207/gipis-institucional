from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import Member

bp = Blueprint('auth', __name__, url_prefix='/auth')


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
        
        # Manejar cambio de contraseña
        new_password = request.form.get('new_password')
        if new_password:
            current_user.set_password(new_password)
        
        db.session.commit()
        flash('Perfil actualizado correctamente', 'success')
        return redirect(url_for('auth.dashboard'))
    
    return render_template('auth/edit_profile.xhtml')
