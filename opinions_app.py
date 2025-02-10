from flask import Flask
# Импортируем класс для работы с ORM:
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Подключаем БД SQLite:
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
# Создаём экземпляр SQLAlchemy и в качестве параметра
# передаём в него экземпляр приложения Flask:
db = SQLAlchemy(app)


@app.route('/')
def index_view():
    return 'Совсем скоро тут будет случайное мнение о фильме!'


if __name__ == '__main__':
    app.run()

# print(app.config)
