import yfinance as yf
import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
}

# Frases a limpiar — orden importa: primero frases largas
FRASES_A_ELIMINAR = [
    "quiero saber cual es",
    "quiero saber",
    "dime el precio de",
    "dame el precio de",
    "cual es el precio de",
    "el precio de",
    "precio de",
    "acciones de",
    "accion de",
    "valor de",
    "bolsa de",
    "precio",
    "accion",
    "acciones",
    "valor",
    "bolsa",
]

def extraer_empresa(consulta):
    texto = consulta
    for frase in FRASES_A_ELIMINAR:
        texto = texto.replace(frase, " ")
    return " ".join(texto.split())

def buscar_ticker(empresa):
    """Busca el ticker de una empresa usando Yahoo Finance search."""
    url = "https://query1.finance.yahoo.com/v1/finance/search"
    params = {"q": empresa, "quotesCount": 1, "newsCount": 0}
    response = requests.get(url, params=params, headers=HEADERS, timeout=10)
    data = response.json()
    quotes = data.get("quotes", [])
    if not quotes:
        return None
    return quotes[0].get("symbol")

def obtener_precio_accion(driver, consulta):
    empresa = extraer_empresa(consulta)

    if not empresa:
        return "No pude identificar la empresa. Intenta con: 'precio de Apple'."

    try:
        # Paso 1: obtener el ticker
        ticker = buscar_ticker(empresa)
        if not ticker:
            return f"No encontré resultados para '{empresa}'. Verifica el nombre de la empresa."

        # Paso 2: usar yfinance para obtener el precio (maneja auth internamente)
        accion = yf.Ticker(ticker)
        info = accion.fast_info

        precio = info.last_price
        divisa = info.currency
        nombre = accion.info.get("longName") or accion.info.get("shortName", ticker)

        if precio is None:
            return f"No se pudo obtener el precio actual de {ticker}."

        return f"{nombre} [{ticker}]: ${precio:.2f} {divisa}."

    except requests.exceptions.Timeout:
        return "La solicitud tardó demasiado. Verifica tu conexión a internet."
    except Exception as e:
        return f"Error inesperado al obtener el precio: {e}"
