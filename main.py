from utils import crear_adn
from replicacion import replicar
from transcripcion import transcribir
from traduccion import traducir


def mostrar_adn(adn):
    print("5' —", adn["superior_5_3"], "— 3'")
    print("3' —", adn["inferior_3_5"], "— 5'")


def main():
    # Ejemplo artificial de 60 bases: inicio ATG y terminación TAA.
    adn_original = crear_adn(
        "ATGGCTTTTGAACCGAAAGGTTACTGCAAT"
        "CTGAGCGTTCATACCGACCAATGGGGATAA"
    )

    print("SIMULACIÓN DEL DOGMA CENTRAL")
    print("Modelo didáctico: una región corta de ADN y una horquilla de replicación.")
    print("Las hebras son complementarias (A-T y C-G) y antiparalelas.")
    print("\nADN original:")
    mostrar_adn(adn_original)

    print("\n1. REPLICACIÓN: ADN -> ADN")
    print("La helicasa separa las dos hebras; cada una sirve como molde.")
    print("Suponemos que la horquilla avanza de izquierda a derecha.")
    print("La ADN polimerasa lee el molde 3' -> 5' y sintetiza ADN 5' -> 3'.")
    print("Necesita un extremo 3' al que añadir bases: la primasa aporta un cebador de ARN.")

    resultado = replicar(
        adn_original,
        tam_fragmento=12,
        tam_cebador=3,
    )

    lider = resultado["sintesis_lider"]

    print("\nSíntesis de la hebra líder:")
    print("Usa la hebra inferior como molde y crece en el sentido de la horquilla.")
    print("La síntesis es continua a partir de un cebador.")
    print("Molde:        3' -", lider["molde_3_5"], "- 5'")
    print("Cebador ARN:  5' -", lider["cebador_arn"], "- 3'")
    print("Extensión ADN (continúa el cebador):", lider["extension_adn"] or "(sin extensión)")
    print("Tras retirar el cebador y rellenar su región con ADN:")
    print("ADN final:    5' -", lider["adn_final"], "- 3'")

    print("\nFragmentos de Okazaki — cada uno escrito 5' -> 3':")
    print("La hebra superior es el molde de la rezagada.")
    print("Cada fragmento crece contra el avance de la horquilla y necesita su cebador.")
    print("Invertimos cada región del molde para mostrarla en el sentido de lectura 3' -> 5'.")

    for numero, fragmento_okazaki in enumerate(
        resultado["fragmentos_okazaki"],
        start=1,
    ):
        print(f"Fragmento {numero}:")
        print("  Molde: 3' -", fragmento_okazaki["molde_3_5"], "- 5'")
        print("  Cebador ARN:", fragmento_okazaki["cebador_arn"])
        print("  Extensión ADN:", fragmento_okazaki["extension_adn"] or "(sin extensión)")
        print("  ADN final:", fragmento_okazaki["adn_final"])

    print("El último fragmento puede ser más corto; su cebador se limita al molde disponible.")
    print("La retirada de los cebadores y el relleno con ADN se agrupan en reemplazar_cebador.")
    print("La ligasa sella las uniones entre los fragmentos de ADN.")
    print("Hebra rezagada unida: 5' -", resultado["rezagada_5_3"], "- 3'")
    print("\nLa replicación es semiconservativa: cada hija conserva una hebra original.")

    for numero, hija in enumerate(resultado["hijas"], start=1):
        print(f"\nMolécula hija {numero}:")
        if numero == 1:
            print("Superior original; inferior nueva (rezagada).")
        else:
            print("Superior nueva (líder); inferior original.")
        mostrar_adn(hija)

    adn_para_transcribir = resultado["hijas"][0]
    arn = transcribir(adn_para_transcribir)

    print("\n2. TRANSCRIPCIÓN: ADN -> ARNm")
    print("Elegimos la hebra inferior de la primera hija como molde.")
    print("La ARN polimerasa lee el molde 3' -> 5' y sintetiza ARNm 5' -> 3'.")
    print("Puede iniciar la síntesis sin un cebador.")
    print("Complementariedad del molde al ARN: A -> U, T -> A, C -> G y G -> C.")
    print("Molde: 3' -", adn_para_transcribir["inferior_3_5"], "- 5'")
    print("ARNm transcrito:")
    print("5' —", arn, "— 3'")
    print("Coincide con la hebra superior codificante, sustituyendo T por U.")
    print("En este modelo transcribimos toda la región, sin simular promotores ni terminadores.")
    print("\n3. TRADUCCIÓN: ARNm -> proteína")
    print("En este modelo, el ribosoma comienza en el primer AUG y lee codones 5' -> 3'.")
    print("Los ARNt aportan los aminoácidos al reconocer los codones con sus anticodones.")
    print("El ribosoma cataliza los enlaces peptídicos entre los aminoácidos.")
    print("UAA, UAG y UGA son señales de parada: actúan factores de liberación, no ARNt.")

    traduccion = traducir(arn)

    if traduccion["inicio"] is not None:
        print("Inicio AUG en la posición:", traduccion["inicio"] + 1)
        for codon, aminoacido in zip(
            traduccion["codones"], traduccion["aminoacidos"]
        ):
            print(f"  {codon} -> {aminoacido}")

        if traduccion["codon_terminacion"] is not None:
            print("  " + traduccion["codon_terminacion"] + " -> STOP (liberación de la cadena)")
            print("Proteína sintetizada (secuencia de aminoácidos):")
        else:
            print("Cadena parcial de aminoácidos:")

        print("-".join(traduccion["aminoacidos"]))
        print("Número de aminoácidos:", len(traduccion["aminoacidos"]))

    for aviso in traduccion["avisos"]:
        print("Aviso:", aviso)


if __name__ == "__main__":
    main()
