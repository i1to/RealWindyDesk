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
        # 打开截图
        screenshot = Image.open(screenshot_path)
        
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
        except IOError:
            font = ImageFont.load_default()
        
        # 添加时间戳
        draw.text((20, 20), f"更新时间: {timestamp}", fill="black", font=font)
        
        # 添加数据来源
        draw.text((20, 50), "数据来源: 中国气象网 (www.weather.com.cn)", fill="black", font=font)
        
        # 保存壁纸
        wallpaper.save(WALLPAPER_PATH)
        print(f"壁纸已保存到 {WALLPAPER_PATH}")
        return True
    except Exception as e:
        print(f"创建壁纸失败: {e}")
        return False

# 设置Windows桌面壁纸
def set_wallpaper():
    try:
        # 使用Windows API设置壁纸
        ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.abspath(WALLPAPER_PATH), 3)
        print("桌面壁纸已更新")
        return True
    except Exception as e:
        print(f"设置壁纸失败: {e}")
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
    print("启动实时风流场桌面壁纸程序...")
    
    # 检查Chrome驱动是否存在
    if not os.path.exists(CHROME_DRIVER_PATH):
        print(f"错误: Chrome驱动文件不存在: {CHROME_DRIVER_PATH}")
        print("请下载适合您Chrome版本的驱动并放置在正确位置")
        print("下载地址: https://chromedriver.chromium.org/downloads")
        return
    
    # 首次运行
    update_wallpaper()
    
    # 设置定时任务
    schedule.every(UPDATE_INTERVAL).seconds.do(update_wallpaper)
    print(f"已设置每 {UPDATE_INTERVAL} 秒更新一次壁纸")
    
    # 主循环
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("程序已停止")

if __name__ == "__main__":
    main()
