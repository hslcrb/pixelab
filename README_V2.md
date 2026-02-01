# PixeLab v2.0 - 하이브리드 벡터-픽셀 에디터

## 🎯 핵심 혁신: 벡터로 저장, 픽셀로 표시

PixeLab v2.0은 **모든 객체를 벡터로 저장**하면서도 **픽셀 그리드에 맞춰 렌더링**하는 혁신적인 하이브리드 시스템입니다.

### 🔥 주요 특징

#### **벡터 기반 편집**
- ✅ 모든 도형(선, 사각형, 원 등)이 **벡터 객체**로 저장
- ✅ 그려진 후에도 **선택하여 이동/편집 가능**
- ✅ 픽셀 손실 없이 **무한 수정**
- ✅ 객체별 독립적 관리

#### **픽셀 퍼펙트 렌더링**
- ✅ 벡터 객체를 **즉시 픽셀화 (Rasterize)**
- ✅ 격자에 맞춰 **안티앨리어싱 적용**
- ✅ 픽셀아트의 정확성 + 벡터의 편집성

#### **프로페셔널 도구**
- ✅ **Select Tool (V)** - 객체 선택 및 이동
- ✅ **Pencil/Brush** - 자유곡선 (VectorPath)
- ✅ **Line Tool** - 완벽한 직선 (Bresenham)
- ✅ **Rectangle/Circle** - 정확한 도형
- ✅ **Eraser** - 객체 단위 삭제

## 시작하기

### 설치
```bash
cd pixelab
./run.sh
```

또는

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py  # 기존 버전
python3 test_vector.py  # 벡터 시스템 테스트
```

### 필수 요구사항
1. **Python 3.8+**
2. **Tkinter** - `sudo apt-get install python3-tk` (Ubuntu/Debian)
3. **Pillow** - `pip install Pillow>=10.0.0`

## 사용 방법

### 벡터 모드 단축키
```
V - Select Tool (객체 선택/이동)
P - Pencil (자유 곡선)
L - Line (직선)
R - Rectangle (사각형)
C - Circle (원)
G - Grid 토글
```

### 작업 흐름
1. **도구 선택** - 키보드 단축키 사용
2. **그리기** - 클릭-드래그-릴리스
3. **편집** - Select Tool(V)로 객체 선택 후 드래그
4. **저장** - .plb 파일로 저장 (벡터 데이터 유지)
5. **내보내기** - PNG/SVG (픽셀화되어 내보냄)

## 파일 형식

### .plb v2.0 (벡터 포맷)
```json
{
  "version": "2.0",
  "width": 32,
  "height": 32,
  "objects": [
    {
      "type": "line",
      "x0": 10, "y0": 10,
      "x1": 20, "y1": 20,
      "color": [255, 0, 0, 255]
    },
    {
      "type": "circle",
      "cx": 16, "cy": 16,
      "radius": 5,
      "color": [0, 0, 255, 255],
      "filled": false
    }
  ]
}
```

**특징**:
- 벡터 객체로 저장 → 무손실 편집
- 버전 1.0 (픽셀 기반)과 하위 호환
- JSON 텍스트 → Git 친화적

## 아키텍처

### 벡터 객체 시스템
```
VectorObject (추상 클래스)
├── VectorPixel     - 단일 픽셀
├── VectorLine      - 직선
├── VectorRectangle - 사각형
├── VectorCircle    - 원
└── VectorPath      - 자유곡선 (Bezier)
```

### 렌더링 파이프라인
```
1. 벡터 객체 생성 (도구)
   ↓
2. ObjectManager에 추가
   ↓
3. Rasterize (픽셀화)
   ├─ 안티앨리어싱 적용
   └─ 격자에 스냅
   ↓
4. PIL Image로 변환
   ↓
5. Tkinter Canvas에 표시
```

### 핵심 모듈
```
src/
├── vector_objects.py      - 벡터 객체 정의
├── object_manager.py      - 객체 관리 및 렌더링
├── vector_tools.py        - 벡터 생성 도구
├── vector_canvas.py       - 벡터 캔버스
├── vector_file_handler.py - PLB v2.0 입출력
├── app.py                 - 메인 애플리케이션
└── ui/                    - UI 컴포넌트
```

## 기술적 세부사항

### 벡터 → 픽셀 변환
- **Bresenham 알고리즘**: 직선 래스터화
- **Midpoint Circle**: 원 래스터화
- **Alpha Blending**: 투명도 합성
- **Grid Snapping**: 격자 정렬

### 성능 최적화
- 객체 단위 렌더링
- 뷰포트 컬링
- 더티 렉트 (Dirty Rectangle)
- PhotoImage 캐싱

## 비교: v1.0 vs v2.0

| 기능 | v1.0 (픽셀) | v2.0 (벡터) |
|-----|-----------|-----------|
| 저장 방식 | 픽셀 배열 | 벡터 객체 |
| 편집 가능 | ❌ 그림 후 수정 불가 | ✅ 언제든 선택/이동 |
| 파일 크기 | 큼 (모든 픽셀) | 작음 (객체만) |
| 확대 | 픽셀 손실 | 벡터 유지 |
| 도구 | 8개 | 9개 (+Select) |
| 실행 취소 | 전체 캔버스 | 객체 단위 |

## 외부 의존성

### Python 패키지
```
Pillow>=10.0.0  # 이미지 처리 및 렌더링
```

### 시스템 패키지
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter
```

## 프로젝트 구조
```
pixelab/
├── main.py              # v1.0 진입점
├── test_vector.py       # v2.0 테스트
├── run.sh               # 자동 실행
├── src/
│   ├── vector_objects.py      (13KB) ★
│   ├── object_manager.py      (4KB)  ★
│   ├── vector_tools.py        (10KB) ★
│   ├── vector_canvas.py       (10KB) ★
│   ├── vector_file_handler.py (5KB)  ★
│   ├── app.py                 (19KB)
│   ├── tools.py               (11KB)
│   └── ui/ ...
├── docs/
│   ├── USER_GUIDE.md
│   ├── DEVELOPER.md
│   ├── FILE_FORMAT.md
│   └── PROJECT_STRUCTURE.md
└── examples/ ...

★ = v2.0 벡터 시스템
```

## 개발 로드맵

### v2.1 (진행 중)
- [ ] 메인 앱에 벡터 시스템 완전 통합
- [ ] Bezier 곡선 도구
- [ ] 객체 복사/붙여넣기
- [ ] 다중 선택

### v2.2 (계획)
- [ ] 레이어 시스템
- [ ] 객체 그룹화
- [ ] 변형 (회전/크기 조정)
- [ ] 진정한 SVG 내보내기 (픽셀 대신 벡터)

### v3.0 (비전)
- [ ] 애니메이션 프레임
- [ ] 타임라인
- [ ] GIF 내보내기

## 코드 통계

```
파일명                        라인 수    크기
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
벡터 시스템
  vector_objects.py            400+     13KB
  object_manager.py            140      4KB
  vector_tools.py              300+     10KB
  vector_canvas.py             250+     10KB
  vector_file_handler.py       140      5KB
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
기존 시스템
  app.py                       570      19KB
  canvas.py                    290      10KB
  tools.py                     360      11KB
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
총계                          2,450+    92KB
```

## 핵심 알고리즘

### 벡터 객체 래스터화
```python
def rasterize(self, width, height):
    """벡터 → 픽셀 변환"""
    pixels = []
    # Bresenham, Midpoint 등 사용
    # 안티앨리어싱 적용
    # 격자에 스냅
    return pixels
```

### 객체 선택개
```python
def contains_point(self, x, y):
    """점이 객체 내부인지 확인"""
    # 선: 거리 기반
    # 사각형: AABB 충돌
    # 원: 반경 체크
    return True/False
```

### Alpha 블렌딩
```python
# 투명도 합성
alpha = a / 255.0
result_r = int(r * alpha + bg_r * (1 - alpha))
```

## 라이선스
MIT License

## 작성자
rheehose - 2026-02-02

---

## 🎨 PixeLab v2.0 - 벡터의 편집성과 픽셀의 정확성을 모두!
