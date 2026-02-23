from flask import Flask

from app.webhook.routes import webhook
from .frontend import main_bp   

# Creating our flask app
def create_app():

    app = Flask(__name__)
    
    # registering all the blueprints
    app.register_blueprint(webhook)
    app.register_blueprint(main_bp)    # The new frontend UI
    
    return app
