import sqlite3
from datetime import date,datetime
import re
DB_NAME="database.db"
#variable de la db

def conexion_db():
    return sqlite3.connect(DB_NAME)
    #conexion a la base de datos

def iniciar_db():
        try:
            conn = conexion_db()
            cursor = conn.cursor()
            cursor.execute("""
                    CREATE TABLE IF NOT EXISTS PRODUCTOS (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    precio REAL NOT NULL,
                    imagen_url TEXT,
                    producto_url TEXT NOT NULL,
                    fecha DATE NOT NULL
                )
            """)
            conn.commit()  
            conn.close()
            print("Base de datos iniciada correctamente") 
            #Funcion de inicializacion de la bd para ver si reacciona y funciona correctamente
        except sqlite3.Error as e :
            print(f"sql error {e}")
            #mensaje por si hay un error en el sql a la hora de comunicarse con la bd
        except Exception as e:
            print(f"ocurrio un error al iniciar la base de datos \n error : {e}")
            #mensaje por si hay un error mas general con el python 

datos={
     "titulo" : str,
     "precio" : float,
     "imagen_url" : str,
     "producto_url" : str,
     "fecha" : str
}
#dict para guardar la info de las consultas en python para despues pasarlas a sqlite

def validar_producto(datos): #FUNCION IMPORTANTE PREGUNTAR POR ALGUN ERROR MEJORA O DUDA
    #Validacion de null o de datos vacios o flotantes 
    campos_obligatorios=("titulo","precio","producto_url","fecha")
    for campo in campos_obligatorios:
        if campo not in datos:
            return False, f"Falta el campo obligatorio: '{campo}'"
        if datos[campo] is None or datos[campo] == "":
            return False, f"El campo '{campo}' no puede estar vacío"
        #coge los campos de los datos y verifica que tengan datos o que no esten vacios
        
    #Validaciones de cada campo
    titulo = datos["titulo"].strip()
    if len(titulo) < 3:
            return False, "El título debe tener al menos 3 caracteres"
    if len(titulo) > 500:
            return False, "El título no puede exceder 500 caracteres"
        #Validacion de titulo para evitar invalidaciones o extracciones erronres POR SI ACASO
    
    try: #IMPORTANTE
        precio = float(datos["precio"])
        if precio <= 0:
            return False, "El precio debe ser mayor a 0"
        if precio > 999999999:  # 999 millones
            return False, "El precio es demasiado alto (máximo 999,999,999)"
    except (ValueError, TypeError):
        return False, "El precio debe ser un número válido"
        #Validacion de precios por si hay algun numero invalido o un negativo o cantidades exageradas o irreales
    
    
    producto_url = datos["producto_url"].strip()
    
    # Verificar que sea URL de MercadoLibre
    patron_ml = r'^https?://.*mercadolibre\.com\.(co)/.*'
    if not re.match(patron_ml, producto_url):
        return False, "URL invalida "
        #Validacion para que todas las url sean de mercado libre  para eso imnporte re para el patron y no complicarme con difflib

    if len(producto_url) > 1000:
        return False, "La URL es demasiado larga"
        #el mismo mensaje dice para que sirve
     
    try:
        fecha_str = datos["fecha"]
        # Intentar parsear la fecha en formato YYYY-MM-DD
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
        
        # Verificar que no sea una fecha futura
        hoy = datetime.now()
        if fecha > hoy:
            return False, "La fecha no puede ser futura"
    except ValueError:
        return False, "La fecha debe estar en formato YYYY-MM-DD"
        #funcion para verificar la fecha que no sea invalida o erronea o sea introducida en un mal formato
     
    return True, ""

def guardar_producto(datos): #FUNCION IMPORTANTE PREGUNTAR POR ALGUN ERROR MEJORA O DUDA
    
    es_valido, error = validar_producto(datos)
    if not es_valido:
        print(f"❌ Validación fallida: {error}")
        return None
        #primero se validan los datos antes de subirlos o insertarlos en la bd
    try:
        conn = conexion_db()
        cursor = conn.cursor()
        
        # Los datos ya están validados es solo insertar en la bd
        cursor.execute("""
            INSERT INTO PRODUCTOS (titulo, precio, imagen_url, producto_url, fecha)
            VALUES (?, ?, ?, ?, ?)
        """, (
            datos["titulo"].strip(),
            float(datos["precio"]),
            datos.get("imagen_url", None),
            datos["producto_url"].strip(),
            datos["fecha"]
        ))
        
        conn.commit()
        producto_id = cursor.lastrowid
        conn.close()
        
        print(f"Producto guardado con ID: {producto_id}")
        return producto_id
        
    except sqlite3.Error as e:
        print(f" Error en base de datos: {e}")
        return None
    except Exception as e:
        print(f" Error inesperado: {e}")
        return None