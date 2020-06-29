from flask import Flask
from flask import request
# 所有flask类都是一个应用实例，
# web副服务器用web服务器网关接口（wsgi）协议
# 将客户端所有请求交给这个对象处理，应用实例是flask类的对象
app = Flask(__name__)
# app就是flask类的对象
# 参数名称是主模块或包的名称

# 应用实例需要知道对每个url的请求要运行哪些代码，
# 需要保存一个url到python函数的映射关系，处理url和函数之间关系的就是路由
# 装饰器

# index() 这样处理入站请求的函数叫做视图函数，部署在服务器上时，
# 访问域名，会触发服务器执行index()函数，这个函数的返回值称为响应
# 客户端收到的内容，如果是web服务器，相应就是给用户的文档，
# 响应可以是html简单字符串也可以是复杂表单


@app.route('/')
def index():
    user_agent = request.headers.get("User-Agent")
    user_agent = user_agent.split("/")
    return '<h1>Hello,world! {}</h1>'.format(user_agent[1])
# 一种比较传统的方式是接受三个参数，url，端点名和视图函数
# app.add_url_rule('/', 'index', index)


# 动态路由：
# 路由 URL 中放在尖括号里的内容就是动态部分，
# 任何能匹配静态部分的 URL 都会映射到这个路由上。调用视图函数时，
# Flask 会将动态部分作为参数传入函数。在这个视图函数中，
# name 参数用于生成个性化的欢迎消息。
@app.route('/user/<name>')
def user(name):
    return '<h1>Hello,world! and {} !</h1>'.format(name)


# flask 把request当作全局变量使用，但实际上肯定不是全局变量
# flask使用上下文让指定的变量可以在一个线程中全局可以访问
# 应用上下文：current_app(当前应用实例)
#           g （处理请求时所用的临时存储对象，每次请求都会重新设置这个变量）
# 请求上下文： request (请求对象，封装了客户端发出的HTTP请求中的内容)
#            session （用户会话，值为一个字典，存储请求之间要“记住”的值）

# 请求对象
#   |属性或方法| 说明| 
#   |---|---|
#   |form| 一个字典，存储提交的所有表单字段| 
#   |args| 一个字典，存储所有通过url查询字符串传递的所有参数| 
#   |values| 一个字典，form和args的合集| 
#   |cookies| 一个字典，存储请求的所有cookie| 
#   |headers| 一个字典，存储所有http首部| 
#   |files | 一个字典，存储请求上传的文件| 
#   |get_data()|返回请求主体缓冲的数据| 
#   |get_json()|返回一个 Python 字典，包含解析请求主体后得到的 JSON| 
#   |blueprint|处理请求的 Flask 蓝本的名称| 
#   |endpoint|处理请求的 Flask 端点的名称；Flask 把视图函数的名称用作路由端点的名称| 
#   |method| HTTP方法 GET POST等| 
#   |scheme| url方案(http或https等)| 
#   |is_secure()|通过安全的连接（HTTPS）发送请求时返回 True| 
#   |host|请求定义的主机名，如果客户端定义了端口号，还包括端口号| 
#   |path|url路径部分| 
#   |query_string| url查询字段部分，返回原始二进制值| 
#   |full_path| url路径和查询字符串部分| 
#   |url| 完整url| 
#   |base_url|同url 没有查询字符串部分| 
#   |remote_addr|CLinet IP address| 
#   |environ| 请求的原始WSGI环境字典| 

