from flask import Flask, render_template_string, render_template

app = Flask(__name__)

buy = ['cheese','watermelon','cherry']

todo = [
    {'id': 1,'name':'Apple','status':'100'},
    {'id': 2,'name': 'Watermelon', 'status': '64'},
    {'id': 3, 'name': 'Cheese', 'status': '100'},

]

country = [
    {'id': 1,'country_name':'Китай','capital':'Пекин','population':'21 843 000'},
    {'id': 2,'country_name': 'ДРК', 'capital': 'Киншаса', 'population': '14 740 000'},
    {'id': 3,'country_name': 'Япония', 'capital': 'Токио', 'population': '14 094 034'},
    {'id': 4,'country_name': 'Россия', 'capital': 'Москва', 'population': '13 149 803'},
    {'id': 5,'country_name': 'Индонезия', 'capital': 'Джакарта', 'population': '11 249 000'}
]


@app.route('/')
def index():
    return render_template('index.html', buy=buy, data=todo)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/prod')
def country_pages():
    return render_template('country.html', todo=todo)


@app.route('/prod/<int:country_index>')
def single_country_pages(country_index):
    single_contry = todo[country_index]
    return render_template('contry_detail.html', single_contry = single_contry)


app.run(debug=True, port=5007)