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
from .User_Management.loginUser import loginUser_bp
from .User_Management.getUserProfile import getUserProfile_bp
from .User_Management.updateUserProfile import updateUserProfile_bp
from .User_Management.deleteUserProfile import deleteUserProfile_bp
from .User_Management.logoutUser import logout_bp

# ORDER_MANAGEMENT
from .Order_Management.createOrder import createOrder_bp

def init_app(app):
    # Menu_Management_registration
    app.register_blueprint(getHome_bp)
    app.register_blueprint(getAllflavors_bp)
    app.register_blueprint(addFlavor_bp)
    app.register_blueprint(deleteFlavor_bp)
    app.register_blueprint(updateFlavor_bp)
    app.register_blueprint(searchFlavor_bp)
    
    # User_Management_registration
    app.register_blueprint(registerUser_bp)
    app.register_blueprint(loginUser_bp)
    app.register_blueprint(getUserProfile_bp)
    app.register_blueprint(updateUserProfile_bp)
    app.register_blueprint(deleteUserProfile_bp)
    app.register_blueprint(logout_bp)
    
    # Order_Management_registration
    app.register_blueprint(createOrder_bp)