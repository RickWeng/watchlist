import os
import sys
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, url_for, escape, render_template
import click

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))

@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
def index():
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)

@app.route('/user/<name>')
def user_page(name):
    return 'User: %s' % escape(name)

@app.route('/test')
def test_url_for():
    return url_for('user_page', name='ricky')

@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')

@app.cli.command()
def forge():
    db.create_all()

    name = 'Ricky Weng'
    movies = [
        {'title': 'Zelig', 'year': '1983'},
        {'title': '童年往事', 'year': '1985'},
        {'title': '戀戀風塵', 'year': '1986'},
        {'title': '重慶森林', 'year': '1994'},
        {'title': '阳光灿烂的日子', 'year': '1994'},
        {'title': 'キッズ・リターン', 'year': '1996'},
        {'title': '小武', 'year': '1998'},
        {'title': '一一', 'year': '2000'},
        {'title': '三峡好人', 'year': '2006'},
        {'title': '海よりもまだ深', 'year': '2016'}
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')




