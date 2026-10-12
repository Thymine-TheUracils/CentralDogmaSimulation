# Simulación del dogma central

Simulador académico en Python que muestra el flujo de la información genética:
ADN -> ADN -> ARNm -> proteína, con explicaciones, esquemas y colores por base.
Permite seguir cómo se copia una molécula de ADN, cómo se obtiene un ARN
mensajero a partir de una de sus hebras y cómo se interpreta ese mensaje para
construir una secuencia de aminoácidos.

## Ejecución

Necesitas Python 3. No hay que instalar bibliotecas adicionales.
Abre una terminal en la carpeta del proyecto y ejecuta:

```sh
python main.py
```

El menú permite seleccionar la secuencia de ejemplo de 60 bases o introducir
una cadena propia. Escribe la hebra codificante de ADN en sentido 5' -> 3', con
A, C, G y T; se aceptan minúsculas y espacios. El programa valida la entrada y
construye automáticamente la hebra complementaria. Introduce únicamente las
bases, sin escribir los extremos `5'` y `3'`. Si la cadena está vacía o contiene
caracteres inválidos, el menú muestra un mensaje y permite corregirla.

No es obligatorio que la cadena propia empiece por ATG ni termine en un codón
de parada. La replicación y la transcripción se pueden realizar igualmente;
la traducción indicará si encuentra un inicio y una terminación.

Primero se muestra la replicación. Pulsa **Enter** para ver la transcripción y
otra vez para ver la traducción. Las pausas entre etapas funcionan por defecto
en una consola interactiva.
Puedes cancelar la ejecución con **Ctrl+C**. Para apreciar los colores, utiliza
una consola compatible; la opción `--sin-color` permite desactivarlos. Si la
salida se redirige a un archivo, los colores y las pausas entre etapas se
desactivan automáticamente.

También puedes seleccionar la secuencia directamente:

```sh
python main.py --ejemplo
python main.py --adn ATGCCGTAA
```

| Opción | Uso |
| --- | --- |
| `--fragmento N` | Tamaño de los fragmentos de Okazaki; por defecto, 12 bases. |
| `--cebador N` | Tamaño del cebador; por defecto, 3 bases. Debe estar entre 1 y el tamaño del fragmento. |
| `--paso-a-paso` | Añade pausas durante la apertura del ADN por la helicasa. |
| `--resumen` | Muestra los resultados sin los detalles ni las pausas entre etapas. |
| `--sin-color` | Desactiva los colores. |
| `--help` | Muestra la ayuda y todas las opciones. |

Por ejemplo:

```sh
python main.py --adn ATGCCGTAA --fragmento 4 --cebador 2
python main.py --ejemplo --resumen
python main.py --ejemplo --paso-a-paso
python main.py --adn "atg ccg taa" --sin-color
```

`--ejemplo` y `--adn` permiten saltar el menú y no se pueden utilizar juntos.
Los modos `--resumen` y `--paso-a-paso` también son excluyentes. El primero
presenta los resultados de las tres etapas de forma compacta; el segundo
permite observar las posiciones de la helicasa pulsando Enter.

### Secuencia de ejemplo

El ejemplo incluido es una secuencia artificial de 60 bases:

```text
5' ATGGCTTTTGAACCGAAAGGTTACTGCAATCTGAGCGTTCATACCGACCAATGGGGATAA 3'
```

Con los parámetros por defecto, genera cinco fragmentos de Okazaki de 12 bases,
cada uno con un cebador de 3 bases. La secuencia contiene un ATG inicial y un
TAA final en el mismo marco de lectura, de modo que permite recorrer todas
las etapas y obtener una cadena de 19 aminoácidos.

## 1. Replicación: ADN -> ADN

La replicación copia el ADN y produce dos moléculas hijas. Las dos hebras de
la molécula original son complementarias: A se empareja con T y C con G.
Además, son antiparalelas, por lo que sus extremos tienen orientaciones opuestas:

```text
5' ATGC 3'
   ||||
3' TACG 5'
```

La **helicasa** separa las hebras y permite utilizar cada una como molde para
construir una nueva. La zona donde el ADN se está abriendo se llama horquilla
de replicación. En el simulador, esta horquilla avanza de izquierda a derecha.
Los esquemas muestran la apertura de un tramo inicial de hasta 24 bases;
las barras verticales indican las bases que siguen emparejadas.

La **primasa** sintetiza un cebador de ARN complementario al molde. Este tramo
corto proporciona el extremo 3' que necesita la **ADN polimerasa** para empezar
a añadir ADN. La polimerasa lee el molde en sentido 3' -> 5' y alarga la hebra
nueva en sentido 5' -> 3'. Esta regla se mantiene tanto en la líder como en
la rezagada.

### Hebra líder y hebra rezagada

La **hebra líder** utiliza la hebra inferior como molde. Puede crecer de forma
continua en el mismo sentido que avanza la horquilla, a partir de un cebador.

La **hebra rezagada** utiliza la hebra superior como molde. Debido a la
orientación opuesta de este molde, se construye en tramos llamados
**fragmentos de Okazaki**. Cada fragmento necesita su propio cebador y se
sintetiza en sentido contrario al avance de la horquilla.

En los detalles de cada fragmento, el programa muestra el molde invertido
para leerlo 3' -> 5' y presentar la hebra nueva 5' -> 3'. Por eso, esos dibujos
locales tienen una orientación distinta a la del esquema general de la
horquilla. Invertir cómo se muestra una cadena no cambia sus bases ni la
regla de síntesis. Las columnas `Cebador (ARN)` y `ADN añadido` identifican
las dos regiones; el espacio entre ellas es solo una separación visual.

### Resultado de la replicación

Los cebadores se retiran y sus posiciones se rellenan con ADN. La **ligasa**
sella las uniones entre los fragmentos, formando una hebra continua. El último
fragmento puede ser más corto si la longitud de la secuencia no es múltiplo
del tamaño elegido; su cebador se limita al molde disponible.

Cada molécula hija contiene una hebra original y una nueva. Este mecanismo
se denomina **replicación semiconservativa**. En el modelo, que no introduce
mutaciones, ambas hijas conservan la secuencia de la molécula inicial.

## 2. Transcripción: ADN -> ARNm

La transcripción obtiene una molécula de **ARN mensajero (ARNm)** a partir
del ADN. El simulador selecciona la hebra inferior de la primera molécula
hija como **hebra molde**. La superior se denomina **hebra codificante**.

La **ARN polimerasa** recorre el molde en sentido 3' -> 5' y sintetiza el
ARNm en sentido 5' -> 3'. Puede iniciar la síntesis sin un cebador. En el ARN
se utiliza uracilo (U) en lugar de timina (T), por lo que las correspondencias
entre el molde de ADN y el ARN son:

| Base del molde de ADN | Base incorporada al ARN |
| --- | --- |
| A | U |
| T | A |
| C | G |
| G | C |

Por ejemplo:

```text
ADN codificante  5' ATGCCGTAA 3'
ADN molde        3' TACGGCATT 5'
ARNm             5' AUGCCGUAA 3'
```

El ARNm es complementario a la hebra molde y coincide con la codificante,
sustituyendo T por U. El resultado de esta etapa es una cadena de ARN que
se utilizará en la traducción. En este modelo se transcribe toda la región
introducida, sin seleccionar promotores ni terminadores.

## 3. Traducción: ARNm -> proteína

La traducción interpreta el ARNm para obtener una cadena de aminoácidos.
El **ribosoma** lee el mensaje en sentido 5' -> 3' agrupando las bases de tres
en tres. Cada grupo es un **codón**, cuya correspondencia se consulta en el
código genético estándar.

### Inicio y elongación

En el simulador, la lectura comienza en el primer **AUG**, que codifica
metionina (`Met`). Esta posición fija el **marco de lectura**: los siguientes
codones se leen a partir de ahí, avanzando tres bases cada vez. Las bases
anteriores al inicio no se traducen.

Los **ARN de transferencia (ARNt)** transportan los aminoácidos y reconocen
los codones mediante sus anticodones complementarios. El ribosoma cataliza
la formación de **enlaces peptídicos**, uniendo los aminoácidos a la cadena.
El programa representa esta correspondencia con una tabla de codones,
posiciones en el ARNm y abreviaturas de tres letras para los aminoácidos.

### Terminación y resultado

Los codones **UAA, UAG y UGA** indican una parada. Cuando aparece uno en el
marco de lectura, actúan los **factores de liberación** y se libera la cadena.
Estos codones no aportan aminoácidos y las bases posteriores no se traducen.

En el ejemplo corto de la transcripción anterior:

```text
ARNm:       AUG   CCG   UAA
Resultado:  Met - Pro - STOP
```

La cadena obtenida tiene dos aminoácidos; `STOP` indica la terminación y no
forma parte de ella. La secuencia de ejemplo de 60 bases produce:

```text
Met-Ala-Phe-Glu-Pro-Lys-Gly-Tyr-Cys-Asn-Leu-Ser-Val-His-Thr-Asp-Gln-Trp-Gly
```

Son 19 aminoácidos, seguidos de una señal UAA. Si no existe AUG, el modelo no
inicia la traducción. Si no encuentra una parada en el marco de lectura,
devuelve una cadena parcial y un aviso. Las últimas una o dos bases, cuando
no completan un codón, no se traducen y también se indican mediante un aviso.
