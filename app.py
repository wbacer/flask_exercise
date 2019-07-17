from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/hello')  # 为视图绑定多个url
@app.route('/hi')
def say_hello():
    return '<h1>Hello, Flask!<h1>'


if __name__ == '__main__':
    app.run()
