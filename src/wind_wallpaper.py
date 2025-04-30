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

# 获取实时风向数据
def fetch_wind_data():
    url = f"https://devapi.qweather.com/v7/weather/now?location={LOCATION}&key={API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data["code"] == "200":
            wind_dir = data["now"]["windDir"]  # 风向描述（如“东北风”）
            wind_deg = float(data["now"]["windDeg"])  # 风向角度（0-360°）
            wind_speed = float(data["now"]["windSpeed"])  # 风速（km/h）
            return wind_dir, wind_deg, wind_speed
        else:
            print(f"API error: {data['code']}")
            return None, None, None
    except requests.RequestException as e:
        print(f"Failed to fetch wind data: {e}")
        return None, None, None

# 绘制风向箭头壁纸
def create_wind_wallpaper(wind_dir, wind_deg, wind_speed):
    # 创建空白图像（1920x1080，适应常见屏幕分辨率）
    img = Image.new("RGB", (1920, 1080), "skyblue")
    draw = ImageDraw.Draw(img)

    # 绘制背景装饰（可选）
    draw.rectangle((50, 50, 1870, 1030), outline="white", width=5)

    # 绘制风向信息
    draw.text((100, 100), f"Wind Direction: {wind_dir}", fill="black", font_size=40)
    draw.text((100, 150), f"Wind Angle: {wind_deg}°", fill="black", font_size=40)
    draw.text((100, 200), f"Wind Speed: {wind_speed} km/h", fill="black", font_size=40)

    # 绘制风向箭头
    center_x, center_y = 960, 540  # 图像中心
    arrow_length = 200
    arrow_angle = math.radians(wind_deg)  # 转换为弧度
    # 箭头终点坐标
    end_x = center_x + arrow_length * math.sin(arrow_angle)
    end_y = center_y - arrow_length * math.cos(arrow_angle)
    # 绘制箭头主线
    draw.line((center_x, center_y, end_x, end_y), fill="red", width=10)
    # 绘制箭头尖
    arrow_tip_size = 30
    angle1 = arrow_angle + math.radians(135)
    angle2 = arrow_angle - math.radians(135)
    tip1_x = end_x + arrow_tip_size * math.sin(angle1)
    tip1_y = end_y - arrow_tip_size * math.cos(angle1)
    tip2_x = end_x + arrow_tip_size * math.sin(angle2)
    tip2_y = end_y - arrow_tip_size * math.cos(angle2)
    draw.line((end_x, end_y, tip1_x, tip1_y), fill="red", width=5)
    draw.line((end_x, end_y, tip2_x, tip2_y), fill="red", width=5)

    # 保存壁纸
    img.save(WALLPAPER_PATH)

# 设置Windows桌面壁纸
def set_wallpaper():
    # 使用Windows API设置壁纸
    ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.abspath(WALLPAPER_PATH), 3)

# 主更新函数
def update_wallpaper():
    print("Fetching wind data...")
    wind_dir, wind_deg, wind_speed = fetch_wind_data()
    if wind_dir and wind_deg is not None and wind_speed is not None:
        print(f"Wind: {wind_dir}, {wind_deg}°, {wind_speed} km/h")
        create_wind_wallpaper(wind_dir, wind_deg, wind_speed)
        set_wallpaper()
        print("Wallpaper updated successfully")
    else:
        print("Skipping wallpaper update due to data fetch failure")

# 主程序
def main():
    # 首次运行
    update_wallpaper()
    # 设置定时任务
    schedule.every(UPDATE_INTERVAL).seconds.do(update_wallpaper)
    print(f"Scheduled wallpaper update every {UPDATE_INTERVAL} seconds")
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()


