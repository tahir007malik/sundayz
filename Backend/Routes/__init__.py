# Backend/Routes/__init__.py
# MENU_MANAGEMENT
from .Menu_Management.getHome import getHome_bp
from .Menu_Management.getAllFlavors import getAllflavors_bp
from .Menu_Management.addFlavor import addFlavor_bp
from .Menu_Management.deleteFlavor import deleteFlavor_bp
from .Menu_Management.updateFlavor import updateFlavor_bp
from .Menu_Management.searchFlavor import searchFlavor_bp

# USER_MANAGEMENT
from .User_Management.registerUser import registerUser_bp

def init_app(app):
    # Menu_Management_registration
    app.register_blueprint(getHome_bp)
    app.register_blueprint(getAllflavors_bp)
    app.register_blueprint(addFlavor_bp)
    app.register_blueprint(deleteFlavor_bp)
    app.register_blueprint(updateFlavor_bp)
    app.register_blueprint(searchFlavor_bp)
    
    # Menu_Management_registration
    app.register_blueprint(registerUser_bp)