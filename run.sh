#!/bin/bash

# PixeLab 실행 스크립트

echo "PixeLab - 픽셀아트 에디터"
echo "=========================="

# Python 버전 확인
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3가 설치되어 있지 않습니다."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1-2)
echo "✓ Python $PYTHON_VERSION 감지됨"

# 가상환경 확인 및 생성
if [ ! -d "venv" ]; then
    echo "📦 가상환경 생성 중..."
    python3 -m venv venv
fi

# 가상환경 활성화
echo "🔌 가상환경 활성화 중..."
source venv/bin/activate

# 의존성 설치
echo "📚 의존성 확인 중..."
pip install -q -r requirements.txt

# 애플리케이션 실행
echo "🚀 PixeLab 시작..."
echo ""
python3 main.py

# 가상환경 비활성화
deactivate
