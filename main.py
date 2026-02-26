from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from utils.sanitizar import sanitizar
from funciones_agentes.obtener_clima import obtener_clima
from funciones_agentes.obtener_precio_accion import obtener_precio_accion

# Configuración de Selenium
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.4472.124 Safari/537.36")
options.add_argument('--disable-blink-features=AutomationControlled')

# Inicialización del driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# ---------------------------
# Procesador de intención
# ---------------------------
def procesar_input(user_input):
    if any(palabra in user_input for palabra in ["clima", "temperatura", "tiempo"]):
        return obtener_clima
    elif any(palabra in user_input for palabra in ["precio", "accion", "acciones", "valor", "bolsa"]):
        return obtener_precio_accion
    return None


# ---------------------------
# Loop principal del chatbot
# ---------------------------
print("Hola, soy tu asistente virtual. ¿En qué puedo ayudarte hoy?")
print("Ejemplos: 'clima en Madrid', 'precio de Apple'\n")

while True:
    try:
        user_input = sanitizar(input("---> "))
    except (EOFError, KeyboardInterrupt):
        print("\nHasta luego 👋")
        break

    if not user_input:
        continue

    if user_input in ["salir", "exit", "q"]:
        print("Hasta luego 👋")
        break

    funcion_agente = procesar_input(user_input)

    if funcion_agente is None:
        print("No entendí tu solicitud. Prueba con: 'clima en [ciudad]' o 'precio de [empresa]'.\n")
    else:
        respuesta = funcion_agente(driver, user_input)
        print(f">>> {respuesta}\n")


# ---------------------------
# Cierre del navegador
# ---------------------------
driver.quit()
