# Plan Tecnico - Carrito

**Especificacion de referencia:** `spec.md` v1.0

## 1. Estructura de datos elegida

El mismo contrato se implementa dos veces: lista de pares
`[producto, cantidad]` (`carrito_lista.py`) y diccionario
`producto -> cantidad` (`carrito_dict.py`). La bateria de `spec.md` corre
sin cambios contra ambas. No se usa `collections.Counter` (prohibido por
`CONSTITUTION.md`).

## 2. Alternativas consideradas

| Alternativa | Ventaja | Por que se descarto |
|---|---|---|
| Lista de pares | Simple, no requiere producto hashable | Buscar/agregar/quitar es O(n) |
| Diccionario | Buscar/agregar/quitar es O(1) amortizado | Requiere producto hashable (no es problema real: son strings) |
| `collections.Counter` | Resolveria la acumulacion directo | Prohibido por la constitucion |

Se implementan las dos alternativas viables para comparar su complejidad.

## 3. Complejidad esperada

| Operacion | Lista | Dict |
|---|---|---|
| `agregar` / `quitar` | O(n) | O(1) amortizado |
| `cantidad_de` | O(n) | O(1) amortizado |
| `total` / `productos` | O(n) | O(n) |
| `esta_vacio` / `vaciar` | O(1) | O(1) |

`n` = cantidad de productos distintos registrados.

## 4. Diseno interno

- `carrito_lista.Carrito._items`: lista de pares `[producto, cantidad]`,
  sin productos repetidos ni cantidades `<= 0`.
- `carrito_dict.Carrito._cantidades`: dict `producto -> cantidad`, sin
  valores `<= 0`.

## 5. Riesgos tecnicos

| Riesgo | Mitigacion |
|---|---|
| Compartir por referencia la estructura interna entre dos instancias (alias) | Cada `Carrito()` crea su propia estructura en `__init__`, nunca la recibe como parametro (ver `autopsia.md`) |
| `ValueError` generico esconde que fallo | Excepciones propias en `excepciones.py`: `CantidadInvalidaError`, `ProductoInexistenteError` |
