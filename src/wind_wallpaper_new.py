import requests
import json
from PIL import Image, ImageDraw, ImageFont
import ctypes
import os
import time
import math
import schedule
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import io
from datetime import datetime

# 配置
WEATHER_URL = "https://www.weather.com.cn/radar/"  # 中国气象网雷达页面
WALLPAPER_PATH = "wind_wallpaper.png"  # 壁纸保存路径
SCREENSHOT_PATH = "wind_screenshot.png"  # 截图保存路径
UPDATE_INTERVAL = 1800  # 更新间隔（秒），30分钟
CHROME_DRIVER_PATH = "chromedriver.exe"  # Chrome驱动路径，需要根据实际情况修改

# 获取实时风流场数据（通过截图方式）
def fetch_wind_data():
    try:
        print("启动浏览器...")
        # 配置Chrome选项
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # 无头模式
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--no-sandbox")

        # 创建Chrome浏览器实例
        service = Service(CHROME_DRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # 访问中国气象网雷达页面
        print(f"访问 {WEATHER_URL}...")
        driver.get(WEATHER_URL)

        # 等待页面加载完成
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".mapContainer"))
        )

        # 点击风流场选项
        print("切换到风流场视图...")
        wind_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//li[contains(text(), '风流场')]"))
        )
        wind_option.click()

        # 等待风流场数据加载
        time.sleep(5)

        # 获取当前时间作为风向数据的时间戳
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")

        # 截取风流场图
        print("截取风流场图...")
        map_element = driver.find_element(By.CSS_SELECTOR, ".mapContainer")
        screenshot = map_element.screenshot_as_png

        # 保存截图
        with open(SCREENSHOT_PATH, "wb") as file:
            file.write(screenshot)

        print(f"风流场截图已保存到 {SCREENSHOT_PATH}")
        driver.quit()

        # 返回时间戳（作为风向描述）和截图路径
        return current_time, SCREENSHOT_PATH, None
    except Exception as e:
        print(f"获取风流场数据失败: {e}")
        if 'driver' in locals():
            driver.quit()
        return None, None, None

# 创建风流场壁纸
def create_wind_wallpaper(timestamp, screenshot_path, _):
    try:
        print(f"正在打开截图: {screenshot_path}")
        # 打开截图
        screenshot = Image.open(screenshot_path)
        print(f"截图尺寸: {screenshot.width}x{screenshot.height}, 格式: {screenshot.format}")

        # 创建壁纸画布（1920x1080，适应常见屏幕分辨率）
        wallpaper = Image.new("RGB", (1920, 1080), "white")

        # 计算截图在壁纸中的位置（居中）
        x = (1920 - screenshot.width) // 2
        y = (1080 - screenshot.height) // 2

        # 将截图粘贴到壁纸上
        wallpaper.paste(screenshot, (x, y))

        # 添加时间戳和来源信息
        draw = ImageDraw.Draw(wallpaper)

        # 使用默认字体（如果没有指定字体文件）
        try:
            font = ImageFont.truetype("arial.ttf", 24)
            print("使用Arial字体")
        except IOError:
            try:
                # 尝试使用Windows系统字体
                font = ImageFont.truetype("C:\\Windows\\Fonts\\Arial.ttf", 24)
                print("使用Windows系统Arial字体")
            except IOError:
                font = ImageFont.load_default()
                print("使用默认字体")

        # 添加时间戳
        draw.text((20, 20), f"更新时间: {timestamp}", fill="black", font=font)

        # 添加数据来源
        draw.text((20, 50), "数据来源: 中国气象网 (www.weather.com.cn)", fill="black", font=font)

        # 确保目录存在
        wallpaper_dir = os.path.dirname(os.path.abspath(WALLPAPER_PATH))
        if not os.path.exists(wallpaper_dir):
            os.makedirs(wallpaper_dir)
            print(f"创建目录: {wallpaper_dir}")

        # 保存壁纸 (使用BMP格式，Windows壁纸更兼容)
        bmp_path = WALLPAPER_PATH.replace('.png', '.bmp')
        wallpaper.save(bmp_path, "BMP")
        print(f"壁纸已保存为BMP格式: {bmp_path}")

        # 同时保存PNG格式作为备份
        wallpaper.save(WALLPAPER_PATH)
        print(f"壁纸已保存为PNG格式: {WALLPAPER_PATH}")

        # 更新全局变量，使用BMP路径
        global WALLPAPER_PATH
        WALLPAPER_PATH = bmp_path

        return True
    except Exception as e:
        print(f"创建壁纸失败: {e}")
        import traceback
        traceback.print_exc()
        return False

# 设置Windows桌面壁纸
def set_wallpaper():
    try:
        # 检查壁纸文件是否存在
        abs_path = os.path.abspath(WALLPAPER_PATH)
        if not os.path.exists(abs_path):
            print(f"错误: 壁纸文件不存在: {abs_path}")
            return False

        print(f"正在设置壁纸: {abs_path}")

        # 尝试使用不同的方法设置壁纸

        # 方法1: 使用Windows API (SPI_SETDESKWALLPAPER = 20)
        result = ctypes.windll.user32.SystemParametersInfoW(20, 0, abs_path, 3)
        if result:
            print("方法1成功: 使用SystemParametersInfoW设置壁纸")
            return True
        else:
            print(f"方法1失败: SystemParametersInfoW返回{result}")

        # 方法2: 尝试使用另一种方式调用API
        SPI_SETDESKWALLPAPER = 0x0014
        SPIF_UPDATEINIFILE = 0x01
        SPIF_SENDCHANGE = 0x02
        result = ctypes.windll.user32.SystemParametersInfoW(
            SPI_SETDESKWALLPAPER,
            0,
            abs_path,
            SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
        )
        if result:
            print("方法2成功: 使用明确常量的SystemParametersInfoW设置壁纸")
            return True
        else:
            print(f"方法2失败: 明确常量的SystemParametersInfoW返回{result}")

        # 方法3: 尝试使用注册表设置壁纸
        try:
            import winreg
            registry_key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                "Control Panel\\Desktop",
                0,
                winreg.KEY_SET_VALUE
            )
            winreg.SetValueEx(registry_key, "WallpaperStyle", 0, winreg.REG_SZ, "0")
            winreg.SetValueEx(registry_key, "TileWallpaper", 0, winreg.REG_SZ, "0")
            winreg.SetValueEx(registry_key, "Wallpaper", 0, winreg.REG_SZ, abs_path)
            winreg.CloseKey(registry_key)

            # 通知Windows更新设置
            ctypes.windll.user32.SendMessageW(0xFFFF, 0x0112, 0xF, 0)
            ctypes.windll.user32.SendMessageW(0xFFFF, 0x0112, 0xF, 0)

            print("方法3成功: 使用注册表设置壁纸")
            return True
        except Exception as reg_error:
            print(f"方法3失败: 注册表方法错误: {reg_error}")

        return False
    except Exception as e:
        print(f"设置壁纸失败: {e}")
        import traceback
        traceback.print_exc()
        return False

# 主更新函数
def update_wallpaper():
    print("获取风流场数据...")
    timestamp, screenshot_path, _ = fetch_wind_data()
    if timestamp and screenshot_path:
        print(f"获取成功，时间戳: {timestamp}")
        if create_wind_wallpaper(timestamp, screenshot_path, None):
            set_wallpaper()
    else:
        print("由于数据获取失败，跳过壁纸更新")

# 主程序
def main():
    print("="*50)
    print("启动实时风流场桌面壁纸程序...")
    print("="*50)

    # 显示系统信息
    import platform
    print(f"操作系统: {platform.system()} {platform.version()}")
    print(f"Python版本: {platform.python_version()}")
    print(f"工作目录: {os.getcwd()}")
    print("-"*50)

    # 检查Chrome驱动是否存在
    if not os.path.exists(CHROME_DRIVER_PATH):
        print(f"错误: Chrome驱动文件不存在: {CHROME_DRIVER_PATH}")
        print("请下载适合您Chrome版本的驱动并放置在正确位置")
        print("下载地址: https://chromedriver.chromium.org/downloads")
        input("按Enter键退出...")
        return

    print(f"Chrome驱动路径: {os.path.abspath(CHROME_DRIVER_PATH)}")

    # 检查是否能够设置壁纸
    try:
        # 创建一个简单的测试图像
        test_img = Image.new("RGB", (100, 100), "white")
        test_path = "test_wallpaper.bmp"
        test_img.save(test_path)

        # 尝试设置测试壁纸
        print("测试壁纸设置功能...")
        old_wallpaper_path = WALLPAPER_PATH
        global WALLPAPER_PATH
        WALLPAPER_PATH = test_path

        if set_wallpaper():
            print("壁纸设置测试成功!")
        else:
            print("警告: 壁纸设置测试失败，程序可能无法设置壁纸")
            print("请确保程序有足够的权限，或以管理员身份运行")
            response = input("是否继续运行程序? (y/n): ")
            if response.lower() != 'y':
                return

        # 恢复原始路径
        WALLPAPER_PATH = old_wallpaper_path

        # 清理测试文件
        try:
            os.remove(test_path)
        except:
            pass
    except Exception as e:
        print(f"壁纸设置测试失败: {e}")
        response = input("是否继续运行程序? (y/n): ")
        if response.lower() != 'y':
            return

    print("-"*50)
    print("开始获取风流场数据...")

    # 首次运行
    success = False
    try:
        # 尝试更新壁纸
        update_wallpaper()

        # 检查壁纸文件是否已创建
        if os.path.exists(WALLPAPER_PATH):
            print("首次更新成功!")
            success = True
        else:
            print("首次更新未能创建壁纸文件")
    except Exception as e:
        print(f"首次更新失败: {e}")
        import traceback
        traceback.print_exc()

    if not success:
        print("首次更新失败，请检查错误信息")
        response = input("是否继续运行程序? (y/n): ")
        if response.lower() != 'y':
            return

    # 设置定时任务
    schedule.every(UPDATE_INTERVAL).seconds.do(update_wallpaper)
    print(f"已设置每 {UPDATE_INTERVAL} 秒更新一次壁纸")

    print("-"*50)
    print("程序现在将在后台运行")
    print("按Ctrl+C可以停止程序")
    print("-"*50)

    # 主循环
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n程序已停止")
    except Exception as e:
        print(f"程序异常: {e}")
        import traceback
        traceback.print_exc()
        input("按Enter键退出...")

if __name__ == "__main__":
    main()
