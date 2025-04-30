# 中国气象网实时风流场桌面壁纸使用指南

本指南将帮助您设置和使用中国气象网实时风流场桌面壁纸程序。

## 安装步骤

### 1. 安装Python依赖

首先，您需要安装程序所需的Python依赖包。在命令行中运行：

```bash
pip install -r requirements.txt
```

### 2. 下载Chrome驱动

程序使用Selenium和Chrome浏览器来获取中国气象网的风流场数据。您需要下载与您的Chrome浏览器版本匹配的ChromeDriver：

1. 检查您的Chrome浏览器版本：
   - 打开Chrome
   - 点击右上角的三点菜单
   - 选择"帮助" > "关于Google Chrome"
   - 记下显示的版本号（例如：96.0.4664.110）

2. 下载对应版本的ChromeDriver：
   - 访问 https://chromedriver.chromium.org/downloads
   - 选择与您Chrome版本匹配的驱动版本
   - 下载适用于您操作系统的驱动文件

3. 将下载的`chromedriver.exe`文件放在程序目录下

### 3. 配置程序

打开`src/wind_wallpaper_new.py`文件，根据需要修改以下配置：

```python
# 配置
WEATHER_URL = "https://www.weather.com.cn/radar/"  # 中国气象网雷达页面
WALLPAPER_PATH = "wind_wallpaper.png"  # 壁纸保存路径
SCREENSHOT_PATH = "wind_screenshot.png"  # 截图保存路径
UPDATE_INTERVAL = 1800  # 更新间隔（秒），30分钟
CHROME_DRIVER_PATH = "chromedriver.exe"  # Chrome驱动路径，需要根据实际情况修改
```

特别注意：
- 如果您将ChromeDriver放在其他位置，请更新`CHROME_DRIVER_PATH`
- 如果您希望更频繁地更新壁纸，可以减小`UPDATE_INTERVAL`的值

## 运行程序

在命令行中运行以下命令启动程序：

```bash
python src/wind_wallpaper_new.py
```

程序将执行以下操作：
1. 启动无头Chrome浏览器
2. 访问中国气象网雷达页面
3. 切换到风流场视图
4. 截取风流场图像
5. 生成包含时间戳和数据来源的壁纸
6. 设置为桌面壁纸
7. 按照设定的时间间隔定期重复上述步骤

## 故障排除

如果程序无法正常运行，请检查以下几点：

1. **ChromeDriver版本不匹配**：
   - 错误信息通常包含"browser version is xxx but ChromeDriver version is yyy"
   - 解决方法：下载与您Chrome浏览器版本匹配的ChromeDriver

2. **网络连接问题**：
   - 确保您的计算机能够访问中国气象网
   - 如果您使用代理，可能需要在程序中配置代理设置

3. **页面元素定位失败**：
   - 如果中国气象网的页面结构发生变化，程序可能无法找到风流场选项或地图容器
   - 解决方法：更新程序中的CSS选择器或XPath表达式

4. **权限问题**：
   - 确保程序有权限写入文件和设置壁纸
   - 尝试以管理员身份运行命令提示符

## 自定义

如果您想自定义壁纸的外观，可以修改`create_wind_wallpaper`函数。例如：

- 更改背景颜色
- 调整截图的位置和大小
- 添加更多信息或装饰元素
- 使用不同的字体和颜色

## 设置开机自启动

要使程序在Windows启动时自动运行：

1. 创建一个批处理文件（例如`start_wind_wallpaper.bat`），内容如下：
   ```batch
   @echo off
   cd /d %~dp0
   python src/wind_wallpaper_new.py
   ```

2. 将此批处理文件的快捷方式放入启动文件夹：
   - 按下`Win+R`，输入`shell:startup`，按回车
   - 将批处理文件的快捷方式复制到打开的文件夹中

## 注意事项

- 程序会在后台持续运行，消耗一定的系统资源
- 频繁更新壁纸可能会增加网络流量和系统负载
- 该程序仅供个人学习和研究使用，请勿用于商业目的
- 数据来源于中国气象网，请尊重其版权和使用条款
