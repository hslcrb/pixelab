# PixeLab 프로젝트 구조

```
pixelab/
├── main.py                     # 애플리케이션 진입점
├── run.sh                      # 실행 스크립트 (자동 venv 설정)
├── requirements.txt            # Python 의존성
├── .gitignore                  # Git 제외 파일 목록
├── README.md                   # 프로젝트 README
│
├── src/                        # 소스 코드
│   ├── __init__.py            # 패키지 초기화
│   ├── app.py                 # 메인 애플리케이션 클래스
│   ├── canvas.py              # 픽셀 캔버스 구현
│   ├── tools.py               # 모든 그리기 도구
│   ├── palette.py             # 색상 팔레트 관리
│   ├── file_handler.py        # PLB/PNG/SVG 파일 입출력
│   └── ui/                    # UI 컴포넌트
│       ├── __init__.py
│       ├── menubar.py         # 메뉴 바
│       ├── toolbar.py         # 도구 모음
│       └── colorpicker.py     # 색상 선택 패널
│
├── docs/                       # 문서
│   ├── USER_GUIDE.md          # 사용자 가이드
│   ├── DEVELOPER.md           # 개발자 문서
│   └── FILE_FORMAT.md         # .plb 파일 형식 명세
│
└── examples/                   # 예제 파일
    ├── README.md              # 예제 설명
    ├── heart.plb              # 8x8 하트
    └── ball.plb               # 16x16 음영 구체
```

## 핵심 컴포넌트 설명

### main.py
- 애플리케이션의 진입점
- Tkinter 루트 윈도우 생성 및 앱 초기화

### src/app.py - PixelLabApp
- 메인 애플리케이션 클래스
- UI 구성 및 이벤트 처리
- 파일 작업, 도구 관리, 히스토리 관리

### src/canvas.py - PixelCanvas
- 픽셀 데이터 저장 (2D 배열)
- 줌/패닝 기능
- 고성능 렌더링 (PIL/ImageTk)
- 좌표 변환 (화면 ↔ 캔버스)

### src/tools.py
- `Tool`: 모든 도구의 기반 추상 클래스
- `PencilTool`: 단일 픽셀 그리기
- `BrushTool`: 브러시 (크기 조절 가능)
- `EraserTool`: 지우개
- `FillTool`: 영역 채우기 (Flood Fill)
- `EyedropperTool`: 색상 추출
- `LineTool`: 직선 (Bresenham 알고리즘)
- `RectangleTool`: 사각형
- `CircleTool`: 원 (Midpoint 알고리즘)

### src/palette.py - ColorPalette
- 색상 팔레트 관리
- RGB ↔ Hex 변환
- 팔레트 직렬화

### src/file_handler.py - FileHandler
- `.plb` 프로젝트 파일 저장/로드 (JSON)
- PNG 내보내기 (스케일링 지원)
- SVG 내보내기 (벡터)

### src/ui/
#### menubar.py - MenuBar
- File, Edit, View, Help 메뉴
- 단축키 표시
- 메뉴 명령 처리

#### toolbar.py - Toolbar
- 도구 버튼 (아이콘 포함)
- 도구 옵션 (크기, 채움)
- 도구 선택 시각화

#### colorpicker.py - ColorPicker
- 현재 색상 표시
- 색상 선택 다이얼로그
- 색상 팔레트 그리드
- 팔레트 추가/삭제

## 데이터 흐름

1. **사용자 입력** → Tkinter 이벤트 → `PixelLabApp` 이벤트 핸들러
2. **도구 사용** → `Tool.on_press/drag/release` → `PixelCanvas.set_pixel`
3. **픽셀 변경** → `History.push` (undo/redo용)
4. **렌더링** → `PixelCanvas.render` → PIL Image → ImageTk → Tkinter Canvas
5. **파일 저장** → `FileHandler.save_plb` → JSON 직렬화 → 파일

## 주요 알고리즘

- **Bresenham's Line Algorithm**: 직선 그리기
- **Midpoint Circle Algorithm**: 원 그리기
- **Flood Fill (BFS)**: 영역 채우기
- **Viewport Culling**: 화면 밖 픽셀 렌더링 최적화
- **Zoom with Pivot**: 마우스 포인터 중심 줌

## 메모리 관리

- 히스토리: 최대 50개 상태 저장 (deepcopy)
- 렌더링: PhotoImage 캐싱으로 재사용
- 큰 캔버스: 필요 시 렌더링 최적화

## 확장 가능성

향후 추가 예정 기능:
- 레이어 시스템
- 애니메이션 프레임
- 커스텀 브러시
- 선택 영역 (Selection)
- 복사/붙여넣기
- 색상 조정 도구
