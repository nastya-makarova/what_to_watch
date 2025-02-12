from datetime import datetime
# Импортируется функция для выбора случайного значения:
from random import randrange

from flask import Flask, redirect, render_template, url_for
# Импортируем класс для работы с ORM:
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, URLField
from wtforms.validators import DataRequired, Length, Optional

app = Flask(__name__)
# Подключаем БД SQLite:
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SECRET_KEY'] = 'A7jLs9hTqW3zV8dU'
# Создаём экземпляр SQLAlchemy и в качестве параметра
# передаём в него экземпляр приложения Flask:
db = SQLAlchemy(app)


class Opinion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    text = db.Column(db.Text, unique=True, nullable=False)
    source = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)


# Класс формы опишите сразу после модели Opinion.
class OpinionForm(FlaskForm):
    title = StringField(
        'Введите название фильма',
        validators=[DataRequired(message='Обязательное поле'), Length(1, 128)]
    )
    text = TextAreaField(
        'Напишите мнение',
        validators=[DataRequired(message='Обязательное поле')]
    )
    source = URLField(
        'Добавьте ссылку на подробный обзор фильма',
        validators=[Length(1, 256), Optional()]
    )
    submit = SubmitField('Добавить')


@app.route('/')
def index_view():
    # Определяется количество мнений в базе данных:
    quantity = Opinion.query.count()
    # Если мнений нет...
    if not quantity:
        # ...то возвращается сообщение:
        return 'В базе данных мнений о фильмах нет.'
    # Иначе выбирается случайное число в диапазоне от 0 до quantity...
    offset_value = randrange(quantity)
    # ...и определяется случайный объект:
    opinion = Opinion.query.offset(offset_value).first()
    return render_template('opinion.html', opinion=opinion)


@app.route('/add', methods=['GET', 'POST'])
def add_opinion_view():
    # Вот тут создаётся новый экземпляр формы:
    form = OpinionForm()
    # Если ошибок не возникло...
    if form.validate_on_submit():
        # ...то нужно создать новый экземпляр класса Opinion:
        opinion = Opinion(
            title=form.title.data,
            text=form.text.data,
            source=form.source.data
        )
        # Затем добавить его в сессию работы с базой данных:
        db.session.add(opinion)
        # И зафиксировать изменения:
        db.session.commit()
        # Затем переадресовать пользователя на страницу добавленного мнения:
        return redirect(url_for('opinion_view', id=opinion.id))
    # Если валидация не пройдена — просто отрисовать страницу с формой:
    return render_template('add_opinion.html', form=form)


@app.route('/opinion/<int:id>')
# Параметром указывается имя переменной:
def opinion_view(id):
    # Теперь можно запросить нужный объект по id.
    opinion = Opinion.query.get_or_404(id)
    # ...и передать его в шаблон (шаблон тот же, что и для главной страницы):
    return render_template('opinion.html', opinion=opinion)


if __name__ == '__main__':
    app.run()

# print(app.config) настройки в виде словаря. Переменная: значение