from utils import COMPLEMENTO_ARN


def arn_polimerasa(molde_3_5):
    """Lee el molde 3' -> 5' y sintetiza ARN 5' -> 3'."""
    bases_arn = []

    for base in molde_3_5:
        bases_arn.append(COMPLEMENTO_ARN[base])

    return "".join(bases_arn)


def transcribir(adn):
    """
    Transcribe la región de ADN proporcionada.

    En este modelo elegimos la hebra inferior como molde.
    """
    molde_transcripcion_3_5 = adn["inferior_3_5"]

    arn_5_3 = arn_polimerasa(molde_transcripcion_3_5)

    return arn_5_3