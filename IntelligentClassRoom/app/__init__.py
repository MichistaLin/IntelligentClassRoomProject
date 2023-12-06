# __init__.py：初始化：创建一个flask应用程序实例
from flask import Flask
from .views import blue
from .exts import init_exts
from flask import current_app
from app.serialapi import start_arduino_reader, connect_arduino


def create_app():
    app = Flask(__name__)
    # 注册蓝图
    app.register_blueprint(blueprint=blue)

    # 配置数据库
    db_uri = 'sqlite:///sqlite3.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri  # 配置数据库文件的路径
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 不追踪数据库的修改，减少资源消耗

    # 初始化插件
    init_exts(app=app)

    with app.app_context():

        start_arduino_reader(connect_arduino, port="COM2")

    return app







