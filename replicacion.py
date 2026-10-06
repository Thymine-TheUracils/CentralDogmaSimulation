from utils import COMPLEMENTO_ADN, COMPLEMENTO_ARN, complementar_adn


def helicasa(adn):
    """Permite trabajar por separado con las dos hebras originales."""
    superior_5_3 = adn["superior_5_3"]
    inferior_3_5 = adn["inferior_3_5"]

    return superior_5_3, inferior_3_5


def primasa(molde_3_5, tam_cebador):
    """Sintetiza un cebador de ARN complementario al inicio del molde."""
    region_cebador = molde_3_5[:tam_cebador]

    bases_arn = []

    for base in region_cebador:
        bases_arn.append(COMPLEMENTO_ARN[base])

    return "".join(bases_arn)


def adn_polimerasa(molde_3_5, cebador_arn):
    """Sintetiza la extensión de ADN situada después del cebador."""
    inicio_extension = len(cebador_arn)
    resto_del_molde = molde_3_5[inicio_extension:]

    bases_adn = []

    for base in resto_del_molde:
        bases_adn.append(COMPLEMENTO_ADN[base])

    return "".join(bases_adn)


def ligasa(tramos_adn):
    """Representa la unión de tramos de ADN que ya están ordenados."""
    return "".join(tramos_adn)


def reemplazar_cebador(molde_3_5, cebador_arn, extension_adn):
    """Representa la eliminación del cebador y el relleno con ADN."""
    region_cebador = molde_3_5[:len(cebador_arn)]

    relleno_adn = complementar_adn(region_cebador)

    return ligasa([relleno_adn, extension_adn])


def sintetizar_hebra(molde_3_5, tam_cebador):
    """Coordina la síntesis de una hebra o de un fragmento."""
    cebador_arn = primasa(molde_3_5, tam_cebador)

    extension_adn = adn_polimerasa(molde_3_5, cebador_arn)

    adn_final = reemplazar_cebador(
        molde_3_5,
        cebador_arn,
        extension_adn,
    )

    return {
        "molde_3_5": molde_3_5,
        "cebador_arn": cebador_arn,
        "extension_adn": extension_adn,
        "adn_final": adn_final,
    }


def replicar(adn, tam_fragmento=100, tam_cebador=10):
    """
    Representa una horquilla que avanza de izquierda a derecha.

    La hebra inferior es el molde de la líder.
    La hebra superior es el molde de la rezagada.
    """
    if not isinstance(tam_fragmento, int) or tam_fragmento <= 0:
        raise ValueError("tam_fragmento debe ser un entero positivo.")

    if (
        not isinstance(tam_cebador, int)
        or not 1 <= tam_cebador <= tam_fragmento
    ):
        raise ValueError(
            "tam_cebador debe estar entre 1 y tam_fragmento."
        )

    # 1. Separación de las hebras originales.
    superior_5_3, inferior_3_5 = helicasa(adn)

    # 2. Síntesis continua de la hebra líder.
    sintesis_lider = sintetizar_hebra(
        inferior_3_5,
        tam_cebador,
    )

    # 3. Síntesis discontinua de la hebra rezagada.
    fragmentos_okazaki = []

    for inicio in range(0, len(superior_5_3), tam_fragmento):
        region_molde_5_3 = superior_5_3[
            inicio:inicio + tam_fragmento
        ]

        # Cada fragmento se sintetiza contra el avance de la horquilla.
        molde_fragmento_3_5 = region_molde_5_3[::-1]

        fragmento_okazaki = sintetizar_hebra(
            molde_fragmento_3_5,
            tam_cebador,
        )

        fragmentos_okazaki.append(fragmento_okazaki)

    # 4. Ordenación y unión de los fragmentos.
    tramos_rezagada = []

    for fragmento_okazaki in reversed(fragmentos_okazaki):
        tramos_rezagada.append(fragmento_okazaki["adn_final"])

    rezagada_5_3 = ligasa(tramos_rezagada)

    # 5. Formación de dos moléculas hijas semiconservativas.
    hija_1 = {
        "superior_5_3": superior_5_3,           # Original.
        "inferior_3_5": rezagada_5_3[::-1],     # Nueva.
    }

    hija_2 = {
        "superior_5_3": sintesis_lider["adn_final"],  # Nueva.
        "inferior_3_5": inferior_3_5,                # Original.
    }

    return {
        "hijas": [hija_1, hija_2],
        "sintesis_lider": sintesis_lider,
        "fragmentos_okazaki": fragmentos_okazaki,
        "rezagada_5_3": rezagada_5_3,
    }