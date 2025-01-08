# 项目名称

## 项目介绍

这个项目是一个多功能的 Flask 应用程序，提供天气信息、课程表、知乎每日内容和 MMC 日历图像的获取和展示功能。应用程序使用了多种 Python 库来处理 HTTP 请求、图像生成和数据解析。

### 功能

- **天气信息**：获取当前天气的 JSON 数据和图像。
- **课程表**：获取当前课程的 JSON 数据和图像。
- **知乎内容**：获取知乎每日内容的图像。
- **MMC 日历**：获取指定频道的日历图像。

## 请求内容

### 1. 获取天气信息

- **获取天气 JSON 数据**：
  ```
  GET /weather/now/json/<location>
  ```
  示例请求：
  ```
  GET /weather/now/json/beijing
  ```

- **获取天气图像**：
  ```
  GET /weather/now/img/<location>
  ```
  示例请求：
  ```
  GET /weather/now/img/beijing
  ```

### 2. 获取课程表

- **获取课程表 JSON 数据**：
  ```
  GET /schedule/json
  ```

- **获取课程表图像**：
  ```
  GET /schedule/img
  ```

### 3. 获取知乎内容图像

- **获取知乎图像**：
  ```
  GET /zhihu/img
  ```

### 4. 获取 MMC 日历图像

- **获取指定频道的日历图像**：
  ```
  GET /MMC/<channel>
  ```
  示例请求：
  ```
  GET /MMC/21
  ```

## 安装依赖

在项目根目录下运行以下命令以安装所需的依赖：
