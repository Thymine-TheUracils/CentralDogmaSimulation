import argparse
import sys
from textwrap import fill
from colores import colorear, configurar_color

from utils import crear_adn, validar_adn
from replicacion import replicar
from transcripcion import transcribir
from traduccion import traducir
from visualizacion import (
    mostrar_apertura,
    mostrar_direcciones,
    mostrar_cebador_y_extension,
    mostrar_transcripcion,
    mostrar_lectura_arn,
)


# Ejemplo artificial de 60 bases: inicio ATG y terminación TAA.
ADN_EJEMPLO = (
    "ATGGCTTTTGAACCGAAAGGTTACTGCAAT"
    "CTGAGCGTTCATACCGACCAATGGGGATAA"
)
ANCHO = 78
BASES_POR_LINEA = 48


def titulo(texto):
    print("\n" + "=" * ANCHO)
    print(colorear(texto, "titulo"))
    print("=" * ANCHO)


def explicar(texto, tipo=None):
    texto = fill(texto, width=ANCHO)
    print(colorear(texto, tipo) if tipo else texto)


def mostrar_secuencia(secuencia, sentido="5-3", desplazamiento=0, tipo="adn"):
    """Divide la cadena sin añadir extremos a los cortes de visualización."""
    extremo_inicial, extremo_final = sentido.split("-")
    for inicio in range(0, len(secuencia), BASES_POR_LINEA):
        tramo = secuencia[inicio:inicio + BASES_POR_LINEA]
        izquierda = extremo_inicial + "'" if inicio == 0 and desplazamiento == 0 else "  "
        derecha = extremo_final + "'" if inicio + len(tramo) == len(secuencia) else ""
        print(f"  {desplazamiento + inicio + 1:>4}-{desplazamiento + inicio + len(tramo):<4}  "
              f"{izquierda} {colorear(tramo, tipo)} {derecha}".rstrip())


def mostrar_adn(adn):
    """Mantiene alineadas las dos hebras en cada bloque."""
    superior = adn["superior_5_3"]
    inferior = adn["inferior_3_5"]
    for inicio in range(0, len(superior), BASES_POR_LINEA):
        fin = min(inicio + BASES_POR_LINEA, len(superior))
        print(f"  Bases {inicio + 1}-{fin}")
        izq_superior, izq_inferior = ("5'", "3'") if inicio == 0 else ("  ", "  ")
        der_superior, der_inferior = ("3'", "5'") if fin == len(superior) else ("", "")
        print(f"  {izq_superior} {colorear(superior[inicio:fin], 'adn')} {der_superior}".rstrip())
        print(f"  {izq_inferior} {colorear(inferior[inicio:fin], 'adn')} {der_inferior}".rstrip())


def mostrar_sintesis(sintesis, cebador_derecha=False):
    mostrar_cebador_y_extension(sintesis, cebador_derecha)
    if not sintesis["extension_adn"]:
        print("  Sin extensión: el cebador ocupa todo el fragmento.")
    print("  ADN tras reemplazar el cebador:")
    mostrar_secuencia(sintesis["adn_final"])


def seleccionar_adn():
    titulo("SELECCIONAR SECUENCIA DE ADN")
    print("  1. Ejemplo didáctico (60 bases, inicio ATG y parada TAA)")
    print("  2. Introducir mi propia cadena")

    while True:
        opcion = input("\nElige una opción (1 o 2): ").strip()
        if opcion == "1":
            return ADN_EJEMPLO
        if opcion == "2":
            break
        print(colorear("Opción inválida. Escribe 1 o 2.", "aviso"))

    explicar("Introduce la hebra codificante de ADN en sentido 5' -> 3', "
             "solo con A, C, G y T. Se aceptan minúsculas y espacios. "
             "La hebra complementaria se construirá automáticamente.")
    while True:
        secuencia = input("\nTu cadena de ADN: ")
        try:
            return validar_adn(secuencia)
        except ValueError as error:
            print(colorear(f"Error: {error} Vuelve a introducir la cadena.", "aviso"))


def leer_argumentos():
    parser = argparse.ArgumentParser(
        description="Simulador didáctico: ADN -> ADN -> ARNm -> proteína.",
        epilog="Ejemplo: python main.py --adn ATGCCGTAA --fragmento 4 --cebador 2",
    )
    secuencias = parser.add_mutually_exclusive_group()
    secuencias.add_argument("--ejemplo", action="store_true",
                           help="usa el ejemplo de 60 bases sin mostrar el menú")
    secuencias.add_argument("--adn", metavar="SECUENCIA",
                           help="usa tu hebra codificante 5' -> 3' sin mostrar el menú")
    parser.add_argument("--fragmento", type=int, default=12, metavar="N",
                        help="bases por fragmento de Okazaki (por defecto: 12)")
    parser.add_argument("--cebador", type=int, default=3, metavar="N",
                        help="bases por cebador (por defecto: 3)")
    parser.add_argument("--sin-color", action="store_true",
                        help="desactiva los colores de la consola")
    modos = parser.add_mutually_exclusive_group()
    modos.add_argument("--resumen", action="store_true",
                       help="muestra los resultados sin el detalle de la síntesis")
    modos.add_argument("--paso-a-paso", action="store_true",
                       help="pausa entre etapas y posiciones de la helicasa; requiere consola interactiva")
    opciones = parser.parse_args()
    if opciones.fragmento <= 0:
        parser.error("--fragmento debe ser un entero positivo.")
    if not 1 <= opciones.cebador <= opciones.fragmento:
        parser.error("--cebador debe estar entre 1 y --fragmento.")
    if opciones.adn is not None:
        try:
            validar_adn(opciones.adn)
        except ValueError as error:
            parser.error(str(error))
    if opciones.paso_a_paso and not sys.stdin.isatty():
        parser.error("--paso-a-paso requiere una consola interactiva.")
    return opciones


def pausar(opciones):
    if opciones.paso_a_paso:
        input("\nPulsa Enter para continuar...")


def main():
    opciones = leer_argumentos()
    configurar_color(opciones.sin_color)
    if opciones.ejemplo:
        secuencia = ADN_EJEMPLO
    elif opciones.adn is not None:
        secuencia = opciones.adn
    else:
        secuencia = seleccionar_adn()
    adn_original = crear_adn(secuencia)

    titulo("SIMULACIÓN DEL DOGMA CENTRAL")
    explicar("Modelo didáctico de una región de ADN. Las hebras son complementarias "
             "(A-T y C-G) y antiparalelas. Los tamaños de fragmentos y cebadores son didácticos.")
    print(f"\nADN: {len(adn_original['superior_5_3'])} pares de bases | "
          f"Fragmento: {opciones.fragmento} bases | Cebador: {opciones.cebador} bases")
    print("\nADN original:")
    mostrar_adn(adn_original)

    pausar(opciones)
    titulo("1. REPLICACIÓN | ADN -> ADN")
    if not opciones.resumen:
        explicar("La helicasa separa las hebras. La horquilla avanza de izquierda a derecha. "
                 "La primasa crea un cebador de ARN. La ADN polimerasa añade ADN "
                 "al extremo 3' del cebador, leyendo el molde 3' -> 5' y sintetizando "
                 "la nueva hebra 5' -> 3'.")
        mostrar_apertura(adn_original, opciones.paso_a_paso)
        mostrar_direcciones()

    resultado = replicar(adn_original, opciones.fragmento, opciones.cebador)
    if not opciones.resumen:
        print("\nHEBRA LÍDER | síntesis continua")
        explicar("Usa la hebra inferior como molde y crece en el sentido de la horquilla.")
        mostrar_sintesis(resultado["sintesis_lider"])
        print("\nHEBRA REZAGADA | síntesis discontinua")
        explicar("Usa la hebra superior como molde. Cada fragmento crece contra el avance "
                 "de la horquilla y necesita su propio cebador. Los moldes se muestran "
                 "invertidos, en el sentido de lectura 3' -> 5'. Por eso, en los esquemas "
                 "locales de abajo, la síntesis se dibuja hacia la derecha.")
        for numero, fragmento in enumerate(resultado["fragmentos_okazaki"], start=1):
            longitud = len(fragmento["adn_final"])
            unidad = "base" if longitud == 1 else "bases"
            print(f"\n  Fragmento de Okazaki {numero} ({longitud} {unidad})")
            mostrar_sintesis(fragmento, cebador_derecha=True)
        explicar("Se retiran los cebadores y se rellena su región con ADN. La ligasa "
                 "sella las uniones entre fragmentos. El último fragmento puede ser más "
                 "corto y su cebador se limita al molde disponible.")
        print("\nRezagada unida (5' -> 3'):")
        mostrar_secuencia(resultado["rezagada_5_3"])

    print(f"\nResultado: 2 moléculas hijas; {len(resultado['fragmentos_okazaki'])} fragmentos de Okazaki.")
    explicar("Replicación semiconservativa: cada hija contiene una hebra original y una nueva.")
    for numero, hija in enumerate(resultado["hijas"], start=1):
        origen = "superior original, inferior nueva" if numero == 1 else "superior nueva, inferior original"
        print(f"\nHija {numero}: {origen}.")
        mostrar_adn(hija)

    pausar(opciones)
    titulo("2. TRANSCRIPCIÓN | ADN -> ARNm")
    adn_molde = resultado["hijas"][0]
    arn = transcribir(adn_molde)
    if not opciones.resumen:
        explicar("La ARN polimerasa usa la hebra inferior de la primera hija como molde. "
                 "Lee 3' -> 5' y sintetiza ARNm 5' -> 3', sin cebador. "
                 "Complementariedad: A -> U, T -> A, C -> G y G -> C.")
        print("\nHebra molde:")
        mostrar_secuencia(adn_molde["inferior_3_5"], "3-5")
        mostrar_transcripcion(adn_molde, arn)
    print(f"\nARNm obtenido ({len(arn)} bases):")
    mostrar_secuencia(arn, tipo="arn")
    if not opciones.resumen:
        explicar("Coincide con la hebra codificante cambiando T por U. Transcribimos "
                 "toda la región, sin modelar promotores, terminadores ni procesamiento del ARN.")

    pausar(opciones)
    titulo("3. TRADUCCIÓN | ARNm -> proteína")
    if not opciones.resumen:
        explicar("El ribosoma comienza en el primer AUG y lee codones 5' -> 3'. "
                 "Los ARNt reconocen los codones con sus anticodones y aportan aminoácidos. "
                 "El ribosoma cataliza los enlaces peptídicos. En UAA, UAG o UGA "
                 "actúan factores de liberación, sin añadir un aminoácido.")
    traduccion = traducir(arn)
    if not opciones.resumen:
        mostrar_lectura_arn(traduccion)
    if traduccion["inicio"] is not None:
        print(f"\nInicio AUG: base {traduccion['inicio'] + 1} del ARNm (posiciones desde 1).")
        if not opciones.resumen:
            print("\n  Nº   Bases ARNm   Codón   Aminoácido")
            print("  " + "-" * 48)
            for numero, codon in enumerate(traduccion["codones"], start=1):
                posicion = traduccion["inicio"] + (numero - 1) * 3 + 1
                aminoacido = (traduccion["aminoacidos"][numero - 1]
                              if numero <= len(traduccion["aminoacidos"]) else "STOP")
                tipo = "aviso" if aminoacido == "STOP" else "proteina"
                print(f"  {numero:>2}   {posicion:>4}-{posicion + 2:<4}    "
                      f"{colorear(codon, 'arn')}     {colorear(aminoacido, tipo)}")
        if traduccion["codon_terminacion"]:
            print(f"\nParada: {traduccion['codon_terminacion']} | cadena liberada.")
            print("Proteína sintetizada:")
        else:
            print("\nCadena parcial (sin señal de terminación):")
        explicar("-".join(traduccion["aminoacidos"]), "proteina")
        print(f"Longitud: {len(traduccion['aminoacidos'])} aminoácidos.")
    else:
        print("\nNo se obtiene una cadena de aminoácidos.")
    for aviso in traduccion["avisos"]:
        explicar("AVISO: " + aviso, "aviso")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nSimulación interrumpida.")
        sys.exit(130)
