import os, yaml, logging
from flask import Flask, render_template, Markup, request

app = Flask(__name__)
app.config.from_pyfile('settings.py')
cache = {}
logger = logging.getLogger(__name__)


def get_page(dir, file):
    filename = (file)
    if filename in cache:
        return cache[filename]
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), dir, filename))
    try:
        file_contents = open(path, encoding='utf-8').read()
    except:
        return None

    data, text = file_contents.split('--\n', 1)
    page = yaml.load(data)
    page['content'] = Markup(Markup.markdown(text))
    page['path'] = file

    cache[filename] = page
    return page


@app.route('/BookOne')
def book_one():
    return render_template('G1.html')


@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/templates/main.css')
def render_home_css():
    return render_template('main.css')


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
app.run(debug=True,host='0.0.0.0', port=port)
