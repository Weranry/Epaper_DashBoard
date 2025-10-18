# E-Paper Dashboard

[中文文档](#中文文档) | [English Documentation](#english-documentation)

---

## 中文文档

### 项目介绍

本项目为 OpenEpaperLink 项目的 Image_Url 功能开发，旨在更简便地获取常用但不需要频繁刷新的信息。由于墨水屏的特殊性质，只需要很少的电量刷新屏幕内容，而不需要额外的电量维持显示。本项目采用 **插件化蓝图架构** 重构，使用 Python Flask 框架开发，支持 Vercel 等无服务器平台部署。

### 架构特点

#### 1. 插件化蓝图架构
- **自动发现**: 插件系统自动发现 `plugins/` 目录下的所有插件
- **模块化**: 每个功能模块独立为一个插件，易于维护和扩展
- **解耦合**: 插件之间相互独立，互不影响

#### 2. 代码复用
- **基类抽象**: 提供 `BaseImageAPI` 和 `BaseJsonAPI` 基类
- **工具函数**: 图像处理（反色、旋转）统一由 `ImageProcessor` 处理
- **统一接口**: 所有图像类端点支持统一的 `invert` 和 `rotate` 参数

#### 3. 项目结构

```
Epaper_DashBoard/
├── core/                       # 核心功能模块
│   ├── base_api.py            # API 基类
│   ├── base_image_creator.py  # 图像创建器基类
│   ├── plugin_manager.py      # 插件管理器
│   └── utils/                 # 工具函数
│       └── image_processor.py # 图像处理工具
├── plugins/                   # 插件目录
│   ├── date_plugin/          # 日期相关功能插件
│   ├── weather_plugin/       # 天气相关功能插件
│   ├── schedule_plugin/      # 课程表功能插件
│   └── misc_plugin/          # 其他功能插件
├── image/                     # 图像生成器
├── lib/                       # 业务逻辑库
├── routes/                    # 旧版路由（向后兼容）
├── web/                       # 网络数据获取
├── assets/                    # 资源文件
├── data/                      # 数据文件
├── main.py                    # 主应用入口
└── requirements.txt           # 项目依赖
```

### 快速开始

#### 安装依赖

```bash
pip install -r requirements.txt
```

#### 运行应用

```bash
python main.py
```

应用默认运行在 `http://localhost:5000`

#### 健康检查

```bash
curl http://localhost:5000/health
```

### API 文档

#### 通用参数

大部分图片类接口支持以下通用参数：

- `invert` (可选, bool, 默认 false): 是否反色，适合墨水屏黑白切换
- `rotate` (可选, int, 0/90/180/270, 默认 0): 图片旋转角度

---

### 日期相关 API (`/date/*`)

#### 1.1 获取今日日期信息
- **接口**: `GET /date/json`
- **参数**: 无
- **返回**: JSON 格式的日期信息
- **示例**:
  ```bash
  curl http://localhost:5000/date/json
  ```
  ```json
  {
    "solar": {
      "solar_year": "2025",
      "solar_month": "10",
      "solar_day": "18",
      "weekday": "周六"
    },
    "lunar": {
      "lunar_year": "二〇二五",
      "lunar_month": "八月",
      "lunar_day": "廿七"
    },
    "ganzhi": {
      "ganzhi_year": "乙巳年",
      "ganzhi_month": "丙戌月",
      "ganzhi_day": "庚申日",
      "shengxiao": "蛇"
    },
    "season": {
      "wu_hou": "菊有黄花",
      "hou": "寒露 三候",
      "fujiu": ""
    },
    "festival": {
      "solar_festival": "",
      "lunar_festival": ""
    }
  }
  ```

#### 1.2 获取今日日期图片
- **接口**: `GET /date/img`
- **参数**: 支持通用参数 (invert, rotate)
- **返回**: JPEG 图片

#### 1.3 获取月历图片
- **接口**: `GET /date/monthimg`
- **参数**: 
  - `year` (可选, int): 年份，默认当前年
  - `month` (可选, int): 月份，默认当前月
  - `first_day` (可选, 'sun'/'mon'): 每周起始日，默认 'mon'
  - 支持通用参数 (invert, rotate)
- **返回**: JPEG 图片

#### 1.4 获取黄历图片（B 版）
- **接口**: `GET /date/huangli/b`
- **参数**: 支持通用参数 (invert, rotate)
- **返回**: JPEG 图片

#### 1.5 获取黄历图片（A 版）
- **接口**: `GET /date/huangli/a`
- **参数**: 支持通用参数 (invert, rotate)
- **返回**: JPEG 图片

---

### 天气相关 API (`/weather/*`)

#### 2.1 获取天气 JSON
- **接口**: `GET /weather/now/json/<location>`
- **参数**: 
  - `location` (必填, 字符串): 地区代码或拼音
- **返回**: JSON 格式的天气信息

#### 2.2 获取天气图片
- **接口**: `GET /weather/now/img/<location>`
- **参数**: 
  - `location` (必填, 字符串): 地区代码或拼音
  - 支持通用参数 (invert, rotate)
- **返回**: JPEG 图片
- **示例**: 
  ```bash
  curl http://localhost:5000/weather/now/img/beijing -o weather.jpg
  ```

#### 2.3 获取天气地形图
- **接口**: `GET /weather/landscape/<lat>/<lon>/<key>`
- **参数**: 
  - `lat` (必填, float): 纬度
  - `lon` (必填, float): 经度
  - `key` (必填, 字符串): API 密钥
  - `units` (可选, int, 默认 0): 单位类型
  - `pressure_min` (可选, float, 默认 980): 最小气压
  - `pressure_max` (可选, float, 默认 1030): 最大气压
  - 支持通用参数 (invert, rotate)
- **返回**: JPEG 图片

---

### 课程表相关 API (`/schedule/*`)

#### 3.1 获取今日课程 JSON
- **接口**: `GET /schedule/json`
- **参数**: 无
- **返回**: JSON 格式的课程信息

#### 3.2 获取今日课程图片
- **接口**: `GET /schedule/img`
- **参数**: 支持通用参数 (invert, rotate)
- **返回**: JPEG 图片

---

### 其他功能 API

#### 4.1 获取知乎热榜图片
- **接口**: `GET /zhihu/img`
- **参数**: 支持通用参数 (invert, rotate)
- **返回**: JPEG 图片

#### 4.2 获取秒秒测月历图片
- **接口**: `GET /miaomiaoce/<channel>`
- **参数**: 
  - `channel` (必填, int): 频道号
  - 支持通用参数 (invert, rotate)
- **返回**: JPEG 图片

**频道对照表**:

| 序号 | 名称   | 频道 |
|------|--------|------|
| 1    | 单词历 | 17   |
| 2    | 党史历 | 16   |
| 3    | 她说历 | 15   |
| 4    | 老爸历 | 14   |
| 5    | 怡禾历 | 13   |
| 6    | 古诗词 | 10   |
| 7    | 冷知识 | 9    |
| 8    | 乌鸡汤 | 6    |
| 9    | 名著历 | 4    |
| 10   | 健康历 | 3    |
| 11   | 胖柠檬 | 2    |
| 12   | 老黄历 | 1    |

#### 4.3 获取 Steam 游戏信息图片
- **接口**: `GET /Steam/getimg/<api_key>/<steam_id>`
- **参数**: 
  - `api_key` (必填, 字符串): Steam API Key
  - `steam_id` (必填, 字符串): Steam 用户 ID
  - 支持通用参数 (invert, rotate)
- **返回**: JPEG 图片

#### 4.4 获取维基百科图片
- **接口**: `GET /wiki/img`
- **参数**: 
  - `height` (可选, int, 默认 800): 图片高度
  - 支持通用参数 (invert, rotate)
- **返回**: JPEG 图片

#### 4.5 获取晴天钟图片
- **接口**: `GET /sunnyclock/<lat>/<lon>`
- **参数**: 
  - `lat` (必填, float): 纬度
  - `lon` (必填, float): 经度
  - 支持通用参数 (invert, rotate)
- **返回**: JPEG 图片

#### 4.6 获取 OneWay 图片
- **接口**: `GET /oneway`
- **参数**: 支持通用参数 (invert, rotate)
- **返回**: JPEG 图片

---

### 开发插件

#### 创建新插件

1. 在 `plugins/` 目录下创建新的插件文件夹，例如 `my_plugin/`

2. 创建 `__init__.py` 文件定义蓝图：

```python
"""My Plugin - description"""
from flask import Blueprint
from .routes import my_route

# Create blueprint
blueprint = Blueprint('my_plugin', __name__, url_prefix='/myplugin')

# Register routes
blueprint.add_url_rule('/endpoint', view_func=my_route, methods=['GET'])
```

3. 创建 `routes.py` 文件定义路由逻辑：

```python
"""My Plugin routes"""
from core.base_api import BaseImageAPI, BaseJsonAPI

class MyAPI(BaseImageAPI):
    """My API description"""
    def __init__(self):
        super().__init__()
    
    def get_my_data(self):
        # Your logic here
        img = create_my_image()
        return self.process_and_send_image(img)

# Create route instance
my_api = MyAPI()
my_route = my_api.get_my_data
```

4. 重启应用，插件将自动被发现和注册

#### 使用基类

**BaseImageAPI**: 用于返回图片的 API
- 自动处理 `invert` 和 `rotate` 参数
- 提供 `process_and_send_image()` 方法处理和发送图片

**BaseJsonAPI**: 用于返回 JSON 的 API
- 提供标准的 JSON API 基础

**BaseImageCreator**: 用于图像创建
- 提供标准的图像创建方法
- 包含常用字体加载

---

### 部署

#### Vercel 部署

项目已配置 `vercel.json`，可直接部署到 Vercel。

#### Docker 部署

```bash
# 构建镜像
docker build -t epaper-dashboard .

# 运行容器
docker run -p 5000:5000 epaper-dashboard
```

---

### 许可证

本项目采用开源许可证，具体请查看 LICENSE 文件。

---

## English Documentation

### Project Introduction

This project is developed for the Image_Url functionality of the OpenEpaperLink project, aiming to easily obtain commonly used information that doesn't require frequent refreshing. Due to the special nature of e-paper displays, they only need minimal power to refresh screen content without additional power to maintain the display. This project has been refactored with a **plugin-based blueprint architecture**, developed using Python Flask framework, and supports deployment on serverless platforms like Vercel.

### Architecture Features

#### 1. Plugin-based Blueprint Architecture
- **Auto-discovery**: Plugin system automatically discovers all plugins in the `plugins/` directory
- **Modular**: Each functional module is independent as a plugin, easy to maintain and extend
- **Decoupled**: Plugins are independent of each other and do not affect one another

#### 2. Code Reuse
- **Base Class Abstraction**: Provides `BaseImageAPI` and `BaseJsonAPI` base classes
- **Utility Functions**: Image processing (invert, rotate) is uniformly handled by `ImageProcessor`
- **Unified Interface**: All image endpoints support unified `invert` and `rotate` parameters

#### 3. Project Structure

```
Epaper_DashBoard/
├── core/                       # Core functionality modules
│   ├── base_api.py            # API base classes
│   ├── base_image_creator.py  # Image creator base class
│   ├── plugin_manager.py      # Plugin manager
│   └── utils/                 # Utility functions
│       └── image_processor.py # Image processing utilities
├── plugins/                   # Plugin directory
│   ├── date_plugin/          # Date-related functionality plugin
│   ├── weather_plugin/       # Weather-related functionality plugin
│   ├── schedule_plugin/      # Schedule functionality plugin
│   └── misc_plugin/          # Miscellaneous functionality plugin
├── image/                     # Image generators
├── lib/                       # Business logic libraries
├── routes/                    # Legacy routes (backward compatible)
├── web/                       # Network data fetching
├── assets/                    # Resource files
├── data/                      # Data files
├── main.py                    # Main application entry
└── requirements.txt           # Project dependencies
```

### Quick Start

#### Install Dependencies

```bash
pip install -r requirements.txt
```

#### Run Application

```bash
python main.py
```

Application runs on `http://localhost:5000` by default

#### Health Check

```bash
curl http://localhost:5000/health
```

### API Documentation

See Chinese documentation above for detailed API endpoints. All endpoints support:
- Common parameters: `invert` (boolean) and `rotate` (0/90/180/270)
- Returns JPEG images or JSON data as appropriate

### Development

#### Creating New Plugins

Follow the plugin structure in the Chinese documentation section. Create a new folder in `plugins/`, define your blueprint in `__init__.py`, and implement your routes in `routes.py`.

### License

This project is open-sourced. Please see LICENSE file for details.
