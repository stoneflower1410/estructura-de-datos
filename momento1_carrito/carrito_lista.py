from excepciones import CantidadInvalidaError, ProductoInexistenteError


def _validar_cantidad(cantidad):
    if not isinstance(cantidad, int) or isinstance(cantidad, bool):
        raise CantidadInvalidaError("cantidad debe ser un entero")
    if cantidad <= 0:
        raise CantidadInvalidaError("cantidad debe ser mayor que 0")


class Carrito:
    """TAD Carrito sobre una lista de pares [producto, cantidad]."""

    def __init__(self):
        self._items = []

    def _indice_de(self, producto):
        """Complejidad: O(n), recorre la lista buscando el producto."""
        for i, (p, _) in enumerate(self._items):
            if p == producto:
                return i
        return -1

    def agregar(self, producto, cantidad):
        """Complejidad: O(n), por la busqueda en _indice_de."""
        _validar_cantidad(cantidad)

        i = self._indice_de(producto)
        if i == -1:
            self._items.append([producto, cantidad])
        else:
            self._items[i][1] += cantidad

    def quitar(self, producto, cantidad):
        """Complejidad: O(n), por la busqueda en _indice_de."""
        _validar_cantidad(cantidad)

        i = self._indice_de(producto)
        if i == -1:
            raise ProductoInexistenteError(f"'{producto}' no esta en el carrito")

        nueva_cantidad = self._items[i][1] - cantidad
        if nueva_cantidad <= 0:
            del self._items[i]
        else:
            self._items[i][1] = nueva_cantidad

    def cantidad_de(self, producto):
        """Complejidad: O(n), por la busqueda en _indice_de."""
        i = self._indice_de(producto)
        if i == -1:
            return 0
        return self._items[i][1]

    def total(self):
        """Complejidad: O(n), suma la cantidad de cada producto registrado."""
        return sum(cantidad for _, cantidad in self._items)

    def esta_vacio(self):
        """Complejidad: O(1), consulta el tamano de _items."""
        return len(self._items) == 0

    def vaciar(self):
        """Complejidad: O(1), reemplaza _items por una lista nueva."""
        self._items = []

    def productos(self):
        """Complejidad: O(n), recorre _items para listar los nombres."""
        return [producto for producto, _ in self._items]
