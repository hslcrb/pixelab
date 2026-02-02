# 🎨 PixeLab - Vector-Pixel Hybrid Editor (v0.0.x)

**PixeLab**은 벡터의 편집성과 픽셀의 미학을 결합한 혁신적인 하이브리드 그래픽 에디터입니다. 모든 픽셀을 독립적인 벡터 객체로 관리하여, 그린 후에도 언제든지 선택, 이동, 색상 변경 및 그룹화가 가능합니다.

---

## 🚀 주요 기능

### 1. 벡터-픽셀 하이브리드 시스템
- **픽셀 = 객체**: 그린 모든 픽셀이 독립적인 `VectorPixel` 객체로 관리됩니다.
- **도형 자동 그룹화**: 선, 사각형, 원 등의 도형은 생성 즉시 하나의 그룹으로 관리되어 편집이 용이합니다.
- **무손실 편집**: 객체를 이동하거나 크기를 조절해도 데이터 손실이 없습니다.

### 2. 고급 이미지 처리 (신기능)
- **자동 이미지 트레이싱**: PNG, JPG 등 비트맵 이미지를 가져오면 자동으로 수천 개의 픽셀 객체로 변환합니다.
- **이미지 자동 그룹화**: 가져온 이미지는 하나의 그룹으로 관리되어 전체 이동 및 편집이 가능합니다.
- **스레딩 기반 로딩**: 큰 이미지를 가져올 때도 UI가 멈추지 않으며 실시간 프로그레스 바를 제공합니다.

### 3. 직관적인 UI/UX
- **다국어 지원**: `F1` 키로 한국어와 영어 UI를 즉시 전환할 수 있습니다.
- **스마트 팔레트**: 다양한 기본 컬러와 커스텀 팔레트 저장 기능을 지원합니다.
- **강력한 확대/축소**: `Ctrl` + `+/-` 또는 마우스 휠을 통해 확대가 가능하며, **픽셀 스케일** 슬라이더로 기본 밀도를 조절할 수 있습니다.
- **격자 시스템**: 정밀한 픽셀 작업을 위한 격자(Grid) 토글 기능을 지원합니다.
- **레이어 시스템**: 다중 레이어를 통해 복잡한 작업을 효율적으로 관리할 수 있습니다. 각 레이어는 가시성 및 잠금 기능을 지원합니다.
- **스크롤 및 네비게이션**: 캔버스 상하좌우 스크롤바와 방향키를 이용한 자유로운 화면 이동을 지원합니다.
- **도움말 시스템**: 단축키와 사용법을 확인할 수 있는 인앱 도움말 창을 제공합니다.

### 4. 강력한 파일 지원
- **.plb (PixeLab Project)**: 모든 객체 정보와 그룹 구조를 저장하는 JSON 기반 자체 형식입니다.
- **PNG 내보내기**: 고해상도 출력을 위한 스케일링(1x~16x) 기능을 지원합니다.
- **SVG 내보내기**: 진정한 벡터 포맷인 SVG로 결과물을 내보낼 수 있습니다.

---

## 🛠 단축키 가이드

### 도구 선택
- `V`, `M`: **선택/이동** (Select/Mouse)
- `P`: **연필** (Pencil)
- `B`: **브러시** (Brush)
- `E`: **지우개** (Eraser)
- `L`: **직선** (Line)
- `R`: **사각형** (Rectangle)
- `C`: **원** (Circle)
- `F`: **채우기** (Fill)
- `I`: **스포이드** (Eyedropper)

### 편집 및 제어
- `Ctrl + G`: **그룹 만들기**
- `Ctrl + U`: **그룹 해제**
- `Delete`: **선택 객체 삭제**
- `Ctrl + I`: **이미지 가져오기**
- `Ctrl + N/O/S`: **새 문서/열기/저장**
- `G`: **격자 토글**
- `F1`: **한/영 UI 전환**
- `Ctrl + +/-`: **확대/축소**
- `방향키 (↑↓←→)`: **화면 이동 (Panning)**
- `Shift + Mouse Wheel`: **좌우 스크롤**

---

## 💻 실행 및 설치

### 로컬 실행
```bash
# 가상환경 설정 및 실행 (Linux/macOS)
cd pixelab
./run.sh
```

### 도커(Docker) 실행
```bash
# GitHub Container Registry에서 이미지 가져오기
docker pull ghcr.io/hslcrb/pixelab:latest

# 실행 (X11 디스플레이 설정 필요)
docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix ghcr.io/hslcrb/pixelab:latest
```

### 단일 실행 파일
GitHub의 **Releases** 섹션에서 Windows, Linux, macOS용 독립 실행 파일을 다운로드할 수 있습니다. 별도의 파이썬 설치 없이 바로 사용 가능합니다.

---

## 🏗 프로젝트 구조

```text
pixelab/
├── pixelab_full.py        # 메인 어플리케이션 진입점
├── Dockerfile             # 도커 빌드 설정
├── .github/workflows/     # CI/CD 자동화 (릴리즈 및 패키지 빌드)
├── src/                   # 소스 코드 모듈
│   ├── vector_canvas.py   # 벡터 렌더링 엔진
│   ├── vector_objects.py  # 객체 모델 (Pixel, Group, Rect 등)
│   ├── vector_tools.py    # 도구 로직
│   ├── object_manager.py  # 객체 관리 및 직렬화
│   ├── i18n.py            # 다국어 번역 엔진
│   ├── palette.py         # 컬러 관리 및 팔레트
│   └── ui/                # UI 컴포넌트 (Toolbar, ColorPicker 등)
└── docs/                  # 추가 리소스 및 로그
```

---

## 📄 .plb 파일 형식 명세

`.plb` 파일은 JSON 형식을 따르며 다음과 같은 구조로 객체를 저장합니다:

```json
{
  "width": 32,
  "height": 32,
  "objects": [
    {
      "type": "pixel",
      "x": 10, "y": 10,
      "color": [255, 0, 0, 255]
    },
    {
      "type": "group",
      "name": "My Group",
      "objects": [ ... ]
    }
  ],
  "palette": ["#000000", "#ffffff", ...]
}
```

---

## 🤝 기여 방법 및 라이선스

1. 본 저장소를 Fork 합니다.
2. 새로운 브랜치를 생성합니다 (`git checkout -b feature/amazing-feature`).
3. 변경 사항을 Commit 합니다 (`git commit -m 'Add some amazing feature'`).
4. 브랜치에 Push 합니다 (`git push origin feature/amazing-feature`).
5. Pull Request를 생성합니다.

**License**: MIT License - 상세 내용은 파일 내 기재되어 있습니다.

---

## 🎨 PixeLab - *Where Vector meets Pixel*
**Version Strategy**: `v0.0.(TotalCommits // 10)` - Increments every 10 commits.  
작성자: rheehose | 2026-02-02
