from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap4
from sqlalchemy import inspect

app = Flask (__name__ ,template_folder='../templates')

bootstrap= Bootstrap4(app)

app.config.from_object(Config)
db = SQLAlchemy(app)

@app.cli.command('init-db')
def init_db_command():
    db.drop_all()
    db.create_all()
    print('Initialized the database.')
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print(tables)


if __name__ == '__main__':
    app.run(host="0.0.0.0")

app.static_folder = 'static'

from app import routes, models