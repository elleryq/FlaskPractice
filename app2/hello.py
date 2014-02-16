from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'Index page'


@app.route('/hello')
def hello():
    return "Hello world!"


@app.route('/user/<username>')
def showUserProfile(username):
    return 'User {0}'.format(username)


@app.route('/post/<int:postId>')
def showPost(postId):
    return 'Post {0}'.format(postId)


@app.route('/login', methods=['GET'])
def showLoginForm():
    return 'Login form'


@app.route('/login', methods=['POST'])
def doLogin():
    return 'doLogin'


if __name__ == '__main__':
    app.debug = True
    app.run()
