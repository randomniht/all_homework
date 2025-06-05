import json
import rich
from rich.console import Console
from rich.table import Table
from abc import  ABC, abstractmethod

class Model:
    def __init__(self):
        self.filename = 'menu.json'
        self.products = self.load_json()

    def load_json(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_json(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.products, f, ensure_ascii=False, indent=4)


    def add_product(self, total_product):
        self.products.append(total_product)
        self.save_json()
    def read_json(self):
        print(json.dumps(self.products, ensure_ascii=False, indent=4))

    def remove_product(self, name):
        product_to_remove = None
        for product in self.products:
            if name in product:
                product_to_remove = product
                break
        if product_to_remove:
            self.products.remove(product_to_remove)
            self.save_json()
            print(f"Продукт '{name}' удален.")
        else:
            print(f"Продукт '{name}' не найден.")



class View:
    def __init__(self, model):
        self.model = model

    def display_products(self, products):
        if not products:
            print("list empty.")
            return
        print("products:")
        self.model.read_json()


class Controller:
    def __init__(self, model):
        self.model = model
        pass

    def add(self, name, price):
        total_product = {name: price}
        self.model.add_product(total_product)

class AbstractView(ABC):
    @abstractmethod
    def display_products(self):
        pass



class RichView(AbstractView):
    def __init__(self, model):
        self.model = model
        self.console = Console()

    def display_products(self):
        products = self.model.products
        if not products:
            self.console.print("Список пуст.")
            return

        table = Table(title="Список продуктов")
        table.add_column("№")
        table.add_column("Название")
        table.add_column("Цена")
        for index, product in enumerate(products, start=1):
            for name, price in product.items():
                table.add_row(str(index), name, f"{price:.2f} ₽")
        self.console.print(table)

model = Model()
controller = Controller(model)
view = View(model)
rich_view = RichView(model)

while True:
    print("Меню:")
    print("1. Показать все продукты")
    print("2. Добавить продукт")
    print("3. Удалить продукт")
    print("0. Выход")

    choice = input("Выберите пункт: \n")

    if choice == '1':
        rich_view.display_products()
    elif choice == '2':
        name = input("Введите название продукта: ")
        price_input = input("Введите цену: ")
        try:
            price = float(price_input)
            controller.add(name, price)
            print("add product")
        except ValueError:
            print("error type must be int ")
    elif choice == '3':
        name = input("Введите название продукта: ")
        model.remove_product(name)
    elif choice == '0':
        print("bye")
        break
    else:
        print("error type must be int ")
