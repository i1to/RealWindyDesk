"""
测试从中国气象网获取风流场数据
"""
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

# 配置
WEATHER_URL = "https://www.weather.com.cn/radar/"  # 中国气象网雷达页面
SCREENSHOT_PATH = "wind_screenshot.png"  # 截图保存路径
CHROME_DRIVER_PATH = "chromedriver.exe"  # Chrome驱动路径，需要根据实际情况修改

def test_fetch_wind_data():
    """测试获取风流场数据"""
    driver = None
    try:
        print("="*50)
        print("测试从中国气象网获取风流场数据")
        print("="*50)
        
        # 步骤1: 检查Chrome驱动
        print("\n步骤1: 检查Chrome驱动...")
        if not os.path.exists(CHROME_DRIVER_PATH):
            print(f"错误: Chrome驱动文件不存在: {CHROME_DRIVER_PATH}")
            return False
        print(f"✓ Chrome驱动已找到: {os.path.abspath(CHROME_DRIVER_PATH)}")
        
        # 步骤2: 启动Chrome浏览器
        print("\n步骤2: 启动Chrome浏览器...")
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # 无头模式
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        service = Service(CHROME_DRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("✓ Chrome浏览器已启动")
        
        # 步骤3: 访问中国气象网
        print("\n步骤3: 访问中国气象网...")
        driver.get(WEATHER_URL)
        print("✓ 页面已加载")
        
        # 步骤4: 打印页面标题
        print(f"\n页面标题: {driver.title}")
        
        # 步骤5: 查找页面元素
        print("\n步骤5: 查找页面元素...")
        
        # 查找所有列表项
        print("查找所有列表项...")
        list_items = driver.find_elements(By.TAG_NAME, "li")
        print(f"找到 {len(list_items)} 个列表项")
        
        # 打印包含"风"字的列表项
        wind_items = [item for item in list_items if '风' in item.text]
        print(f"包含'风'字的列表项: {len(wind_items)}")
        for i, item in enumerate(wind_items):
            print(f"  {i+1}. {item.text}")
        
        # 查找地图容器
        print("\n查找地图容器...")
        map_containers = driver.find_elements(By.CSS_SELECTOR, ".mapContainer, div[class*='map'], div[id*='map']")
        print(f"找到 {len(map_containers)} 个可能的地图容器")
        for i, container in enumerate(map_containers):
            print(f"  {i+1}. 类名: {container.get_attribute('class')}, ID: {container.get_attribute('id')}")
        
        # 步骤6: 尝试点击风流场选项
        print("\n步骤6: 尝试点击风流场选项...")
        wind_option = None
        
        # 方法1: 使用XPath
        try:
            wind_options = driver.find_elements(By.XPATH, "//li[contains(text(), '风流场')]")
            if wind_options:
                wind_option = wind_options[0]
                print(f"✓ 方法1成功: 找到风流场选项: {wind_option.text}")
            else:
                print("✗ 方法1失败: 未找到风流场选项")
        except Exception as e:
            print(f"✗ 方法1异常: {e}")
        
        # 方法2: 遍历所有列表项
        if not wind_option:
            try:
                for item in list_items:
                    if '风流场' in item.text or ('风' in item.text and '流' in item.text):
                        wind_option = item
                        print(f"✓ 方法2成功: 找到风流场选项: {item.text}")
                        break
                
                if not wind_option:
                    print("✗ 方法2失败: 未找到风流场选项")
            except Exception as e:
                print(f"✗ 方法2异常: {e}")
        
        # 如果找到了风流场选项，尝试点击
        if wind_option:
            try:
                print("\n尝试点击风流场选项...")
                driver.execute_script("arguments[0].scrollIntoView(true);", wind_option)
                driver.execute_script("arguments[0].click();", wind_option)
                print("✓ 已点击风流场选项")
                
                # 等待数据加载
                print("等待数据加载...")
                time.sleep(5)
            except Exception as e:
                print(f"✗ 点击风流场选项失败: {e}")
        
        # 步骤7: 截取页面
        print("\n步骤7: 截取页面...")
        try:
            # 尝试截取地图容器
            if map_containers:
                screenshot = map_containers[0].screenshot_as_png
                print("✓ 地图容器截图成功")
            else:
                # 截取整个页面
                screenshot = driver.get_screenshot_as_png()
                print("✓ 整页截图成功")
            
            # 保存截图
            with open(SCREENSHOT_PATH, "wb") as file:
                file.write(screenshot)
            
            print(f"✓ 截图已保存到: {os.path.abspath(SCREENSHOT_PATH)}")
        except Exception as e:
            print(f"✗ 截取页面失败: {e}")
            return False
        
        # 步骤8: 关闭浏览器
        print("\n步骤8: 关闭浏览器...")
        driver.quit()
        print("✓ 浏览器已关闭")
        
        print("\n="*50)
        print("测试完成!")
        print(f"请查看截图文件: {os.path.abspath(SCREENSHOT_PATH)}")
        print("="*50)
        
        return True
    except Exception as e:
        print(f"\n测试失败: {e}")
        import traceback
        traceback.print_exc()
        if driver:
            try:
                driver.quit()
                print("浏览器已关闭")
            except:
                pass
        return False

if __name__ == "__main__":
    test_fetch_wind_data()
    input("\n按Enter键退出...")
