"""Colores ANSI opcionales, usando solo la biblioteca estándar."""

import os
import sys


COLORES = {
    "adn": "\033[92m",        # Verde
    "arn": "\033[96m",        # Cian
    "enzima": "\033[93m",     # Amarillo
    "proteina": "\033[95m",   # Magenta
    "titulo": "\033[94m",     # Azul
    "aviso": "\033[91m",      # Rojo
}
ACTIVO = False

COLORES_BASES = {
    "A": "\033[92m",  # Verde
    "C": "\033[94m",  # Azul
    "G": "\033[93m",  # Amarillo
    "T": "\033[91m",  # Rojo
    "U": "\033[95m",  # Magenta
}


def configurar_color(sin_color=False):
    """Desactiva ANSI si la salida va a un archivo o la consola no lo soporta."""
    global ACTIVO
    ACTIVO = (not sin_color and sys.stdout.isatty()
              and "NO_COLOR" not in os.environ and os.environ.get("TERM") != "dumb")
    if ACTIVO and os.name == "nt":
        # Windows requiere habilitar el procesamiento ANSI en la consola.
        import ctypes
        from ctypes import wintypes

        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel.GetStdHandle.argtypes = [wintypes.DWORD]
        kernel.GetStdHandle.restype = wintypes.HANDLE
        kernel.GetConsoleMode.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD)]
        kernel.SetConsoleMode.argtypes = [wintypes.HANDLE, wintypes.DWORD]
        consola = kernel.GetStdHandle(-11)  # Salida estándar.
        modo = wintypes.DWORD()
        ACTIVO = bool(kernel.GetConsoleMode(consola, ctypes.byref(modo))
                      and kernel.SetConsoleMode(consola, modo.value | 0x0004))


def colorear(texto, tipo):
    if not ACTIVO or not texto:
        return texto
    # Las secuencias de ADN y ARN usan el mismo color para cada base.
    # Las etiquetas (como [ARN]) mantienen el color de su categoría.
    if tipo in ("adn", "arn") and set(texto) <= set("ACGTU \n"):
        return colorear_bases(texto)
    return COLORES[tipo] + texto + "\033[0m"


def colorear_bases(secuencia):
    if not ACTIVO:
        return secuencia
    bases = []
    for base in secuencia:
        if base in COLORES_BASES:
            bases.append(COLORES_BASES[base] + base + "\033[0m")
        else:
            bases.append(base)
    return "".join(bases)
