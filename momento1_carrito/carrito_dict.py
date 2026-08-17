from excepciones import CantidadInvalidaError, ProductoInexistenteError


def _validar_cantidad(cantidad):
    if not isinstance(cantidad, int) or isinstance(cantidad, bool):
        raise CantidadInvalidaError("cantidad debe ser un entero")
    if cantidad <= 0:
        raise CantidadInvalidaError("cantidad debe ser mayor que 0")


class Carrito:
    """TAD Carrito sobre un diccionario producto -> cantidad."""

    def __init__(self):
        self._cantidades = {}

    def agregar(self, producto, cantidad):
        """Complejidad: O(1) amortizado, por la busqueda por hash del dict."""
        _validar_cantidad(cantidad)
        self._cantidades[producto] = self._cantidades.get(producto, 0) + cantidad

    def quitar(self, producto, cantidad):
        """Complejidad: O(1) amortizado, por la busqueda por hash del dict."""
        _validar_cantidad(cantidad)

        if producto not in self._cantidades:
            raise ProductoInexistenteError(f"'{producto}' no esta en el carrito")

        nueva_cantidad = self._cantidades[producto] - cantidad
        if nueva_cantidad <= 0:
            del self._cantidades[producto]
        else:
            self._cantidades[producto] = nueva_cantidad

    def cantidad_de(self, producto):
        """Complejidad: O(1) amortizado, por la busqueda por hash del dict."""
        return self._cantidades.get(producto, 0)

    def total(self):
        """Complejidad: O(n), suma la cantidad de cada producto registrado."""
        return sum(self._cantidades.values())

    def esta_vacio(self):
        """Complejidad: O(1), consulta el tamano de _cantidades."""
        return len(self._cantidades) == 0

    def vaciar(self):
        """Complejidad: O(1), reemplaza _cantidades por un dict nuevo."""
        self._cantidades = {}

    def productos(self):
        """Complejidad: O(n), recorre _cantidades para listar las claves."""
        return list(self._cantidades.keys())
