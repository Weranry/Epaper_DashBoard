# E-Paper_Dashboard

## 项目介绍

本项目为OpenEpaperLink项目的Image_Url功能开发，旨在更简便的获取常用但不需要频繁刷新的信息，由于墨水屏的特殊性质，只需要很少的电量刷新屏幕内容，而不需要额外的电量维持显示，因此我们可以借助静态图片的形式展示一些信息，例如：今天的日历，当前的天气等等。本项目使用Python开发，另有JavaScript版本（目前已弃用），可使用Vercel部署，这种api项目，在请求量和请求次数不是很频繁的状况下，还是更适合使用Vercel这样的无服务器函数，在成本及效果上更优，由于JavaScript的Canvas库需要C++编译器，所以我不得不寻找一种替代方案即PureImage库，但是该库的功能还是较少，而且JavaScript在某些方面的效率并不高，所以我转向了Python开发。


## API接口文档

所有接口均为 HTTP GET 请求，返回 JSON 或 JPEG 图片。

### 公共参数约定

部分图片类接口支持以下通用参数：

- `invert`（可选，bool，默认false）：是否反色，适合墨水屏黑白切换。
- `rotate`（可选，int，0/90/180/270，默认0）：图片旋转角度。

如无特殊说明，以上参数均可用于图片输出接口。

### 1. 日期相关

#### 1.1 获取今日日期信息
**接口**：`/date/json`
**方法**：GET
**参数**：无
**返回**：JSON
**示例返回**：
```json
{
	"solar": "2025-09-12",
	"lunar": "八月初十",
	"ganzhi": "乙巳年 丁酉月 戊子日",
	"season": "白露",
	"festival": "教师节"
}
```

#### 1.2 获取今日日期图片
**接口**：`/date/img`
**方法**：GET
**参数**：
- `invert`（可选，bool，默认false）：是否反色
- `rotate`（可选，int，0/90/180/270，默认0）：旋转角度
**返回**：JPEG图片

#### 1.3 获取月历图片
**接口**：`/date/monthimg`
**方法**：GET
**参数**：
- `year`（可选，int，默认当前年）
- `month`（可选，int，默认当前月）
- `first_day`（可选，'sun'或'mon'，默认'mon'）：每周起始日
- `invert`（可选，bool，默认false）
- `rotate`（可选，int，0/90/180/270，默认0）
**返回**：JPEG图片

#### 1.4 获取黄历图片（B版）
**接口**：`/date/huangli/b`
**方法**：GET
**参数**：
- `invert`（可选，bool，默认false）
- `rotate`（可选，int，0/90/180/270，默认0）
**返回**：JPEG图片

#### 1.5 获取黄历图片（A版）
**接口**：`/date/huangli/a`
**方法**：GET
**参数**：
- `invert`（可选，bool，默认false）
- `rotate`（可选，int，0/90/180/270，默认0）
**返回**：JPEG图片

---

### 2. 天气相关

#### 2.1 获取天气JSON
**接口**：`/weather/now/json/<location>`
**方法**：GET
**参数**：
- `location`（必填，字符串）：地区代码或拼音
**返回**：JSON

#### 2.2 获取天气图片
**接口**：`/weather/now/img/<location>`
**方法**：GET
**参数**：
- `location`（必填，字符串）
- `invert`（可选，bool，默认false）
- `rotate`（可选，int，0/90/180/270，默认0）
**返回**：JPEG图片

#### 2.3 获取天气地形图
**接口**：`/weatherls/<lat>/<lon>/<key>`
**方法**：GET
**参数**：
- `lat`（必填，float）：纬度
- `lon`（必填，float）：经度
- `key`（必填，字符串）：API密钥
- `units`（可选，int，默认0）：单位类型
- `pressure_min`（可选，float，默认980）：最小气压
- `pressure_max`（可选，float，默认1030）：最大气压
**返回**：JPEG图片

---

### 3. 课程表相关

#### 3.1 获取今日课程JSON
**接口**：`/schedule/json`
**方法**：GET
**参数**：无
**返回**：JSON

#### 3.2 获取今日课程图片
**接口**：`/schedule/img`
**方法**：GET
**参数**：
- `invert`（可选，bool，默认false）
- `rotate`（可选，int，0/90/180/270，默认0）
**返回**：JPEG图片

---

### 4. 其他信息类

#### 4.1 获取知乎热榜图片
**接口**：`/zhihu/img`
**方法**：GET
**参数**：
- `invert`（可选，bool，默认false）
- `rotate`（可选，int，0/90/180/270，默认0）
**返回**：JPEG图片

#### 4.2 获取喵喵测月历图片
**接口**：`/miaomiaoce/<channel>`
**方法**：GET
**参数**：
- `channel`（必填，int）：频道号
- `invert`（可选，bool，默认false）
- `rotate`（可选，int，0/90/180/270，默认0）
**返回**：JPEG图片

#### 4.3 获取Steam游戏信息图片
**接口**：`/Steam/getimg/<api_key>/<steam_id>`
**方法**：GET
**参数**：
- `api_key`（必填，字符串）：Steam API Key
- `steam_id`（必填，字符串）：Steam用户ID
- `invert`（可选，bool，默认false）
- `rotate`（可选，int，0/90/180/270，默认0）
**返回**：JPEG图片

#### 4.4 获取维基百科图片
**接口**：`/wiki/img`
**方法**：GET
**参数**：
- `height`（可选，int，默认800）
- `invert`（可选，bool，默认false）
- `rotate`（可选，int，0/90/180/270，默认0）
**返回**：JPEG图片

#### 4.5 获取晴天钟图片
**接口**：`/sunnyclock/<lat>/<lon>`
**方法**：GET
**参数**：
- `lat`（必填，float）：纬度
- `lon`（必填，float）：经度
- `invert`（可选，bool，默认false）
- `rotate`（可选，int，0/90/180/270，默认0）
**返回**：JPEG图片

#### 4.6 获取OneWay图片
**接口**：`/oneway`
**方法**：GET
**参数**：
- `invert`（可选，bool，默认false）
- `rotate`（可选，int，0/90/180/270，默认0）
**返回**：JPEG图片

---

## 主页

访问 `/` 可查看主页，返回 `index.html`。

## 其他

如需 favicon.ico，请访问 `/favicon.ico`。

---

如需更多帮助或有定制需求，请联系开发者。

