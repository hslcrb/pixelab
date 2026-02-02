# 📄 .plb (PixeLab) File Specification (v2.1)

The `.plb` file format is the native workspace format for **PixeLab**. It is designed to be an open, transparent, and easy-to-parse JSON format that stores both the vector object data and the workspace environment state.

Since version 2.1, it follows a strict schema to ensure that other services, editors, or viewers can easily render or manipulate PixeLab projects.

---

## 🛠 File Structure (JSON Schema)

A `.plb` file is a plain JSON file with the following root keys:

| Key | Type | Description |
| :--- | :--- | :--- |
| `version` | `string` | Format version (Currently `"2.1"`) |
| `width` | `int` | Canvas logical width (number of pixels) |
| `height` | `int` | Canvas logical height (number of pixels) |
| `layers` | `array` | List of layer objects (Order: Bottom to Top) |
| `current_layer_index` | `int` | Index of the last active layer |
| `palette` | `array` | List of Hex color strings used in the project |
| `logs` | `array` | History of activity logs (timestamp + message) |
| `metadata` | `object` | Information about creation, author, and software |

---

## 🏗 Detailed Key Descriptions

### 1. Layers (`layers`)
Each layer in the array is an object containing:
- `name`: String name of the layer.
- `visible`: Boolean visibility flag.
- `locked`: Boolean lock flag (prevents editing).
- `objects`: Array of **Vector Objects**.

### 2. Vector Objects (`objects`)
PixeLab supports various vector types. Each object must have a `type` key:

#### Pixel (`type: "pixel"`)
```json
{
  "type": "pixel",
  "x": 10, "y": 20,
  "color": [255, 0, 0, 255]
}
```

#### Line (`type: "line"`)
```json
{
  "type": "line",
  "x0": 0, "y0": 0, "x1": 10, "y1": 10,
  "color": [0, 255, 0, 255],
  "thickness": 1
}
```

#### Rectangle (`type: "rectangle"`)
```json
{
  "type": "rectangle",
  "x0": 5, "y0": 5, "x1": 15, "y1": 15,
  "color": [0, 0, 255, 255],
  "filled": true
}
```

#### Path / Stroke (`type: "path"`)
Used by the Pencil and High-Performance Brush.
```json
{
  "type": "path",
  "points": [[10, 10], [11, 12], [13, 15]],
  "color": [255, 255, 0, 255],
  "thickness": 3,
  "closed": false
}
```

#### Group (`type: "group"`)
Can contain nested objects (including other groups).
```json
{
  "type": "group",
  "name": "Head",
  "objects": [ ... ]
}
```

---

## 🔓 Open Data Philosophy

The `.plb` format is **100% Open Source**. We encourage third-party developers to:
1. **Web Viewers**: Build web-based previewers using Three.js or Canvas API by parsing this JSON.
2. **Game Engines**: Write importers for Unity/Godot to turn `.plb` files directly into game assets.
3. **Converters**: Create scripts to convert `.plb` to other formats like Aseprite or CSS Box-Shadow.

---

## 🚀 Performance Tips for Parsers

- **Rasterization Order**: Always render from `layers[0]` to `layers[n]`, and within each layer, from `objects[0]` to `objects[n]`.
- **Coordinate System**: (0, 0) is the top-left corner of the canvas.
- **Color Format**: Colors are stored as `[R, G, B, A]` integer arrays (0-255).

---
*PixeLab Standard Specification - 2026*
