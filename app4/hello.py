from flask import Flask
from flask import render_template
from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired


class MyForm(Form):
    name = TextField('name', validators=[DataRequired()])


app = Flask(__name__)
app.config['WTF_CSRF_SECRET_KEY'] = 'your_csrf_secret_key'
app.config['SECRET_KEY'] = 'your_secret_key'


@app.route('/', methods=('GET', 'POST'))
def hello_world():
    form = MyForm()
    if form.validate_on_submit():
        return 'Successed with {0}'.format(form.name.data)
    return render_template('hello.html', form=form)


if __name__ == '__main__':
    app.debug = True
    app.run()
