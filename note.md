# 使用 flask 构建网络应用

需要安装的包：

- flask
- flask-login
- flask-sqlalchemy

整体的框架：

。。。

其中的 `__init__.py` 使整个文件夹可以被 python 识别为一个 module.

flask.Flask 对象实现了 WSGI 接口，所谓的 WSGI 是 Web Server Gateway Interface，是 Web 服务器和 Web 应用程序之间的接口，WSGI 的出现可以提高 Web 程序的可以执行。Flask 对象是整个应用最核心的对象，作用是一个注册表，记录所有的 view 函数，URL 规则，template 配置，等等。
我们通常可以使用下面的语句初始化一个 Flask 对象：

```python
app = flask.Flask(__name__)
```

`SECRET_KEY` 是一个秘密的字符串，用于seesion cookie等内容的签名。通常是无意义的长字符串。

`app.run(debug=True)` 其中的 `debug=True` 的作用是开启调试模式，如果我们对代码做了任何修改，Web 服务器就会重新运行程序。

蓝图

一个网站通常包含许多页面，如果在一个`.py`文件中实现所有页面的逻辑，会十分凌乱。
一个 Blueprint 中包含一组 routes. 使用 Blueprint 可以把功能相近的页面分成一组，实现模块化组织。
例如，`admin` Blueprint 中可以包含和登录，登出相关的页面逻辑。相关的 templates 和 static 文件也可以放在同一文件夹下。

```
/blueprint-tutorial
├── /myapp_with_blueprints
│   ├── __init__.py
│   ├── /admin
│   │   ├── /templates
│   │   ├── /static
│   │   └── routes.py
│   ├── /core
│   │   ├── /templates
│   │   ├── /static
│   │   └── routes.py
│   ├── /products
│   │   ├── /templates
│   │   ├── /static
│   │   └── routes.py
│   └── /profile
|       ├── /templates
|       ├── /static
|       └── routes.py		
├── app.py
├── /static
└── /templates
```

```python
# Defining a blueprint
admin_bp = Blueprint(
    'admin_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@admin_bp.route('/admin')   # Focus here
def admin_home():
    return "Hello Admin!"
```

### blueprint 的使用

Blueprint 的构造函数的第一个参数是 Blueprint 的名字，由于内部路径选择，第三个和第四个参数是可选参数，指定了 template 和 static 文件存放的文件夹。
我们也可以使用可选参数 `url_prefix` 指定 blueprint 的 url 前缀。

通过 `@bluprint.route(route)`, 我们可以把一个 URL 绑定到一个 blueprint. 
当用户进入 `/admin` 页面时，`admin_home` 函数就会执行。

### blueprint 的注册

Flask 对象可以登记 Blueprint 对象。
`app.register_blueprint(viewsBP)`

### 蓝图文件寻址

我们在 HTML 文件中经常需要链接 CSS 或 js。一个 blueprint有一个小的抽象的文件系统，一个blueprint只能访问这个小的文件系统内的文件。
这个文件系统包含两个文件夹：`static` 和 `templates`。我们在定义 blueprint时可以通过参数指定两个文件夹在本地文件系统上的文件路径。
而在 HTML template 里面需要用 `{{ url_for('static', filename='index.js') }}` 这样的语法来访问该文件。

## template

flask 使用 jinga 对 html 进行渲染。

1. 控制逻辑

使用`{% %}`包裹的是jinga的控制逻辑，有以下几种：

```
{% block title %}Home{% endblock %}
{% extends "base.html" %}

{% if arg == 1 %}
    <p>1</p>
{% elif arg == 2 %}
    <p>2</p>
{% else %}
    <p>not 1 or 2</p>
{% endif %}


```

2. python 语句

```
{{ url_for('static', filename) }}
```


使用jinga渲染HTML页面可以携带参数。
我们通过`render_template(htmlFile, key=value)`的`**content`参数和HTML代码里`{{ key }}`的让python带参渲染HTML页面。

## flask-sqlalchemy

class SQLAlchemy

python 的 flask-sqlalchemy 基于 统一的 sqlalchemy. 可以自动地进行 sqlalchemy对象的创建，使用和清除。

SQLAlchemy 对象`db`可以让你访问 `db.Model` 类以及使用 `db.session` 来执行查询。

### 定义 Model

定义一个 db.class 的子类作为一个 model 类。自动把 CamelCase 命名风格的类名自动转换为 snake_case 风格的表名.


### 基于 SQLAlchemy 或 flask-sqlalchemy 的 CRUD

查询

sa.select(Model) 返回一个 statement.
可以对这个 statement 进行修改得到新的 statement.
例如， sa.select(Model).filter_by(col=val)
然后通过 session.execute (或 flask-sa 中的 db.session.execute) 执行statement, 得到result.
对result进行分析的函数：
- all 返回所有行(`seq[Row]`)
- first 返回第一个行(`seq[Row]`)或None

注意这里的 Row 类型。他代表了查询结果的一行，但是并不等同于一个 Model 的实例，而是更像一个 named tuple.
注意看以下两个例子：
```python
result = db.session.execute(sa.select(User).filter_by(email=email)).first()
```
这里，`result._mapping['User']`是一个 Model.User 的实例，可以使用 `result.User` 访问。
```python
result = db.session.execute(sa.select(User.id).filter_by(email=email)).first()
```
这里，`result.id` 是一个 python 内置的 `int` 类型。

所以 Row 的属性元素可以是数据库中的一个表项，也可以是一个 Model 的实例。


## flask-login

flask-login 为 flask 提供了用户会话管理，可以管理用户的登录，登出和在一段时间内 remember 用户的会话。














- [Blueprint](https://www.freecodecamp.org/news/how-to-use-blueprints-to-organize-flask-apps/)
- [SQLAlchemy](https://docs.sqlalchemy.org/)
- [flask-sqlalchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/)
- [flask-login](https://flask-login.readthedocs.io/)
- [flask-demo](https://github.com/techwithtim/Flask-Web-App-Tutorial/)
