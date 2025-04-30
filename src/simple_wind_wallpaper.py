"""
简化版风流场壁纸程序，用于测试基本功能
"""
import os
import sys
import logging
import traceback
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import ctypes

# 配置
WALLPAPER_PATH = "wind_wallpaper.png"  # 壁纸保存路径
LOG_FILE = "simple_wind_wallpaper.log"  # 日志文件

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

def create_simple_wallpaper():
    """创建一个简单的壁纸"""
    global WALLPAPER_PATH
    try:
        logger.info("创建简单壁纸")
        print("创建简单壁纸...")
        
        # 创建壁纸画布（1920x1080，适应常见屏幕分辨率）
        wallpaper = Image.new("RGB", (1920, 1080), "lightblue")
        
        # 添加文本
        draw = ImageDraw.Draw(wallpaper)
        
        # 使用默认字体
        font = ImageFont.load_default()
        
        # 添加时间戳
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        draw.text((20, 20), f"更新时间: {timestamp}", fill="black", font=font)
        
        # 添加说明文本
        draw.text((20, 50), "这是一个测试壁纸", fill="black", font=font)
        
        # 保存壁纸 (使用BMP格式，Windows壁纸更兼容)
        bmp_path = WALLPAPER_PATH.replace('.png', '.bmp')
        wallpaper.save(bmp_path, "BMP")
        print(f"壁纸已保存为BMP格式: {bmp_path}")
        
        # 更新全局变量，使用BMP路径
        WALLPAPER_PATH = bmp_path
        
        return True
    except Exception as e:
        logger.error(f"创建壁纸失败: {e}")
        logger.error(traceback.format_exc())
        print(f"创建壁纸失败: {e}")
        return False

def set_wallpaper():
    """设置Windows桌面壁纸"""
    global WALLPAPER_PATH
    try:
        logger.info("设置壁纸")
        print("设置壁纸...")
        
        # 检查壁纸文件是否存在
        abs_path = os.path.abspath(WALLPAPER_PATH)
        if not os.path.exists(abs_path):
            logger.error(f"壁纸文件不存在: {abs_path}")
            print(f"错误: 壁纸文件不存在: {abs_path}")
            return False
        
        # 方法1: 使用Windows API (SPI_SETDESKWALLPAPER = 20)
        print("尝试方法1: 使用SystemParametersInfoW...")
        result = ctypes.windll.user32.SystemParametersInfoW(20, 0, abs_path, 3)
        if result:
            print("方法1成功: 使用SystemParametersInfoW设置壁纸")
            return True
        else:
            print(f"方法1失败: SystemParametersInfoW返回{result}")
        
        # 方法2: 尝试使用另一种方式调用API
        print("尝试方法2: 使用明确常量的SystemParametersInfoW...")
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
        
        print("所有方法都失败了")
        return False
    except Exception as e:
        logger.error(f"设置壁纸失败: {e}")
        logger.error(traceback.format_exc())
        print(f"设置壁纸失败: {e}")
        return False

def main():
    """主函数"""
    try:
        logger.info("="*50)
        logger.info("启动简化版风流场壁纸程序")
        logger.info("="*50)
        
        print("="*50)
        print("启动简化版风流场壁纸程序")
        print("="*50)
        print(f"日志文件: {os.path.abspath(LOG_FILE)}")
        print("-"*50)
        
        # 创建壁纸
        if create_simple_wallpaper():
            print("壁纸创建成功")
            
            # 设置壁纸
            if set_wallpaper():
                print("壁纸设置成功")
            else:
                print("壁纸设置失败")
        else:
            print("壁纸创建失败")
        
        print("\n程序执行完成")
        input("按Enter键退出...")
    except Exception as e:
        logger.error(f"程序异常: {e}")
        logger.error(traceback.format_exc())
        print(f"程序异常: {e}")
        input("按Enter键退出...")

if __name__ == "__main__":
    main()
