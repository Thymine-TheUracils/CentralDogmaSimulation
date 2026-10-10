"""Esquemas de consola: muestran el proceso sin cambiar los cálculos."""

from colores import colorear


def mostrar_apertura(adn, paso_a_paso=False):
    """Muestra tres estados de apertura de un tramo de hasta 24 bases."""
    superior = adn["superior_5_3"][:24]
    inferior = adn["inferior_3_5"][:24]
    longitud = len(superior)
    completo = longitud == len(adn["superior_5_3"])
    extremo_superior = " 3'" if completo else " ..."
    extremo_inferior = " 5'" if completo else " ..."

    print("\nAPERTURA DE LA DOBLE HEBRA")
    print(f"  Vista de las primeras {longitud} bases.")
    print("  H = helicasa | barras = bases emparejadas | avance --->")
    # Evitamos repetir posiciones cuando la cadena solo tiene una base.
    posiciones = sorted(set([0, longitud // 2, longitud]))
    for paso, abiertas in enumerate(posiciones):
        if paso > 0 and paso_a_paso:
            input("\nPulsa Enter para avanzar la helicasa...")
        print(f"\n  Bases abiertas en esta vista: {abiertas}/{longitud}")
        if abiertas == 0:
            print("  " + colorear("H --->", "enzima"))
            print("  5' " + colorear(superior, "adn") + extremo_superior)
            print("     " + "|" * longitud)
            print("  3' " + colorear(inferior, "adn") + extremo_inferior)
        elif abiertas < longitud:
            # Las dos ramas abiertas llegan a H; a su derecha sigue el dúplex.
            print("  5' " + colorear(superior[:abiertas], "adn") + "\\")
            print(" " * (6 + abiertas) + colorear(superior[abiertas:], "adn") + extremo_superior)
            print(" " * (5 + abiertas) + colorear("H", "enzima") + "|" * (longitud - abiertas))
            print(" " * (6 + abiertas) + colorear(inferior[abiertas:], "adn") + extremo_inferior)
            print("  3' " + colorear(inferior[:abiertas], "adn") + "/")
        else:
            print("  5' " + colorear(superior, "adn") + extremo_superior)
            print(" " * (5 + longitud) + colorear("H --->", "enzima"))
            print("  3' " + colorear(inferior, "adn") + extremo_inferior)
    if not completo:
        print("  La helicasa continúa por el resto del ADN (...).")


def mostrar_direcciones():
    """Esquema de orientaciones; no representa longitudes reales."""
    print("\nDIRECCIONES EN LA HORQUILLA (esquema, no a escala)")
    print("                                      " + colorear("H ---> avance", "enzima"))
    print("  Molde superior    5' " + colorear("------------------------", "adn") + " 3'")
    print("  Rezagada nueva    3' <---" + colorear("[ARN]", "arn")
          + "  <---" + colorear("[ARN]", "arn") + "     5'")
    print("                       fragmentos de Okazaki")
    print()
    print("  Líder nueva       5' " + colorear("[ARN]", "arn")
          + colorear("------------------>", "adn") + " 3'")
    print("  Molde inferior    3' " + colorear("------------------------", "adn") + " 5'")
    print("  [ARN] = cebador; cada flecha indica síntesis 5' -> 3'.")
    print("  La líder crece hacia H; cada fragmento crece alejándose de H.")


def mostrar_cebador_y_extension(sintesis, cebador_derecha=False):
    """Separa cebador y extensión en columnas alineadas con su región del molde."""
    cebador = sintesis["cebador_arn"]
    hibrida = cebador + sintesis["extension_adn"]
    longitud = len(hibrida)
    for inicio in range(0, longitud, 48):
        fin = min(inicio + 48, longitud)
        izquierda_molde, izquierda_nueva = ("3'", "5'") if inicio == 0 else ("  ", "  ")
        derecha_molde, derecha_nueva = ("5'", "3'") if fin == longitud else ("", "")
        corte = max(inicio, min(fin, len(cebador)))
        tramo_arn = hibrida[inicio:corte]
        tramo_adn = hibrida[corte:fin]
        ancho_cebador = max(len(tramo_arn), len("Cebador (ARN)")) if tramo_arn else 0
        ancho_adn = max(len(tramo_adn), len("ADN añadido")) if tramo_adn else 0
        separador = "  " if tramo_arn and tramo_adn else ""
        etiqueta_arn = "Cebador (ARN)" if tramo_arn else ""
        etiqueta_adn = "ADN añadido" if tramo_adn else ""
        print(f"  Bases locales {inicio + 1}-{fin}")
        print(f"           {etiqueta_arn:<{ancho_cebador}}{separador}{etiqueta_adn}".rstrip())
        molde_arn = sintesis["molde_3_5"][inicio:corte]
        molde_adn = sintesis["molde_3_5"][corte:fin]
        # El relleno se calcula antes del color para conservar la alineación.
        relleno = " " * (ancho_cebador - len(tramo_arn))
        antes, despues = (relleno, "") if cebador_derecha else ("", relleno)
        molde = (antes + colorear(molde_arn, "adn") + despues
                 + separador + colorear(molde_adn, "adn") + " " * (ancho_adn - len(molde_adn)))
        nueva = (antes + colorear(tramo_arn, "arn") + despues
                 + separador + colorear(tramo_adn, "adn") + " " * (ancho_adn - len(tramo_adn)))
        print(f"  Molde {izquierda_molde} {molde} {derecha_molde}".rstrip())
        print(("           " + antes + "|" * len(tramo_arn) + despues
               + separador + "|" * len(tramo_adn)).rstrip())
        print(f"  Nueva {izquierda_nueva} {nueva} {derecha_nueva}".rstrip())


def mostrar_transcripcion(adn, arn):
    """Alinea molde y ARN en una vista corta del comienzo de la transcripción."""
    longitud = min(24, len(arn))
    final_molde = " 5'" if longitud == len(arn) else " ..."
    final_arn = " 3'" if longitud == len(arn) else " ..."
    print("\n  " + colorear("ARN polimerasa --->", "enzima") + " lee el molde 3' -> 5'")
    print(f"  Molde 3' {colorear(adn['inferior_3_5'][:longitud], 'adn')}{final_molde}")
    print("           " + "|" * longitud)
    print(f"  ARNm  5' {colorear(arn[:longitud], 'arn')}{final_arn}")
    print("           ---> síntesis de ARN 5' -> 3' (sin cebador)")


def mostrar_lectura_arn(traduccion):
    """Sitúa el ribosoma sobre el primer codón del marco seleccionado."""
    if traduccion["inicio"] is None:
        return
    codones = traduccion["codones"][:6]
    resto = " ..." if len(traduccion["codones"]) > len(codones) else ""
    print("\n  " + colorear("Ribosoma --->", "enzima") + " lectura del ARNm 5' -> 3'")
    print("  " + colorear("[", "enzima") + colorear(codones[0], "arn")
          + colorear("]", "enzima") + " "
          + colorear(" ".join(codones[1:]), "arn") + resto)
    print("    |")
    print("   " + colorear("ARNt", "arn") + " -> "
          + colorear("Met", "proteina") + " (primer aminoácido)")
    print("  Los siguientes codones se leen en la tabla inferior.")
