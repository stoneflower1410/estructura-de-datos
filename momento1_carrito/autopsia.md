# Autopsia: dos cajas comparten el mismo carrito

> **Nota:** no se conto con el fragmento de codigo real del profesor. El
> codigo de abajo es un fragmento representativo del bug clasico de alias
> en Python, distinto al que uso Andres en su version (el de el es un
> argumento por defecto mutable; este es el otro patron clasico: pasar la
> misma lista a dos instancias sin copiarla). La causa raiz es la misma en
> los dos casos: una referencia compartida.

## El fragmento con el bug

```python
class Caja:
    def __init__(self, carrito):
        self.carrito = carrito

    def agregar(self, producto, cantidad):
        self.carrito.append((producto, cantidad))


carrito_base = []
caja1 = Caja(carrito_base)
caja2 = Caja(carrito_base)

caja1.agregar("pan", 1)

print(caja2.carrito)
```

## Diagnostico

La causa no es una copia mal hecha. `caja1.carrito` y `caja2.carrito`
nunca fueron dos listas: son dos nombres distintos que apuntan al mismo
objeto lista en memoria, `carrito_base`.

`Caja.__init__` recibe `carrito` como parametro y hace
`self.carrito = carrito`. Esa linea no copia nada: en Python, asignar una
variable a otra nunca duplica el objeto, solo agrega una referencia mas
al mismo objeto. Como `caja1 = Caja(carrito_base)` y
`caja2 = Caja(carrito_base)` pasan la misma lista `carrito_base` a las dos
llamadas, `caja1.carrito`, `caja2.carrito` y `carrito_base` terminan siendo
tres nombres que apuntan al mismo objeto lista.

Cuando `caja1.agregar(...)` hace `self.carrito.append(...)`, no crea una
lista nueva: muta el objeto lista compartido. Como `caja2.carrito` apunta
al mismo objeto, el cambio es visible tambien desde `caja2`, aunque nadie
le haya pedido nada a `caja2`.

Diferencia entre mutar y reasignar:
- `self.carrito.append(x)` muta el objeto al que apunta `self.carrito`.
  Todo el que tenga una referencia a ese mismo objeto ve el cambio.
- `self.carrito = self.carrito + [x]` reasigna `self.carrito` a un objeto
  lista nuevo. Otras referencias que apunten al objeto viejo no ven el
  cambio.

## Diagrama de memoria - ANTES de `caja1.agregar("pan", 1)`

```
Variables/atributos                Objetos en memoria

carrito_base ------------------------.
                                       \
caja1  ---------> [Caja @0x100] --.    +--> [ ] (lista vacia @0x200)
                    carrito -------'   /
                                       /
caja2  ---------> [Caja @0x101] --.   /
                    carrito -------'--'
```

`carrito_base`, `caja1.carrito` y `caja2.carrito` son tres flechas
distintas que apuntan al mismo objeto lista `@0x200`. Solo existe una
lista en memoria.

## Diagrama de memoria - DESPUES de `caja1.agregar("pan", 1)`

```
Variables/atributos                Objetos en memoria

carrito_base ------------------------.
                                       \
caja1  ---------> [Caja @0x100] --.    +--> [("pan", 1)]  (@0x200, MUTADA)
                    carrito -------'   /
                                       /
caja2  ---------> [Caja @0x101] --.   /
                    carrito -------'--'
```

El objeto `@0x200` sigue siendo el mismo (misma direccion), pero ahora
tiene un elemento adentro. Como `caja2.carrito` sigue apuntando a
`@0x200`, `caja2.carrito` tambien "tiene" el pan, sin que nadie se lo haya
agregado directamente a `caja2`.

## La correccion

```python
class Caja:
    def __init__(self, carrito):
        self.carrito = list(carrito)

    def agregar(self, producto, cantidad):
        self.carrito.append((producto, cantidad))


carrito_base = []
caja1 = Caja(carrito_base)
caja2 = Caja(carrito_base)

caja1.agregar("pan", 1)

print(caja2.carrito)
```

### Por que funciona, en terminos de memoria

`list(carrito)` construye una lista nueva con los mismos elementos que
`carrito`, no una referencia al mismo objeto. Esa linea se ejecuta cada
vez que se llama a `__init__`, asi que cada instancia recibe su propia
copia independiente de la lista, aunque las dos hayan recibido
originalmente `carrito_base` como argumento.

```
carrito_base ---------> [ ] (lista @0x200, sin usar despues de __init__)

caja1  ---------> [Caja @0x100] --> carrito ---> [ ] (lista @0x300, propia de caja1)

caja2  ---------> [Caja @0x101] --> carrito ---> [ ] (lista @0x301, propia de caja2)
```

Ahora `caja1.carrito` y `caja2.carrito` apuntan a objetos distintos.
Mutar uno con `.append(...)` no afecta al otro, porque ya no hay alias
entre ellos ni con `carrito_base`.

Esta es la misma razon, vista desde la memoria, por la que el TAD Carrito
de este proyecto (`carrito_lista.py`, `carrito_dict.py`) nunca comparte su
lista o diccionario interno con nadie desde afuera: cada `Carrito()` crea
su propia estructura en `__init__` (`self._items = []` /
`self._cantidades = {}`) y nunca la recibe como parametro, evitando que
dos instancias terminen apuntando, sin querer, al mismo objeto.
