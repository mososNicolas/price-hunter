from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
from datetime import date

# para evitar que no encuentre el modulo de obtener_producto
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.scrapers.mercadolibre import obtener_producto
from src.core.db import guardar_producto, iniciar_db

app = Flask(__name__)
CORS(app) # evita errores por tener puertos diferentes

iniciar_db()

@app.route('/api/track', methods=['POST'])
def track_product():
    data = request.get_json()

    if not data or 'url' not in data:
        return jsonify({"error": "Peticion invalida: Falta el campo 'url'"}), 400

    url_usuario = data['url']
    resultado = obtener_producto(url_usuario)
    
    if not resultado:
        return jsonify({"error": "No se pudo rastrear el producto"}), 400
    
    try:
        producto_db = {
            "titulo": resultado["titulo"],
            "precio": resultado["precio"],
            "imagen_url": resultado["imagen"],
            "producto_url": resultado["url"],
            "fecha": date.today().isoformat()
        }

        id_db = guardar_producto(producto_db)
        if id_db:
            print("Guardado con exito")
            resultado["id_db"] = id_db
        else:
            print("El producto no se ha pudo guardar en DB")
    except Exception as e:
        print(f"Error en guardar: {e}")

    print("resultados obtenidos :)")
    return jsonify(resultado), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)