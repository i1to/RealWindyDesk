@echo off
echo 正在安装中国气象网实时风流场桌面壁纸程序...
echo.

REM 检查Python是否已安装
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未检测到Python。请安装Python 3.6或更高版本。
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 安装依赖
echo 正在安装Python依赖...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo 安装依赖失败。请检查网络连接或手动运行 'pip install -r requirements.txt'
    pause
    exit /b 1
)

echo.
echo 依赖安装完成！
echo.

REM 检查ChromeDriver
if not exist chromedriver.exe (
    echo 警告: 未找到ChromeDriver (chromedriver.exe)
    echo 请下载与您Chrome浏览器版本匹配的ChromeDriver，并将其放在程序目录下。
    echo 下载地址: https://chromedriver.chromium.org/downloads
    echo.
)

echo 安装完成！
echo.
echo 使用方法:
echo 1. 确保已下载ChromeDriver并放置在程序目录下
echo 2. 运行 'python src/wind_wallpaper_new.py' 启动程序
echo.
echo 详细说明请参阅 USAGE_GUIDE.md 文件
echo.
pause
