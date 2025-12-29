import os 
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv 

load_dotenv()

def obtener_producto(url):
    # version temporal con cookie en el env, sin esta cookie el scraper no funcionara
    cookie = os.getenv("ML_COOKIE")

    if not cookie:
        print("ERROR: No se encontro la variable ML_COOKIE en el archivo .env")
        return None 
    
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
        'Cookie': cookie
    }

    try:
        r = requests.get(url, headers=headers)
        if r.status_code != 200 :
            print("Nos bloquearon o la pagina no existe")
            return None 
        
        soup = BeautifulSoup(r.text, 'html.parser')

        # obtener el titulo
        tag_titulo = soup.find("h1","ui-pdp-title")
        if not tag_titulo:
            print("No se ha encontrado el titulo")
            return None
        titulo = tag_titulo.get_text(strip=True)

        # obtener el precio
        tag_precio = soup.find("meta",attrs={'itemprop':'price'})
        if tag_precio:
            precio = float(tag_precio["content"])
        else:
            print("No se encontro el precio")
            return None
        
        # obtener la imagen del producto
        tag_img = soup.find("meta", attrs={'property':'og:image'})
        if tag_img:
            img_url = tag_img["content"]
        else:
            print("No se encontro la imagen")
            return None
        
        # retornamos el producto
        resultado = {
            "titulo": titulo,
            "precio": precio,
            "imagen": img_url,
            "url": url
        }

        return resultado

    except Exception as e:
        print(e)
        return None 

# bloque de prueba para el modulo 

if __name__ == "__main__" : 
    url_prueba = "https://www.mercadolibre.com.co/audifonos-sony-inalambricos-in-ear-wi-c100-color-azul/p/MCO26990277#polycard_client=recommendations_home_top-sales-highlights-recommendations&reco_backend=top_sales_highlights&wid=MCO1342642113&reco_client=home_top-sales-highlights-recommendations&reco_item_pos=2&reco_backend_type=function&reco_id=903c741d-d46b-464b-bf3b-402e281bc780&sid=recos&c_id=/home/top-sales-first-recommendations/element&c_uid=a0f88372-99ee-47c3-a762-632a66d7f11e"
    datos = obtener_producto(url_prueba)
    
    if datos:
        print("Datos cargados correctamente")
        print(datos)
    else:
        print("Fallo")
