@echo off
echo 正在启动中国气象网实时风流场桌面壁纸程序...
echo 程序将在后台运行，您可以关闭此窗口。
echo 要停止程序，请在任务管理器中结束Python进程。
echo.
start /b pythonw src/wind_wallpaper_new.py
echo 程序已启动！
timeout /t 5
