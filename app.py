from flask import Flask, url_for, escape

app = Flask(__name__)

@app.route('/')
def hello():
    return u'欢迎来到我的 Watchlist!'

@app.route('/user/<name>')
def user_page(name):
    return 'User: %s' % escape(name)

@app.route('/test')
def test_url_for():
    return url_for('user_page', name='ricky')




