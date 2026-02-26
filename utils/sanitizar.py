import unicodedata

def sanitizar(text):
    # Pasar a minúsculas
    text = text.lower()

    # Normalizar el texto (separa letras de acentos)
    text = unicodedata.normalize("NFD", text)

    # Eliminar solo tildes y diéresis, pero conservar la ñ y otros caracteres especiales
    # Category "Mn" incluye tildes, pero excluimos el carácter base 'n' con tilde
    texto_limpio = []
    for i, c in enumerate(text):
        if unicodedata.category(c) == "Mn":
            # Verificar si el carácter base anterior forma parte de ñ
            if texto_limpio and texto_limpio[-1] == "n" and unicodedata.name(c, "") == "COMBINING TILDE":
                texto_limpio.append("n")  # mantenemos la ñ como "n" simplificada
            # Para otros acentos (tildes sobre vocales), simplemente los eliminamos
            continue
        texto_limpio.append(c)

    return "".join(texto_limpio)
