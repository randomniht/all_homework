import json


class Model:
    def __init__(self, controller):
        self.controller = controller

    def puck_json(self, total_product):
        self.controller.add()
        with open('menu.json', 'w', encoding='utf-8') as f:
            json.dump(total_product, f, ensure_ascii=False)


class View:
    def __init__(self, model):
        self.model = model

    def view_json(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            products = json.load(f)
            for product in products:
                name = product.get('name')
                price = product.get('price')
                print(f"Продукт: {name}, Цена: {price}")

    pass


class Controller:
    def __init__(self, model):
        self.model = model
        pass

    def add(self, product, price):
        total_product = {product: price}
        self.model.puck_json(total_product)


model = Model
controller = Controller
view = View