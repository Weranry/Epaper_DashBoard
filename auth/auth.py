import os
from flask import request, Response
#from dotenv import load_dotenv
# 加载.env文件中的环境变量
#load_dotenv()
#本地调试用

# 获取API密钥
API_KEY = os.environ.get("API_KEY")

# 不需要鉴权的路径列表
EXEMPT_ROUTES = [
    '/favicon.ico',  
    '/status',
    # 可以添加其他不需要鉴权的路径
]

def setup_auth(app):
    @app.before_request
    def verify_api_key():
        # 跳过不需要鉴权的路径
        if request.path in EXEMPT_ROUTES:
            return None
            
        # 从请求参数、请求头中获取API密钥
        api_key = request.args.get('api_key') or \
                request.headers.get('X-API-Key')
        
        if not api_key:
            # 直接返回状态码和纯文本错误信息
            return Response("请使用 APIKey 再访问（401）", status=401, mimetype='text/plain')
        
        if api_key != API_KEY:
            # 直接返回状态码和纯文本错误信息
            return Response("无效的 APIKey ，没有权限访问（403）", status=403, mimetype='text/plain')