from flask import Flask
from flask import render_template
from flask_wtf import Form
from flask.ext.sqlalchemy import SQLAlchemy
from wtforms import TextField, TextAreaField, SubmitField, DateTimeField
from wtforms.validators import DataRequired
from datetime import datetime


class GuestbookForm(Form):
    author = TextField('Author', validators=[DataRequired()])
    message = TextAreaField('Message')
    email = TextField('E-Mail')
    submit = SubmitField("Leave")
    postedOn = DateTimeField("Posted")


app = Flask(__name__)
app.config['WTF_CSRF_SECRET_KEY'] = 'your_csrf_secret_key'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///guestbook.db"

db = SQLAlchemy(app)


class Guestbook(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Unicode(144))
    author = db.Column(db.Unicode(40))
    email = db.Column(db.Unicode(120))
    postedOn = db.Column(db.DateTime)

db.create_all()


@app.route('/', methods=('GET', 'POST'))
def index():
    form = GuestbookForm()
    if form.validate_on_submit():
        entry = Guestbook()
        form.populate_obj(entry)
        entry.postedOn = datetime.now()
        db.session.add(entry)
        db.session.commit()
    entries = Guestbook.query.order_by(Guestbook.postedOn)
    return render_template('index.html', form=form, entries=entries)


if __name__ == '__main__':
    app.debug = True
    app.run()
