# Backend/Routes/__init__.py
from .Menu_Management.getHome import getHome_bp
from .Menu_Management.getAllFlavors import getAllflavors_bp
from .Menu_Management.addFlavor import addFlavor_bp
from .Menu_Management.updateFlavor import updateFlavor_bp

def init_app(app):
    app.register_blueprint(getHome_bp)
    app.register_blueprint(getAllflavors_bp)
    app.register_blueprint(addFlavor_bp)
    app.register_blueprint(updateFlavor_bp)