# .plb 파일 형식 명세

**버전**: 1.0  
**파일 확장자**: `.plb` (PixeLab Binary의 약자이지만 실제로는 JSON 텍스트 형식)

## 개요

.plb 파일은 PixeLab 프로젝트를 저장하기 위한 전용 파일 형식입니다. JSON 기반의 텍스트 형식으로, 사람이 읽을 수 있고 버전 관리 시스템(Git)과 호환됩니다.

## 파일 구조

### 기본 스키마

```json
{
  "version": "1.0",
  "width": <number>,
  "height": <number>,
  "palette": [<color_string>, ...],
  "pixels": [<pixel_array>, ...],
  "metadata": {
    "created": <iso8601_datetime>,
    "modified": <iso8601_datetime>,
    "author": <string>,
    "title": <string>,
    "description": <string>
  }
}
```

### 필드 설명

#### `version` (필수)
- **타입**: String
- **값**: "1.0"
- **설명**: 파일 형식 버전. 하위 호환성 보장을 위해 사용

#### `width` (필수)
- **타입**: Number (Integer)
- **범위**: 1 ~ 512
- **설명**: 캔버스의 너비 (픽셀 단위)

#### `height` (필수)
- **타입**: Number (Integer)
- **범위**: 1 ~ 512
- **설명**: 캔버스의 높이 (픽셀 단위)

#### `palette` (선택)
- **타입**: Array of Strings
- **형식**: 각 문자열은 "#RRGGBB" 형식의 16진수 색상 코드
- **예시**: `["#000000", "#FFFFFF", "#FF0000"]`
- **설명**: 사용자가 저장한 색상 팔레트
- **기본값**: `[]` (빈 배열)

#### `pixels` (필수)
- **타입**: Array of Arrays
- **형식**: `[[R, G, B, A], ...]`
- **크기**: `width × height` 개의 요소
- **설명**: 각 픽셀의 RGBA 값
  - `R`: Red (0-255)
  - `G`: Green (0-255)
  - `B`: Blue (0-255)
  - `A`: Alpha/투명도 (0-255, 0=완전 투명, 255=완전 불투명)
- **순서**: 좌상단부터 우측으로, 한 행이 끝나면 다음 행으로 (Row-major order)

**예시** (2x2 캔버스):
```json
"pixels": [
  [255, 0, 0, 255],    // (0,0) - 빨강
  [0, 255, 0, 255],    // (1,0) - 초록
  [0, 0, 255, 255],    // (0,1) - 파랑
  [255, 255, 0, 255]   // (1,1) - 노랑
]
```

#### `metadata` (선택)
- **타입**: Object
- **설명**: 프로젝트에 대한 메타데이터

##### `metadata.created`
- **타입**: String
- **형식**: ISO 8601 (예: "2026-02-02T00:53:34+09:00")
- **설명**: 파일이 처음 생성된 시각

##### `metadata.modified`
- **타입**: String
- **형식**: ISO 8601
- **설명**: 파일이 마지막으로 수정된 시각

##### `metadata.author`
- **타입**: String
- **설명**: 작성자 이름 (선택)

##### `metadata.title`
- **타입**: String
- **설명**: 작품 제목 (선택)

##### `metadata.description`
- **타입**: String
- **설명**: 작품 설명 (선택)

## 예시 파일

### 최소 예시 (4x4 체커보드)

```json
{
  "version": "1.0",
  "width": 4,
  "height": 4,
  "pixels": [
    [0, 0, 0, 255], [255, 255, 255, 255], [0, 0, 0, 255], [255, 255, 255, 255],
    [255, 255, 255, 255], [0, 0, 0, 255], [255, 255, 255, 255], [0, 0, 0, 255],
    [0, 0, 0, 255], [255, 255, 255, 255], [0, 0, 0, 255], [255, 255, 255, 255],
    [255, 255, 255, 255], [0, 0, 0, 255], [255, 255, 255, 255], [0, 0, 0, 255]
  ]
}
```

### 전체 예시 (메타데이터 포함)

```json
{
  "version": "1.0",
  "width": 16,
  "height": 16,
  "palette": [
    "#000000",
    "#FFFFFF",
    "#FF0000",
    "#00FF00",
    "#0000FF",
    "#FFFF00",
    "#FF00FF",
    "#00FFFF"
  ],
  "pixels": [
    [255, 255, 255, 255],
    [255, 255, 255, 255],
    ...
  ],
  "metadata": {
    "created": "2026-02-02T00:53:34+09:00",
    "modified": "2026-02-02T01:30:00+09:00",
    "author": "rheehose",
    "title": "My First Pixel Art",
    "description": "A simple 16x16 pixel art created with PixeLab"
  }
}
```

## 파일 읽기 및 쓰기

### Python 예시 (읽기)

```python
import json

def load_plb(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 버전 확인
    if data.get('version') != '1.0':
        raise ValueError(f"Unsupported version: {data.get('version')}")
    
    width = data['width']
    height = data['height']
    pixels = data['pixels']
    palette = data.get('palette', [])
    
    # 검증
    if len(pixels) != width * height:
        raise ValueError("Pixel data size mismatch")
    
    return data
```

### Python 예시 (쓰기)

```python
import json
from datetime import datetime

def save_plb(filepath, width, height, pixels, palette=None):
    data = {
        "version": "1.0",
        "width": width,
        "height": height,
        "pixels": pixels,
        "metadata": {
            "created": datetime.now().isoformat(),
            "modified": datetime.now().isoformat()
        }
    }
    
    if palette:
        data["palette"] = palette
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
```

## 버전 관리

### 버전 1.0
- 초기 버전
- 기본 픽셀 데이터 및 팔레트 지원

### 향후 버전 계획

#### 버전 1.1 (예정)
- 레이어 지원
- 각 레이어별 픽셀 데이터 및 가시성 설정

```json
{
  "version": "1.1",
  "layers": [
    {
      "name": "Background",
      "visible": true,
      "opacity": 1.0,
      "pixels": [...]
    },
    {
      "name": "Foreground",
      "visible": true,
      "opacity": 0.8,
      "pixels": [...]
    }
  ]
}
```

#### 버전 2.0 (예정)
- 애니메이션 프레임 지원
- 프레임별 픽셀 데이터 및 타이밍 정보

## 호환성

### 상위 버전 읽기
- PixeLab은 알 수 없는 필드를 무시하고 필수 필드만 읽습니다
- 이를 통해 향후 버전의 파일도 부분적으로 읽을 수 있습니다

### 하위 버전 읽기
- 새 버전의 PixeLab은 항상 이전 버전의 파일을 읽을 수 있어야 합니다
- 부족한 필드는 기본값으로 처리됩니다

## 파일 크기 최적화

### 일반적인 파일 크기
- 32x32 캔버스: 약 10-30 KB
- 64x64 캔버스: 약 40-120 KB
- 128x128 캔버스: 약 160-500 KB

### 최적화 팁
1. **압축**: .plb.gz로 gzip 압축 가능 (약 50-70% 크기 감소)
2. **인덱싱**: 팔레트를 활용하여 픽셀 데이터를 인덱스로 저장 (향후 버전)
3. **RLE 압축**: Run-Length Encoding으로 반복 픽셀 최적화 (향후 버전)

## 다른 형식으로 변환

### PLB → PNG
```python
from PIL import Image

def plb_to_png(plb_path, png_path):
    data = load_plb(plb_path)
    width = data['width']
    height = data['height']
    pixels = data['pixels']
    
    img = Image.new('RGBA', (width, height))
    img.putdata([tuple(p) for p in pixels])
    img.save(png_path)
```

### PLB → SVG
```python
def plb_to_svg(plb_path, svg_path):
    data = load_plb(plb_path)
    width = data['width']
    height = data['height']
    pixels = data['pixels']
    
    with open(svg_path, 'w') as f:
        f.write(f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">\n')
        
        for y in range(height):
            for x in range(width):
                idx = y * width + x
                r, g, b, a = pixels[idx]
                
                if a > 0:  # 투명하지 않은 픽셀만
                    color = f'rgb({r},{g},{b})'
                    opacity = a / 255.0
                    f.write(f'  <rect x="{x}" y="{y}" width="1" height="1" '
                           f'fill="{color}" opacity="{opacity}"/>\n')
        
        f.write('</svg>\n')
```

## 보안 고려사항

1. **파일 크기 제한**: 악의적으로 큰 width/height 값 방지
2. **픽셀 개수 검증**: `len(pixels) == width * height` 확인
3. **색상 값 범위**: RGBA 각 값이 0-255 범위 내인지 확인
4. **JSON 파싱 오류**: 손상된 파일에 대한 예외 처리

## 라이선스

이 파일 형식 명세는 MIT 라이선스 하에 공개되며, 누구나 자유롭게 구현할 수 있습니다.
