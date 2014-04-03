from flask import Flask, render_template, request, redirect, url_for, flash
from flask.ext.babel import Babel
from flask.ext.mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.user import current_user, login_required
from flask.ext.user import UserManager, UserMixin, SQLAlchemyAdapter
from flask.ext.wtf import Form
from flask.ext.bootstrap import Bootstrap
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import Required
from datetime import datetime


# Use a Class-based config to avoid needing a 2nd file
class ConfigClass(object):
    # Configure Flask
    # Change this for production!!!
    SECRET_KEY = 'THIS IS AN INSECURE SECRET'
    # Use Sqlite file db
    SQLALCHEMY_DATABASE_URI = 'sqlite:///basic_app.sqlite'
    CSRF_ENABLED = True

    # Configure Flask-Mail -- Required for Confirm email and Forgot password
    # features
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    # Some servers use MAIL_USE_TLS=True instead
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'email@example.com'
    MAIL_PASSWORD = 'password'
    MAIL_DEFAULT_SENDER = '"Sender" <noreply@example.com>'

    # Configure Flask-User
    # Register and Login with username
    USER_ENABLE_USERNAME = True
    # Require Email confirmation
    #USER_ENABLE_CONFIRM_EMAIL = True
    USER_ENABLE_CONFIRM_EMAIL = False
    USER_ENABLE_CHANGE_USERNAME = True
    USER_ENABLE_CHANGE_PASSWORD = True
    USER_ENABLE_FORGOT_PASSWORD = True
    USER_ENABLE_RETYPE_PASSWORD = True


def create_app(test_config=None):                   # For automated tests
    # Setup Flask and read config from ConfigClass defined above
    app = Flask(__name__)
    app.config.from_object(__name__ + '.ConfigClass')

    # Load local_settings.py if file exists         # For automated tests
    try:
        app.config.from_object('local_settings')
    except:
        pass

    # Over-write app config                         # For automated tests
    if test_config:
        for key, value in test_config.items():
            app.config[key] = value

    # Setup Flask-Mail, Flask-Babel and Flask-SQLAlchemy
    app.mail = Mail(app)
    app.babel = babel = Babel(app)
    app.db = db = SQLAlchemy(app)

    @babel.localeselector
    def get_locale():
        translations = [str(translation)
                        for translation in babel.list_translations()]
        return request.accept_languages.best_match(translations)

    # Define User model. Make sure to add flask.ext.user UserMixin!!
    class User(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)
        active = db.Column(db.Boolean(), nullable=False, default=False)
        email = db.Column(db.String(255), nullable=False, unique=True)
        password = db.Column(db.String(255), nullable=False, default='')
        username = db.Column(db.String(50), nullable=False, unique=True)
        confirmed_at = db.Column(db.DateTime())
        reset_password_token = db.Column(
            db.String(100), nullable=False, default='')
        tweets = db.relationship('Tweet', backref='user', lazy='dynamic')

    app.User = User

    class Tweet(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        text = db.Column(db.String(144), nullable=False, default='')
        tweeted_at = db.Column(db.DateTime())
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Create all database tables
    db.create_all()

    # Setup Flask-User
    db_adapter = SQLAlchemyAdapter(db,  User)       # Select database adapter
    # Init Flask-User and bind to app
    user_manager = UserManager(db_adapter, app)

    # Setup forms
    class TweetForm(Form):
        text = StringField('Message', validators=[Required()])
        submit = SubmitField('Submit')

    # The '/' page is accessible to anyone
    @app.route('/')
    def home_page():
        if current_user.is_authenticated():
            return profile_page()
        return render_template("index.html")

    # The '/profile' page requires a logged-in user
    @app.route('/profile')
    # Use of @login_required decorator
    @login_required
    def profile_page():
        return render_template("profile.html")

    @app.route('/tweet/new', methods=['GET', 'POST'])
    @login_required
    def new_tweet():
        form = TweetForm()
        if form.validate_on_submit():
            tweet = Tweet()
            form.populate_obj(tweet)
            tweet.tweeted_at = datetime.now()
            tweet.user = current_user
            db.session.add(tweet)
            db.session.commit()
            flash("Your message is tweeted.")
            return redirect(url_for("list_tweet"))
        return render_template("new_tweet.html", form=form)

    @app.route('/tweet/list')
    @login_required
    def list_tweet():
        tweets = Tweet.query.order_by(Tweet.tweeted_at).limit(50)
        print(tweets[0].user.username)
        return render_template("list_tweet.html", tweets=tweets)

    bootstrap = Bootstrap(app)
    return app


# Start development web server
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
