"""
中国气象网风流场查看器
使用Selenium截取风流场图像，并在PyQt5桌面应用程序中显示
"""
import sys
import os
import logging
import traceback
from datetime import datetime
import time
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QDesktopWidget, QPushButton
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import io
from PIL import Image

# 配置
LOG_FILE = "wind_flow_viewer.log"
UPDATE_INTERVAL = 300  # 更新间隔（秒），5分钟
WEATHER_URL = "https://www.weather.com.cn/radar/"  # 中国气象网雷达页面
CHROME_DRIVER_PATH = "chromedriver.exe"  # Chrome驱动路径，需要根据实际情况修改
SCREENSHOT_PATH = "wind_screenshot.png"  # 截图保存路径

# 创建日志记录器
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger()

class WindFlowFetcher(QThread):
    """风流场数据获取线程"""
    
    # 定义信号
    screenshot_ready = pyqtSignal(str)  # 截图路径
    status_update = pyqtSignal(str)  # 状态更新
    error_occurred = pyqtSignal(str)  # 错误信息
    
    def __init__(self):
        super().__init__()
        self.running = True
    
    def run(self):
        """线程主函数"""
        while self.running:
            try:
                self.status_update.emit("正在获取风流场数据...")
                screenshot_path = self.fetch_wind_data()
                
                if screenshot_path:
                    self.screenshot_ready.emit(screenshot_path)
                    self.status_update.emit(f"数据已更新 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                else:
                    self.error_occurred.emit("获取风流场数据失败")
                
                # 等待下一次更新
                for i in range(UPDATE_INTERVAL):
                    if not self.running:
                        break
                    time.sleep(1)
            except Exception as e:
                logger.error(f"获取风流场数据异常: {e}")
                logger.error(traceback.format_exc())
                self.error_occurred.emit(f"获取风流场数据异常: {e}")
                
                # 出错后等待一段时间再重试
                for i in range(60):
                    if not self.running:
                        break
                    time.sleep(1)
    
    def stop(self):
        """停止线程"""
        self.running = False
    
    def fetch_wind_data(self):
        """获取风流场数据"""
        driver = None
        try:
            self.status_update.emit("启动浏览器...")
            logger.info("启动浏览器")
            
            # 配置Chrome选项
            chrome_options = Options()
            chrome_options.add_argument("--headless")  # 无头模式
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")  # 解决内存不足问题
            
            # 创建Chrome浏览器实例
            service = Service(CHROME_DRIVER_PATH)
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # 访问中国气象网雷达页面
            self.status_update.emit(f"访问 {WEATHER_URL}...")
            logger.info(f"访问 {WEATHER_URL}")
            driver.get(WEATHER_URL)
            
            # 等待页面加载完成
            self.status_update.emit("等待页面元素加载...")
            logger.info("等待页面元素加载")
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".mapContainer"))
            )
            
            # 点击风流场选项
            self.status_update.emit("切换到风流场视图...")
            logger.info("切换到风流场视图")
            
            # 查找风流场选项
            wind_options = driver.find_elements(By.XPATH, "//li[contains(text(), '风流场')]")
            
            if wind_options:
                wind_option = wind_options[0]
                logger.info(f"找到风流场选项: {wind_option.text}")
            else:
                # 如果找不到，尝试其他方法
                logger.info("使用备用方法查找风流场选项")
                
                # 尝试查找所有列表项
                all_options = driver.find_elements(By.TAG_NAME, "li")
                wind_option = None
                
                for option in all_options:
                    if '风' in option.text or '流场' in option.text:
                        wind_option = option
                        logger.info(f"找到可能的风流场选项: {option.text}")
                        break
                
                if not wind_option:
                    # 如果仍然找不到，尝试点击可能的按钮或链接
                    buttons = driver.find_elements(By.TAG_NAME, "button")
                    links = driver.find_elements(By.TAG_NAME, "a")
                    
                    for element in buttons + links:
                        if '风' in element.text or '流场' in element.text:
                            wind_option = element
                            logger.info(f"找到可能的风流场按钮/链接: {element.text}")
                            break
                
                if not wind_option:
                    raise Exception("找不到风流场选项")
            
            # 点击风流场选项
            driver.execute_script("arguments[0].scrollIntoView(true);", wind_option)
            driver.execute_script("arguments[0].click();", wind_option)
            logger.info("已点击风流场选项")
            
            # 等待风流场数据加载
            self.status_update.emit("等待风流场数据加载...")
            logger.info("等待风流场数据加载")
            time.sleep(5)
            
            # 截取风流场图
            self.status_update.emit("截取风流场图...")
            logger.info("截取风流场图")
            
            # 尝试找到地图容器
            map_elements = driver.find_elements(By.CSS_SELECTOR, ".mapContainer")
            if map_elements:
                map_element = map_elements[0]
                logger.info("找到地图容器")
            else:
                # 尝试查找其他可能的地图容器
                map_elements = driver.find_elements(By.CSS_SELECTOR, "div[class*='map'], div[id*='map']")
                if map_elements:
                    map_element = map_elements[0]
                    logger.info(f"找到备用地图容器: {map_element.get_attribute('class')}")
                else:
                    # 如果找不到任何地图容器，截取整个页面
                    logger.warning("找不到地图容器，将截取整个页面")
                    map_element = driver.find_element(By.TAG_NAME, "body")
            
            # 截取元素
            screenshot = map_element.screenshot_as_png
            logger.info("截图已获取")
            
            # 保存截图
            with open(SCREENSHOT_PATH, "wb") as file:
                file.write(screenshot)
            
            logger.info(f"风流场截图已保存到: {os.path.abspath(SCREENSHOT_PATH)}")
            
            # 关闭浏览器
            driver.quit()
            logger.info("浏览器已关闭")
            
            return SCREENSHOT_PATH
        except Exception as e:
            logger.error(f"获取风流场数据失败: {e}")
            logger.error(traceback.format_exc())
            
            if driver:
                try:
                    driver.quit()
                    logger.info("浏览器已关闭")
                except:
                    logger.error("关闭浏览器时出错")
            
            return None

class WindFlowViewer(QMainWindow):
    """风流场查看器"""
    
    def __init__(self):
        super().__init__()
        
        # 设置窗口属性
        self.setWindowTitle("中国气象网风流场查看器")
        
        # 获取屏幕尺寸
        screen = QDesktopWidget().screenGeometry()
        self.screen_width = screen.width()
        self.screen_height = screen.height()
        
        # 设置窗口尺寸和位置
        self.resize(int(self.screen_width * 0.8), int(self.screen_height * 0.8))
        self.center()
        
        # 创建中央部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # 创建布局
        self.layout = QVBoxLayout(self.central_widget)
        
        # 创建图像标签
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("background-color: black;")
        self.layout.addWidget(self.image_label)
        
        # 创建状态标签
        self.status_label = QLabel("正在初始化...")
        self.status_label.setStyleSheet("background-color: rgba(0, 0, 0, 0.5); color: white; padding: 5px;")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.status_label)
        
        # 创建按钮布局
        button_layout = QVBoxLayout()
        
        # 创建刷新按钮
        self.refresh_button = QPushButton("刷新数据")
        self.refresh_button.clicked.connect(self.refresh_data)
        button_layout.addWidget(self.refresh_button)
        
        # 创建设为壁纸按钮
        self.wallpaper_button = QPushButton("设为壁纸")
        self.wallpaper_button.clicked.connect(self.set_as_wallpaper)
        button_layout.addWidget(self.wallpaper_button)
        
        # 创建全屏按钮
        self.fullscreen_button = QPushButton("全屏显示")
        self.fullscreen_button.clicked.connect(self.toggle_fullscreen)
        button_layout.addWidget(self.fullscreen_button)
        
        # 创建退出按钮
        self.exit_button = QPushButton("退出")
        self.exit_button.clicked.connect(self.close)
        button_layout.addWidget(self.exit_button)
        
        # 添加按钮布局到主布局
        self.layout.addLayout(button_layout)
        
        # 创建风流场数据获取线程
        self.fetcher = WindFlowFetcher()
        self.fetcher.screenshot_ready.connect(self.update_image)
        self.fetcher.status_update.connect(self.update_status)
        self.fetcher.error_occurred.connect(self.show_error)
        
        # 启动线程
        self.fetcher.start()
        
        logger.info("风流场查看器已启动")
    
    def center(self):
        """将窗口居中显示"""
        frame_geometry = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())
    
    def update_image(self, screenshot_path):
        """更新图像"""
        try:
            # 加载图像
            pixmap = QPixmap(screenshot_path)
            
            # 调整图像大小以适应窗口
            pixmap = pixmap.scaled(self.image_label.width(), self.image_label.height(), 
                                   Qt.KeepAspectRatio, Qt.SmoothTransformation)
            
            # 设置图像
            self.image_label.setPixmap(pixmap)
            
            logger.info("图像已更新")
        except Exception as e:
            logger.error(f"更新图像失败: {e}")
            logger.error(traceback.format_exc())
            self.status_label.setText(f"更新图像失败: {e}")
    
    def update_status(self, status):
        """更新状态"""
        self.status_label.setText(status)
    
    def show_error(self, error):
        """显示错误"""
        self.status_label.setText(f"错误: {error}")
    
    def refresh_data(self):
        """刷新数据"""
        # 停止当前线程
        self.fetcher.stop()
        self.fetcher.wait()
        
        # 创建新线程
        self.fetcher = WindFlowFetcher()
        self.fetcher.screenshot_ready.connect(self.update_image)
        self.fetcher.status_update.connect(self.update_status)
        self.fetcher.error_occurred.connect(self.show_error)
        
        # 启动线程
        self.fetcher.start()
    
    def set_as_wallpaper(self):
        """设置为壁纸"""
        try:
            import ctypes
            
            # 检查截图文件是否存在
            if not os.path.exists(SCREENSHOT_PATH):
                self.status_label.setText("错误: 截图文件不存在")
                return
            
            # 设置壁纸
            abs_path = os.path.abspath(SCREENSHOT_PATH)
            ctypes.windll.user32.SystemParametersInfoW(20, 0, abs_path, 3)
            
            self.status_label.setText("已设置为桌面壁纸")
            logger.info("已设置为桌面壁纸")
        except Exception as e:
            logger.error(f"设置壁纸失败: {e}")
            logger.error(traceback.format_exc())
            self.status_label.setText(f"设置壁纸失败: {e}")
    
    def toggle_fullscreen(self):
        """切换全屏显示"""
        if self.isFullScreen():
            self.showNormal()
            self.fullscreen_button.setText("全屏显示")
        else:
            self.showFullScreen()
            self.fullscreen_button.setText("退出全屏")
    
    def keyPressEvent(self, event):
        """按键事件处理"""
        # 按ESC键退出全屏或关闭程序
        if event.key() == Qt.Key_Escape:
            if self.isFullScreen():
                self.showNormal()
                self.fullscreen_button.setText("全屏显示")
            else:
                self.close()
        # 按F5键刷新
        elif event.key() == Qt.Key_F5:
            self.refresh_data()
        # 按F11键切换全屏
        elif event.key() == Qt.Key_F11:
            self.toggle_fullscreen()
        else:
            super().keyPressEvent(event)
    
    def closeEvent(self, event):
        """关闭事件处理"""
        # 停止线程
        self.fetcher.stop()
        self.fetcher.wait()
        
        logger.info("风流场查看器已关闭")
        super().closeEvent(event)

def main():
    """主函数"""
    try:
        logger.info("="*50)
        logger.info("启动中国气象网风流场查看器")
        logger.info("="*50)
        
        # 检查Chrome驱动是否存在
        if not os.path.exists(CHROME_DRIVER_PATH):
            logger.error(f"Chrome驱动文件不存在: {CHROME_DRIVER_PATH}")
            print(f"错误: Chrome驱动文件不存在: {CHROME_DRIVER_PATH}")
            print("请下载适合您Chrome版本的驱动并放置在正确位置")
            print("下载地址: https://chromedriver.chromium.org/downloads")
            input("按Enter键退出...")
            return
        
        # 创建应用程序
        app = QApplication(sys.argv)
        
        # 创建主窗口
        window = WindFlowViewer()
        window.show()
        
        # 运行应用程序
        sys.exit(app.exec_())
    except Exception as e:
        logger.error(f"程序异常: {e}")
        logger.error(traceback.format_exc())
        print(f"程序异常: {e}")
        input("按Enter键退出...")

if __name__ == "__main__":
    main()
