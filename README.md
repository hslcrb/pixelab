# 🎨 PixeLab - Ultimate Vector-Pixel Hybrid Editor

[![Version](https://img.shields.io/badge/version-v0.0.x-blue.svg)](https://github.com/hslcrb/pixelab/releases)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-yellow.svg)](https://www.python.org/)

**PixeLab** is a revolutionary hybrid graphics editor that merges the **precision of Vector** with the **aesthetics of Pixel Art**. Unlike traditional pixel editors, every dot in PixeLab is a smart `VectorObject` that can be selected, moved, and styled even after drawing.

[English](#english) | [한국어](#한국어)

---

<a name="한국어"></a>
## 🚀 주요 기능 (Key Features)

### 1. ⚡ 극한의 성능 (Extreme Performance)
- **PIL ImageDraw 가속**: 하드웨어 가속급 고성능 렌더링 엔진 탑재.
- **지능형 레이어 캐싱**: 변경된 부분만 다시 그리는 레이어 캐싱 시스템으로 수천 명의 객체 위에서도 60FPS 실시간 편집 가능.
- **비동기 렌더링**: 입력과 렌더링을 분리하여 렉(Lag) 없는 부드러운 반응성 제공.

### 2. 🧬 벡터-픽셀 하이브리드 시스템
- **모든 것이 객체**: 그린 모든 픽셀은 독립적인 벡터 데이터입니다. 언제든 위치와 색상을 바꿀 수 있습니다.
- **스마트 브러시**: 고밀도 브러시 스트로크도 단 하나의 `VectorPath` 객체로 관리하여 데이터 효율을 극대화합니다.
- **무손실 확대/축소**: 데이터의 손실 없이 극한까지 확대하고 정밀하게 작업하세요.

### 3. 🖼️ 고급 이미지 트레이싱
- **PNG/JPG 가져오기**: 일반 비트맵 이미지를 가져오면 인공지능급 트레이싱 로직이 수만 개의 픽셀 객체로 자동 변환합니다.
- **스레딩 기반 로딩**: 큰 이미지 변환 시에도 UI가 멈추지 않으며 실시간 상태를 확인할 수 있습니다.

### 4. 🌐 완벽한 다국어 및 UI
- **실시간 한/영 전환**: `F1` 키로 모든 레이블, 메뉴, 툴팁을 즉시 전환합니다.
- **커스텀 팔레트**: 당신만의 색상 조합을 저장하고 프로젝트 파일에 포함할 수 있습니다.

---

## 📄 .plb 파일 형식 (Open Specification)

PixeLab은 투명한 데이터 공유를 위해 **.plb** 형식을 공개 표준으로 지향합니다.
JSON 기반으로 설계되어 다른 서비스나 엔진(Unity, Godot 등)에서 쉽게 파싱할 수 있습니다.

**[상세 명세서 보기 (PLB_SPEC.md)](./PLB_SPEC.md)**

---

## 🛠 단축키 (Quick Shortcuts)

| 키(Key) | 기능 (Function) |
| :--- | :--- |
| `V`, `M` | **선택/이동** (Select) |
| `P`, `B` | **연필/브러시** (Pencil/Brush) |
| `L`, `R`, `C` | **직선/사각형/원** (Shapes) |
| `Ctrl + G/U` | **그룹화 / 그룹해제** |
| `F1` | **한/영 언어 전환** |
| `G` | **격자 토글** |
| `Ctrl + Scroll` | **확대 / 축소** |

---

<a name="english"></a>
## 💻 Getting Started

```bash
# Clone the repository
git clone https://github.com/hslcrb/pixelab.git
cd pixelab

# Run the application
./run.sh
```

---

## 🏗 Project Architecture

- **`pixelab_full.py`**: The ultimate entry point.
- **`src/vector_canvas.py`**: The high-performance rendering heart.
- **`src/object_manager.py`**: State management & layer caching.
- **`src/vector_objects.py`**: Vector object definitions & PIL acceleration.
- **`src/i18n.py`**: Real-time translation engine.

---

## 🤝 Contribution & License

We love contributions! Feel free to open issues or pull requests.
Released under the **MIT License**.

---
### 🎨 PixeLab - *Redefining Pixel Art with Vector Precision*
Author: **rheehose** | [GitHub](https://github.com/hslcrb)
