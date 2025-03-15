import os

from flask import send_from_directory

from app.controllers.project_controller import project_blueprint


def register_routes(app):
    app.register_blueprint(project_blueprint)

    @app.route('/static/<path:filename>')
    def static_files(filename):
        return send_from_directory(os.path.join(app.root_path, 'static'), filename)