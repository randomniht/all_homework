import json


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

model = Model()
controller = Controller(model)
view = View(model)

while True:
    print("Меню:")
    print("1. Показать все продукты")
    print("2. Добавить продукт")
    print("0. Выход")

    choice = input("Выберите пункт: ")

    if choice == '1':
        view.display_products(model.products)
    elif choice == '2':
        name = input("Введите название продукта: ")
        price_input = input("Введите цену: ")
        try:
            price = float(price_input)
            controller.add(name, price)
            print("✅ Продукт добавлен!")
        except ValueError:
            print("error type must be int ")
    elif choice == '0':
        print("bye")
        break
    else:
        print("error type must be int ")