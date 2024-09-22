from flask import Flask
from flask_cors import CORS
from config import Config
from logging_config import configure_logging
import logging

logger = logging.getLogger(__name__)

def create_app():
    # Configure logging before creating the app
    configure_logging()
    logger.info("Configuring logging")

    app = Flask(__name__)
    
    # CORS configuration
    CORS(app)
    logger.info("CORS initialised")

    app.config.from_object(Config)
    logger.info("Flask app created and configured")

    # Initialize extensions if any (e.g., database, login manager)

    # Register Blueprints or Routes
    from routes.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    logger.info("Registered main blueprint")

    logger.info("App creation completed")
    return app

if __name__ == '__main__':
    logger.info("Starting the application")
    app = create_app()
    app.run(debug=True, port=5000)
    logger.info("Application started")
