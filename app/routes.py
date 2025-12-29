from flask import request, jsonify, render_template
from app import app
import sys
import os
from datetime import date

# para evitar que no encuentre el modulo de obtener_producto
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.scrapers.mercadolibre import obtener_producto
from app.core.db import guardar_producto

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/api/track', methods=['POST'])
def track_product():
    url_sucia = request.form.get('url')
    url = url_sucia.split('#')[0].split('?')[0]

    if not url: 
        return "Error: Falta la URl", 400 

    resultado = obtener_producto(url)
    
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
            resultado["id_db"] = id_db
        else:
            print("El producto no se ha podido guardar en DB")
    except Exception as e:
        print(f"Error en guardar: {e}")

    return jsonify(resultado), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)