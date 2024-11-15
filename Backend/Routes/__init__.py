# Backend/Routes/__init__.py
from .home import home_bp
from .flavor import flavor_bp
from .order import order_bp

def init_app(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(flavor_bp)
    app.register_blueprint(order_bp)