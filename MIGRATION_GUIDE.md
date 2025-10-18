# 迁移指南 / Migration Guide

## 从旧版本迁移 / Migrating from Old Version

本文档说明如何从旧版本架构迁移到新的插件化架构。

This document explains how to migrate from the old architecture to the new plugin-based architecture.

---

## 主要变更 / Major Changes

### 1. 架构变更 / Architecture Changes

**旧架构 / Old Architecture:**
```
main.py (包含所有路由注册 / Contains all route registrations)
routes/ (各个独立的 API 类 / Individual API classes)
```

**新架构 / New Architecture:**
```
main.py (插件自动发现 / Plugin auto-discovery)
plugins/ (模块化插件 / Modular plugins)
  ├── date_plugin/
  ├── weather_plugin/
  ├── schedule_plugin/
  └── misc_plugin/
core/ (共享基类和工具 / Shared base classes and utilities)
```

### 2. API 端点变更 / API Endpoint Changes

所有 API 端点保持不变，向后兼容。

All API endpoints remain unchanged and are backward compatible.

**示例 / Examples:**
- `/date/json` - 仍然工作 / Still works
- `/date/img` - 仍然工作 / Still works
- `/weather/now/json/<location>` - 仍然工作 / Still works
- 等等... / etc...

**特殊变更 / Special Changes:**
- `/weatherls/<lat>/<lon>/<key>` 改为 `/weather/landscape/<lat>/<lon>/<key>`
  - 旧端点仍可访问（通过 misc_plugin）
  - Old endpoint still accessible (via misc_plugin)

### 3. 代码变更 / Code Changes

#### 3.1 通用参数处理 / Common Parameter Handling

**旧代码 / Old Code:**
```python
# 在每个 API 类中重复
invert = request.args.get('invert', 'false').lower() == 'true'
rotate = int(request.args.get('rotate', 0))

if invert:
    img = ImageOps.invert(img.convert('RGB'))
if rotate in [90, 180, 270]:
    img = img.rotate(rotate, expand=True)
```

**新代码 / New Code:**
```python
from core.base_api import BaseImageAPI

class MyAPI(BaseImageAPI):
    def get_image(self):
        img = create_my_image()
        return self.process_and_send_image(img)  # 自动处理参数 / Auto handles parameters
```

#### 3.2 图像字节转换 / Image Bytes Conversion

**旧代码 / Old Code:**
```python
# 在每个图像创建器中重复
def get_image_bytes(self, img):
    img_io = BytesIO()
    img.save(img_io, 'JPEG', quality=95, subsampling=0)
    img_io.seek(0)
    return img_io
```

**新代码 / New Code:**
```python
from core.base_image_creator import BaseImageCreator

class MyImageCreator(BaseImageCreator):
    def create_image(self, data):
        img = self.create_base_image()
        # ... 绘制逻辑 / drawing logic
        return img
    
    # get_image_bytes 已由基类提供 / Already provided by base class
```

---

## 如何添加新功能 / How to Add New Features

### 方法 1: 创建新插件 / Method 1: Create New Plugin

1. 在 `plugins/` 下创建新目录 / Create new directory under `plugins/`
2. 创建 `__init__.py` 定义蓝图 / Create `__init__.py` to define blueprint
3. 创建 `routes.py` 实现路由 / Create `routes.py` to implement routes
4. 重启应用 / Restart application

**示例 / Example:**

```python
# plugins/my_plugin/__init__.py
from flask import Blueprint
from .routes import my_route

blueprint = Blueprint('my_plugin', __name__, url_prefix='/my')
blueprint.add_url_rule('/endpoint', view_func=my_route, methods=['GET'])
```

```python
# plugins/my_plugin/routes.py
from core.base_api import BaseImageAPI

class MyAPI(BaseImageAPI):
    def get_data(self):
        # 实现逻辑 / Implementation logic
        pass

my_api = MyAPI()
my_route = my_api.get_data
```

### 方法 2: 扩展现有插件 / Method 2: Extend Existing Plugin

如果功能与现有插件相关，可以直接在该插件中添加新路由。

If the feature is related to an existing plugin, add a new route directly in that plugin.

---

## 配置管理 / Configuration Management

### 环境变量 / Environment Variables

设置 `FLASK_ENV` 环境变量来选择配置：

Set the `FLASK_ENV` environment variable to select configuration:

```bash
# 开发环境 / Development
export FLASK_ENV=development
python main.py

# 生产环境 / Production  
export FLASK_ENV=production
python main.py

# 测试环境 / Testing
export FLASK_ENV=testing
python main.py
```

### 自定义配置 / Custom Configuration

在 `config.py` 中修改或添加配置选项。

Modify or add configuration options in `config.py`.

---

## 兼容性说明 / Compatibility Notes

### 保持的功能 / Preserved Features

✅ 所有原有 API 端点 / All original API endpoints
✅ 所有请求参数 / All request parameters  
✅ 响应格式（JSON/JPEG）/ Response formats (JSON/JPEG)
✅ 通用参数（invert, rotate）/ Common parameters (invert, rotate)

### 新增功能 / New Features

✨ 插件自动发现 / Plugin auto-discovery
✨ 配置管理系统 / Configuration management system
✨ 基类代码复用 / Base class code reuse
✨ 健康检查端点 / Health check endpoint (`/health`)
✨ 更好的日志记录 / Better logging

### 已移除功能 / Removed Features

❌ 无 / None - 完全向后兼容 / Fully backward compatible

---

## 故障排查 / Troubleshooting

### 插件未加载 / Plugin Not Loading

**检查项 / Check:**
1. 插件目录是否有 `__init__.py` / Plugin directory has `__init__.py`
2. `__init__.py` 中是否定义了 `blueprint` 变量 / `blueprint` variable defined in `__init__.py`
3. 查看启动日志中的错误信息 / Check error messages in startup logs

### API 返回 404 / API Returns 404

**检查项 / Check:**
1. 路由是否正确注册 / Route correctly registered
2. URL 前缀是否正确 / URL prefix is correct
3. 使用 `/health` 端点检查插件是否加载 / Use `/health` endpoint to check plugin loading

### 图像处理错误 / Image Processing Error

**检查项 / Check:**
1. 是否继承了正确的基类 / Inherited correct base class
2. 是否调用了 `process_and_send_image()` / Called `process_and_send_image()`
3. 图像对象是否为有效的 PIL Image / Image object is valid PIL Image

---

## 性能优化建议 / Performance Optimization Recommendations

1. **使用缓存 / Use Caching:**
   - 对于不经常变化的数据，考虑添加缓存
   - For infrequently changing data, consider adding caching

2. **异步处理 / Async Processing:**
   - 对于耗时操作，考虑使用异步处理
   - For time-consuming operations, consider async processing

3. **图像优化 / Image Optimization:**
   - 根据需要调整图像质量和大小
   - Adjust image quality and size as needed

---

## 获取帮助 / Getting Help

如果遇到问题，请：

If you encounter issues, please:

1. 查看日志输出 / Check log output
2. 访问 `/health` 端点检查系统状态 / Visit `/health` endpoint to check system status
3. 在 GitHub 上提交 Issue / Submit an issue on GitHub
4. 查看完整文档 `README.md` / See full documentation in `README.md`

---

## 示例代码对比 / Example Code Comparison

### 创建新的图像 API / Creating New Image API

**旧方式 / Old Way:**
```python
# routes/my_module/my_api.py
from flask import send_file, request
from PIL import ImageOps

class MyAPI:
    def get_image(self):
        # 获取参数 / Get parameters
        invert = request.args.get('invert', 'false').lower() == 'true'
        rotate = int(request.args.get('rotate', 0))
        
        # 创建图像 / Create image
        img = create_my_image()
        
        # 处理反色 / Process invert
        if invert:
            img = ImageOps.invert(img.convert('RGB'))
        
        # 处理旋转 / Process rotation
        if rotate in [90, 180, 270]:
            img = img.rotate(rotate, expand=True)
        
        # 转换为字节 / Convert to bytes
        img_io = BytesIO()
        img.save(img_io, 'JPEG', quality=95, subsampling=0)
        img_io.seek(0)
        
        return send_file(img_io, mimetype='image/jpeg')

# main.py
my_api = MyAPI()
app.add_url_rule('/my/img', view_func=my_api.get_image, methods=['GET'])
```

**新方式 / New Way:**
```python
# plugins/my_plugin/__init__.py
from flask import Blueprint
from .routes import my_image_route

blueprint = Blueprint('my_plugin', __name__, url_prefix='/my')
blueprint.add_url_rule('/img', view_func=my_image_route, methods=['GET'])

# plugins/my_plugin/routes.py
from core.base_api import BaseImageAPI

class MyImageAPI(BaseImageAPI):
    def get_image(self):
        img = create_my_image()
        return self.process_and_send_image(img)

my_api = MyImageAPI()
my_image_route = my_api.get_image

# main.py - 无需修改，插件自动加载！
# main.py - No changes needed, plugin auto-loads!
```

---

## 总结 / Summary

新架构提供了：/ New architecture provides:

- ✅ 更好的代码组织 / Better code organization
- ✅ 更容易的功能扩展 / Easier feature extension
- ✅ 减少代码重复 / Reduced code duplication
- ✅ 更好的可维护性 / Better maintainability
- ✅ 完全向后兼容 / Full backward compatibility

开始使用新架构吧！🚀

Start using the new architecture! 🚀
