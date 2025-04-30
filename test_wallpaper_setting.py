"""
测试壁纸设置功能
"""
import os
import ctypes
import sys
from PIL import Image

def test_set_wallpaper():
    """测试设置壁纸的不同方法"""
    print("="*50)
    print("测试壁纸设置功能")
    print("="*50)
    
    # 创建测试图像
    test_img = Image.new("RGB", (1920, 1080), "blue")
    test_path = os.path.abspath("test_wallpaper.bmp")
    test_img.save(test_path)
    print(f"创建测试图像: {test_path}")
    
    # 方法1: 使用Windows API (SPI_SETDESKWALLPAPER = 20)
    print("\n方法1: 使用SystemParametersInfoW")
    try:
        result = ctypes.windll.user32.SystemParametersInfoW(20, 0, test_path, 3)
        print(f"结果: {result}")
        if result:
            print("方法1成功!")
        else:
            print("方法1失败")
    except Exception as e:
        print(f"方法1异常: {e}")
    
    input("检查壁纸是否已更改，然后按Enter继续...")
    
    # 方法2: 使用明确的常量
    print("\n方法2: 使用明确常量的SystemParametersInfoW")
    try:
        SPI_SETDESKWALLPAPER = 0x0014
        SPIF_UPDATEINIFILE = 0x01
        SPIF_SENDCHANGE = 0x02
        result = ctypes.windll.user32.SystemParametersInfoW(
            SPI_SETDESKWALLPAPER, 
            0, 
            test_path, 
            SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
        )
        print(f"结果: {result}")
        if result:
            print("方法2成功!")
        else:
            print("方法2失败")
    except Exception as e:
        print(f"方法2异常: {e}")
    
    input("检查壁纸是否已更改，然后按Enter继续...")
    
    # 方法3: 使用注册表
    print("\n方法3: 使用注册表设置壁纸")
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
        winreg.SetValueEx(registry_key, "Wallpaper", 0, winreg.REG_SZ, test_path)
        winreg.CloseKey(registry_key)
        
        # 通知Windows更新设置
        ctypes.windll.user32.SendMessageW(0xFFFF, 0x0112, 0xF, 0)
        ctypes.windll.user32.SendMessageW(0xFFFF, 0x0112, 0xF, 0)
        
        print("方法3成功!")
    except Exception as e:
        print(f"方法3异常: {e}")
    
    input("检查壁纸是否已更改，然后按Enter继续...")
    
    # 清理
    try:
        os.remove(test_path)
        print(f"已删除测试图像: {test_path}")
    except:
        print(f"无法删除测试图像: {test_path}")
    
    print("\n测试完成!")

if __name__ == "__main__":
    # 检查是否以管理员身份运行
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    
    if not is_admin:
        print("警告: 程序未以管理员身份运行，可能无法设置壁纸")
        print("建议以管理员身份运行此程序")
        response = input("是否继续? (y/n): ")
        if response.lower() != 'y':
            sys.exit(0)
    
    test_set_wallpaper()
