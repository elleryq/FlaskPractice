from flask import Flask
from flask import render_template
from flask.ext.wtf import Form
from flask.ext.bootstrap import Bootstrap
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required
# http://pythonhosted.org/Flask-Bootstrap/basic-usage.html

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Please_replace_me'

bootstrap = Bootstrap(app)


class LoginForm(Form):
    name = StringField('Username', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Submit')


@app.route('/')
def hello_world():
    return render_template('hello.html', form=LoginForm())


if __name__ == '__main__':
    app.debug = True
    app.run()
