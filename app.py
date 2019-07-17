from flask import Flask, request

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
    return '<h1>Hello, %s is pig !</h1>' % name


# 等同于
@app.route('/greet')
@app.route('/greet/<name>')
def greet2(name='Programmer'):
    return '<h1>Hello, %s !</h1>' % name


@app.route('/hello1', methods=['GET'])
def hello():
    name = request.args.get('name', 'Flask')
    print(request.args)  # 解析后的数据
    print(request.query_string)  # 原始查询语句
    return '<h1>Hello, %s!</h1>' % name


@app.route('/colors/<any(blue, white, red):color>')  # any转换器
def three_colors(color):
    colors = ['blue', 'white', 'red']
    print(str(colors)[1:-1])
    return '<p> Love is patient and kind. Love is not jealous or boastful or proud or rude.</p>'


if __name__ == '__main__':
    app.run()
