from flask import Flask
from flask_cors import CORS
from app.core.db import iniciar_db

app = Flask(__name__)
CORS(app) # evita errores por tener puertos diferentes

iniciar_db()

from app import routes