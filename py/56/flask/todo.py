from flask import Flask, render_template_string, render_template, request, redirect

app = Flask(__name__)

todo = ['Погулять', 'Посмотреть фильм', 'Выучить джаваскрипт']
todo = [
    {'name': 'Погулять', 'status': 'Не выполнено'},
    {'name': 'Посмотреть фильм', 'status': 'Не выполнено'}
]

countries_data = [{'name': 'Россия', 'capital': 'Москва', 'people': 12000000},
             {'name': 'Китай', 'capital': 'Пекин', 'people': 23000000}]

@app.route('/')
def index():
    return render_template('index.html', data=todo)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/countries')
def countries():
    return render_template('countries.html', countries=countries_data)

@app.route('/countries/<string:country_name>')
def countries_detail(country_name):
    # написать логику поиска страны по имени и передать ее в шаблон
    # перебрать список стран и найти ту, что в country_name

    for country in countries_data:
        if country['name'] == country_name:
            return render_template('countries_detail.html', country=country)
    return 'Такой страны нет'


@app.route('/countries/add', methods=['POST'])
def countries_add():
    # добавить словарь request.form в общий список, но так, чтобы ключи совпадали!
    country = {
        'name': request.form['name'],
        'capital': request.form['capital'],
        'people': request.form['population']
    }
    countries_data.append(country)
    return redirect('/countries')


@app.route('/countries/<string:country_name>/delete', methods=['POST'])
def countries_delete(country_name):
    for index, country in enumerate(countries_data):
        if country['name'] == country_name:
            countries_data.pop(index)
    return redirect('/countries')

app.run(debug=True)