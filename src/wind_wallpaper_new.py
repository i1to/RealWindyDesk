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
import logging
import sys
import traceback

# 配置日志记录
LOG_FILE = "wind_wallpaper.log"

# 创建日志记录器
logger = logging.getLogger("wind_wallpaper")
logger.setLevel(logging.DEBUG)

# 创建文件处理器
file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
file_handler.setLevel(logging.DEBUG)

# 创建控制台处理器
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

# 创建格式化器
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# 添加处理器到记录器
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# 全局异常处理函数
def log_uncaught_exceptions(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        # 正常的Ctrl+C中断
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger.critical("未捕获的异常", exc_info=(exc_type, exc_value, exc_traceback))
    print("程序遇到了一个未处理的错误。详细信息已记录到日志文件中。")
    print(f"请查看日志文件: {os.path.abspath(LOG_FILE)}")
    input("按Enter键退出...")

# 设置全局异常处理器
sys.excepthook = log_uncaught_exceptions

# 配置
WEATHER_URL = "https://www.weather.com.cn/radar/"  # 中国气象网雷达页面
WALLPAPER_PATH = "wind_wallpaper.png"  # 壁纸保存路径
SCREENSHOT_PATH = "wind_screenshot.png"  # 截图保存路径
UPDATE_INTERVAL = 1800  # 更新间隔（秒），30分钟
CHROME_DRIVER_PATH = "chromedriver.exe"  # Chrome驱动路径，需要根据实际情况修改

# 获取实时风流场数据（通过截图方式）
def fetch_wind_data():
    driver = None
    try:
        logger.info("开始获取风流场数据")
        logger.info("步骤1: 启动Chrome浏览器")
        print("\n步骤1: 启动Chrome浏览器...")

        # 配置Chrome选项
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # 无头模式
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")  # 解决内存不足问题
        chrome_options.add_argument("--disable-extensions")  # 禁用扩展
        chrome_options.add_argument("--disable-browser-side-navigation")  # 避免超时错误
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")  # 避免渲染问题

        logger.debug(f"Chrome选项: {chrome_options.arguments}")

        # 创建Chrome浏览器实例
        chrome_driver_path = os.path.abspath(CHROME_DRIVER_PATH)
        logger.info(f"使用驱动: {chrome_driver_path}")
        print(f"使用驱动: {chrome_driver_path}")

        try:
            service = Service(CHROME_DRIVER_PATH)
            driver = webdriver.Chrome(service=service, options=chrome_options)
            logger.info("Chrome浏览器已启动")
            print("✓ Chrome浏览器已启动")
        except Exception as e:
            logger.error(f"启动Chrome浏览器失败: {e}")
            logger.error(traceback.format_exc())
            raise Exception(f"启动Chrome浏览器失败: {e}")

        # 访问中国气象网雷达页面
        logger.info(f"步骤2: 访问中国气象网 {WEATHER_URL}")
        print(f"\n步骤2: 访问中国气象网 {WEATHER_URL}...")

        try:
            driver.get(WEATHER_URL)
            logger.info("页面已加载")
            print("✓ 页面已加载")
        except Exception as e:
            logger.error(f"访问网站失败: {e}")
            logger.error(traceback.format_exc())
            raise Exception(f"访问网站失败: {e}")

        # 等待页面加载完成
        logger.info("步骤3: 等待页面元素加载")
        print("\n步骤3: 等待页面元素加载...")
        try:
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".mapContainer"))
            )
            logger.info("地图容器已加载")
            print("✓ 地图容器已加载")
        except Exception as e:
            logger.warning(f"等待地图容器超时: {e}")
            print(f"✗ 等待地图容器超时: {e}")
            logger.info("尝试查找页面上的其他元素")
            print("尝试查找页面上的其他元素...")

            # 保存页面源码到日志，帮助调试
            page_source = driver.page_source
            logger.debug("页面源码片段:")
            logger.debug(page_source[:2000] + "..." if len(page_source) > 2000 else page_source)

            # 打印页面源码片段到控制台
            print("\n页面源码片段:")
            print(page_source[:500] + "..." if len(page_source) > 500 else page_source)

            # 尝试查找其他可能的元素
            try:
                body = driver.find_element(By.TAG_NAME, "body")
                body_text_length = len(body.text)
                logger.info(f"找到body元素，内容长度: {body_text_length}")
                print(f"找到body元素，内容长度: {body_text_length}")

                # 保存页面截图，帮助调试
                try:
                    debug_screenshot_path = "debug_screenshot.png"
                    driver.save_screenshot(debug_screenshot_path)
                    logger.info(f"已保存调试截图: {os.path.abspath(debug_screenshot_path)}")
                except Exception as ss_e:
                    logger.error(f"保存调试截图失败: {ss_e}")

                # 尝试查找所有可能的地图容器
                containers = driver.find_elements(By.CSS_SELECTOR, "div[class*='map'], div[id*='map']")
                if containers:
                    logger.info(f"找到 {len(containers)} 个可能的地图容器")
                    print(f"找到 {len(containers)} 个可能的地图容器")
                    map_element = containers[0]  # 使用第一个找到的容器
                    logger.info(f"使用容器: 类名={map_element.get_attribute('class')}, ID={map_element.get_attribute('id')}")
                else:
                    logger.error("找不到任何地图容器")
                    raise Exception("找不到任何地图容器")
            except Exception as inner_e:
                logger.error(f"查找替代元素失败: {inner_e}")
                logger.error(traceback.format_exc())
                print(f"✗ 查找替代元素失败: {inner_e}")
                raise Exception("无法加载页面元素，请检查网站结构是否已更改")

        # 点击风流场选项
        logger.info("步骤4: 切换到风流场视图")
        print("\n步骤4: 切换到风流场视图...")
        try:
            # 首先尝试使用XPath查找
            logger.debug("尝试使用XPath查找风流场选项")
            wind_options = driver.find_elements(By.XPATH, "//li[contains(text(), '风流场')]")

            if wind_options:
                wind_option = wind_options[0]
                logger.info(f"找到风流场选项: {wind_option.text}")
                print(f"✓ 找到风流场选项: {wind_option.text}")
            else:
                logger.info("使用备用方法查找风流场选项")
                print("使用备用方法查找风流场选项...")

                # 尝试查找所有列表项
                logger.debug("尝试查找所有列表项")
                all_options = driver.find_elements(By.TAG_NAME, "li")
                logger.debug(f"找到 {len(all_options)} 个列表项")

                # 记录所有列表项的文本，帮助调试
                for i, opt in enumerate(all_options[:20]):  # 只记录前20个，避免日志过大
                    logger.debug(f"列表项 {i+1}: {opt.text}")

                wind_option = None

                for option in all_options:
                    if '风' in option.text or '流场' in option.text:
                        wind_option = option
                        logger.info(f"找到可能的风流场选项: {option.text}")
                        print(f"✓ 找到可能的风流场选项: {option.text}")
                        break

                if not wind_option:
                    # 如果仍然找不到，尝试点击可能的按钮或链接
                    logger.debug("尝试查找按钮或链接")
                    buttons = driver.find_elements(By.TAG_NAME, "button")
                    links = driver.find_elements(By.TAG_NAME, "a")
                    logger.debug(f"找到 {len(buttons)} 个按钮和 {len(links)} 个链接")

                    for element in buttons + links:
                        if '风' in element.text or '流场' in element.text:
                            wind_option = element
                            logger.info(f"找到可能的风流场按钮/链接: {element.text}")
                            print(f"✓ 找到可能的风流场按钮/链接: {element.text}")
                            break

                if not wind_option:
                    logger.error("找不到风流场选项")
                    raise Exception("找不到风流场选项")

            # 点击风流场选项
            logger.info("点击风流场选项")
            print("点击风流场选项...")
            try:
                driver.execute_script("arguments[0].scrollIntoView(true);", wind_option)
                logger.debug("已滚动到风流场选项")
                driver.execute_script("arguments[0].click();", wind_option)
                logger.info("已点击风流场选项")
                print("✓ 已点击风流场选项")
            except Exception as click_e:
                logger.error(f"点击风流场选项时出错: {click_e}")
                logger.error(traceback.format_exc())
                raise Exception(f"点击风流场选项失败: {click_e}")

        except Exception as e:
            logger.error(f"切换到风流场视图失败: {e}")
            logger.error(traceback.format_exc())
            print(f"✗ 切换到风流场视图失败: {e}")
            logger.info("尝试直接查找地图元素")
            print("尝试直接查找地图元素...")

        # 等待风流场数据加载
        logger.info("步骤5: 等待风流场数据加载")
        print("\n步骤5: 等待风流场数据加载...")
        time.sleep(10)  # 增加等待时间，确保数据完全加载
        logger.info("等待完成")
        print("✓ 等待完成")

        # 获取当前时间作为风向数据的时间戳
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        logger.info(f"当前时间: {current_time}")
        print(f"当前时间: {current_time}")

        # 截取风流场图
        logger.info("步骤6: 截取风流场图")
        print("\n步骤6: 截取风流场图...")
        try:
            # 尝试找到地图容器
            logger.debug("尝试找到地图容器")
            map_elements = driver.find_elements(By.CSS_SELECTOR, ".mapContainer")
            if map_elements:
                map_element = map_elements[0]
                logger.info("找到地图容器")
                print("✓ 找到地图容器")
            else:
                # 尝试查找其他可能的地图容器
                logger.debug("尝试查找备用地图容器")
                map_elements = driver.find_elements(By.CSS_SELECTOR, "div[class*='map'], div[id*='map']")
                if map_elements:
                    map_element = map_elements[0]
                    container_class = map_element.get_attribute('class')
                    container_id = map_element.get_attribute('id')
                    logger.info(f"找到备用地图容器: 类名={container_class}, ID={container_id}")
                    print(f"✓ 找到备用地图容器: {container_class}")
                else:
                    # 如果找不到任何地图容器，截取整个页面
                    logger.warning("找不到地图容器，将截取整个页面")
                    print("找不到地图容器，将截取整个页面")
                    map_element = driver.find_element(By.TAG_NAME, "body")

            # 截取元素
            logger.info("正在截取...")
            print("正在截取...")
            try:
                screenshot = map_element.screenshot_as_png
                logger.info("截图已获取")
                print("✓ 截图已获取")
            except Exception as ss_e:
                logger.error(f"元素截图失败: {ss_e}")
                logger.error(traceback.format_exc())
                raise Exception(f"元素截图失败: {ss_e}")

            # 保存截图
            try:
                with open(SCREENSHOT_PATH, "wb") as file:
                    file.write(screenshot)

                screenshot_path = os.path.abspath(SCREENSHOT_PATH)
                logger.info(f"风流场截图已保存到: {screenshot_path}")
                print(f"✓ 风流场截图已保存到: {screenshot_path}")
            except Exception as save_e:
                logger.error(f"保存截图失败: {save_e}")
                logger.error(traceback.format_exc())
                raise Exception(f"保存截图失败: {save_e}")

        except Exception as e:
            logger.error(f"截取风流场图失败: {e}")
            logger.error(traceback.format_exc())
            print(f"✗ 截取风流场图失败: {e}")
            logger.info("尝试截取整个页面")
            print("尝试截取整个页面...")

            try:
                # 截取整个页面
                logger.debug("截取整个页面")
                screenshot = driver.get_screenshot_as_png()

                # 保存截图
                with open(SCREENSHOT_PATH, "wb") as file:
                    file.write(screenshot)

                screenshot_path = os.path.abspath(SCREENSHOT_PATH)
                logger.info(f"整页截图已保存到: {screenshot_path}")
                print(f"✓ 整页截图已保存到: {screenshot_path}")
            except Exception as e2:
                logger.error(f"截取整个页面也失败了: {e2}")
                logger.error(traceback.format_exc())
                print(f"✗ 截取整个页面也失败了: {e2}")
                raise Exception("无法获取任何截图")

        logger.info("步骤7: 关闭浏览器")
        print("\n步骤7: 关闭浏览器...")
        driver.quit()
        logger.info("浏览器已关闭")
        print("✓ 浏览器已关闭")

        # 返回时间戳（作为风向描述）和截图路径
        logger.info(f"获取风流场数据成功: 时间={current_time}, 截图={SCREENSHOT_PATH}")
        return current_time, SCREENSHOT_PATH, None
    except Exception as e:
        logger.error(f"获取风流场数据失败: {e}")
        logger.error(traceback.format_exc())
        print(f"\n✗ 获取风流场数据失败: {e}")

        if driver:
            try:
                driver.quit()
                logger.info("浏览器已关闭")
                print("浏览器已关闭")
            except Exception as quit_e:
                logger.error(f"关闭浏览器时出错: {quit_e}")
                print("关闭浏览器时出错")

        return None, None, None

# 创建风流场壁纸
def create_wind_wallpaper(timestamp, screenshot_path, _):
    try:
        logger.info(f"开始创建风流场壁纸，使用截图: {screenshot_path}")
        print(f"正在打开截图: {screenshot_path}")

        # 检查截图文件是否存在
        if not os.path.exists(screenshot_path):
            logger.error(f"截图文件不存在: {screenshot_path}")
            raise FileNotFoundError(f"截图文件不存在: {screenshot_path}")

        # 打开截图
        try:
            screenshot = Image.open(screenshot_path)
            img_size = f"{screenshot.width}x{screenshot.height}"
            img_format = screenshot.format
            logger.info(f"截图已打开: 尺寸={img_size}, 格式={img_format}")
            print(f"截图尺寸: {img_size}, 格式: {img_format}")
        except Exception as img_e:
            logger.error(f"打开截图失败: {img_e}")
            logger.error(traceback.format_exc())
            raise Exception(f"打开截图失败: {img_e}")

        # 创建壁纸画布（1920x1080，适应常见屏幕分辨率）
        logger.debug("创建壁纸画布 (1920x1080)")
        wallpaper = Image.new("RGB", (1920, 1080), "white")

        # 计算截图在壁纸中的位置（居中）
        x = (1920 - screenshot.width) // 2
        y = (1080 - screenshot.height) // 2
        logger.debug(f"截图位置: x={x}, y={y}")

        # 将截图粘贴到壁纸上
        try:
            wallpaper.paste(screenshot, (x, y))
            logger.debug("截图已粘贴到壁纸上")
        except Exception as paste_e:
            logger.error(f"粘贴截图失败: {paste_e}")
            logger.error(traceback.format_exc())
            raise Exception(f"粘贴截图失败: {paste_e}")

        # 添加时间戳和来源信息
        logger.debug("添加时间戳和来源信息")
        draw = ImageDraw.Draw(wallpaper)

        # 使用默认字体（如果没有指定字体文件）
        font = None
        try:
            font = ImageFont.truetype("arial.ttf", 24)
            logger.info("使用Arial字体")
            print("使用Arial字体")
        except IOError:
            logger.debug("Arial字体不可用，尝试使用Windows系统字体")
            try:
                # 尝试使用Windows系统字体
                font = ImageFont.truetype("C:\\Windows\\Fonts\\Arial.ttf", 24)
                logger.info("使用Windows系统Arial字体")
                print("使用Windows系统Arial字体")
            except IOError:
                logger.warning("无法加载Arial字体，使用默认字体")
                font = ImageFont.load_default()
                print("使用默认字体")

        # 添加时间戳
        timestamp_text = f"更新时间: {timestamp}"
        logger.debug(f"添加时间戳: {timestamp_text}")
        draw.text((20, 20), timestamp_text, fill="black", font=font)

        # 添加数据来源
        source_text = "数据来源: 中国气象网 (www.weather.com.cn)"
        logger.debug(f"添加数据来源: {source_text}")
        draw.text((20, 50), source_text, fill="black", font=font)

        # 确保目录存在
        wallpaper_dir = os.path.dirname(os.path.abspath(WALLPAPER_PATH))
        if not os.path.exists(wallpaper_dir):
            logger.info(f"创建目录: {wallpaper_dir}")
            os.makedirs(wallpaper_dir)
            print(f"创建目录: {wallpaper_dir}")

        # 保存壁纸 (使用BMP格式，Windows壁纸更兼容)
        global WALLPAPER_PATH  # 声明全局变量，必须在使用前声明

        bmp_path = WALLPAPER_PATH.replace('.png', '.bmp')
        try:
            wallpaper.save(bmp_path, "BMP")
            logger.info(f"壁纸已保存为BMP格式: {bmp_path}")
            print(f"壁纸已保存为BMP格式: {bmp_path}")
        except Exception as bmp_e:
            logger.error(f"保存BMP格式壁纸失败: {bmp_e}")
            logger.error(traceback.format_exc())
            raise Exception(f"保存BMP格式壁纸失败: {bmp_e}")

        # 同时保存PNG格式作为备份
        try:
            wallpaper.save(WALLPAPER_PATH)
            logger.info(f"壁纸已保存为PNG格式: {WALLPAPER_PATH}")
            print(f"壁纸已保存为PNG格式: {WALLPAPER_PATH}")
        except Exception as png_e:
            logger.warning(f"保存PNG格式壁纸失败: {png_e}")
            print(f"警告: 保存PNG格式壁纸失败: {png_e}")
            # 继续执行，因为BMP格式已保存成功

        # 更新全局变量，使用BMP路径
        old_path = WALLPAPER_PATH
        WALLPAPER_PATH = bmp_path
        logger.info(f"更新壁纸路径: {old_path} -> {WALLPAPER_PATH}")

        logger.info("创建风流场壁纸成功")
        return True
    except Exception as e:
        logger.error(f"创建壁纸失败: {e}")
        logger.error(traceback.format_exc())
        print(f"创建壁纸失败: {e}")
        return False

# 设置Windows桌面壁纸
def set_wallpaper():
    try:
        logger.info("开始设置Windows桌面壁纸")

        # 检查壁纸文件是否存在
        abs_path = os.path.abspath(WALLPAPER_PATH)
        logger.debug(f"壁纸文件路径: {abs_path}")

        if not os.path.exists(abs_path):
            logger.error(f"壁纸文件不存在: {abs_path}")
            print(f"错误: 壁纸文件不存在: {abs_path}")
            return False

        # 检查文件大小和类型
        try:
            file_size = os.path.getsize(abs_path) / 1024  # KB
            logger.info(f"壁纸文件大小: {file_size:.2f} KB")

            # 检查文件是否为有效的图像文件
            try:
                with Image.open(abs_path) as img:
                    logger.info(f"壁纸图像信息: 格式={img.format}, 尺寸={img.width}x{img.height}, 模式={img.mode}")
            except Exception as img_e:
                logger.warning(f"无法验证壁纸图像: {img_e}")
        except Exception as fs_e:
            logger.warning(f"无法获取文件信息: {fs_e}")

        logger.info(f"正在设置壁纸: {abs_path}")
        print(f"正在设置壁纸: {abs_path}")

        # 尝试使用不同的方法设置壁纸

        # 方法1: 使用Windows API (SPI_SETDESKWALLPAPER = 20)
        logger.debug("尝试方法1: 使用SystemParametersInfoW")
        try:
            result = ctypes.windll.user32.SystemParametersInfoW(20, 0, abs_path, 3)
            if result:
                logger.info("方法1成功: 使用SystemParametersInfoW设置壁纸")
                print("方法1成功: 使用SystemParametersInfoW设置壁纸")
                return True
            else:
                logger.warning(f"方法1失败: SystemParametersInfoW返回{result}")
                print(f"方法1失败: SystemParametersInfoW返回{result}")
        except Exception as m1_e:
            logger.error(f"方法1异常: {m1_e}")
            logger.error(traceback.format_exc())
            print(f"方法1异常: {m1_e}")

        # 方法2: 尝试使用另一种方式调用API
        logger.debug("尝试方法2: 使用明确常量的SystemParametersInfoW")
        try:
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
                logger.info("方法2成功: 使用明确常量的SystemParametersInfoW设置壁纸")
                print("方法2成功: 使用明确常量的SystemParametersInfoW设置壁纸")
                return True
            else:
                logger.warning(f"方法2失败: 明确常量的SystemParametersInfoW返回{result}")
                print(f"方法2失败: 明确常量的SystemParametersInfoW返回{result}")
        except Exception as m2_e:
            logger.error(f"方法2异常: {m2_e}")
            logger.error(traceback.format_exc())
            print(f"方法2异常: {m2_e}")

        # 方法3: 尝试使用注册表设置壁纸
        logger.debug("尝试方法3: 使用注册表设置壁纸")
        try:
            import winreg
            logger.debug("打开注册表键: Control Panel\\Desktop")
            registry_key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                "Control Panel\\Desktop",
                0,
                winreg.KEY_SET_VALUE
            )

            logger.debug("设置注册表值: WallpaperStyle=0")
            winreg.SetValueEx(registry_key, "WallpaperStyle", 0, winreg.REG_SZ, "0")

            logger.debug("设置注册表值: TileWallpaper=0")
            winreg.SetValueEx(registry_key, "TileWallpaper", 0, winreg.REG_SZ, "0")

            logger.debug(f"设置注册表值: Wallpaper={abs_path}")
            winreg.SetValueEx(registry_key, "Wallpaper", 0, winreg.REG_SZ, abs_path)

            logger.debug("关闭注册表键")
            winreg.CloseKey(registry_key)

            # 通知Windows更新设置
            logger.debug("发送更新消息到Windows")
            ctypes.windll.user32.SendMessageW(0xFFFF, 0x0112, 0xF, 0)
            ctypes.windll.user32.SendMessageW(0xFFFF, 0x0112, 0xF, 0)

            logger.info("方法3成功: 使用注册表设置壁纸")
            print("方法3成功: 使用注册表设置壁纸")
            return True
        except Exception as reg_error:
            logger.error(f"方法3失败: 注册表方法错误: {reg_error}")
            logger.error(traceback.format_exc())
            print(f"方法3失败: 注册表方法错误: {reg_error}")

        # 如果所有方法都失败，尝试使用PowerShell
        logger.debug("尝试方法4: 使用PowerShell")
        try:
            import subprocess
            ps_command = f'powershell -command "Add-Type -TypeDefinition \\"using System; using System.Runtime.InteropServices; public class Wallpaper {{ [DllImport(\\"user32.dll\\")] public static extern int SystemParametersInfo(int uAction, int uParam, string lpvParam, int fuWinIni); }}\\"; [Wallpaper]::SystemParametersInfo(20, 0, \'{abs_path.replace("\\", "\\\\")}\', 3)"'
            logger.debug(f"执行PowerShell命令: {ps_command}")

            result = subprocess.run(ps_command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                logger.info("方法4成功: 使用PowerShell设置壁纸")
                print("方法4成功: 使用PowerShell设置壁纸")
                return True
            else:
                logger.warning(f"方法4失败: PowerShell返回{result.returncode}")
                logger.warning(f"错误输出: {result.stderr}")
                print(f"方法4失败: PowerShell返回错误")
        except Exception as ps_e:
            logger.error(f"方法4异常: {ps_e}")
            logger.error(traceback.format_exc())
            print(f"方法4异常: {ps_e}")

        logger.error("所有设置壁纸的方法都失败了")
        print("所有设置壁纸的方法都失败了")
        return False
    except Exception as e:
        logger.error(f"设置壁纸失败: {e}")
        logger.error(traceback.format_exc())
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
    logger.info("="*50)
    logger.info("启动实时风流场桌面壁纸程序...")
    logger.info("="*50)

    # 显示系统信息
    import platform
    logger.info(f"操作系统: {platform.system()} {platform.version()}")
    logger.info(f"Python版本: {platform.python_version()}")
    logger.info(f"工作目录: {os.getcwd()}")
    logger.info(f"日志文件: {os.path.abspath(LOG_FILE)}")
    logger.info("-"*50)

    # 检查是否以管理员身份运行
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

    logger.info(f"是否以管理员身份运行: {'是' if is_admin else '否'}")
    if not is_admin:
        logger.warning("程序未以管理员身份运行，可能无法设置壁纸")

    print("="*50)
    print("启动实时风流场桌面壁纸程序...")
    print("="*50)
    print(f"日志文件: {os.path.abspath(LOG_FILE)}")
    print("-"*50)

    # 检查是否在非交互式模式下运行
    non_interactive = os.environ.get('NON_INTERACTIVE', '0') == '1'
    if non_interactive:
        logger.info("检测到非交互式模式，将自动执行所有步骤")
        print("检测到非交互式模式，将自动执行所有步骤...")
    else:
        try:
            input("第1步: 准备开始检查环境。按Enter键继续...")
        except EOFError:
            logger.warning("无法读取用户输入，可能是在非交互式环境中运行")
            print("检测到非交互式环境，将自动继续执行...")
            non_interactive = True

    # 检查Chrome驱动是否存在
    logger.info("检查Chrome驱动...")
    print("\n正在检查Chrome驱动...")
    if not os.path.exists(CHROME_DRIVER_PATH):
        print(f"错误: Chrome驱动文件不存在: {CHROME_DRIVER_PATH}")
        print("请下载适合您Chrome版本的驱动并放置在正确位置")
        print("下载地址: https://chromedriver.chromium.org/downloads")
        input("按Enter键退出...")
        return

    print(f"✓ Chrome驱动已找到: {os.path.abspath(CHROME_DRIVER_PATH)}")

    # 检查Chrome浏览器
    print("\n正在检查Chrome浏览器...")
    chrome_found = False
    possible_chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expanduser("~") + r"\AppData\Local\Google\Chrome\Application\chrome.exe"
    ]

    for path in possible_chrome_paths:
        if os.path.exists(path):
            print(f"✓ Chrome浏览器已找到: {path}")
            chrome_found = True
            break

    if not chrome_found:
        logger.warning("未找到Chrome浏览器，程序可能无法正常运行")
        print("警告: 未找到Chrome浏览器，程序可能无法正常运行")
        print("请确保已安装Chrome浏览器")

        if non_interactive:
            logger.info("非交互式模式，自动继续执行")
            print("非交互式模式，自动继续执行...")
        else:
            response = input("是否继续? (y/n): ")
            if response.lower() != 'y':
                return

    if non_interactive:
        logger.info("非交互式模式，跳过用户确认")
        print("\n第2步: 准备测试壁纸设置功能（自动继续）...")
    else:
        input("\n第2步: 准备测试壁纸设置功能。按Enter键继续...")

    # 检查是否能够设置壁纸
    print("\n正在测试壁纸设置功能...")
    try:
        # 创建一个简单的测试图像
        print("创建测试图像...")
        test_img = Image.new("RGB", (100, 100), "blue")
        test_path = "test_wallpaper.bmp"
        test_img.save(test_path)
        print(f"✓ 测试图像已创建: {os.path.abspath(test_path)}")

        # 尝试设置测试壁纸
        print("\n尝试设置测试壁纸...")
        global WALLPAPER_PATH  # 声明全局变量，必须在使用前声明
        old_wallpaper_path = WALLPAPER_PATH
        WALLPAPER_PATH = test_path

        wallpaper_set = False

        # 方法1
        print("\n尝试方法1: 使用SystemParametersInfoW...")
        if set_wallpaper():
            print("✓ 壁纸设置测试成功!")
            wallpaper_set = True
        else:
            print("✗ 方法1失败")

            # 如果方法1失败，尝试直接调用API
            print("\n尝试方法2: 直接调用Windows API...")
            try:
                SPI_SETDESKWALLPAPER = 0x0014
                SPIF_UPDATEINIFILE = 0x01
                SPIF_SENDCHANGE = 0x02
                abs_path = os.path.abspath(test_path)
                result = ctypes.windll.user32.SystemParametersInfoW(
                    SPI_SETDESKWALLPAPER,
                    0,
                    abs_path,
                    SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
                )
                if result:
                    print("✓ 方法2成功!")
                    wallpaper_set = True
                else:
                    print(f"✗ 方法2失败: 返回值 {result}")
            except Exception as e:
                print(f"✗ 方法2异常: {e}")

            # 如果方法2也失败，尝试使用注册表
            if not wallpaper_set:
                print("\n尝试方法3: 使用注册表...")
                try:
                    import winreg
                    abs_path = os.path.abspath(test_path)
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

                    print("✓ 方法3成功!")
                    wallpaper_set = True
                except Exception as e:
                    print(f"✗ 方法3异常: {e}")

        # 恢复原始路径
        WALLPAPER_PATH = old_wallpaper_path

        # 询问用户壁纸是否已更改
        if non_interactive:
            logger.info("非交互式模式，假设壁纸设置成功")
            print("\n非交互式模式，假设壁纸设置成功")
            wallpaper_set = True
        else:
            response = input("\n您的桌面壁纸是否变成了蓝色? (y/n): ")
            if response.lower() == 'y':
                print("✓ 壁纸设置测试成功!")
                wallpaper_set = True
            else:
                print("✗ 壁纸设置测试失败")
                wallpaper_set = False

        # 清理测试文件
        try:
            os.remove(test_path)
            print(f"✓ 测试图像已删除: {test_path}")
        except Exception as e:
            print(f"警告: 无法删除测试图像: {e}")

        if not wallpaper_set:
            logger.warning("所有壁纸设置方法都失败了")
            print("\n警告: 所有壁纸设置方法都失败了")
            print("可能的原因:")
            print("1. 程序没有足够的权限")
            print("2. 系统策略限制了壁纸更改")
            print("3. Windows版本不兼容")
            print("\n建议:")
            print("- 以管理员身份运行程序")
            print("- 检查系统策略设置")
            print("- 尝试手动更改壁纸以确认权限")

            if non_interactive:
                logger.info("非交互式模式，自动继续执行")
                print("\n非交互式模式，自动继续执行...")
            else:
                response = input("\n是否继续运行程序? (y/n): ")
                if response.lower() != 'y':
                    return
    except Exception as e:
        logger.error(f"壁纸设置测试失败: {e}")
        logger.error(traceback.format_exc())
        print(f"\n壁纸设置测试失败: {e}")

        if non_interactive:
            logger.info("非交互式模式，自动继续执行")
            print("\n非交互式模式，自动继续执行...")
        else:
            response = input("\n是否继续运行程序? (y/n): ")
            if response.lower() != 'y':
                return

    if non_interactive:
        logger.info("非交互式模式，跳过用户确认")
        print("\n第3步: 准备获取风流场数据（自动继续）...")
    else:
        input("\n第3步: 准备获取风流场数据。按Enter键继续...")

    print("\n正在获取风流场数据...")
    print("这可能需要一些时间，请耐心等待...")

    # 首次运行
    success = False
    try:
        # 尝试更新壁纸
        timestamp, screenshot_path, _ = fetch_wind_data()

        if timestamp and screenshot_path:
            print(f"\n✓ 风流场数据获取成功!")
            print(f"时间戳: {timestamp}")
            print(f"截图路径: {screenshot_path}")

            print("\n正在创建壁纸...")
            if create_wind_wallpaper(timestamp, screenshot_path, None):
                print(f"\n✓ 壁纸创建成功: {WALLPAPER_PATH}")

                print("\n正在设置壁纸...")
                if set_wallpaper():
                    print("\n✓ 壁纸设置成功!")
                    success = True
                else:
                    print("\n✗ 壁纸设置失败")
            else:
                print("\n✗ 壁纸创建失败")
        else:
            print("\n✗ 风流场数据获取失败")
    except Exception as e:
        print(f"\n首次更新失败: {e}")
        import traceback
        traceback.print_exc()

    if not success:
        logger.warning("首次更新失败")
        print("\n首次更新失败，请检查上面的错误信息")

        if non_interactive:
            logger.info("非交互式模式，自动继续执行")
            print("非交互式模式，自动继续执行...")
        else:
            response = input("是否继续运行程序? (y/n): ")
            if response.lower() != 'y':
                return

    if non_interactive:
        logger.info("非交互式模式，跳过用户确认")
        print("\n第4步: 准备设置定时更新（自动继续）...")
    else:
        input("\n第4步: 准备设置定时更新。按Enter键继续...")

    # 设置定时任务
    schedule.every(UPDATE_INTERVAL).seconds.do(update_wallpaper)
    print(f"\n✓ 已设置每 {UPDATE_INTERVAL} 秒更新一次壁纸")

    print("\n="*50)
    print("程序设置完成!")
    print("="*50)
    print("程序现在将在后台运行")
    print("每次更新都会在控制台显示进度")
    print("按Ctrl+C可以停止程序")
    print("="*50)

    if non_interactive:
        logger.info("非交互式模式，自动开始运行程序")
        print("非交互式模式，自动开始运行程序...")
    else:
        input("按Enter键开始运行程序...")

    # 主循环
    try:
        logger.info("开始主循环")
        update_count = 0
        while True:
            schedule.run_pending()

            # 每60秒显示一次心跳信息
            if update_count % 60 == 0:
                idle_seconds = schedule.idle_seconds()
                logger.debug(f"程序正在运行... 下次更新还有 {idle_seconds:.0f} 秒")
                print(f"程序正在运行... 下次更新还有 {idle_seconds:.0f} 秒")

            update_count += 1
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("用户中断程序")
        print("\n程序已停止")
    except Exception as e:
        logger.error(f"程序异常: {e}")
        logger.error(traceback.format_exc())
        print(f"\n程序异常: {e}")

    if non_interactive:
        logger.info("非交互式模式，自动退出")
        print("\n程序已结束")
    else:
        input("\n按Enter键退出...")

if __name__ == "__main__":
    main()
