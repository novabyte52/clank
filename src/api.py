"""
poop
"""
from flask import Flask
from .routes.main_routes import register_routes

app = Flask(__name__)

# Register routes
register_routes(app)
