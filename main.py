from app import create_app
from config.config import config
from app import jwt
from app import client

# 调用工厂函数构建应用实例
app, ws = create_app(config['development'])

# flask shell 构建上下文
@app.shell_context_processor
def make_shell_context():
    return {
        'jwt': jwt,
        'db': client
    }

if __name__ == "__main__":
    ws.run(app, host='0.0.0.0', port=1314)
    import app.utils