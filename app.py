# 验证url适用范围
from urllib.parse import urlparse, urljoin

from flask import Flask, request, redirect, url_for
from flask import session, render_template

app = Flask(__name__)
app.secret_key = 'ljh'

# 演示ajax
from jinja2.utils import generate_lorem_ipsum


@app.route('/post')
def show_post():
    post_body = generate_lorem_ipsum(2)
    return """
    <h1>A very long post </h1>
    <div class="body"> %s </div>
    <button id="load">Load More</button>
    <script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
    <script type="text/javascript">
    $(function() {
        $('#load').click(function() {
            $.ajax({
                url: '/more',
                type: 'get',
                success: function(data){
                    $('.body').append(data);
                }
            })
        })
    })
    </script>""" % post_body


@app.route('/more')
def load_post():
    return 'I love U, xgx'
    # return generate_lorem_ipsum(n=1)


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def redirect_back(default='hello', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
        return redirect(url_for(default, **kwargs))


# 重定向回各自的路由
@app.route('/foo')
def foo():
    return '<h1>Foo page<h1><a href="%s">Do something</a>' % url_for('do_something', next=request.full_path)


@app.route('/bar')
def bar():
    return '<h1>Bar page<h1><a href="%s">Do something</a>' % url_for('do_something', next=request.full_path)


@app.route('/do_something_and_redirect')
def do_something():
    # return redirect(request.referrer or url_for('hello'))
    # return redirect(request.args.get('next', url_for('hello')))
    return redirect_back()


# 模拟用户登录
@app.route('/login')
def login():
    session['logged_in'] = True
    return redirect(url_for('hello_world'))


@app.route('/')
@app.route('/hello')
def hello_world():  # 验证登录
    name = request.args.get('name')
    if name is None:
        name = request.cookies.get('name', 'ljh')
        response = '<h1>Hello %s!</h1>' % name
        if 'logged_in' in session:
            response += '[Authenticated]'
        else:
            response += '[Not Authenticated]'
        return response
    # return 'Hello World!'
    return redirect(url_for('say_hello'))


@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')
    return redirect(url_for('hello_world'))


@app.route('/hello')  # 为视图绑定多个url
@app.route('/hi')
def say_hello():
    return '<h1>say Hello, Flask!</h1>'


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
    return '<p> %s is patient and kind. Love is not jealous or boastful or proud or rude.</p>' % color, 302,


# 电影清单数据
user = {
    'username': 'ljh',
    'bio': 'A boy who loves movie and music.'
}
movies = [
    {'name': 'My Neighbour Totoro', 'year': '1998'},
    {'name': 'Three Colors Trilogy', 'year': '1993'},
    {'name': 'Forrest Gump', 'year': '1994'},
    {'name': 'My Neighbour Totoro', 'year': '1998'},
]


@app.route('/watchlist')
def watchlist():
    return render_template('watchlist.html', user=user, movies=movies)


if __name__ == '__main__':
    app.run()
