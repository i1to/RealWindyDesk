"""
中国气象网风流场实时动态壁纸
将中国气象网的风流场页面直接嵌入到桌面背景中
"""
import sys
import os
import logging
import traceback
from datetime import datetime
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QTimer, QUrl, QSize, QPoint
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings, QWebEngineProfile

# 配置
LOG_FILE = "wind_flow_live_wallpaper.log"
WEATHER_URL = "https://www.weather.com.cn/radar/"  # 中国气象网雷达页面
UPDATE_INTERVAL = 3600  # 刷新间隔（秒），1小时

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

class WindFlowLiveWallpaper(QMainWindow):
    """风流场实时动态壁纸"""

    def __init__(self):
        super().__init__()

        # 设置窗口属性
        self.setWindowTitle("中国气象网风流场实时动态壁纸")
        # 只有当图标文件存在时才设置窗口图标
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        # 设置窗口标志，使其始终显示在桌面上
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnBottomHint | Qt.Tool)

        # 设置窗口属性，使其透明
        self.setAttribute(Qt.WA_TranslucentBackground)

        # 获取屏幕尺寸
        screen_geometry = QApplication.desktop().screenGeometry()
        self.screen_width = screen_geometry.width()
        self.screen_height = screen_geometry.height()

        # 设置窗口尺寸为全屏
        self.setGeometry(0, 0, self.screen_width, self.screen_height)

        # 创建中央部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 创建布局
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # 创建Web视图
        self.web_view = QWebEngineView()

        # 配置Web视图
        self.web_view.page().profile().clearHttpCache()  # 清除HTTP缓存
        self.web_view.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        self.web_view.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.web_view.settings().setAttribute(QWebEngineSettings.AutoLoadImages, True)
        self.web_view.settings().setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        self.web_view.settings().setAttribute(QWebEngineSettings.WebGLEnabled, True)

        # 添加Web视图到布局
        self.layout.addWidget(self.web_view)

        # 创建状态标签
        self.status_label = QLabel("正在加载中国气象网风流场页面...")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFont(QFont("Arial", 12))
        self.status_label.setStyleSheet("background-color: rgba(0, 0, 0, 150); color: white; padding: 10px;")
        self.status_label.setFixedHeight(40)
        self.layout.addWidget(self.status_label)

        # 创建定时器，用于定期刷新页面
        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.refresh_page)
        self.refresh_timer.start(UPDATE_INTERVAL * 1000)  # 毫秒

        # 创建定时器，用于隐藏状态标签
        self.status_timer = QTimer(self)
        self.status_timer.timeout.connect(self.hide_status)
        self.status_timer.setSingleShot(True)

        # 加载中国气象网风流场页面
        self.load_wind_flow_page()

        logger.info("风流场实时动态壁纸已启动")

    def load_wind_flow_page(self):
        """加载中国气象网风流场页面"""
        try:
            logger.info("加载中国气象网风流场页面")
            self.status_label.setText("正在加载中国气象网风流场页面...")
            self.status_label.show()
            self.status_timer.start(10000)  # 10秒后隐藏状态标签

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
            logger.info("页面加载成功，注入JavaScript代码")
            self.status_label.setText("页面加载成功，正在处理...")

            # 注入JavaScript代码，切换到风流场视图并隐藏不需要的元素
            js_code = """
            // 函数：查找并点击风流场选项
            function findAndClickWindFlowOption() {
                console.log('尝试查找风流场选项...');

                // 方法1：查找包含"风流场"文本的元素
                var elements = document.querySelectorAll('li, a, button, div, span');
                for (var i = 0; i < elements.length; i++) {
                    if (elements[i].textContent.includes('风流场')) {
                        console.log('找到风流场元素:', elements[i].textContent);
                        elements[i].click();
                        return true;
                    }
                }

                // 方法2：查找包含"风"或"流场"的元素
                for (var i = 0; i < elements.length; i++) {
                    if (elements[i].textContent.includes('风') || elements[i].textContent.includes('流场')) {
                        console.log('找到可能的风流场元素:', elements[i].textContent);
                        elements[i].click();
                        return true;
                    }
                }

                console.log('未找到风流场元素');
                return false;
            }

            // 函数：隐藏不需要的元素
            function hideUnnecessaryElements() {
                console.log('隐藏不需要的元素...');

                // 隐藏页眉、页脚、菜单等
                var elementsToHide = document.querySelectorAll('header, footer, nav, .menu, .sidebar, .ad, .logo, .search, .nav');
                for (var i = 0; i < elementsToHide.length; i++) {
                    elementsToHide[i].style.display = 'none';
                }

                // 隐藏所有按钮和输入框
                var buttons = document.querySelectorAll('button, input, select');
                for (var i = 0; i < buttons.length; i++) {
                    buttons[i].style.display = 'none';
                }

                // 尝试找到地图容器并使其全屏显示
                var mapContainer = document.querySelector('.mapContainer') ||
                                   document.querySelector('div[class*="map"]') ||
                                   document.querySelector('div[id*="map"]');
                if (mapContainer) {
                    console.log('找到地图容器');
                    mapContainer.style.width = '100vw';
                    mapContainer.style.height = '100vh';
                    mapContainer.style.position = 'fixed';
                    mapContainer.style.top = '0';
                    mapContainer.style.left = '0';
                    mapContainer.style.zIndex = '1000';

                    // 设置页面背景为黑色
                    document.body.style.backgroundColor = 'black';
                    document.body.style.margin = '0';
                    document.body.style.padding = '0';
                    document.body.style.overflow = 'hidden';

                    return true;
                }

                console.log('未找到地图容器');
                return false;
            }

            // 执行操作
            setTimeout(function() {
                var clickResult = findAndClickWindFlowOption();
                console.log('点击风流场选项结果:', clickResult);

                // 等待风流场加载
                setTimeout(function() {
                    var hideResult = hideUnnecessaryElements();
                    console.log('隐藏元素结果:', hideResult);
                }, 3000);
            }, 2000);

            // 返回成功
            true;
            """

            # 执行JavaScript代码
            self.web_view.page().runJavaScript(js_code, self.on_js_executed)
        else:
            logger.error("页面加载失败")
            self.status_label.setText("页面加载失败，请检查网络连接")

    def on_js_executed(self, result):
        """JavaScript代码执行完成后的处理"""
        if result:
            logger.info("JavaScript代码执行成功")
            self.status_label.setText("风流场实时动态壁纸已启动")
            self.status_timer.start(3000)  # 3秒后隐藏状态标签
        else:
            logger.warning("JavaScript代码执行失败")
            self.status_label.setText("处理页面失败，请按F5刷新")

    def hide_status(self):
        """隐藏状态标签"""
        self.status_label.hide()

    def refresh_page(self):
        """刷新页面"""
        logger.info("刷新页面")
        self.status_label.setText("正在刷新页面...")
        self.status_label.show()
        self.web_view.reload()
        self.status_timer.start(10000)  # 10秒后隐藏状态标签

    def keyPressEvent(self, event):
        """按键事件处理"""
        # 按ESC键退出程序
        if event.key() == Qt.Key_Escape:
            self.close()
        # 按F5键刷新页面
        elif event.key() == Qt.Key_F5:
            self.refresh_page()
        # 按F1键显示/隐藏状态标签
        elif event.key() == Qt.Key_F1:
            if self.status_label.isVisible():
                self.status_label.hide()
            else:
                self.status_label.setText("风流场实时动态壁纸 - 按ESC退出，按F5刷新")
                self.status_label.show()
                self.status_timer.start(5000)  # 5秒后隐藏状态标签
        else:
            super().keyPressEvent(event)

    def closeEvent(self, event):
        """关闭事件处理"""
        logger.info("风流场实时动态壁纸已关闭")
        super().closeEvent(event)

def check_dependencies():
    """检查依赖项是否已安装"""
    try:
        # 检查PyQt5
        import PyQt5
        logger.info(f"PyQt5版本: {PyQt5.QtCore.QT_VERSION_STR}")

        # 检查PyQtWebEngine
        import PyQt5.QtWebEngineWidgets
        logger.info("PyQtWebEngine已安装")

        return True
    except ImportError as e:
        logger.error(f"依赖项检查失败: {e}")
        print(f"错误: 缺少必要的依赖项: {e}")
        print("请运行以下命令安装依赖项:")
        print("pip install PyQt5 PyQtWebEngine")
        return False

def main():
    """主函数"""
    try:
        logger.info("="*50)
        logger.info("启动中国气象网风流场实时动态壁纸")
        logger.info("="*50)

        # 检查依赖项
        if not check_dependencies():
            input("按Enter键退出...")
            return 1

        # 创建应用程序
        app = QApplication(sys.argv)

        # 创建主窗口
        window = WindFlowLiveWallpaper()
        window.show()

        # 运行应用程序
        return app.exec_()
    except Exception as e:
        logger.error(f"程序异常: {e}")
        logger.error(traceback.format_exc())
        print(f"程序异常: {e}")
        input("按Enter键退出...")
        return 1

if __name__ == "__main__":
    sys.exit(main())
