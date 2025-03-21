from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user


def role_required(*roles):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if not current_user.is_authenticated:
                    flash("Debes iniciar sesión para acceder a esta página.", "warning")
                    return redirect(url_for('auth.login'))
                
                # Si el usuario no es admin ni empleado, asumir que es cliente
                if "is_client" in roles and not current_user.is_admin and not current_user.is_employee:
                    return func(*args, **kwargs)

                if not any(getattr(current_user, role, False) for role in roles):
                    flash("No autorizado", "danger")
                    return redirect(url_for('no_autorizado'))
                    
                return func(*args, **kwargs)
            return wrapper
        return decorator