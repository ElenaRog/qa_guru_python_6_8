"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from models import Product, Cart


@pytest.fixture
def product_book():
    return Product("book", 100.0, "This is a book", 1000)


@pytest.fixture
def product_ended():
    return Product("ended", 2.0, "This is some ended product", 0)


@pytest.fixture
def product_pen():
    return Product("pen", 10.5, "This is a pen", 200)


@pytest.fixture
def cart():
    return Cart()


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product_book, product_pen, product_ended):
        assert product_book.check_quantity(300)
        assert not product_pen.check_quantity(400)
        assert product_ended.check_quantity(0)

    def test_product_buy(self, product_book):
        product_book.buy(500)
        assert product_book.quantity == 500

    def test_product_buy_more_than_available(self, product_ended):
        with pytest.raises(ValueError):
            product_ended.buy(2)


class TestCart:
    def test_add_product(self, cart, product_book):
        cart.add_product(product_book, 5)
        assert product_book in cart.products
        assert cart.products.get(product_book) == 5

    def test_add_product_with_zero_count(self, cart, product_book):
        with pytest.raises(ValueError):
            cart.add_product(product_book, 0)

    def test_remove_product(self, cart, product_book):
        cart.add_product(product_book, 5)
        cart.remove_product(product_book, 3)
        assert product_book in cart.products
        assert cart.products.get(product_book) == 2

    def test_remove_all_product(self, cart, product_book, product_pen):
        cart.add_product(product_book, 5)
        cart.add_product(product_pen, 10)

        cart.remove_product(product_book, 5)
        assert product_book not in cart.products

        cart.remove_product(product_pen)
        assert product_pen not in cart.products

    def test_remove_product_more_than_available(self, cart, product_book):
        cart.add_product(product_book, 2)
        cart.remove_product(product_book, 5)
        assert product_book not in cart.products

    def test_remove_product_not_in_cart(self, cart, product_book):
        with pytest.raises(NameError):
            cart.remove_product(product_book, 5)

    def test_clear(self, cart, product_book, product_pen):
        cart.add_product(product_book)
        cart.add_product(product_pen, 10)

        cart.clear()
        assert len(cart.products) == 0

    def test_get_total_price(self, cart, product_book, product_pen):
        cart.add_product(product_book, 7)
        cart.add_product(product_pen, 126)

        assert cart.get_total_price() == 2023

    def test_buy(self, cart, product_book, product_pen):
        cart.add_product(product_book, 7)
        cart.add_product(product_pen, 126)

        cart.buy()
        assert product_book.quantity == 993
        assert product_pen.quantity == 74
        assert len(cart.products) == 0

    def test_buy_unavailable_product(self, cart, product_book, product_pen):
        cart.add_product(product_book, 7)
        cart.add_product(product_pen, 126)
        product_pen.buy(100)
        with pytest.raises(ValueError):
            cart.buy()
