# 安全说明 / Security Notes

## 安全最佳实践 / Security Best Practices

### 1. 生产环境部署 / Production Deployment

⚠️ **重要 / IMPORTANT**: 在生产环境中，请务必设置正确的环境变量：

In production, always set the correct environment variables:

```bash
# 设置为生产模式 / Set to production mode
export FLASK_ENV=production

# 或者在启动时指定 / Or specify at startup
FLASK_ENV=production python main.py
```

**不要在生产环境使用 Debug 模式！**

**DO NOT use Debug mode in production!**

Debug 模式会：
- 暴露敏感的错误信息 / Expose sensitive error information
- 允许远程代码执行 / Allow remote code execution
- 降低性能 / Reduce performance

### 2. API 密钥管理 / API Key Management

对于需要 API 密钥的端点（如 Steam、Weather Landscape），请：

For endpoints requiring API keys (like Steam, Weather Landscape):

```bash
# 不要将密钥硬编码在代码中 / Don't hardcode keys
# ❌ 错误 / Wrong
api_key = "your-secret-key-here"

# ✅ 正确 / Correct - 使用环境变量 / Use environment variables
api_key = os.environ.get('STEAM_API_KEY')
```

### 3. 输入验证 / Input Validation

所有用户输入都应该被验证：

All user input should be validated:

```python
from flask import request

def my_route():
    # 验证参数类型 / Validate parameter types
    try:
        rotate = int(request.args.get('rotate', 0))
        if rotate not in [0, 90, 180, 270]:
            return {"error": "Invalid rotate value"}, 400
    except ValueError:
        return {"error": "Invalid parameter"}, 400
```

### 4. 文件上传安全 / File Upload Security

如果实现文件上传功能：

If implementing file upload:

```python
from werkzeug.utils import secure_filename
import os

# 验证文件名 / Validate filename
filename = secure_filename(file.filename)

# 验证文件类型 / Validate file type
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
if not filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
    return {"error": "Invalid file type"}, 400

# 限制文件大小 / Limit file size
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
if len(file.read()) > MAX_FILE_SIZE:
    return {"error": "File too large"}, 400
```

### 5. CORS 配置 / CORS Configuration

如果需要跨域访问：

If cross-origin access is needed:

```python
from flask_cors import CORS

# 仅允许特定域 / Allow specific origins only
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://yourdomain.com"]
    }
})

# 不要使用 / Don't use:
# CORS(app, resources={r"/*": {"origins": "*"}})
```

### 6. 速率限制 / Rate Limiting

建议添加速率限制防止滥用：

Recommend adding rate limiting to prevent abuse:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/endpoint')
@limiter.limit("10 per minute")
def limited_endpoint():
    return {"data": "..."}
```

### 7. HTTPS / SSL

在生产环境中始终使用 HTTPS：

Always use HTTPS in production:

```python
# 强制 HTTPS / Force HTTPS
from flask_talisman import Talisman

Talisman(app, 
    force_https=True,
    strict_transport_security=True,
    content_security_policy={
        'default-src': "'self'",
    }
)
```

### 8. 依赖安全 / Dependency Security

定期更新依赖并检查漏洞：

Regularly update dependencies and check for vulnerabilities:

```bash
# 检查过时的包 / Check outdated packages
pip list --outdated

# 使用安全工具 / Use security tools
pip install safety
safety check

# 或使用 / Or use
pip install pip-audit
pip-audit
```

---

## 安全检查清单 / Security Checklist

部署前请确认：

Before deployment, verify:

- [ ] `FLASK_ENV=production` 已设置 / is set
- [ ] Debug 模式已关闭 / Debug mode is disabled
- [ ] API 密钥使用环境变量 / API keys use environment variables
- [ ] 所有用户输入都经过验证 / All user input is validated
- [ ] 使用 HTTPS / Using HTTPS
- [ ] 添加了速率限制 / Rate limiting is enabled
- [ ] 依赖包是最新版本 / Dependencies are up-to-date
- [ ] 敏感数据不在日志中 / Sensitive data not in logs
- [ ] 错误信息不暴露内部细节 / Error messages don't expose internal details

---

## 报告安全问题 / Reporting Security Issues

如果发现安全漏洞，请通过以下方式报告：

If you discover a security vulnerability, please report it via:

1. GitHub Security Advisory
2. 私信项目维护者 / Private message to project maintainers
3. 发送邮件至 / Email to: [security contact]

**请不要公开披露安全问题，直到问题被修复。**

**Please do not publicly disclose security issues until they are fixed.**

---

## 已知限制 / Known Limitations

### 1. 外部 API 依赖 / External API Dependencies

本项目依赖外部 API（天气、知乎等），这些 API 可能：

This project depends on external APIs (weather, Zhihu, etc.), which may:

- 更改其接口 / Change their interfaces
- 限制请求速率 / Rate limit requests  
- 返回恶意内容 / Return malicious content

**建议**: 实现缓存和数据验证

**Recommendation**: Implement caching and data validation

### 2. 图像生成 / Image Generation

动态生成的图像可能：

Dynamically generated images may:

- 消耗服务器资源 / Consume server resources
- 被用于 DoS 攻击 / Be used for DoS attacks

**建议**: 添加速率限制和资源监控

**Recommendation**: Add rate limiting and resource monitoring

---

## 更新日志 / Changelog

### v2.0 (当前版本 / Current)

- ✅ 配置管理系统，支持环境变量控制 debug 模式
- ✅ 插件隔离，减少攻击面
- ✅ 统一的错误处理
- ✅ 结构化日志

### v1.0 (旧版本 / Old)

- ⚠️ Debug 模式在代码中硬编码
- ⚠️ 缺少统一的配置管理

---

## 参考资料 / References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Flask Security](https://flask.palletsprojects.com/en/latest/security/)
- [Python Security Best Practices](https://python.readthedocs.io/en/latest/library/security.html)

---

**保持安全！/ Stay Secure!** 🔒
