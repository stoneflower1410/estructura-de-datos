# Mismo archivo de pytest que el de Andres

import pytest
from carrito_dict import Carrito as CarritoDict
from carrito_lista import Carrito as CarritoLista
from excepciones import CantidadInvalidaError, ProductoInexistenteError

IMPLEMENTACIONES = [CarritoLista, CarritoDict]


@pytest.fixture(params=IMPLEMENTACIONES, ids=["lista", "dict"])
def carrito_cls(request):
    return request.param


@pytest.fixture
def carrito(carrito_cls):
    return carrito_cls()


def test_carrito_nuevo_esta_vacio(carrito):
    """CA-01: un carrito recien creado esta vacio."""
    assert carrito.esta_vacio() is True


def test_total_de_carrito_vacio_es_cero(carrito):
    """CA-02: el total de un carrito vacio es 0."""
    assert carrito.total() == 0


def test_cantidad_de_producto_ausente_en_carrito_vacio_es_cero(carrito):
    """CA-03: cantidad_de de un producto ausente en carrito vacio es 0."""
    assert carrito.cantidad_de("manzana") == 0


def test_quitar_de_carrito_vacio_lanza_error(carrito):
    """CA-04: quitar de un carrito vacio se rechaza."""
    with pytest.raises(ProductoInexistenteError):
        carrito.quitar("manzana", 1)


def test_agregar_un_producto_nuevo(carrito):
    """CA-05: agregar un producto nuevo lo deja registrado con esa cantidad."""
    carrito.agregar("manzana", 3)
    assert carrito.cantidad_de("manzana") == 3
    assert carrito.esta_vacio() is False


def test_agregar_el_mismo_producto_dos_veces_acumula(carrito):
    """CA-06: agregar el mismo producto dos veces acumula la cantidad."""
    carrito.agregar("manzana", 3)
    carrito.agregar("manzana", 2)
    assert carrito.cantidad_de("manzana") == 5


def test_agregar_productos_distintos(carrito):
    """CA-07: productos distintos se mantienen separados y el total los suma."""
    carrito.agregar("manzana", 3)
    carrito.agregar("pera", 5)
    assert carrito.cantidad_de("manzana") == 3
    assert carrito.cantidad_de("pera") == 5
    assert carrito.total() == 8


def test_agregar_cantidad_cero_lanza_error(carrito):
    """CA-08: agregar cantidad 0 se rechaza."""
    with pytest.raises(CantidadInvalidaError):
        carrito.agregar("manzana", 0)


def test_agregar_cantidad_negativa_lanza_error(carrito):
    """CA-09: agregar cantidad negativa se rechaza."""
    with pytest.raises(CantidadInvalidaError):
        carrito.agregar("manzana", -1)


def test_agregar_cantidad_no_entera_lanza_error(carrito):
    """CA-10: agregar una cantidad no entera se rechaza."""
    with pytest.raises(CantidadInvalidaError):
        carrito.agregar("manzana", 1.5)


def test_nombres_de_producto_distinguen_mayusculas(carrito):
    """CA-11: los nombres de producto distinguen mayusculas de minusculas."""
    carrito.agregar("Manzana", 1)
    carrito.agregar("manzana", 2)
    assert carrito.cantidad_de("Manzana") == 1
    assert carrito.cantidad_de("manzana") == 2
    assert carrito.total() == 3


def test_quitar_parcialmente(carrito):
    """CA-12: quitar una cantidad parcial reduce lo registrado."""
    carrito.agregar("manzana", 5)
    carrito.quitar("manzana", 2)
    assert carrito.cantidad_de("manzana") == 3


def test_quitar_todo_elimina_el_producto(carrito):
    """CA-13: quitar toda la cantidad elimina el producto del carrito."""
    carrito.agregar("manzana", 3)
    carrito.quitar("manzana", 3)
    assert carrito.cantidad_de("manzana") == 0
    assert carrito.esta_vacio() is True


def test_quitar_producto_inexistente_lanza_error(carrito):
    """CA-14: quitar un producto no registrado se rechaza."""
    carrito.agregar("manzana", 3)
    with pytest.raises(ProductoInexistenteError):
        carrito.quitar("pera", 1)


def test_quitar_mas_de_lo_disponible_trunca_a_cero(carrito):
    """CA-15: quitar mas cantidad de la disponible trunca a 0 sin lanzar error."""
    carrito.agregar("manzana", 2)
    carrito.quitar("manzana", 3)
    assert carrito.cantidad_de("manzana") == 0
    assert carrito.esta_vacio() is True


def test_quitar_cantidad_cero_lanza_error(carrito):
    """CA-16: quitar cantidad 0 se rechaza."""
    carrito.agregar("manzana", 3)
    with pytest.raises(CantidadInvalidaError):
        carrito.quitar("manzana", 0)


def test_quitar_cantidad_negativa_lanza_error(carrito):
    """CA-17: quitar cantidad negativa se rechaza."""
    carrito.agregar("manzana", 3)
    with pytest.raises(CantidadInvalidaError):
        carrito.quitar("manzana", -1)


def test_total_suma_todos_los_productos(carrito):
    """CA-18: el total suma las cantidades de todos los productos registrados."""
    carrito.agregar("manzana", 3)
    carrito.agregar("pera", 4)
    carrito.agregar("uva", 10)
    assert carrito.total() == 17


def test_total_despues_de_quitar(carrito):
    """CA-19: el total refleja correctamente una operacion de quitar posterior."""
    carrito.agregar("manzana", 5)
    carrito.agregar("pera", 2)
    carrito.quitar("manzana", 5)
    assert carrito.total() == 2


def test_vaciar_deja_el_carrito_vacio(carrito):
    """CA-20: vaciar() deja el carrito vacio."""
    carrito.agregar("manzana", 3)
    carrito.agregar("pera", 4)
    carrito.vaciar()
    assert carrito.esta_vacio() is True
    assert carrito.total() == 0


def test_vaciar_carrito_ya_vacio_no_lanza_error(carrito):
    """CA-21: vaciar() en un carrito ya vacio no lanza error."""
    carrito.vaciar()
    assert carrito.esta_vacio() is True


def test_productos_devuelve_los_registrados(carrito):
    """CA-22: productos() devuelve los nombres registrados."""
    carrito.agregar("manzana", 3)
    carrito.agregar("pera", 4)
    assert set(carrito.productos()) == {"manzana", "pera"}


def test_productos_de_carrito_vacio_es_lista_vacia(carrito):
    """CA-23: productos() de un carrito vacio devuelve una lista vacia."""
    assert carrito.productos() == []
