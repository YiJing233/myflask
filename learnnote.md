# learnNote

《Flask Web 开发：基于 Python 的 Web 应用开发实战》(第二版)学习笔记

## 虚拟环境

### 创建虚拟环境

`python3 -m venv virtual-environment-name`

在本项目中即：

`python3 -m venv venv`

### 进入虚拟环境

Linux/macOS:
`source venv/bin/activate`

Windows:
`venv\Scripts\activate

## Flask 原理

Flask 应用都必须创建一个应用实例。Web 服务器使用一种名为 Web 服务器网关接口（WSGI，Web server gateway interface，读作“wiz-ghee”）的协议，把接收自客户端的所有请求都转交给这个对象处理。`

## 路由

客户端（例如 Web 浏览器）把请求发送给 Web 服务器，Web 服务器再把请求发送给 Flask 应用实例。应用实例需要知道对每个 URL 的请求要运行哪些代码，所以保存了一个 URL 到 Python 函数的映射关系。处理 URL 和函数之间关系的程序称为路由。

路由实现的方式是`app.route`装饰器

### 基本路由

index() 这样处理入站请求的函数叫做视图函数，部署在服务器上时，
访问域名，会触发服务器执行 index()函数，这个函数的返回值称为响应
客户端收到的内容，如果是 web 服务器，相应就是给用户的文档，
响应可以是 html 简单字符串也可以是复杂表单

```python
@app.route('/')
def index():
    user_agent = request.headers.get("User-Agent")
    user_agent = user_agent.split("/")
    return '<h1>Hello,world! {}</h1>'.format(user_agent[1])
#一种比较传统的方式是接受三个参数，url，端点名和视图函数
app.add_url_rule('/', 'index', index)
```

### 动态路由

路由 URL 中放在尖括号里的内容就是动态部分，
任何能匹配静态部分的 URL 都会映射到这个路由上。调用视图函数时，
Flask 会将动态部分作为参数传入函数。在这个视图函数中，
name 参数用于生成个性化的欢迎消息。

```python
@app.route('/user/<name>')
def user(name):
    return '<h1>Hello,world! and {} !</h1>'.format(name)
```

## 请求上下文

flask 把 request 当作全局变量使用，但实际上肯定不是全局变量
flask 使用上下文让指定的变量可以在一个线程中全局可以访问
**应用上下文**：

- current_app(当前应用实例)
- g （处理请求时所用的临时存储对象，每次请求都会重新设置这个变量）

**请求上下文**：

- request (请求对象，封装了客户端发出的 HTTP 请求中的内容)
- session （用户会话，值为一个字典，存储请求之间要“记住”的值）

## 请求对象(request)常用属性和方法表

| 属性或方法   | 说明                                                                  |
| ------------ | --------------------------------------------------------------------- |
| form         | 一个字典，存储提交的所有表单字段                                      |
| args         | 一个字典，存储所有通过 url 查询字符串传递的所有参数                   |
| values       | 一个字典，form 和 args 的合集                                         |
| cookies      | 一个字典，存储请求的所有 cookie                                       |
| headers      | 一个字典，存储所有 http 首部                                          |
| files        | 一个字典，存储请求上传的文件                                          |
| get_data()   | 返回请求主体缓冲的数据                                                |
| get_json()   | 返回一个 Python 字典，包含解析请求主体后得到的 JSON                   |
| blueprint    | 处理请求的 Flask 蓝本的名称                                           |
| endpoint     | 处理请求的 Flask 端点的名称；Flask 把视图函数的名称用作路由端点的名称 |
| method       | HTTP 方法 GET POST 等                                                 |
| scheme       | url 方案(http 或 https 等)                                            |
| is_secure()  | 通过安全的连接（HTTPS）发送请求时返回 True                            |
| host         | 请求定义的主机名，如果客户端定义了端口号，还包括端口号                |
| path         | url 路径部分                                                          |
| query_string | url 查询字段部分，返回原始二进制值                                    |
| full_path    | url 路径和查询字符串部分                                              |
| url          | 完整 url                                                              |
| base_url     | 同 url 没有查询字符串部分                                             |
| remote_addr  | CLinet IP address                                                     |
| environ      | 请求的原始 WSGI 环境字典                                              |

## 请求钩子函数

例如，在请求开始时，需要创建数据库连接或者验证发起请求的用户身份。为了避免在每个视图函数中都重复编写代码，Flask 提供了注册通用函数的功能，注册的函数可在请求被分派到视图函数之前或之后调用即为钩子函数。请求钩子通过装饰器实现。Flask 支持以下 4 种。

before_request:注册一个函数，在每次请求之前运行。

before_first_request:注册一个函数，只在处理第一个请求之前运行。可以通过这个钩子添加服务器初始化任务。

after_request:注册一个函数，如果没有未处理的异常抛出，在每次请求之后运行。

teardown_request:注册一个函数，即使有未处理的异常抛出，也在每次请求之后运行。

在请求钩子函数和视图函数之间共享数据一般使用上下文全局变量 g。例如，before_request 处理程序可以从数据库中加载已登录用户，并将其保存到 g.user 中。随后调用视图函数时，便可以通过 g.user 获取用户。

## 响应环节

如果视图函数返回的响应需要使用不同的状态码，可以把数字代码作为第二个返回值，添加到响应文本之后。

```python
@app.route('/')
def index():
    return '<h1>Bad Request</h1>', 400
```

Flask 视图函数还可以返回一个响应对象。make_response() 函数可接受 1 个、2 个或 3 个参数（和视图函数的返回值一样），然后返回一个等效的响应对象

```python
from flask import make_response

@app.route('/')
def index():
    response = make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie('answer', '42')
    return response
```

### Flask响应对象

|属性或方法|说明|
|----|----|
|status_code| http状态码|
|headers|一个类似字典的对象，包含随响应发送的所有首部|
|set_cookie()| 为响应添加一个cookie|
|delete_cookie()|删除一个 cookie|
|content_length|响应主体的长度|
|content_type|响应主体的媒体类型|
|set_data()|使用字符串或字节值设定响应|
|get_data()|获取响应主体|

## 重定向问题

重定向的状态码通常是 302，在 Location 首部中提供目标 URL。重定向响应可以使用 3 个值形式的返回值生成，也可在响应对象中设定。不过，由于使用频繁，Flask 提供了 redirect() 辅助函数，用于生成这种响应：

```python
from flask import redirect
@app.route('/')
def index():
    return redirect('http://www.example.com')
```

## 第二章补充

Flask 的设计考虑了可扩展性，故而没有提供一些重要的功能，例如数据库和用户身份验证，所以开发者可以自由选择最适合应用的包，或者按需求自行开发。

社区成员开发了大量不同用途的 Flask 扩展，如果这还不能满足需求，任何 Python 标准包或代码库都可以使用
