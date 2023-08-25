class Product:
    """
    Класс продукта
    """
    name: str
    price: float
    description: str
    quantity: int

    def __init__(self, name, price, description, quantity):
        self.name = name
        self.price = price
        self.description = description
        if quantity < 0:
            raise ValueError
        self.quantity = quantity

    def check_quantity(self, quantity) -> bool:
        return self.quantity >= quantity

    def buy(self, quantity):
        if self.check_quantity(quantity):
            self.quantity -= quantity
        else:
            raise ValueError

    def __hash__(self):
        return hash(self.name + self.description)


class Cart:
    # Словарь продуктов и их количество в корзине
    products: dict[Product, int]

    def __init__(self):
        # По-умолчанию корзина пустая
        self.products = {}

    def add_product(self, product: Product, buy_count=1):
        """
        Метод добавления продукта в корзину.
        Если продукт уже есть в корзине, то увеличиваем количество
        """
        if buy_count <= 0:
            raise ValueError

        if product not in self.products:
            self.products.setdefault(product, 0)
        self.products[product] += buy_count

    def remove_product(self, product: Product, remove_count=None):
        """
        Метод удаления продукта из корзины.
        Если remove_count не передан, то удаляется вся позиция
        Если remove_count больше, чем количество продуктов в позиции, то удаляется вся позиция
        """

        if product not in self.products:
            raise NameError

        elif remove_count is None or self.products[product] <= remove_count:
            self.products.pop(product)

        elif remove_count <= 0:
            raise ValueError

        else:
            self.products[product] -= remove_count

    def clear(self):

        # for product in self.products.keys():
        self.products = {}

    def get_total_price(self) -> float:

        total_prise = 0.0

        for product in self.products.keys():
            total_prise += product.price * self.products.get(product)

        return total_prise

    def buy(self):
        """
        Метод покупки.
        Учтите, что товаров может не хватать на складе.
        В этом случае нужно выбросить исключение ValueError
        """
        for product, value in self.products.items():
            if not product.check_quantity(value):
                self.products.pop(product)  # Удаление неликвидного товара из корзины
                raise ValueError

        for product, value in self.products.items():
            product.buy(value)

        print(f'Сумма покупки составила {self.get_total_price()} у.е.')

        self.clear()
