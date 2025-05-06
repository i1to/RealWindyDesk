"""
Real-time Wind Flow Visualization Desktop Wallpaper
Embeds the Earth Nullschool wind flow visualization directly into the desktop background
"""
import sys
import os
import logging
import traceback
from datetime import datetime
import time
import requests
import argparse
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QTimer, QUrl, QSize, QPoint
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings, QWebEngineProfile

# Configuration
LOG_FILE = "wind_flow_live_wallpaper.log"
WEATHER_URL = "https://earth.nullschool.net/zh-cn/#current/wind/surface/level/patterson=0.00,0.00,185"  # Earth Nullschool wind visualization
UPDATE_INTERVAL = 3600  # Refresh interval (seconds), 1 hour

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

        # Set window properties
        self.setWindowTitle("Earth Nullschool Wind Flow Live Wallpaper")
        # Only set the window icon if the icon file exists
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

        # Create status label
        self.status_label = QLabel("Loading Earth Nullschool wind visualization...")
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
        """Load Earth Nullschool wind visualization page"""
        try:
            logger.info("Loading Earth Nullschool wind visualization page")
            self.status_label.setText("Loading Earth Nullschool wind visualization...")
            self.status_label.show()
            self.status_timer.start(10000)  # Hide status label after 10 seconds

            # 测试网络连接
            try:
                logger.info(f"测试网络连接到 {WEATHER_URL}")
                test_response = requests.head(WEATHER_URL, timeout=10)
                logger.info(f"网络连接测试结果: 状态码 {test_response.status_code}")
                if test_response.status_code >= 400:
                    logger.warning(f"网站返回错误状态码: {test_response.status_code}")
                    self.status_label.setText(f"网站返回错误状态码: {test_response.status_code}，尝试继续加载...")
            except Exception as net_e:
                logger.warning(f"网络连接测试失败: {net_e}")
                self.status_label.setText(f"网络连接测试失败: {net_e}，尝试继续加载...")

            # 配置Web视图
            logger.info("配置Web视图")
            settings = self.web_view.settings()
            settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
            settings.setAttribute(QWebEngineSettings.PluginsEnabled, True)
            settings.setAttribute(QWebEngineSettings.AutoLoadImages, True)
            settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
            settings.setAttribute(QWebEngineSettings.WebGLEnabled, True)

            # 设置用户代理
            page = self.web_view.page()
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            page.profile().setHttpUserAgent(user_agent)
            logger.info(f"设置用户代理: {user_agent}")

            # 清除缓存
            logger.info("清除缓存")
            page.profile().clearHttpCache()

            # 加载中国气象网雷达页面
            logger.info(f"开始加载URL: {WEATHER_URL}")
            self.web_view.load(QUrl(WEATHER_URL))

            # 连接加载完成信号
            self.web_view.loadFinished.connect(self.on_page_loaded)

            # 连接加载进度信号
            self.web_view.loadProgress.connect(self.on_load_progress)

            # 连接错误信号
            page.loadStarted.connect(lambda: logger.info("页面开始加载"))
            page.loadFinished.connect(lambda ok: logger.info(f"页面加载完成: {'成功' if ok else '失败'}"))

        except Exception as e:
            logger.error(f"加载页面失败: {e}")
            logger.error(traceback.format_exc())
            self.status_label.setText(f"加载页面失败: {e}")

    def on_load_progress(self, progress):
        """Page loading progress update"""
        logger.debug(f"Page loading progress: {progress}%")
        if progress % 20 == 0:  # Log every 20%
            logger.info(f"Page loading progress: {progress}%")
        self.status_label.setText(f"Loading Earth Nullschool wind visualization... {progress}%")

    def on_page_loaded(self, success):
        """Process after page loading is complete"""
        if success:
            logger.info("Page loaded successfully, injecting JavaScript code")
            self.status_label.setText("Page loaded successfully, processing...")

            # 获取页面HTML源码进行调试
            self.web_view.page().toHtml(self.debug_html)

            # 注入JavaScript代码，切换到风流场视图并隐藏不需要的元素
            js_code = """
            // 调试函数：记录页面信息
            function logPageInfo() {
                console.log('页面标题:', document.title);
                console.log('页面URL:', window.location.href);

                // 记录所有可点击元素
                var clickableElements = document.querySelectorAll('a, button, li, div[onclick], span[onclick]');
                console.log('可点击元素数量:', clickableElements.length);
                for (var i = 0; i < Math.min(clickableElements.length, 20); i++) {
                    console.log('元素', i, ':', clickableElements[i].tagName, clickableElements[i].textContent.trim());
                }

                // 记录所有菜单项
                var menuItems = document.querySelectorAll('.menu-item, .nav-item, li');
                console.log('菜单项数量:', menuItems.length);
                for (var i = 0; i < Math.min(menuItems.length, 20); i++) {
                    if (menuItems[i].textContent) {
                        console.log('菜单项', i, ':', menuItems[i].textContent.trim());
                    }
                }
            }

            // 函数：切换到风流场视图
            function switchToWindFlow() {
                console.log('尝试切换到风流场视图...');

                // 根据截图分析，尝试查找底部的风流场按钮或选项
                var windFlowButtons = [];

                // 查找底部工具栏中的按钮
                var bottomButtons = document.querySelectorAll('.bottom-toolbar button, .bottom-bar button, .toolbar button');
                console.log('底部按钮数量:', bottomButtons.length);

                // 查找所有按钮和可点击元素
                var allButtons = document.querySelectorAll('button, [role="button"], .btn, .button');
                console.log('所有按钮数量:', allButtons.length);

                // 查找所有包含"风"字的元素
                var windElements = [];
                var allElements = document.querySelectorAll('*');
                for (var i = 0; i < allElements.length; i++) {
                    if (allElements[i].textContent &&
                        (allElements[i].textContent.includes('风') ||
                         allElements[i].textContent.includes('流场'))) {
                        windElements.push(allElements[i]);
                    }
                }
                console.log('包含"风"字的元素数量:', windElements.length);

                // 尝试点击风流场相关元素
                for (var i = 0; i < windElements.length; i++) {
                    try {
                        console.log('尝试点击元素:', windElements[i].textContent);
                        windElements[i].click();
                        console.log('已点击风流场相关元素');
                        break;
                    } catch (e) {
                        console.error('点击失败:', e);
                    }
                }

                // 特定网站的处理：根据截图，尝试查找并点击特定位置的按钮
                try {
                    // 尝试查找底部工具栏中的按钮
                    var toolbarButtons = document.querySelectorAll('.toolbar button, .toolbar-item');
                    if (toolbarButtons.length > 0) {
                        console.log('找到工具栏按钮数量:', toolbarButtons.length);
                        // 尝试点击可能的风流场按钮（通常在底部工具栏）
                        for (var i = 0; i < toolbarButtons.length; i++) {
                            console.log('工具栏按钮', i, ':', toolbarButtons[i].textContent);
                        }

                        // 根据截图，风流场按钮可能在底部工具栏的左侧
                        if (toolbarButtons.length >= 2) {
                            console.log('尝试点击第二个工具栏按钮');
                            toolbarButtons[1].click();
                        }
                    }

                    // 尝试查找左侧的图层控制面板
                    var layerControls = document.querySelectorAll('.layer-control, .layer-panel, .sidebar-left');
                    if (layerControls.length > 0) {
                        console.log('找到图层控制面板');
                        var layerItems = layerControls[0].querySelectorAll('li, .layer-item');
                        for (var i = 0; i < layerItems.length; i++) {
                            if (layerItems[i].textContent &&
                                (layerItems[i].textContent.includes('风') ||
                                 layerItems[i].textContent.includes('流场'))) {
                                console.log('找到风流场图层选项:', layerItems[i].textContent);
                                layerItems[i].click();
                                break;
                            }
                        }
                    }
                } catch (e) {
                    console.error('特定网站处理失败:', e);
                }
            }

            // 函数：隐藏所有UI元素，只保留地图
            function hideAllUIElements() {
                console.log('隐藏所有UI元素...');

                // 隐藏顶部标题栏和logo
                var header = document.querySelector('header, .header, .navbar, .nav-bar, .top-bar');
                if (header) {
                    console.log('隐藏顶部标题栏');
                    header.style.display = 'none';
                }

                // 隐藏所有可能的UI元素
                var uiElements = [
                    'header', '.header', '.navbar', '.nav-bar', '.top-bar',
                    'footer', '.footer', '.bottom-bar',
                    '.sidebar', '.sidebar-left', '.sidebar-right',
                    '.panel', '.control-panel', '.layer-panel',
                    '.logo', '.brand', '.title', '.app-title',
                    '.toolbar', '.toolbar-top', '.toolbar-bottom',
                    '.menu', '.menu-bar', '.nav-menu',
                    '.search', '.search-box', '.search-bar',
                    '.zoom-control', '.map-controls', '.leaflet-control',
                    '.legend', '.map-legend', '.color-legend',
                    '.info-box', '.info-panel', '.popup',
                    '.attribution', '.copyright', '.credits'
                ];

                // 隐藏所有匹配的元素
                uiElements.forEach(function(selector) {
                    var elements = document.querySelectorAll(selector);
                    for (var i = 0; i < elements.length; i++) {
                        console.log('隐藏元素:', selector);
                        elements[i].style.display = 'none';
                    }
                });

                // 隐藏所有按钮和控件
                var controls = document.querySelectorAll('button, .btn, .button, input, select, .control');
                for (var i = 0; i < controls.length; i++) {
                    controls[i].style.display = 'none';
                }

                // 特别处理：隐藏顶部的标题和logo（根据截图）
                var topElements = document.querySelectorAll('.top, .top-container, .header-container');
                for (var i = 0; i < topElements.length; i++) {
                    topElements[i].style.display = 'none';
                }

                // 查找并隐藏所有可能的标题文本
                var titleElements = document.querySelectorAll('h1, h2, h3, .title, .heading');
                for (var i = 0; i < titleElements.length; i++) {
                    titleElements[i].style.display = 'none';
                }

                // 查找并隐藏所有可能的logo
                var logoElements = document.querySelectorAll('.logo, .brand, img[src*="logo"]');
                for (var i = 0; i < logoElements.length; i++) {
                    logoElements[i].style.display = 'none';
                }
            }

            // 函数：使地图全屏显示
            function makeMapFullscreen() {
                console.log('使地图全屏显示...');

                // 查找地图容器
                var mapContainers = [
                    '.map-container', '.map', '#map',
                    '.leaflet-container', '.mapContainer',
                    'div[class*="map"]', 'div[id*="map"]',
                    '.amap-container', '.bmap-container', '.tmap-container'
                ];

                var mapContainer = null;

                // 尝试查找地图容器
                for (var i = 0; i < mapContainers.length; i++) {
                    var containers = document.querySelectorAll(mapContainers[i]);
                    if (containers.length > 0) {
                        mapContainer = containers[0];
                        console.log('找到地图容器:', mapContainers[i]);
                        break;
                    }
                }

                // 如果找不到地图容器，尝试查找最大的容器
                if (!mapContainer) {
                    console.log('未找到地图容器，尝试查找最大的容器');
                    var allDivs = document.querySelectorAll('div');
                    var largestDiv = null;
                    var largestArea = 0;

                    for (var i = 0; i < allDivs.length; i++) {
                        var rect = allDivs[i].getBoundingClientRect();
                        var area = rect.width * rect.height;
                        if (area > largestArea) {
                            largestArea = area;
                            largestDiv = allDivs[i];
                        }
                    }

                    if (largestDiv) {
                        mapContainer = largestDiv;
                        console.log('使用最大的div作为地图容器');
                    }
                }

                // 如果找到地图容器，使其全屏显示
                if (mapContainer) {
                    console.log('设置地图容器为全屏');

                    // 保存原始样式
                    var originalStyle = {
                        position: mapContainer.style.position,
                        top: mapContainer.style.top,
                        left: mapContainer.style.left,
                        width: mapContainer.style.width,
                        height: mapContainer.style.height,
                        zIndex: mapContainer.style.zIndex
                    };

                    // 设置为全屏
                    mapContainer.style.position = 'fixed';
                    mapContainer.style.top = '0';
                    mapContainer.style.left = '0';
                    mapContainer.style.width = '100vw';
                    mapContainer.style.height = '100vh';
                    mapContainer.style.zIndex = '9999';

                    // 设置页面背景为黑色
                    document.body.style.backgroundColor = 'black';
                    document.body.style.margin = '0';
                    document.body.style.padding = '0';
                    document.body.style.overflow = 'hidden';

                    return true;
                } else {
                    console.log('未找到地图容器');
                    return false;
                }
            }

            // 主函数
            function main() {
                // 记录页面信息
                logPageInfo();

                // 切换到风流场视图
                switchToWindFlow();

                // 等待一段时间，让风流场加载
                setTimeout(function() {
                    // 隐藏所有UI元素
                    hideAllUIElements();

                    // 使地图全屏显示
                    makeMapFullscreen();

                    console.log('处理完成');
                }, 2000);
            }

            // 执行主函数
            main();

            // 设置定期检查，确保UI元素保持隐藏
            setInterval(function() {
                hideAllUIElements();
                makeMapFullscreen();
            }, 5000);
            """

            # 执行JavaScript代码
            self.web_view.page().runJavaScript(js_code, self.on_js_executed)
        else:
            logger.error("页面加载失败")
            self.status_label.setText("页面加载失败，请检查网络连接")

            # 尝试获取错误信息
            self.web_view.page().toHtml(self.debug_html_on_error)

    def debug_html(self, html):
        """调试用：记录页面HTML源码"""
        try:
            # 只记录前1000个字符，避免日志文件过大
            logger.debug(f"页面HTML源码片段: {html[:1000]}...")

            # 保存完整HTML到文件，方便调试
            with open("page_source.html", "w", encoding="utf-8") as f:
                f.write(html)
            logger.info("已保存完整HTML源码到 page_source.html")
        except Exception as e:
            logger.error(f"保存HTML源码失败: {e}")

    def debug_html_on_error(self, html):
        """页面加载失败时的HTML调试"""
        try:
            logger.debug(f"页面加载失败时的HTML源码片段: {html[:1000]}...")

            # 保存完整HTML到文件，方便调试
            with open("error_page_source.html", "w", encoding="utf-8") as f:
                f.write(html)
            logger.info("已保存错误页面的HTML源码到 error_page_source.html")

            # 分析可能的错误原因
            if "404" in html:
                logger.error("可能的错误原因: 页面返回404错误")
                self.status_label.setText("错误: 页面不存在 (404)")
            elif "403" in html:
                logger.error("可能的错误原因: 页面返回403错误")
                self.status_label.setText("错误: 访问被拒绝 (403)")
            elif "500" in html:
                logger.error("可能的错误原因: 页面返回500错误")
                self.status_label.setText("错误: 服务器内部错误 (500)")
            elif "无法访问此网站" in html or "ERR_CONNECTION" in html:
                logger.error("可能的错误原因: 网络连接问题")
                self.status_label.setText("错误: 无法连接到网站，请检查网络")
            elif len(html) < 100:
                logger.error("可能的错误原因: 页面内容为空或非常短")
                self.status_label.setText("错误: 页面内容为空")
            else:
                logger.error("未能确定具体错误原因")
                self.status_label.setText("错误: 页面加载失败，原因未知")
        except Exception as e:
            logger.error(f"分析错误页面时出错: {e}")
            logger.error(traceback.format_exc())

    def on_js_executed(self, result):
        """JavaScript代码执行完成后的处理"""
        try:
            if result:
                logger.info("JavaScript代码执行成功")

                # 如果结果是对象，记录详细信息
                if isinstance(result, dict):
                    logger.info("JavaScript返回结果:")
                    for key, value in result.items():
                        logger.info(f"  {key}: {value}")

                self.status_label.setText("Wind Flow Live Wallpaper is running")
                self.status_timer.start(3000)  # Hide status label after 3 seconds

                # 5秒后再次检查页面状态
                QTimer.singleShot(5000, self.check_page_status)
            else:
                logger.warning("JavaScript代码执行失败或返回空结果")
                self.status_label.setText("处理页面失败，请按F5刷新")

                # 尝试重新加载页面
                QTimer.singleShot(5000, self.refresh_page)
        except Exception as e:
            logger.error(f"处理JavaScript执行结果时出错: {e}")
            logger.error(traceback.format_exc())
            self.status_label.setText(f"处理JavaScript执行结果时出错: {e}")

    def check_page_status(self):
        """检查页面状态"""
        try:
            # 注入JavaScript代码，检查页面状态
            js_check = """
            // 检查页面状态
            function checkPageStatus() {
                // 检查是否有地图容器
                var mapContainer = document.querySelector('.mapContainer') ||
                                   document.querySelector('div[class*="map"]') ||
                                   document.querySelector('div[id*="map"]');

                // 检查是否有风流场相关元素
                var windElements = [];
                var elements = document.querySelectorAll('*');
                for (var i = 0; i < elements.length; i++) {
                    if (elements[i].textContent &&
                        (elements[i].textContent.includes('风流场') ||
                         elements[i].textContent.includes('风向') ||
                         elements[i].textContent.includes('风速'))) {
                        windElements.push({
                            tag: elements[i].tagName,
                            text: elements[i].textContent.trim(),
                            visible: elements[i].offsetParent !== null
                        });
                    }
                }

                var result = {
                    url: window.location.href,
                    title: document.title,
                    hasMapContainer: mapContainer !== null,
                    windElements: windElements.slice(0, 10)  // 只返回前10个元素
                };

                console.log('页面状态检查结果:', result);
                return result;
            }

            checkPageStatus();
            """

            self.web_view.page().runJavaScript(js_check, self.on_check_status)
        except Exception as e:
            logger.error(f"检查页面状态时出错: {e}")
            logger.error(traceback.format_exc())

    def on_check_status(self, result):
        """处理页面状态检查结果"""
        try:
            if result:
                logger.info("页面状态检查结果:")
                for key, value in result.items():
                    if key != 'windElements':
                        logger.info(f"  {key}: {value}")
                    else:
                        logger.info(f"  风流场相关元素数量: {len(value)}")
                        for i, elem in enumerate(value):
                            logger.info(f"    元素{i+1}: {elem['tag']} - {elem['text']} - 可见: {elem['visible']}")

                # Check if wind flow visualization loaded successfully
                if result.get('hasMapContainer', False):
                    logger.info("Map container detected, page loaded successfully")
                    self.status_label.setText("Wind Flow Live Wallpaper is running")
                    self.status_timer.start(3000)  # Hide status label after 3 seconds
                else:
                    logger.warning("No map container detected, loading may have failed")
                    self.status_label.setText("Wind flow map not detected, press F5 to refresh")
            else:
                logger.warning("页面状态检查返回空结果")
                self.status_label.setText("无法检查页面状态，请按F5刷新")
        except Exception as e:
            logger.error(f"处理页面状态检查结果时出错: {e}")
            logger.error(traceback.format_exc())

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

def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="中国气象网风流场实时动态壁纸")
    parser.add_argument("--verbose", action="store_true", help="启用详细日志")
    parser.add_argument("--url", default=WEATHER_URL, help=f"指定要加载的URL (默认: {WEATHER_URL})")
    parser.add_argument("--interval", type=int, default=UPDATE_INTERVAL, help=f"刷新间隔（秒）(默认: {UPDATE_INTERVAL})")
    parser.add_argument("--test", action="store_true", help="测试模式，不设置为桌面背景")
    return parser.parse_args()

def main():
    """主函数"""
    try:
        # 解析命令行参数
        args = parse_arguments()

        # 设置日志级别
        if args.verbose:
            logger.setLevel(logging.DEBUG)
            print("已启用详细日志模式")

        # 更新全局变量
        global WEATHER_URL, UPDATE_INTERVAL
        if args.url != WEATHER_URL:
            WEATHER_URL = args.url
            print(f"使用自定义URL: {WEATHER_URL}")

        if args.interval != UPDATE_INTERVAL:
            UPDATE_INTERVAL = args.interval
            print(f"使用自定义刷新间隔: {UPDATE_INTERVAL}秒")

        logger.info("="*50)
        logger.info("启动中国气象网风流场实时动态壁纸")
        logger.info("="*50)
        logger.info(f"URL: {WEATHER_URL}")
        logger.info(f"刷新间隔: {UPDATE_INTERVAL}秒")
        logger.info(f"测试模式: {'是' if args.test else '否'}")

        # 检查依赖项
        if not check_dependencies():
            print("依赖项检查失败，请安装必要的依赖项")
            input("按Enter键退出...")
            return 1

        # 测试网络连接
        try:
            logger.info(f"测试网络连接到 {WEATHER_URL}")
            test_response = requests.head(WEATHER_URL, timeout=10)
            logger.info(f"网络连接测试结果: 状态码 {test_response.status_code}")
            if test_response.status_code >= 400:
                logger.warning(f"网站返回错误状态码: {test_response.status_code}")
                print(f"警告: 网站返回错误状态码: {test_response.status_code}")
                response = input("是否继续? (y/n): ")
                if response.lower() != 'y':
                    return 1
        except Exception as e:
            logger.warning(f"网络连接测试失败: {e}")
            print(f"警告: 网络连接测试失败: {e}")
            response = input("是否继续? (y/n): ")
            if response.lower() != 'y':
                return 1

        # 创建应用程序
        app = QApplication(sys.argv)

        # 创建主窗口
        window = WindFlowLiveWallpaper()

        # 如果是测试模式，不设置为桌面背景
        if args.test:
            logger.info("测试模式: 不设置为桌面背景")
            window.setWindowFlags(Qt.Window)  # 使用普通窗口标志

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
