# PixeLab - 픽셀아트 에디터

프로페셔널한 픽셀아트/도트아트 제작을 위한 Python 기반 에디터입니다.

## 주요 기능

### 핵심 기능
- **고해상도 격자 캔버스**: 빠른 렌더링과 정밀한 픽셀 편집
- **무제한 줌인/줌아웃**: 마우스 휠 또는 줌 슬라이더로 자유로운 확대/축소
- **다양한 그리기 도구**:
  - 연필 (Pencil): 단일 픽셀 그리기
  - 브러시 (Brush): 다양한 크기의 브러시
  - 지우개 (Eraser): 픽셀 지우기
  - 채우기 (Fill): 영역 채우기
  - 선 도구 (Line): 직선 그리기
  - 사각형 도구 (Rectangle): 사각형 그리기
  - 원 도구 (Circle): 원형 그리기
  - 스포이드 (Eyedropper): 색상 추출

### 색상 시스템
- **24-bit 트루컬러 지원**: RGB 색상 선택기
- **색상 팔레트**: 자주 사용하는 색상 저장 및 관리
- **투명도 지원**: 알파 채널 완벽 지원

### 파일 형식
- **.plb (PixeLab 프로젝트 파일)**: 
  - 레이어, 팔레트, 히스토리 등 모든 프로젝트 정보 저장
  - JSON 기반 텍스트 포맷으로 버전 관리 가능
- **PNG 내보내기**: 투명도를 포함한 래스터 이미지
- **SVG 내보내기**: 벡터 형식으로 확대해도 깨끗한 이미지

### 추가 기능
- **실행 취소/다시 실행**: 무제한 히스토리
- **레이어 시스템**: 다중 레이어 지원 (향후 버전)
- **격자 표시/숨기기**: 토글 가능한 그리드
- **패닝 (Pan)**: Space + 드래그로 캔버스 이동

## 설치 및 실행

### 필수 요구사항

#### Python
- Python 3.8 이상

#### 외부 라이브러리
```bash
pip install Pillow tkinter
```

**참고**: `tkinter`는 대부분의 Python 설치에 포함되어 있습니다. 
만약 없다면:
- **Ubuntu/Debian**: `sudo apt-get install python3-tk`
- **Fedora**: `sudo dnf install python3-tkinter`
- **macOS**: Homebrew Python을 사용하는 경우 자동 포함
- **Windows**: Python 설치 시 자동 포함

### 실행 방법

#### 직접 실행
```bash
python main.py
```

#### 스크립트 사용 (Linux/macOS)
```bash
chmod +x run.sh
./run.sh
```

## 사용 방법

### 기본 조작
1. **그리기**: 좌측 도구 패널에서 도구 선택 후 캔버스에 드래그
2. **색상 선택**: 우측 색상 팔레트에서 색상 클릭 또는 "색상 선택" 버튼
3. **줌**: 마우스 휠 또는 상단 줌 슬라이더
4. **패닝**: Space 키를 누른 채로 드래그

### 파일 작업
- **새 파일**: File → New (Ctrl+N)
- **열기**: File → Open (Ctrl+O) - .plb 파일
- **저장**: File → Save (Ctrl+S) - .plb 파일
- **다른 이름으로 저장**: File → Save As (Ctrl+Shift+S)
- **PNG 내보내기**: File → Export → PNG
- **SVG 내보내기**: File → Export → SVG

### 단축키
- `Ctrl+N`: 새 파일
- `Ctrl+O`: 열기
- `Ctrl+S`: 저장
- `Ctrl+Z`: 실행 취소
- `Ctrl+Y`: 다시 실행
- `G`: 격자 토글
- `Space + 드래그`: 캔버스 패닝

## 프로젝트 구조

```
pixelab/
├── main.py                 # 애플리케이션 진입점
├── src/
│   ├── __init__.py
│   ├── app.py             # 메인 애플리케이션 클래스
│   ├── canvas.py          # 픽셀 캔버스 구현
│   ├── tools.py           # 그리기 도구 클래스들
│   ├── palette.py         # 색상 팔레트 관리
│   ├── file_handler.py    # 파일 입출력 (PLB, PNG, SVG)
│   └── ui/
│       ├── __init__.py
│       ├── toolbar.py     # 도구 모음
│       ├── menubar.py     # 메뉴 바
│       └── colorpicker.py # 색상 선택 위젯
├── docs/
│   ├── USER_GUIDE.md      # 사용자 가이드
│   ├── DEVELOPER.md       # 개발자 문서
│   └── FILE_FORMAT.md     # .plb 파일 형식 명세
├── requirements.txt       # Python 의존성
├── run.sh                # 실행 스크립트
├── .gitignore
└── README.md
```

## .plb 파일 형식

PixeLab 전용 프로젝트 파일 형식으로, JSON 기반의 텍스트 포맷입니다.

```json
{
  "version": "1.0",
  "width": 64,
  "height": 64,
  "palette": ["#000000", "#FFFFFF", ...],
  "pixels": [[r, g, b, a], ...],
  "metadata": {
    "created": "2026-02-02T00:53:34+09:00",
    "modified": "2026-02-02T00:53:34+09:00"
  }
}
```

자세한 내용은 [FILE_FORMAT.md](docs/FILE_FORMAT.md)를 참조하세요.

## 라이선스

MIT License

## 기여

이슈 및 풀 리퀘스트를 환영합니다!

## 작성자

rheehose

## 버전 히스토리

- **v1.0.0** (2026-02-02): 초기 릴리스
  - 기본 그리기 도구
  - PLB, PNG, SVG 지원
  - 줌/패닝 기능
