from flask import Flask, render_template_string, render_template

app = Flask(__name__)

buy = ['cheese','watermelon','cherry']
@app.route('/')
def index():
    return render_template('index.html', buy=buy)
@app.route('/about')
def about():
    return render_template('about.html')
app.run(debug=True)