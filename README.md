# Simulación del dogma central

Proyecto académico en Python para seguir el flujo ADN -> ADN -> ARNm -> proteína.
Se construye por etapas, con funciones pequeñas y salida explicativa en consola.

## Ejecutar la versión actual

Desde la carpeta del proyecto:

```sh
python main.py
```

El simulador no necesita bibliotecas externas. Utiliza una secuencia artificial
de 60 bases que puede cambiarse en `main.py`:

```text
ATGGCTTTTGAACCGAAAGGTTACTGCAATCTGAGCGTTCATACCGACCAATGGGGATAA
```

Empieza en ATG y termina en TAA, sin señales de terminación intermedias en ese
marco de lectura. La replicación genera cinco fragmentos de Okazaki de 12 bases,
cada uno con un cebador de 3 bases. Estos tamaños son didácticos y no biológicos.
La ejecución muestra la replicación, la transcripción y la traducción, hasta
obtener una secuencia de 19 aminoácidos y una parada UAA.

## Organización

- `utils.py`: valida ADN y ARN y construye dos hebras de ADN complementarias alineadas.
- `replicacion.py`: representa helicasa, primasa, ADN polimerasa, sustitución de
  cebadores y ligasa; devuelve dos moléculas hijas.
- `transcripcion.py`: genera ARN complementario a la hebra inferior.
- `traduccion.py`: lee el ARNm en codones y obtiene una secuencia de aminoácidos.
- `main.py`: coordina las etapas y explica sus resultados.

El punto de entrada actual es `main.py`. El paquete de `src/` todavía contiene
el ejemplo inicial y no ejecuta la simulación.

## Cómo interpretar las hebras

La hebra superior se escribe 5' -> 3' y la inferior, alineada debajo, 3' -> 5'.
Son antiparalelas: sus extremos tienen orientaciones opuestas. La complementariedad
del ADN es A-T y C-G. Complementar una secuencia mantiene el orden de las posiciones;
invertirla cambia el sentido en el que se muestra.

La horquilla del modelo avanza de izquierda a derecha. La hebra inferior sirve
de molde para la líder, que se sintetiza de forma continua. La superior sirve
de molde para la rezagada: cada fragmento de Okazaki crece en sentido contrario
al avance de la horquilla. Ambas hebras nuevas se sintetizan siempre 5' -> 3'.
Los fragmentos se muestran individualmente en ese sentido y se unen en el orden
necesario para reconstruir la rezagada completa.

La primasa genera un cebador de ARN y la ADN polimerasa lo extiende con ADN.
Después se retira el cebador, se rellena su región con ADN y la ligasa sella las
uniones. Cada molécula hija conserva una hebra original y contiene otra nueva:
por eso la replicación se llama semiconservativa.

Para la transcripción elegimos la hebra inferior de la primera hija. La ARN
polimerasa lee el molde 3' -> 5' y produce ARNm 5' -> 3', sin necesitar cebador.
Las correspondencias molde-ARN son A-U, T-A, C-G y G-C. El resultado coincide con
la hebra superior codificante, cambiando T por U.

La traducción utiliza el [código genético estándar del NCBI](https://www.ncbi.nlm.nih.gov/Taxonomy/Utils/wprintgc.cgi#SG1).
`traducir(arn)` busca el primer AUG y, desde esa posición, avanza de tres en tres
bases. AUG codifica Met (metionina). Los codones UAA, UAG y UGA detienen la lectura
y no añaden aminoácidos a la cadena. Los aminoácidos se representan con sus
abreviaturas de tres letras, por ejemplo Ala (alanina) y Gly (glicina).

La función devuelve un diccionario con `inicio` (índice desde cero, o `None` si no
hay AUG), `codones` (incluye la parada si se encuentra), `aminoacidos` (sin STOP),
`codon_terminacion`, `fragmento_incompleto` y `avisos`. No se leen las bases
anteriores al inicio ni las posteriores a la parada. Si falta AUG, no se obtiene
una cadena; si falta una parada en fase, se devuelve una cadena parcial y un
aviso. Las últimas una o dos bases, si no completan un codón, no se traducen.
Se aceptan minúsculas y espacios; un ARN vacío o con bases inválidas produce
`ValueError`.

## Simplificaciones del modelo

Las cadenas son textos, no estructuras tridimensionales. Los tamaños de los
fragmentos y los cebadores se reducen para facilitar la explicación; no son
medidas biológicas. Un fragmento final corto puede quedar cubierto completamente
por su cebador y no tener extensión de ADN antes del reemplazo.

La apertura y la síntesis se representan por sus resultados, sin animar el avance
de la horquilla. La eliminación de cebadores y el relleno se agrupan en una
función, sin distinguir las enzimas de maduración de cada organismo. Se transcribe
toda la región entregada, sin modelar promotores, terminadores ni procesamiento
del ARN.

La iniciación de la traducción se simplifica eligiendo el primer AUG, sin modelar
señales de reconocimiento ni otros posibles codones de inicio. Los ARNt, el
ribosoma y los factores de liberación se explican en consola; no se simulan
individualmente su unión ni su movimiento. Se obtiene la secuencia primaria,
sin modelar el plegamiento ni las modificaciones de la proteína.

## Requisitos y próximos pasos

| Requisito de la práctica | Estado actual |
| --- | --- |
| Apertura del ADN, cebadores y enzimas de replicación | Representados y explicados |
| Hebra líder y rezagada con fragmentos de Okazaki | Implementadas |
| Transcripción mediante una hebra molde y complementariedad | Implementada |
| Lectura de codones y aminoácidos hasta una señal de terminación | Implementada con el código genético estándar |
| Visualización de cada etapa y de la proteína final | Disponible en consola; presentación por mejorar |
| Entrega del simulador en GitHub | Pendiente de comprobar al finalizar |

El ejemplo actual contiene 20 tripletes: 19 codifican aminoácidos y el último
corresponde a UAA en el ARNm. La secuencia obtenida es:

```text
Met-Ala-Phe-Glu-Pro-Lys-Gly-Tyr-Cys-Asn-Leu-Ser-Val-His-Thr-Asp-Gln-Trp-Gly
```

Los siguientes pasos serán repasar la lógica de traducción, mejorar la salida
para la presentación y revisar la entrega en GitHub.

## Comprobaciones

Las pruebas usan `unittest`, incluido en Python:

```sh
python -m unittest discover -s tests -v
```
