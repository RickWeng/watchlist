import click

from watchlist import app, db
from watchlist.models import User, Movie

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

@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    db.create_all()

    user = User.query.first()
    if user:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)
    else:
        click.echo('Creating user...')
        user = User(username=username, name='Admin')
        user.set_password(password)
        db.session.add(user)

    db.session.commit()
    click.echo('Done.')
