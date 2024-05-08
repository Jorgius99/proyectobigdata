import subprocess
from datetime import datetime
from scraper import scrapear_datos
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver


def aceptar_cookies():
    # Configurar el navegador
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")  # Para ejecutar en segundo plano sin abrir una ventana
    driver = webdriver.Firefox(options=options)
    driver.get("https://www.expansion.com/mercados/cotizaciones/indices/ibex35_I.IB.html")

    try:
        # Esperar hasta que se encuentre el botón de aceptar cookies
        boton_cookies = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Aceptar')]"))
        )
        # Hacer clic en el botón de aceptar cookies
        boton_cookies.click()
    except:
        print("No se pudo encontrar el botón de aceptar cookies o hubo un error al hacer clic.")

    # Cerrar el navegador
    driver.quit()

def obtener_datos():
    # Aceptar cookies automáticamente antes de recopilar datos
    aceptar_cookies()

    datos_recopilados = scrapear_datos()
    datos_filtrados = []

    for datos in datos_recopilados:
        nombre_accion = datos[0]
        primer_valor = datos[1]
        ultima_cotizacion = datos[5]
        maximo_sesion = datos[6]
        minimo_sesion = datos[7]
        fecha_hora = datos[-1]

        datos_filtrados.append((nombre_accion, primer_valor, ultima_cotizacion, maximo_sesion, minimo_sesion, fecha_hora))

    return datos_filtrados

def generar_csv(datos, fecha_actual):
    nombre_archivo = f'datos_{fecha_actual}.csv'
    with open(nombre_archivo, 'a') as archivo:
        for dato in datos:
            archivo.write(','.join(dato) + '\n')

def generar_archivo():
    datos = obtener_datos()
    fecha_actual = datetime.now().strftime("%Y-%m-%d")

    generar_csv(datos, fecha_actual)

if __name__ == "__main__":
    generar_archivo()

