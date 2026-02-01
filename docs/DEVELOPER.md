# PixeLab 개발자 문서

## 아키텍처 개요

PixeLab은 모듈식 아키텍처로 설계되었으며, 각 컴포넌트가 명확한 책임을 가지고 있습니다.

### 전체 구조

```
┌─────────────┐
│   main.py   │  ← 애플리케이션 진입점
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│          src/app.py                 │  ← 메인 애플리케이션 클래스
│  (PixelLabApp)                      │
└───┬─────────────────────────────┬───┘
    │                             │
    ▼                             ▼
┌────────────────┐         ┌─────────────────┐
│  UI Components │         │  Core Components│
├────────────────┤         ├─────────────────┤
│ - MenuBar      │         │ - Canvas        │
│ - Toolbar      │         │ - Tools         │
│ - ColorPicker  │         │ - Palette       │
│                │         │ - FileHandler   │
└────────────────┘         └─────────────────┘
```

## 핵심 컴포넌트

### 1. PixelLabApp (`src/app.py`)

메인 애플리케이션 클래스로, Tkinter의 `Tk` 인스턴스를 관리합니다.

**책임**:
- 윈도우 초기화 및 설정
- UI 컴포넌트 배치
- 이벤트 핸들링 조정
- 전역 상태 관리

**주요 속성**:
```python
self.canvas: PixelCanvas          # 픽셀 캔버스
self.current_tool: Tool           # 현재 선택된 도구
self.current_color: tuple         # 현재 선택된 색상 (R, G, B, A)
self.palette: ColorPalette        # 색상 팔레트
self.file_handler: FileHandler    # 파일 입출력 핸들러
self.history: History             # 실행 취소/다시 실행
```

**주요 메서드**:
```python
def setup_ui(self):
    """UI 컴포넌트 초기화 및 배치"""
    
def on_tool_select(self, tool_name):
    """도구 선택 이벤트 핸들러"""
    
def on_color_change(self, color):
    """색상 변경 이벤트 핸들러"""
    
def save_project(self):
    """프로젝트 저장"""
    
def load_project(self):
    """프로젝트 불러오기"""
```

### 2. PixelCanvas (`src/canvas.py`)

픽셀 캔버스의 핵심 구현체입니다.

**책임**:
- 픽셀 데이터 저장 및 관리
- 캔버스 렌더링
- 줌/패닝 처리
- 마우스 이벤트를 픽셀 좌표로 변환

**데이터 구조**:
```python
self.width: int                    # 캔버스 너비 (픽셀)
self.height: int                   # 캔버스 높이 (픽셀)
self.pixels: list[list[tuple]]     # 2D 배열: pixels[y][x] = (R, G, B, A)
self.zoom_level: float             # 현재 줌 레벨 (1.0 = 100%)
self.pan_offset: tuple             # (offset_x, offset_y)
self.show_grid: bool               # 격자 표시 여부
```

**주요 메서드**:
```python
def get_pixel(self, x, y) -> tuple:
    """(x, y) 위치의 픽셀 색상 반환"""
    
def set_pixel(self, x, y, color):
    """(x, y) 위치에 픽셀 설정"""
    
def screen_to_canvas(self, screen_x, screen_y) -> tuple:
    """화면 좌표를 캔버스 좌표로 변환"""
    
def canvas_to_screen(self, canvas_x, canvas_y) -> tuple:
    """캔버스 좌표를 화면 좌표로 변환"""
    
def render(self):
    """캔버스를 화면에 렌더링"""
    
def zoom_at(self, x, y, delta):
    """(x, y) 위치를 중심으로 줌"""
    
def pan(self, dx, dy):
    """캔버스 이동"""
```

**렌더링 최적화**:
- 뷰포트 컬링: 화면에 보이는 픽셀만 렌더링
- 더티 사각형: 변경된 영역만 다시 그리기
- 캔버스 캐싱: PhotoImage를 재사용

### 3. Tools (`src/tools.py`)

모든 그리기 도구의 기반 클래스와 구현체들입니다.

**도구 기반 클래스**:
```python
class Tool(ABC):
    """모든 도구의 추상 기반 클래스"""
    
    @abstractmethod
    def on_mouse_down(self, x, y, canvas):
        """마우스 버튼을 눌렀을 때"""
        pass
    
    @abstractmethod
    def on_mouse_drag(self, x, y, canvas):
        """마우스를 드래그할 때"""
        pass
    
    @abstractmethod
    def on_mouse_up(self, x, y, canvas):
        """마우스 버튼을 뗐을 때"""
        pass
    
    def get_cursor(self) -> str:
        """도구의 커서 모양 반환"""
        return "crosshair"
```

**구현된 도구들**:

#### PencilTool
```python
class PencilTool(Tool):
    """단일 픽셀 그리기"""
    
    def on_mouse_down(self, x, y, canvas):
        canvas.set_pixel(x, y, self.color)
    
    def on_mouse_drag(self, x, y, canvas):
        # Bresenham 알고리즘으로 이전 점과 현재 점 사이를 채움
        self._draw_line(self.last_x, self.last_y, x, y, canvas)
```

#### BrushTool
```python
class BrushTool(Tool):
    """여러 픽셀을 한 번에 그리기"""
    
    def __init__(self, size=3):
        self.size = size  # 브러시 크기 (n×n)
    
    def on_mouse_drag(self, x, y, canvas):
        for dy in range(-self.size//2, self.size//2 + 1):
            for dx in range(-self.size//2, self.size//2 + 1):
                canvas.set_pixel(x + dx, y + dy, self.color)
```

#### FillTool
```python
class FillTool(Tool):
    """영역 채우기 (Flood Fill)"""
    
    def on_mouse_down(self, x, y, canvas):
        target_color = canvas.get_pixel(x, y)
        self._flood_fill(x, y, target_color, self.color, canvas)
    
    def _flood_fill(self, x, y, target, replacement, canvas):
        # BFS 또는 DFS로 구현
        # 스택 오버플로우 방지를 위해 큐 사용
        queue = [(x, y)]
        visited = set()
        
        while queue:
            cx, cy = queue.pop(0)
            if (cx, cy) in visited:
                continue
            if canvas.get_pixel(cx, cy) != target:
                continue
            
            canvas.set_pixel(cx, cy, replacement)
            visited.add((cx, cy))
            
            # 4방향 확인
            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                queue.append((cx+dx, cy+dy))
```

#### LineTool
```python
class LineTool(Tool):
    """직선 그리기"""
    
    def on_mouse_down(self, x, y, canvas):
        self.start_x, self.start_y = x, y
        self.preview_canvas = canvas.copy()
    
    def on_mouse_drag(self, x, y, canvas):
        # 미리보기: 원본 복원 후 현재 선 그리기
        canvas.restore(self.preview_canvas)
        self._draw_line(self.start_x, self.start_y, x, y, canvas)
    
    def on_mouse_up(self, x, y, canvas):
        # 최종 라인 확정
        self._draw_line(self.start_x, self.start_y, x, y, canvas)
    
    def _draw_line(self, x0, y0, x1, y1, canvas):
        # Bresenham's line algorithm
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        
        while True:
            canvas.set_pixel(x0, y0, self.color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy
```

### 4. ColorPalette (`src/palette.py`)

색상 팔레트 관리입니다.

**책임**:
- 색상 목록 저장
- 색상 추가/삭제
- 팔레트 직렬화/역직렬화

```python
class ColorPalette:
    def __init__(self):
        self.colors = [
            (0, 0, 0, 255),        # 검정
            (255, 255, 255, 255),  # 흰색
            (255, 0, 0, 255),      # 빨강
            (0, 255, 0, 255),      # 초록
            (0, 0, 255, 255),      # 파랑
        ]
    
    def add_color(self, color: tuple):
        """색상 추가"""
        if color not in self.colors:
            self.colors.append(color)
    
    def remove_color(self, index: int):
        """색상 삭제"""
        if 0 <= index < len(self.colors):
            del self.colors[index]
    
    def to_hex_list(self) -> list:
        """16진수 문자열 리스트로 변환"""
        return [self._rgba_to_hex(c) for c in self.colors]
    
    def _rgba_to_hex(self, rgba: tuple) -> str:
        r, g, b, a = rgba
        return f"#{r:02x}{g:02x}{b:02x}"
```

### 5. FileHandler (`src/file_handler.py`)

파일 입출력을 담당합니다.

**지원 형식**:
- `.plb`: 프로젝트 파일 (JSON)
- `.png`: PNG 이미지
- `.svg`: SVG 벡터 이미지

```python
class FileHandler:
    @staticmethod
    def save_plb(filepath: str, canvas: PixelCanvas, palette: ColorPalette):
        """PLB 파일 저장"""
        data = {
            "version": "1.0",
            "width": canvas.width,
            "height": canvas.height,
            "palette": palette.to_hex_list(),
            "pixels": canvas.get_flat_pixels(),  # 1D 배열로 변환
            "metadata": {
                "created": datetime.now().isoformat(),
                "modified": datetime.now().isoformat()
            }
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    
    @staticmethod
    def load_plb(filepath: str) -> dict:
        """PLB 파일 불러오기"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 버전 확인
        if data.get('version') != '1.0':
            raise ValueError(f"Unsupported version: {data.get('version')}")
        
        return data
    
    @staticmethod
    def export_png(filepath: str, canvas: PixelCanvas, scale: int = 1):
        """PNG로 내보내기"""
        from PIL import Image
        
        img = Image.new('RGBA', (canvas.width, canvas.height))
        pixels = []
        
        for y in range(canvas.height):
            for x in range(canvas.width):
                pixels.append(canvas.get_pixel(x, y))
        
        img.putdata(pixels)
        
        # 스케일링
        if scale > 1:
            new_size = (canvas.width * scale, canvas.height * scale)
            img = img.resize(new_size, Image.NEAREST)  # 픽셀 아트는 NEAREST
        
        img.save(filepath)
    
    @staticmethod
    def export_svg(filepath: str, canvas: PixelCanvas):
        """SVG로 내보내기"""
        with open(filepath, 'w') as f:
            f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write(f'<svg width="{canvas.width}" height="{canvas.height}" ')
            f.write(f'xmlns="http://www.w3.org/2000/svg">\n')
            
            for y in range(canvas.height):
                for x in range(canvas.width):
                    r, g, b, a = canvas.get_pixel(x, y)
                    
                    if a > 0:  # 투명하지 않은 픽셀만
                        opacity = a / 255.0
                        f.write(f'  <rect x="{x}" y="{y}" width="1" height="1" ')
                        f.write(f'fill="rgb({r},{g},{b})" opacity="{opacity}"/>\n')
            
            f.write('</svg>\n')
```

## UI 컴포넌트

### MenuBar (`src/ui/menubar.py`)

메뉴 바 구현입니다.

```python
class MenuBar:
    def __init__(self, parent, app):
        self.app = app
        self.menubar = tk.Menu(parent)
        
        # File 메뉴
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label="New", command=app.new_file, accelerator="Ctrl+N")
        self.file_menu.add_command(label="Open...", command=app.open_file, accelerator="Ctrl+O")
        self.file_menu.add_command(label="Save", command=app.save_file, accelerator="Ctrl+S")
        self.file_menu.add_separator()
        
        # Export 서브메뉴
        self.export_menu = tk.Menu(self.file_menu, tearoff=0)
        self.export_menu.add_command(label="Export as PNG...", command=app.export_png)
        self.export_menu.add_command(label="Export as SVG...", command=app.export_svg)
        self.file_menu.add_cascade(label="Export", menu=self.export_menu)
        
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        
        # Edit 메뉴
        self.edit_menu = tk.Menu(self.menubar, tearoff=0)
        self.edit_menu.add_command(label="Undo", command=app.undo, accelerator="Ctrl+Z")
        self.edit_menu.add_command(label="Redo", command=app.redo, accelerator="Ctrl+Y")
        self.menubar.add_cascade(label="Edit", menu=self.edit_menu)
```

### Toolbar (`src/ui/toolbar.py`)

도구 패널입니다.

```python
class Toolbar(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#2b2b2b", width=60)
        self.app = app
        
        self.tools = [
            ("Pencil", "✏️", "p"),
            ("Brush", "🖌️", "b"),
            ("Eraser", "🧹", "e"),
            ("Fill", "🪣", "f"),
            ("Eyedropper", "💧", "i"),
            ("Line", "📏", "l"),
            ("Rectangle", "▢", "r"),
            ("Circle", "○", "c"),
        ]
        
        self.buttons = {}
        
        for name, icon, key in self.tools:
            btn = tk.Button(
                self,
                text=f"{icon}\n{name}",
                command=lambda n=name: app.select_tool(n),
                bg="#3c3c3c",
                fg="white",
                relief=tk.FLAT,
                padx=5,
                pady=10
            )
            btn.pack(fill=tk.X, padx=5, pady=2)
            self.buttons[name] = btn
            
            # 단축키 바인딩
            parent.bind(key, lambda e, n=name: app.select_tool(n))
```

## 히스토리 시스템 (실행 취소/다시 실행)

```python
class History:
    def __init__(self, max_size=100):
        self.max_size = max_size
        self.undo_stack = []
        self.redo_stack = []
    
    def push(self, state):
        """새 상태 저장"""
        # 상태는 캔버스 픽셀 데이터의 딥 카피
        self.undo_stack.append(copy.deepcopy(state))
        
        # 스택 크기 제한
        if len(self.undo_stack) > self.max_size:
            self.undo_stack.pop(0)
        
        # 새 작업 시 redo 스택 초기화
        self.redo_stack.clear()
    
    def undo(self):
        """실행 취소"""
        if not self.undo_stack:
            return None
        
        current_state = self.undo_stack.pop()
        self.redo_stack.append(current_state)
        
        return self.undo_stack[-1] if self.undo_stack else None
    
    def redo(self):
        """다시 실행"""
        if not self.redo_stack:
            return None
        
        state = self.redo_stack.pop()
        self.undo_stack.append(state)
        
        return state
```

## 테스트

### 단위 테스트

```bash
# 테스트 실행
python -m pytest tests/
```

### 테스트 구조
```
tests/
├── test_canvas.py
├── test_tools.py
├── test_file_handler.py
└── test_palette.py
```

### 예시 테스트
```python
import unittest
from src.canvas import PixelCanvas

class TestPixelCanvas(unittest.TestCase):
    def setUp(self):
        self.canvas = PixelCanvas(width=10, height=10)
    
    def test_set_get_pixel(self):
        color = (255, 0, 0, 255)
        self.canvas.set_pixel(5, 5, color)
        self.assertEqual(self.canvas.get_pixel(5, 5), color)
    
    def test_out_of_bounds(self):
        with self.assertRaises(IndexError):
            self.canvas.set_pixel(100, 100, (0, 0, 0, 255))
```

## 빌드 및 배포

### 실행 파일 생성 (PyInstaller)

```bash
# PyInstaller 설치
pip install pyinstaller

# 실행 파일 생성
pyinstaller --onefile --windowed --name=PixeLab main.py
```

### 패키징 (pip)

```bash
# setup.py 작성 후
python setup.py sdist bdist_wheel
```

## 기여 가이드

1. Fork 후 브랜치 생성
2. 기능 개발 또는 버그 수정
3. 테스트 작성 및 실행
4. Pull Request 제출

### 코드 스타일
- PEP 8 준수
- 타입 힌트 사용  권장
- Docstring 작성 (Google 스타일)

```python
def example_function(param1: int, param2: str) -> bool:
    """
    함수의 간단한 설명.
    
    Args:
        param1: 첫 번째 매개변수 설명
        param2: 두 번째 매개변수 설명
    
    Returns:
        반환값 설명
    
    Raises:
        ValueError: 발생 조건 설명
    """
    pass
```

## 추가 리소스

- [Tkinter 문서](https://docs.python.org/3/library/tkinter.html)
- [Pillow 문서](https://pillow.readthedocs.io/)
- [픽셀아트 튜토리얼](https://www.pixilart.com/tutorials)
