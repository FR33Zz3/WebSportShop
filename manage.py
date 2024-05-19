from main import app, db
from flask_migrate import Migrate
from flask.cli import with_appcontext
import click

migrate = Migrate(app, db)

@click.command(name='create_db')
@with_appcontext
def create_db():
    db.create_all()
    click.echo('Database created')

if __name__ == '__main__':
    app.cli.add_command(create_db)
    app.run(debug=True)