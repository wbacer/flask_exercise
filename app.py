from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/hello')  # 为视图绑定多个url
@app.route('/hi')
def say_hello():
    return '<h1>Hello, Flask!</h1>'


@app.route('/greet', defaults={'name': 'Programmer'})  # 设置默认值
@app.route('/greet/<name>')  # 动态url
def greet1(name):
    return '<h1>Hello, %s!</h1>' % name


# 等同于
@app.route('/greet')
@app.route('/greet/<name>')
def greet2(name='Programmer'):
    return '<h1>Hello, %s!</h1>' % name


if __name__ == '__main__':
    app.run()
