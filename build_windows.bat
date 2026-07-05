@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ==> 检查 Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo 请先安装 Python 3: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ==> 安装依赖...
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

echo ==> 开始打包 Windows 版...
pyinstaller --noconfirm --clean ^
  --windowed ^
  --name "考勤表数据提取" ^
  --collect-all openpyxl ^
  extract_attendance_gui.py

if exist "dist\考勤表数据提取\考勤表数据提取.exe" (
    echo.
    echo 打包成功!
    echo 程序位置: %cd%\dist\考勤表数据提取\考勤表数据提取.exe
    echo 可将整个 dist\考勤表数据提取 文件夹压缩后发给 Windows 用户
) else (
    echo 打包失败，请检查上方错误信息
)

pause
