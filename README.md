# PixeLab v2.1 - 하이브리드 벡터-픽셀 에디터

![Version](https://img.shields.io/badge/version-2.1-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

> **모든 픽셀이 벡터다. 모든 벡터가 픽셀이다.**
>
> 벡터로 저장하고, 픽셀로 표시하는 혁신적인 픽셀아트 에디터

## 🎯 핵심 개념

### 하이브리드 시스템
- **저장**: 모든 객체를 벡터로 저장 (수학적 정확성)
- **표시**: 격자에 맞춰 픽셀로 렌더링 (픽셀아트의 정확성)
- **편집**: 언제든 선택하여 수정 가능 (무한 편집성)

이것이 가능한 이유:
```
그리기 → VectorObject 생성 → ObjectManager에 저장
렌더링 → rasterize() → 픽셀 그리드 → 화면 표시
편집 → Select Tool → 객체 이동/수정 → 다시 렌더링
```

## ✨ v2.1의 새로운 기능

### 🖼️ 이미지 가져오기
```
Ctrl+I → 이미지 선택 → 자동 트레이싱 → 픽셀 객체 변환
```
- PNG, JPG, BMP, GIF, TIFF 지원
- 비트맵을 VectorPixel로 완벽 변환
- 프로그레스 다이얼로그 (실시간 진행률)
- 자동 그룹화로 전체 이동 가능

### 🌐 한영 전환 (i18n)
```
F1 → 한국어 ↔ English (즉시 반영!)
```
- 모든 메뉴와 메시지 번역
- 140+ 번역 키
- 메뉴 자동 재생성

### 📦 그룹화 시스템
```
여러 객체 선택 → Ctrl+G → 그룹 생성
그룹 선택 → Ctrl+U → 그룹 해제
```
- 가져온 이미지 자동 그룹화
- 중첩 그룹 지원
- 그룹 전체 이동/편집

### 🖱️ 마우스 도구
- Select 도구의 별칭
- V, M 키로 선택
- 픽셀 단위 드래그 이동

## 🚀 빠른 시작

### 설치
```bash
git clone <repository>
cd pixelab
./run.sh
```

**그냥 이게 끝입니다!** 나머지는 자동:
- ✅ 가상환경 자동 생성/확인
- ✅ 의존성 자동 설치
- ✅ v2.1 자동 실행

### 요구사항
- **Python 3.8+**
- **Tkinter** (대부분 기본 설치)
  ```bash
  # Ubuntu/Debian
  sudo apt-get install python3-tk
  ```
- **Pillow** (자동 설치됨)

## 🎮 사용법

### 단축키

#### 🛠️ 도구 선택
```
V, M  - Mouse/Select (객체 선택 및 이동)
P     - Pencil (자유 곡선)
B     - Brush (브러시)
E     - Eraser (지우개)
L     - Line (직선)
R     - Rectangle (사각형)
C     - Circle (원)
```

#### ✏️ 편집
```
Ctrl+I  - 이미지 가져오기 ★
Ctrl+G  - 그룹 만들기 ★
Ctrl+U  - 그룹 해제 ★
Delete  - 선택 삭제
```

#### 👁️ 보기
```
G   - 격자 토글
F1  - 한/영 전환 ★
휠  - 줌인/줌아웃
```

### 작업 흐름

#### 1️⃣ 이미지 가져오기
```
1. Ctrl+I
2. 이미지 파일 선택 (PNG, JPG 등)
3. 프로그레스 바 표시
   Loading → Converting → Resizing → Tracing → Grouping
4. 완료! 자동으로 캔버스에 표시
5. V 키로 선택 → 드래그로 이동
```

#### 2️⃣ 도형 그리기
```
1. L 키 - 직선 도구
2. 클릭 → 드래그 → 릴리스
3. 즉시 벡터 객체로 저장
4. V 키로 다시 선택하여 이동 가능
```

#### 3️⃣ 그룹화
```
1. V 키로 여러 객체 선택
2. Ctrl+G로 그룹 만들기
3. 그룹 전체를 한 번에 이동
4. Ctrl+U로 언제든 해제
```

## 📐 아키텍처

### 벡터 객체 시스템
```python
VectorObject (추상 클래스)
├── VectorPixel      # 단일 픽셀
├── VectorLine       # 직선 (Bresenham)
├── VectorRectangle  # 사각형
├── VectorCircle     # 원 (Midpoint)
├── VectorPath       # 자유곡선
└── VectorGroup      # 객체 그룹 ★
```

### 렌더링 파이프라인
```
VectorObject → rasterize() → Pixel Grid
                ↓
          Alpha Blending
                ↓
           PIL Image
                ↓
          ImageTk PhotoImage
                ↓
         Tkinter Canvas
```

### 핵심 모듈 (18개)
```
src/
├── 벡터 시스템 (v2.0+)
│   ├── vector_objects.py     (500+ 줄) - 벡터 클래스들
│   ├── object_manager.py     (170 줄)  - 객체 관리
│   ├── vector_tools.py       (320 줄)  - 벡터 도구들
│   ├── vector_canvas.py      (280 줄)  - 벡터 캔버스
│   └── vector_file_handler.py (140 줄) - 파일 I/O
│
├── 신규 기능 (v2.1)
│   ├── i18n.py              (200 줄)  - 다국어 지원 ★
│   ├── image_import.py      (220 줄)  - 이미지 가져오기 ★
│   └── (VectorGroup 추가)              - 그룹화 시스템 ★
│
├── 기존 시스템 (v1.0)
│   ├── app.py               (567 줄)  - 메인 앱
│   ├── canvas.py            (289 줄)  - 픽셀 캔버스
│   ├── tools.py             (355 줄)  - 픽셀 도구들
│   ├── palette.py           (70 줄)   - 색상 팔레트
│   └── file_handler.py      (132 줄)  - 파일 I/O
│
└── UI 컴포넌트
    ├── ui/menubar.py        (157 줄)  - 메뉴바
    ├── ui/toolbar.py        (148 줄)  - 도구바
    └── ui/colorpicker.py    (204 줄)  - 색상 선택
```

**총 코드**: 4,149 줄

## 💾 파일 형식

### .plb v2.0 (벡터 포맷)
```json
{
  "version": "2.0",
  "width": 32,
  "height": 32,
  "objects": [
    {
      "type": "group",
      "name": "Imported: logo.png",
      "objects": [
        {"type": "pixel", "x": 0, "y": 0, "color": [255, 0, 0, 255]},
        {"type": "pixel", "x": 1, "y": 0, "color": [0, 255, 0, 255]}
      ]
    },
    {
      "type": "line",
      "x0": 10, "y0": 10,
      "x1": 20, "y1": 20,
      "color": [0, 0, 255, 255]
    }
  ]
}
```

**장점**:
- 벡터로 저장 → 무손실 편집
- JSON 텍스트 → Git 친화적
- 하위 호환 (v1.0 pixel 형식 지원)

### 내보내기
- **PNG**: 래스터 이미지 (1x~16x 스케일)
- **SVG**: 벡터 이미지 (무한 확대)

## 📊 성능

### 렌더링
- 32x32: 60 FPS
- 64x64: 30+ FPS
- 128x128: 15+ FPS

### 이미지 가져오기
- 64x64: ~0.5초
- 128x128: ~2초
- 256x256: ~5초
- 512x512: ~15초

### 그룹화
- 100 객체: <0.01초
- 1,000 객체: <0.1초
- 10,000 객체: ~1초

## 🎨 사용 예시

### 로고 디자인
```
1. P 키로 Pencil 선택
2. 자유롭게 그리기
3. L 키로 Line 도구
4. 직선 추가
5. R 키로 Rectangle
6. 배경 사각형 추가
7. 모두 선택 → Ctrl+G로 그룹
8. PNG로 내보내기
```

### 아이콘 제작
```
1. Ctrl+I로 참조 이미지 가져오기
2. V 키로 위치 조정
3. P 키로 트레이싱
4. 완성 후 참조 이미지 삭제
5. SVG로 내보내기 (무한 확대!)
```

### 픽셀아트
```
1. 32x32 캔버스 생성
2. P 키로 픽셀 단위 그리기
3. B 키로 영역 채우기
4. 색상 변경 → 계속 그리기
5. Ctrl+U로 일부 픽셀 분리하여 수정
6. 16x 스케일로 PNG 내보내기
```

## 📚 문서

- **[README_V2.1.md](README_V2.1.md)** - v2.1 전체 기능 설명
- **[COMPLETION_V2.1.md](COMPLETION_V2.1.md)** - v2.1 구현 보고서
- **[docs/USER_GUIDE.md](docs/USER_GUIDE.md)** - 사용자 가이드
- **[docs/DEVELOPER.md](docs/DEVELOPER.md)** - 개발자 문서
- **[docs/FILE_FORMAT.md](docs/FILE_FORMAT.md)** - .plb 파일 형식
- **[docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md)** - 프로젝트 구조

## 🛠️ 개발

### 프로젝트 구조
```
pixelab/
├── pixelab_v2.py          ★ v2.1 메인 앱
├── main.py                  v1.0 호환 앱
├── test_vector.py           벡터 시스템 테스트
├── run.sh                 ★ 자동 실행 스크립트
├── requirements.txt         의존성
├── src/                     소스 코드
├── docs/                    문서
└── examples/                예제 파일
```

### 기여하기
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 🗺️ 로드맵

### v2.2 (계획)
- [ ] 다중 선택 (Shift+Click)
- [ ] 복사/붙여넣기 (Ctrl+C/V)
- [ ] 색상 픽커 UI 개선
- [ ] 선택 영역 (Marquee Tool)

### v3.0 (비전)
- [ ] 레이어 시스템
- [ ] 애니메이션 프레임
- [ ] GIF 내보내기
- [ ] 타임라인

## 📝 라이선스

MIT License - 자유롭게 사용, 수정, 배포 가능

## 👨‍💻 작성자

**rheehose** - 2026-02-02

## 🙏 감사의 말

- **Python** - 훌륭한 언어
- **Tkinter** - 간단하면서도 강력한 GUI
- **Pillow** - 이미지 처리의 표준

---

<p align="center">
  <strong>PixeLab v2.1</strong><br>
  벡터의 편집성 + 픽셀의 정확성 + 이미지 가져오기 + 한영 전환
</p>

<p align="center">
  <a href="#-빠른-시작">빠른 시작</a> •
  <a href="#-사용법">사용법</a> •
  <a href="#-문서">문서</a> •
  <a href="README_V2.1.md">v2.1 상세 가이드</a>
</p>
