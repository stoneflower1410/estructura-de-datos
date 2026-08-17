class CantidadInvalidaError(Exception):
    """La cantidad pasada a agregar/quitar no es un entero mayor que 0."""


class ProductoInexistenteError(Exception):
    """Se pidio quitar un producto que no esta registrado en el carrito."""
