import os

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from sqlalchemy import func
from werkzeug.security import check_password_hash, generate_password_hash

from app.config.db import db
from app.models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username').strip().lower()
        password = request.form.get('password')
        
        user = User.query.filter(func.lower(User.username) == username).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Inicio de sesión exitoso", "success")
            return redirect('/')
        
        flash("Usuario o contraseña incorrectos", "danger")

    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash("Las contraseñas no coinciden", "danger")
            return redirect(url_for('auth.register'))
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("El usuario ya existe", "warning")
            return redirect(url_for('auth.register'))

        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
        secret_key = os.urandom(24).hex()

        new_user = User(username=username, password=hashed_password, secret_key=secret_key, is_admin=False)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registro exitoso, ahora puedes iniciar sesión", "success")
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada exitosamente", "info")
    return redirect(url_for('auth.login'))