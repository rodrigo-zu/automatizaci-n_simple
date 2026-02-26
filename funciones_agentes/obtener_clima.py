import requests

API_KEY = "75e1d70f95b0625984d0ce578f630b0c"

# Frases a limpiar para extraer la ciudad — orden importa: primero frases largas
FRASES_A_ELIMINAR = [
    "quiero saber cual es",
    "quiero saber",
    "dime el clima en",
    "dime la temperatura en",
    "dame el clima en",
    "dame la temperatura en",
    "cual es el clima en",
    "cual es la temperatura en",
    "el clima en",
    "la temperatura en",
    "el tiempo en",
    "clima en",
    "temperatura en",
    "tiempo en",
    "el clima",
    "la temperatura",
    "el tiempo",
    "clima",
    "temperatura",
    "tiempo",
]

# Ciudades/países cuyo nombre en español no reconoce bien la API de OpenWeatherMap
TRADUCCIONES_CIUDAD = {
    "nueva delhi": "New Delhi",
    "nueva york": "New York",
    "nueva orleans": "New Orleans",
    "los angeles": "Los Angeles",
    "san francisco": "San Francisco",
    "ciudad de mexico": "Mexico City",
    "tokio": "Tokyo",
    "moscu": "Moscow",
    "pekin": "Beijing",
    "seul": "Seoul",
    # Si escriben solo el país, asumimos la capital
    "india": "New Delhi",
    "japon": "Tokyo",
    "china": "Beijing",
    "rusia": "Moscow",
    "corea": "Seoul",
    "alemania": "Berlin",
    "francia": "Paris",
    "italia": "Rome",
    "reino unido": "London",
    "estados unidos": "New York",
    "canada": "Ottawa",
    "australia": "Sydney",
    "brasil": "Brasilia",
    "argentina": "Buenos Aires",
}

def extraer_ciudad(consulta):
    texto = consulta
    for frase in FRASES_A_ELIMINAR:
        texto = texto.replace(frase, " ")
    ciudad = " ".join(texto.split())
    return TRADUCCIONES_CIUDAD.get(ciudad.lower(), ciudad)

def obtener_clima(driver, consulta):
    ciudad = extraer_ciudad(consulta)

    if not ciudad:
        return "No pude identificar la ciudad. Intenta con: 'clima en Madrid'."

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": ciudad,
        "appid": API_KEY,
        "units": "metric",
        "lang": "es"
    }
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        data = response.json()

        if response.status_code != 200:
            mensaje_error = data.get("message", "error desconocido")
            return f"No se pudo obtener el clima: {mensaje_error}. ¿Escribiste bien el nombre de la ciudad?"

        temperatura = data["main"]["temp"]
        estado = data["weather"][0]["description"]
        ciudad_nombre = data["name"]
        pais = data["sys"]["country"]

        return f"El clima en {ciudad_nombre}, {pais} es {estado} con {temperatura}°C."

    except requests.exceptions.Timeout:
        return "La solicitud tardó demasiado. Verifica tu conexión a internet."
    except Exception as e:
        return f"Error inesperado al obtener el clima: {e}"
