import logging

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mongoengine import MongoEngine

jwt = JWTManager()
db = MongoEngine()

# 工厂函数
def create_app(config=None):
    app = Flask(__name__)

    # 如果有配置对象传入, 则应用到实例中
    if config:
        app.config.from_object(config)
        config.init_app(app)

    # 初始化 jwt
    jwt.init_app(app)
    # 解决跨域
    CORS(app)
    # 数据库
    db.init_app(app)    

    # 将蓝图组装到应用上    
    # api蓝图, 封装RestFul接口相关模块
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')
    # auth蓝图, 封装用户登陆和jwt token管理相关模块
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/api')
    # admin 蓝图, 封装管理员相关接口
    from .api import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/api/admin')
    # main蓝图, 封装其它视图相关模块
    # from .main import main as main_blueprint
    # app.register_blueprint(main_blueprint)

    from .ws import ws
    ws.init_app(app)
    logging.getLogger('socketio').setLevel(logging.ERROR)
    logging.getLogger('engineio').setLevel(logging.ERROR)

    return app, ws
