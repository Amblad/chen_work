#!/bin/bash
# 在 MacBook 上打包考勤表提取工具
# 用法: chmod +x build_mac.sh && ./build_mac.sh

set -e

cd "$(dirname "$0")"

echo "==> 检查 Python..."
if ! command -v python3 &>/dev/null; then
  echo "请先安装 Python 3: https://www.python.org/downloads/macos/"
  exit 1
fi

python3 --version

echo "==> 安装依赖..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 -m pip install pyinstaller

echo "==> 开始打包..."
python3 -m PyInstaller --noconfirm --clean AttendanceExtractor.spec

APP_PATH="dist/考勤表数据提取.app"

if [ -d "$APP_PATH" ]; then
  echo ""
  echo "打包成功!"
  echo "应用位置: $(pwd)/$APP_PATH"
  echo ""
  echo "使用方法:"
  echo "  1. 双击 dist/考勤表数据提取.app 运行"
  echo "  2. 若提示无法打开，在终端执行:"
  echo "     xattr -cr \"$APP_PATH\""
  echo "  3. 可将 .app 拖到「应用程序」文件夹"
  echo ""
  echo "分发给他人: 将 dist/考勤表数据提取.app 压缩成 zip 发送即可"
else
  echo "打包失败，请检查上方错误信息"
  exit 1
fi
