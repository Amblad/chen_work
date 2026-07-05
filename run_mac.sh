#!/bin/bash
# Mac 用户没有 .app 时，用源码直接运行（需已安装 Python 3）
set -e
cd "$(dirname "$0")"

echo "==> 检查 Python..."
python3 --version

echo "==> 安装依赖..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

echo "==> 启动程序..."
python3 extract_attendance_gui.py
