#!/bin/bash

# PixeLab v2.1 실행 스크립트
# 가상환경 자동 체크 및 실행

set -e  # 에러 발생 시 중단

# 색상 코드
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     PixeLab v2.1 - Vector Edition         ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════╝${NC}"
echo ""

# Python 버전 확인
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3가 설치되어 있지 않습니다.${NC}"
    echo "설치: sudo apt-get install python3"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
echo -e "${GREEN}✓${NC} Python $PYTHON_VERSION 감지됨"

# 가상환경 확인 및 생성
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}📦 가상환경이 없습니다. 생성 중...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✓${NC} 가상환경 생성 완료"
else
    echo -e "${GREEN}✓${NC} 가상환경 발견됨"
fi

# 가상환경 활성화
echo -e "${BLUE}🔌 가상환경 활성화 중...${NC}"
source venv/bin/activate

# 의존성 확인 (requirements.txt와 비교)
NEED_INSTALL=false

# Pillow 설치 확인
if ! python3 -c "import PIL" 2>/dev/null; then
    NEED_INSTALL=true
fi

if [ "$NEED_INSTALL" = true ]; then
    echo -e "${YELLOW}📚 의존성 설치 중...${NC}"
    pip install -q --upgrade pip
    pip install -q -r requirements.txt
    echo -e "${GREEN}✓${NC} 의존성 설치 완료"
else
    echo -e "${GREEN}✓${NC} 의존성 확인 완료"
fi

# 실행할 파일 선택
APP_FILE="pixelab_v2.py"

# 파일 존재 확인
if [ ! -f "$APP_FILE" ]; then
    echo -e "${YELLOW}⚠️  $APP_FILE 없음, main.py 실행${NC}"
    APP_FILE="main.py"
fi

# 애플리케이션 실행
echo ""
echo -e "${BLUE}╔════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║          🚀 PixeLab v2.1 시작!             ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}단축키:${NC}"
echo "  F1     - 한/영 전환"
echo "  V, M   - Mouse/Select"
echo "  Ctrl+I - 이미지 가져오기"
echo "  Ctrl+G - 그룹 만들기"
echo "  Ctrl+U - 그룹 해제"
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

python3 "$APP_FILE"

# 종료 코드 체크
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✓ PixeLab이 정상 종료되었습니다.${NC}"
else
    echo ""
    echo -e "${RED}❌ PixeLab이 오류로 종료되었습니다 (코드: $EXIT_CODE)${NC}"
fi

# 가상환경 비활성화
deactivate

exit $EXIT_CODE

