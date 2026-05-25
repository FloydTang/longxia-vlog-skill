#!/bin/bash
# 龙虾简单 Vlog 一键渲染脚本
# 用法: bash render-vlog.sh <项目路径>
# 前提：assets/ 下已有照片、配音、BGM

set -e

PROJECT_DIR="${1:-.}"
cd "$PROJECT_DIR"

echo "🦞 龙虾 Vlog 渲染脚本"
echo "======================"
echo "项目目录: $(pwd)"
echo ""

# Step 1: 校验
echo "📐 校验模板..."
npx hyperframes validate 2>&1 | tail -20
echo ""

# Step 2: 渲染
echo "🎬 开始渲染..."
npx hyperframes render --fps 10 2>&1

# Step 3: 输出结果
RENDER_DIR="renders"
if [ -d "$RENDER_DIR" ]; then
  LATEST=$(ls -t "$RENDER_DIR"/*.mp4 2>/dev/null | head -1)
  if [ -n "$LATEST" ]; then
    echo ""
    echo "✅ 渲染完成！"
    ls -lh "$LATEST"
    echo "📁 $LATEST"
  fi
fi
