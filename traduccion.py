from utils import validar_arn


# Código genético estándar, con abreviaturas de tres letras.
CODIGO_GENETICO = {
    "UUU": "Phe", "UUC": "Phe", "UUA": "Leu", "UUG": "Leu",
    "UCU": "Ser", "UCC": "Ser", "UCA": "Ser", "UCG": "Ser",
    "UAU": "Tyr", "UAC": "Tyr", "UAA": "STOP", "UAG": "STOP",
    "UGU": "Cys", "UGC": "Cys", "UGA": "STOP", "UGG": "Trp",
    "CUU": "Leu", "CUC": "Leu", "CUA": "Leu", "CUG": "Leu",
    "CCU": "Pro", "CCC": "Pro", "CCA": "Pro", "CCG": "Pro",
    "CAU": "His", "CAC": "His", "CAA": "Gln", "CAG": "Gln",
    "CGU": "Arg", "CGC": "Arg", "CGA": "Arg", "CGG": "Arg",
    "AUU": "Ile", "AUC": "Ile", "AUA": "Ile", "AUG": "Met",
    "ACU": "Thr", "ACC": "Thr", "ACA": "Thr", "ACG": "Thr",
    "AAU": "Asn", "AAC": "Asn", "AAA": "Lys", "AAG": "Lys",
    "AGU": "Ser", "AGC": "Ser", "AGA": "Arg", "AGG": "Arg",
    "GUU": "Val", "GUC": "Val", "GUA": "Val", "GUG": "Val",
    "GCU": "Ala", "GCC": "Ala", "GCA": "Ala", "GCG": "Ala",
    "GAU": "Asp", "GAC": "Asp", "GAA": "Glu", "GAG": "Glu",
    "GGU": "Gly", "GGC": "Gly", "GGA": "Gly", "GGG": "Gly",
}


def traducir(arn):
    """Lee ARNm 5' -> 3' desde el primer AUG hasta la primera parada en fase.

    Elegir el primer AUG es una simplificación didáctica de la iniciación.
    Los índices se cuentan desde cero en el ARN normalizado.
    """
    arn = validar_arn(arn)

    inicio = arn.find("AUG")
    resultado = {
        "inicio": None if inicio == -1 else inicio,
        "codones": [],
        "aminoacidos": [],
        "codon_terminacion": None,
        "fragmento_incompleto": "",
        "avisos": [],
    }

    if inicio == -1:
        resultado["avisos"].append("No hay AUG: no se inicia la traducción en este modelo.")
        return resultado

    for posicion in range(inicio, len(arn), 3):
        codon = arn[posicion:posicion + 3]

        if len(codon) < 3:
            resultado["fragmento_incompleto"] = codon
            resultado["avisos"].append(
                f"Quedan bases sin un codón completo: {codon}. No se traducen."
            )
            break

        resultado["codones"].append(codon)
        aminoacido = CODIGO_GENETICO[codon]

        if aminoacido == "STOP":
            resultado["codon_terminacion"] = codon
            break

        resultado["aminoacidos"].append(aminoacido)

    if resultado["codon_terminacion"] is None:
        resultado["avisos"].append(
            "No se encontró una señal de terminación en el marco de lectura: "
            "la cadena obtenida es parcial."
        )

    return resultado
