from utils import crear_adn
from replicacion import replicar
from transcripcion import transcribir


def mostrar_adn(adn):
    print("5' —", adn["superior_5_3"], "— 3'")
    print("3' —", adn["inferior_3_5"], "— 5'")


def main():
    adn_original = crear_adn("ATGCCGTAA")

    print("ADN original:")
    mostrar_adn(adn_original)

    resultado = replicar(
        adn_original,
        tam_fragmento=4,
        tam_cebador=2,
    )

    lider = resultado["sintesis_lider"]

    print("\nSíntesis de la hebra líder:")
    print("Cebador ARN:", lider["cebador_arn"])
    print("Extensión ADN:", lider["extension_adn"])
    print("ADN final:", lider["adn_final"])

    print("\nFragmentos de Okazaki — cada uno escrito 5' -> 3':")

    for numero, fragmento_okazaki in enumerate(
        resultado["fragmentos_okazaki"],
        start=1,
    ):
        print(f"Fragmento {numero}:")
        print("  Cebador ARN:", fragmento_okazaki["cebador_arn"])
        print("  Extensión ADN:", fragmento_okazaki["extension_adn"])
        print("  ADN final:", fragmento_okazaki["adn_final"])

    for numero, hija in enumerate(resultado["hijas"], start=1):
        print(f"\nMolécula hija {numero}:")
        mostrar_adn(hija)

    adn_para_transcribir = resultado["hijas"][0]
    arn = transcribir(adn_para_transcribir)

    print("\nARN transcrito:")
    print("5' —", arn, "— 3'")


if __name__ == "__main__":
    main()