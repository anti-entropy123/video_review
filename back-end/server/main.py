from app import create_app
from config.config import config
from app import jwt
from app import db

# 调用工厂函数构建应用实例
app, ws = create_app(config['development'])

# flask shell 构建上下文
@app.shell_context_processor
def make_shell_context():
    return {
        'jwt': jwt,
        'db': db
    }

if __name__ == "__main__":
    # print(app.url_map)
    ws.run(app, host='0.0.0.0', port=1314, 
        # keyfile='cert/2_api.video-review.top.key', certfile='cert/1_api.video-review.top_bundle.crt'
    )