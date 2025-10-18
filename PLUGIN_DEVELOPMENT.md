# 插件开发指南 / Plugin Development Guide

本指南介绍如何为 E-Paper Dashboard 开发插件。

This guide explains how to develop plugins for E-Paper Dashboard.

---

## 插件结构 / Plugin Structure

### 基本结构 / Basic Structure

```
plugins/
└── my_plugin/
    ├── __init__.py      # 插件入口，定义蓝图 / Plugin entry, defines blueprint
    ├── routes.py        # 路由实现 / Route implementations
    └── README.md        # (可选) 插件文档 / (Optional) Plugin documentation
```

---

## 快速开始 / Quick Start

### 步骤 1: 创建插件目录 / Step 1: Create Plugin Directory

```bash
mkdir -p plugins/my_plugin
```

### 步骤 2: 创建 `__init__.py` / Step 2: Create `__init__.py`

```python
"""My Plugin - provides XYZ functionality"""
from flask import Blueprint
from .routes import example_route

# Create blueprint
blueprint = Blueprint('my_plugin', __name__, url_prefix='/myplugin')

# Register routes
blueprint.add_url_rule('/example', view_func=example_route, methods=['GET'])
```

### 步骤 3: 创建 `routes.py` / Step 3: Create `routes.py`

```python
"""My Plugin routes"""
from core.base_api import BaseImageAPI, BaseJsonAPI
from flask import jsonify

class ExampleAPI(BaseImageAPI):
    """Example API endpoint"""
    
    def __init__(self):
        super().__init__()
    
    def get_example(self):
        # Your implementation here
        # 在这里实现你的逻辑
        return jsonify({"message": "Hello from my plugin!"})

# Create route instance
example_api = ExampleAPI()
example_route = example_api.get_example
```

### 步骤 4: 重启应用 / Step 4: Restart Application

```bash
python main.py
```

插件将被自动发现和注册！

The plugin will be automatically discovered and registered!

---

## 使用基类 / Using Base Classes

### BaseImageAPI - 图像 API 基类 / Image API Base Class

用于返回图像的 API 端点。

For API endpoints that return images.

**功能 / Features:**
- ✅ 自动处理 `invert` 参数 / Auto handles `invert` parameter
- ✅ 自动处理 `rotate` 参数 / Auto handles `rotate` parameter
- ✅ 提供 `process_and_send_image()` 方法 / Provides `process_and_send_image()` method

**示例 / Example:**

```python
from core.base_api import BaseImageAPI
from PIL import Image

class MyImageAPI(BaseImageAPI):
    def get_my_image(self):
        # 创建图像 / Create image
        img = Image.new('RGB', (400, 300), color='white')
        
        # 使用基类方法自动处理参数并发送
        # Use base class method to auto-process and send
        return self.process_and_send_image(img)

my_api = MyImageAPI()
my_route = my_api.get_my_image
```

**可用方法 / Available Methods:**

- `get_common_params()`: 获取通用参数（invert, rotate）/ Get common parameters
- `process_and_send_image(img, mimetype='image/jpeg')`: 处理并发送图像 / Process and send image

### BaseJsonAPI - JSON API 基类 / JSON API Base Class

用于返回 JSON 的 API 端点。

For API endpoints that return JSON.

**示例 / Example:**

```python
from core.base_api import BaseJsonAPI
from flask import jsonify

class MyJsonAPI(BaseJsonAPI):
    def get_my_data(self):
        data = {
            "key": "value",
            "items": [1, 2, 3]
        }
        return jsonify(data)

my_json_api = MyJsonAPI()
my_json_route = my_json_api.get_my_data
```

### BaseImageCreator - 图像创建器基类 / Image Creator Base Class

用于创建图像的类。

For classes that create images.

**功能 / Features:**
- ✅ 预加载常用字体 / Pre-loads common fonts
- ✅ 提供标准图像创建方法 / Provides standard image creation methods
- ✅ 统一的图像字节转换 / Unified image bytes conversion

**示例 / Example:**

```python
from core.base_image_creator import BaseImageCreator
from PIL import ImageDraw

class MyImageCreator(BaseImageCreator):
    def create_image(self, data):
        # 创建基础图像 / Create base image
        img = self.create_base_image(width=400, height=300)
        draw = ImageDraw.Draw(img)
        
        # 绘制内容 / Draw content
        draw.text((10, 10), "Hello World", font=self.font_medium, fill=1)
        
        # 转换为 RGB / Convert to RGB
        return img.convert('RGB')

creator = MyImageCreator()
img = creator.create_image({"text": "example"})
img_bytes = creator.get_image_bytes(img)
```

**可用属性 / Available Attributes:**

- `self.font_small`: 12px 字体 / 12px font
- `self.font_normal`: 14px 字体 / 14px font
- `self.font_medium`: 18px 字体 / 18px font
- `self.font_large`: 24px 字体 / 24px font
- `self.font_xlarge`: 120px 字体 / 120px font
- `self.image_processor`: 图像处理器实例 / ImageProcessor instance

**可用方法 / Available Methods:**

- `create_base_image(width, height, mode)`: 创建基础图像 / Create base image
- `get_image_bytes(img, format, quality, subsampling)`: 转换为字节 / Convert to bytes

---

## 图像处理工具 / Image Processing Utilities

### ImageProcessor

处理图像的工具类。

Utility class for image processing.

```python
from core.utils.image_processor import ImageProcessor

processor = ImageProcessor()

# 应用反色 / Apply invert
img = processor.apply_invert(img, invert=True)

# 应用旋转 / Apply rotation
img = processor.apply_rotation(img, rotate=90)

# 应用所有处理 / Apply all processing
img = processor.process_image(img, invert=True, rotate=90)

# 转换为字节 / Convert to bytes
img_bytes = processor.get_image_bytes(img)
```

---

## 路由注册 / Route Registration

### 基本路由 / Basic Routes

```python
# plugins/my_plugin/__init__.py
blueprint = Blueprint('my_plugin', __name__, url_prefix='/myplugin')

# 简单路由 / Simple route
blueprint.add_url_rule('/simple', view_func=simple_route, methods=['GET'])

# 带参数的路由 / Route with parameters
blueprint.add_url_rule('/item/<int:item_id>', view_func=item_route, methods=['GET'])

# 多种方法 / Multiple methods
blueprint.add_url_rule('/data', view_func=data_route, methods=['GET', 'POST'])
```

### URL 参数 / URL Parameters

```python
# 路径参数 / Path parameters
@blueprint.route('/user/<username>')
def user_profile(username):
    return f"User: {username}"

# 类型转换 / Type conversion
@blueprint.route('/post/<int:post_id>')
def show_post(post_id):
    return f"Post ID: {post_id}"

# 查询参数 / Query parameters
from flask import request

def my_route():
    page = request.args.get('page', default=1, type=int)
    size = request.args.get('size', default=10, type=int)
    return jsonify({"page": page, "size": size})
```

---

## 错误处理 / Error Handling

### 返回错误响应 / Return Error Responses

```python
from flask import jsonify

class MyAPI(BaseImageAPI):
    def get_data(self):
        data = fetch_data()
        
        if data is None:
            return jsonify({"error": "Data not found"}), 404
        
        if not validate(data):
            return jsonify({"error": "Invalid data"}), 400
        
        return jsonify(data)
```

### 异常处理 / Exception Handling

```python
class MyAPI(BaseImageAPI):
    def get_image(self):
        try:
            img = create_image()
            return self.process_and_send_image(img)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            logger.error(f"Error creating image: {e}")
            return jsonify({"error": "Internal server error"}), 500
```

---

## 测试插件 / Testing Plugins

### 手动测试 / Manual Testing

```bash
# 启动服务器 / Start server
python main.py

# 测试端点 / Test endpoint
curl http://localhost:5000/myplugin/example

# 测试带参数 / Test with parameters
curl "http://localhost:5000/myplugin/image?invert=true&rotate=90" -o test.jpg
```

### 使用 Python 测试 / Testing with Python

```python
import requests

# 测试 JSON 端点 / Test JSON endpoint
response = requests.get('http://localhost:5000/myplugin/data')
print(response.json())

# 测试图像端点 / Test image endpoint
response = requests.get('http://localhost:5000/myplugin/image')
with open('output.jpg', 'wb') as f:
    f.write(response.content)
```

---

## 最佳实践 / Best Practices

### 1. 命名规范 / Naming Conventions

- 插件目录：`my_plugin` (小写+下划线) / Plugin directory: lowercase with underscores
- 蓝图名称：`'my_plugin'` / Blueprint name
- URL 前缀：`'/myplugin'` (小写) / URL prefix: lowercase
- 类名：`MyPluginAPI` (驼峰命名) / Class names: CamelCase

### 2. 文档 / Documentation

在每个插件中添加文档字符串：

Add docstrings to each plugin:

```python
"""
My Plugin

This plugin provides XYZ functionality for E-Paper Dashboard.

Endpoints:
- GET /myplugin/example - Returns example data
- GET /myplugin/image - Returns an image

Author: Your Name
Version: 1.0.0
"""
```

### 3. 日志记录 / Logging

使用 Python logging 模块：

Use Python logging module:

```python
import logging

logger = logging.getLogger(__name__)

class MyAPI(BaseImageAPI):
    def get_data(self):
        logger.info("Fetching data...")
        data = fetch_data()
        logger.debug(f"Fetched {len(data)} items")
        return jsonify(data)
```

### 4. 配置管理 / Configuration Management

使用 Flask 配置系统：

Use Flask configuration system:

```python
from flask import current_app

class MyAPI(BaseImageAPI):
    def get_data(self):
        # 访问配置 / Access configuration
        timeout = current_app.config.get('MY_TIMEOUT', 30)
        return fetch_data(timeout=timeout)
```

### 5. 依赖管理 / Dependency Management

如果插件需要额外的依赖，在插件目录中创建 `requirements.txt`：

If plugin requires additional dependencies, create `requirements.txt` in plugin directory:

```
# plugins/my_plugin/requirements.txt
extra-package==1.0.0
```

---

## 高级功能 / Advanced Features

### 1. 数据缓存 / Data Caching

```python
from functools import lru_cache
from datetime import datetime, timedelta

class MyAPI(BaseImageAPI):
    _cache = None
    _cache_time = None
    
    def _get_cached_data(self):
        now = datetime.now()
        
        # 缓存 5 分钟 / Cache for 5 minutes
        if (self._cache is None or 
            self._cache_time is None or 
            now - self._cache_time > timedelta(minutes=5)):
            
            self._cache = fetch_expensive_data()
            self._cache_time = now
        
        return self._cache
    
    def get_data(self):
        data = self._get_cached_data()
        return jsonify(data)
```

### 2. 异步请求 / Async Requests

```python
import asyncio
import aiohttp

class MyAPI(BaseImageAPI):
    async def fetch_async(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.text()
    
    def get_data(self):
        # 运行异步函数 / Run async function
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        data = loop.run_until_complete(self.fetch_async('http://api.example.com'))
        loop.close()
        return jsonify({"data": data})
```

### 3. 文件上传 / File Upload

```python
from flask import request
from werkzeug.utils import secure_filename

class MyAPI(BaseImageAPI):
    def upload_file(self):
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        
        if file:
            filename = secure_filename(file.filename)
            # 处理文件 / Process file
            return jsonify({"filename": filename}), 200
```

---

## 示例插件 / Example Plugins

### 示例 1: 简单文本图像 / Example 1: Simple Text Image

```python
# plugins/text_plugin/__init__.py
from flask import Blueprint
from .routes import text_image_route

blueprint = Blueprint('text', __name__, url_prefix='/text')
blueprint.add_url_rule('/img', view_func=text_image_route, methods=['GET'])

# plugins/text_plugin/routes.py
from core.base_api import BaseImageAPI
from core.base_image_creator import BaseImageCreator
from flask import request
from PIL import ImageDraw

class TextImageCreator(BaseImageCreator):
    def create_text_image(self, text, color='black'):
        img = self.create_base_image(400, 300)
        draw = ImageDraw.Draw(img)
        draw.text((20, 20), text, font=self.font_large, fill=1)
        return img.convert('RGB')

class TextImageAPI(BaseImageAPI):
    def __init__(self):
        super().__init__()
        self.creator = TextImageCreator()
    
    def get_text_image(self):
        text = request.args.get('text', 'Hello World')
        img = self.creator.create_text_image(text)
        return self.process_and_send_image(img)

text_image_api = TextImageAPI()
text_image_route = text_image_api.get_text_image
```

### 示例 2: API 数据聚合 / Example 2: API Data Aggregation

```python
# plugins/aggregate_plugin/__init__.py
from flask import Blueprint
from .routes import aggregate_route

blueprint = Blueprint('aggregate', __name__, url_prefix='/aggregate')
blueprint.add_url_rule('/data', view_func=aggregate_route, methods=['GET'])

# plugins/aggregate_plugin/routes.py
from core.base_api import BaseJsonAPI
from flask import jsonify
import requests

class AggregateAPI(BaseJsonAPI):
    def get_aggregate_data(self):
        # 从多个 API 获取数据 / Fetch from multiple APIs
        data1 = requests.get('http://api1.example.com/data').json()
        data2 = requests.get('http://api2.example.com/data').json()
        
        # 聚合数据 / Aggregate data
        result = {
            'source1': data1,
            'source2': data2,
            'combined': self._combine(data1, data2)
        }
        
        return jsonify(result)
    
    def _combine(self, data1, data2):
        # 合并逻辑 / Merge logic
        return {**data1, **data2}

aggregate_api = AggregateAPI()
aggregate_route = aggregate_api.get_aggregate_data
```

---

## 故障排查 / Troubleshooting

### 插件未加载 / Plugin Not Loading

**问题 / Issue:** 插件没有出现在日志中 / Plugin doesn't appear in logs

**解决方案 / Solution:**
1. 检查目录结构 / Check directory structure
2. 确保有 `__init__.py` / Ensure `__init__.py` exists
3. 检查是否定义了 `blueprint` 变量 / Check if `blueprint` variable is defined

### 导入错误 / Import Errors

**问题 / Issue:** `ModuleNotFoundError` 或 `ImportError`

**解决方案 / Solution:**
1. 检查导入路径 / Check import paths
2. 确保所有依赖已安装 / Ensure all dependencies are installed
3. 检查 Python 路径 / Check Python path

### 路由冲突 / Route Conflicts

**问题 / Issue:** 路由被覆盖或不可访问 / Routes are overridden or inaccessible

**解决方案 / Solution:**
1. 使用唯一的 URL 前缀 / Use unique URL prefix
2. 检查是否有重复的路由定义 / Check for duplicate route definitions
3. 使用 `/health` 端点查看已注册的插件 / Use `/health` endpoint to see registered plugins

---

## 资源 / Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Pillow Documentation](https://pillow.readthedocs.io/)
- [Python Logging](https://docs.python.org/3/library/logging.html)

---

## 贡献 / Contributing

欢迎贡献新插件！

Contributions of new plugins are welcome!

1. Fork 项目 / Fork the project
2. 创建插件 / Create your plugin
3. 测试插件 / Test your plugin
4. 提交 Pull Request / Submit a Pull Request

---

Happy coding! 🚀
