"""
中国气象网风流场桌面应用程序
使用PyQt5创建一个透明的桌面应用程序，显示中国气象网的风流场数据
"""
import sys
import os
import logging
import traceback
from datetime import datetime
import time
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QDesktopWidget
from PyQt5.QtCore import Qt, QTimer, QUrl, QSize
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings

# 配置
LOG_FILE = "wind_flow_desktop.log"
UPDATE_INTERVAL = 300  # 更新间隔（秒），5分钟
WEATHER_URL = "https://www.weather.com.cn/radar/"  # 中国气象网雷达页面

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

class WindFlowDesktop(QMainWindow):
    """风流场桌面应用程序"""
    
    def __init__(self):
        super().__init__()
        
        # 设置窗口属性
        self.setWindowTitle("中国气象网风流场")
        self.setWindowIcon(QIcon("icon.png"))  # 如果有图标文件的话
        
        # 获取屏幕尺寸
        screen = QDesktopWidget().screenGeometry()
        self.screen_width = screen.width()
        self.screen_height = screen.height()
        
        # 设置窗口尺寸和位置
        self.resize(self.screen_width, self.screen_height)
        self.move(0, 0)
        
        # 设置窗口透明度和样式
        self.setWindowOpacity(0.9)  # 90%不透明度
        self.setStyleSheet("background-color: rgba(255, 255, 255, 0.8);")  # 半透明白色背景
        
        # 设置窗口标志，使其始终显示在桌面上
        self.setWindowFlags(Qt.WindowStaysOnBottomHint | Qt.FramelessWindowHint)
        
        # 创建中央部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # 创建布局
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建Web视图，用于显示中国气象网的风流场数据
        self.web_view = QWebEngineView()
        self.web_view.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        self.web_view.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.web_view.settings().setAttribute(QWebEngineSettings.AutoLoadImages, True)
        
        # 添加Web视图到布局
        self.layout.addWidget(self.web_view)
        
        # 创建状态标签，显示更新时间
        self.status_label = QLabel("正在加载...")
        self.status_label.setStyleSheet("background-color: rgba(0, 0, 0, 0.5); color: white; padding: 5px;")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.status_label)
        
        # 创建定时器，定期更新风流场数据
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_wind_flow)
        self.timer.start(UPDATE_INTERVAL * 1000)  # 毫秒
        
        # 初始加载
        self.load_wind_flow_page()
        
        logger.info("风流场桌面应用程序已启动")
    
    def load_wind_flow_page(self):
        """加载中国气象网风流场页面"""
        try:
            logger.info("加载中国气象网风流场页面")
            self.status_label.setText("正在加载中国气象网风流场页面...")
            
            # 加载中国气象网雷达页面
            self.web_view.load(QUrl(WEATHER_URL))
            
            # 连接加载完成信号
            self.web_view.loadFinished.connect(self.on_page_loaded)
        except Exception as e:
            logger.error(f"加载页面失败: {e}")
            logger.error(traceback.format_exc())
            self.status_label.setText(f"加载页面失败: {e}")
    
    def on_page_loaded(self, success):
        """页面加载完成后的处理"""
        if success:
            logger.info("页面加载成功，切换到风流场视图")
            self.status_label.setText("页面加载成功，切换到风流场视图...")
            
            # 使用JavaScript切换到风流场视图
            # 注意：这里的JavaScript代码需要根据实际网页结构进行调整
            js_code = """
            // 查找包含"风流场"文本的元素并点击
            var elements = document.querySelectorAll('li, a, button, div');
            for (var i = 0; i < elements.length; i++) {
                if (elements[i].textContent.includes('风流场')) {
                    elements[i].click();
                    console.log('找到并点击了风流场元素');
                    return true;
                }
            }
            console.log('未找到风流场元素');
            return false;
            """
            
            # 执行JavaScript代码
            self.web_view.page().runJavaScript(js_code, self.on_switch_to_wind_flow)
        else:
            logger.error("页面加载失败")
            self.status_label.setText("页面加载失败，请检查网络连接")
    
    def on_switch_to_wind_flow(self, result):
        """切换到风流场视图后的处理"""
        if result:
            logger.info("已切换到风流场视图")
            self.status_label.setText(f"已切换到风流场视图 - 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # 隐藏网页中不需要的元素
            js_hide_elements = """
            // 隐藏不需要的元素，如页眉、页脚、菜单等
            var elementsToHide = document.querySelectorAll('header, footer, nav, .menu, .sidebar, .ad');
            for (var i = 0; i < elementsToHide.length; i++) {
                elementsToHide[i].style.display = 'none';
            }
            
            // 尝试找到地图容器并使其全屏显示
            var mapContainer = document.querySelector('.mapContainer') || 
                               document.querySelector('div[class*="map"]') || 
                               document.querySelector('div[id*="map"]');
            if (mapContainer) {
                mapContainer.style.width = '100%';
                mapContainer.style.height = '100vh';
                mapContainer.style.position = 'fixed';
                mapContainer.style.top = '0';
                mapContainer.style.left = '0';
                mapContainer.style.zIndex = '1000';
                return true;
            }
            return false;
            """
            
            self.web_view.page().runJavaScript(js_hide_elements, self.on_elements_hidden)
        else:
            logger.warning("未能切换到风流场视图")
            self.status_label.setText("未能切换到风流场视图，尝试手动查找元素")
            
            # 尝试其他方法查找风流场元素
            js_find_wind_flow = """
            // 尝试查找包含"风"或"流场"的元素
            var elements = document.querySelectorAll('li, a, button, div');
            for (var i = 0; i < elements.length; i++) {
                if (elements[i].textContent.includes('风') || elements[i].textContent.includes('流场')) {
                    elements[i].click();
                    console.log('找到并点击了可能的风流场元素: ' + elements[i].textContent);
                    return true;
                }
            }
            console.log('未找到任何可能的风流场元素');
            return false;
            """
            
            self.web_view.page().runJavaScript(js_find_wind_flow, self.on_switch_to_wind_flow)
    
    def on_elements_hidden(self, result):
        """隐藏不需要的元素后的处理"""
        if result:
            logger.info("已隐藏不需要的元素并调整地图容器")
        else:
            logger.warning("未找到地图容器")
    
    def update_wind_flow(self):
        """定期更新风流场数据"""
        logger.info("更新风流场数据")
        self.status_label.setText("正在更新风流场数据...")
        
        # 刷新页面
        self.web_view.reload()
    
    def keyPressEvent(self, event):
        """按键事件处理"""
        # 按ESC键退出程序
        if event.key() == Qt.Key_Escape:
            self.close()
        # 按F5键刷新
        elif event.key() == Qt.Key_F5:
            self.update_wind_flow()
        # 按F11键切换全屏
        elif event.key() == Qt.Key_F11:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()
        # 按住Alt键时，允许拖动窗口
        elif event.key() == Qt.Key_Alt:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnBottomHint)
            self.show()
        else:
            super().keyPressEvent(event)
    
    def keyReleaseEvent(self, event):
        """按键释放事件处理"""
        # 释放Alt键时，恢复窗口属性
        if event.key() == Qt.Key_Alt:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnBottomHint)
            self.show()
        else:
            super().keyReleaseEvent(event)

def main():
    """主函数"""
    try:
        logger.info("="*50)
        logger.info("启动中国气象网风流场桌面应用程序")
        logger.info("="*50)
        
        # 创建应用程序
        app = QApplication(sys.argv)
        
        # 创建主窗口
        window = WindFlowDesktop()
        window.show()
        
        # 运行应用程序
        sys.exit(app.exec_())
    except Exception as e:
        logger.error(f"程序异常: {e}")
        logger.error(traceback.format_exc())
        print(f"程序异常: {e}")

if __name__ == "__main__":
    main()
