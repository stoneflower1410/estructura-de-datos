# Constitucion del proyecto - Carrito

## Base del proyecto y colaboracion

Este proyecto se hizo con ayuda de un companero de curso, Andres, y usa su
proyecto (mismo enunciado, "Momento 1 - Carrito") como punto de partida:
la estructura de carpetas `specs/CONSTITUTION.md` + `specs/01-carrito/`, el
esqueleto de la bateria de pruebas y el enfoque general de dos
implementaciones (lista y dict) vienen de ahi. Por eso es esperable
encontrar similitudes estructurales entre ambos repositorios.

Lo que es propio de este autor y decidido de forma independiente:

- Las excepciones propias `CantidadInvalidaError` y `ProductoInexistenteError`
  en vez de `ValueError` generico.
- La decision sobre que pasa al pedir `quitar` mas cantidad de la
  disponible: aqui se trunca a 0 en vez de rechazarse con un error (ver
  seccion de ambiguedades en `specs/01-carrito/spec.md`).
- Las operaciones extra `vaciar()` y `productos()`, que no estan en la
  version de Andres.
- El fragmento de codigo y el analisis de `autopsia.md`, que usa un bug de
  alias distinto (constructor que recibe la lista sin copiarla) al de la
  version de Andres (argumento por defecto mutable).

## Principios

1. El contrato del carrito se implementa al menos dos veces, sobre
   estructuras internas distintas, y una unica bateria de pruebas
   verifica ambas sin modificarse.
2. No se usa collections.Counter como sustituto del conteo de cantidades.
3. La especificacion va antes que el codigo. Si cambia el comportamiento,
   primero cambia spec.md.
4. Ninguna operacion publica se considera terminada sin pruebas de caso
   normal y de casos extremos pasando.
5. Los errores del contrato se senalan con excepciones propias
   (`CantidadInvalidaError`, `ProductoInexistenteError`), no con
   `ValueError` generico.

## Restricciones

- Lenguaje: Python 3.11+
- Dependencias permitidas: pytest
- Estructuras internas permitidas para el Carrito: list, dict

## Definicion de terminado

- [x] Los criterios de aceptacion tienen prueba y pasan
- [x] Las dos implementaciones pasan la misma bateria sin modificarla
- [x] spec.md, plan.md y tasks.md reflejan el estado real

## Uso de asistentes de IA

Permitido para: redactar explicaciones, y ayudar a estructurar archivos
como CONSTITUTION.md, spec.md, plan.md, tasks.md, las pruebas y las
implementaciones a partir de decisiones que toma el autor (Yo) del
proyecto. Tambien se uso para verificar que la estructura general del
proyecto se alineara con la metodologia SDD, para entender las
alternativas de diseno antes de decidir cual usar.

No permitido para: Tomar decisiones completamente de manera autonoma sin
autorizacion.
