COMPLEMENTO_ADN = {
    "A": "T",
    "T": "A",
    "C": "G",
    "G": "C",
}

COMPLEMENTO_ARN = {
    "A": "U",
    "T": "A",
    "C": "G",
    "G": "C",
}


def validar_adn(secuencia):
    secuencia = "".join(secuencia.split()).upper()

    if not secuencia or set(secuencia) - set(COMPLEMENTO_ADN):
        raise ValueError("El ADN debe contener solamente A, C, G y T.")

    return secuencia


def complementar_adn(molde):
    bases = []

    for base in molde:
        bases.append(COMPLEMENTO_ADN[base])

    return "".join(bases)


def crear_adn(secuencia):
    """Construye una doble hebra alineada a partir de una hebra 5' -> 3'."""
    superior = validar_adn(secuencia)
    inferior = complementar_adn(superior)

    return {
        "superior_5_3": superior,
        "inferior_3_5": inferior,
    }