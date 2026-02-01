"""
Drawing Tools - All pixel manipulation tools
"""
from abc import ABC, abstractmethod
import copy


class Tool(ABC):
    """Base class for all drawing tools"""
    
    def __init__(self, color=(0, 0, 0, 255)):
        self.color = color
        self.last_x = None
        self.last_y = None
        self.temp_canvas = None
    
    @abstractmethod
    def on_press(self, x, y, canvas):
        """Called when mouse button is pressed"""
        pass
    
    @abstractmethod
    def on_drag(self, x, y, canvas):
        """Called when mouse is dragged"""
        pass
    
    @abstractmethod
    def on_release(self, x, y, canvas):
        """Called when mouse button is released"""
        pass
    
    def set_color(self, color):
        """Set tool color"""
        self.color = color
    
    def get_cursor(self):
        """Get cursor style for this tool"""
        return "crosshair"


class PencilTool(Tool):
    """Single pixel drawing tool"""
    
    def on_press(self, x, y, canvas):
        canvas.set_pixel(x, y, self.color)
        self.last_x, self.last_y = x, y
    
    def on_drag(self, x, y, canvas):
        if self.last_x is not None:
            self._draw_line(self.last_x, self.last_y, x, y, canvas)
        self.last_x, self.last_y = x, y
    
    def on_release(self, x, y, canvas):
        self.last_x, self.last_y = None, None
    
    def _draw_line(self, x0, y0, x1, y1, canvas):
        """Bresenham's line algorithm"""
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


class BrushTool(Tool):
    """Multi-pixel brush tool"""
    
    def __init__(self, color=(0, 0, 0, 255), size=3):
        super().__init__(color)
        self.size = size
    
    def set_size(self, size):
        """Set brush size"""
        self.size = max(1, min(10, size))
    
    def on_press(self, x, y, canvas):
        self._draw_brush(x, y, canvas)
        self.last_x, self.last_y = x, y
    
    def on_drag(self, x, y, canvas):
        if self.last_x is not None:
            self._draw_line_brush(self.last_x, self.last_y, x, y, canvas)
        self.last_x, self.last_y = x, y
    
    def on_release(self, x, y, canvas):
        self.last_x, self.last_y = None, None
    
    def _draw_brush(self, cx, cy, canvas):
        """Draw brush at position"""
        radius = self.size // 2
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                # Circular brush
                if dx*dx + dy*dy <= radius*radius:
                    canvas.set_pixel(cx + dx, cy + dy, self.color)
    
    def _draw_line_brush(self, x0, y0, x1, y1, canvas):
        """Draw brush along line"""
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        
        while True:
            self._draw_brush(x0, y0, canvas)
            
            if x0 == x1 and y0 == y1:
                break
            
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy


class EraserTool(BrushTool):
    """Eraser tool - brush that sets alpha to 0"""
    
    def __init__(self, size=3):
        super().__init__(color=(0, 0, 0, 0), size=size)
    
    def set_color(self, color):
        """Eraser always uses transparent color"""
        pass  # Ignore color changes


class FillTool(Tool):
    """Flood fill tool"""
    
    def on_press(self, x, y, canvas):
        target_color = canvas.get_pixel(x, y)
        if target_color and target_color != self.color:
            self._flood_fill(x, y, target_color, canvas)
    
    def on_drag(self, x, y, canvas):
        pass  # No dragging for fill
    
    def on_release(self, x, y, canvas):
        pass
    
    def _flood_fill(self, x, y, target_color, canvas):
        """BFS flood fill"""
        if not canvas.get_pixel(x, y):
            return
        
        visited = set()
        queue = [(x, y)]
        
        while queue:
            cx, cy = queue.pop(0)
            
            if (cx, cy) in visited:
                continue
            if not (0 <= cx < canvas.width and 0 <= cy < canvas.height):
                continue
            
            current_color = canvas.get_pixel(cx, cy)
            if current_color != target_color:
                continue
            
            canvas.set_pixel(cx, cy, self.color)
            visited.add((cx, cy))
            
            # Add 4-connected neighbors
            queue.append((cx + 1, cy))
            queue.append((cx - 1, cy))
            queue.append((cx, cy + 1))
            queue.append((cx, cy - 1))


class EyedropperTool(Tool):
    """Pick color from canvas"""
    
    def __init__(self, color_callback=None):
        super().__init__()
        self.color_callback = color_callback
    
    def on_press(self, x, y, canvas):
        color = canvas.get_pixel(x, y)
        if color and self.color_callback:
            self.color_callback(color)
    
    def on_drag(self, x, y, canvas):
        self.on_press(x, y, canvas)
    
    def on_release(self, x, y, canvas):
        pass
    
    def get_cursor(self):
        return "target"


class LineTool(Tool):
    """Straight line drawing tool"""
    
    def on_press(self, x, y, canvas):
        self.start_x, self.start_y = x, y
        self.temp_canvas = canvas.copy_pixels()
    
    def on_drag(self, x, y, canvas):
        if self.temp_canvas:
            canvas.restore_pixels(self.temp_canvas)
            self._draw_line(self.start_x, self.start_y, x, y, canvas)
    
    def on_release(self, x, y, canvas):
        if self.temp_canvas:
            canvas.restore_pixels(self.temp_canvas)
            self._draw_line(self.start_x, self.start_y, x, y, canvas)
            self.temp_canvas = None
    
    def _draw_line(self, x0, y0, x1, y1, canvas):
        """Bresenham's line algorithm"""
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


class RectangleTool(Tool):
    """Rectangle drawing tool"""
    
    def __init__(self, color=(0, 0, 0, 255), filled=False):
        super().__init__(color)
        self.filled = filled
    
    def on_press(self, x, y, canvas):
        self.start_x, self.start_y = x, y
        self.temp_canvas = canvas.copy_pixels()
    
    def on_drag(self, x, y, canvas):
        if self.temp_canvas:
            canvas.restore_pixels(self.temp_canvas)
            self._draw_rectangle(self.start_x, self.start_y, x, y, canvas)
    
    def on_release(self, x, y, canvas):
        if self.temp_canvas:
            canvas.restore_pixels(self.temp_canvas)
            self._draw_rectangle(self.start_x, self.start_y, x, y, canvas)
            self.temp_canvas = None
    
    def _draw_rectangle(self, x0, y0, x1, y1, canvas):
        """Draw rectangle"""
        x_min, x_max = min(x0, x1), max(x0, x1)
        y_min, y_max = min(y0, y1), max(y0, y1)
        
        if self.filled:
            for y in range(y_min, y_max + 1):
                for x in range(x_min, x_max + 1):
                    canvas.set_pixel(x, y, self.color)
        else:
            # Top and bottom
            for x in range(x_min, x_max + 1):
                canvas.set_pixel(x, y_min, self.color)
                canvas.set_pixel(x, y_max, self.color)
            
            # Left and right
            for y in range(y_min, y_max + 1):
                canvas.set_pixel(x_min, y, self.color)
                canvas.set_pixel(x_max, y, self.color)


class CircleTool(Tool):
    """Circle drawing tool"""
    
    def __init__(self, color=(0, 0, 0, 255), filled=False):
        super().__init__(color)
        self.filled = filled
    
    def on_press(self, x, y, canvas):
        self.start_x, self.start_y = x, y
        self.temp_canvas = canvas.copy_pixels()
    
    def on_drag(self, x, y, canvas):
        if self.temp_canvas:
            canvas.restore_pixels(self.temp_canvas)
            self._draw_circle(self.start_x, self.start_y, x, y, canvas)
    
    def on_release(self, x, y, canvas):
        if self.temp_canvas:
            canvas.restore_pixels(self.temp_canvas)
            self._draw_circle(self.start_x, self.start_y, x, y, canvas)
            self.temp_canvas = None
    
    def _draw_circle(self, cx, cy, x1, y1, canvas):
        """Draw circle using midpoint algorithm"""
        # Calculate radius from bounding box
        radius = int(max(abs(x1 - cx), abs(y1 - cy)))
        
        if self.filled:
            # Filled circle
            for y in range(cy - radius, cy + radius + 1):
                for x in range(cx - radius, cx + radius + 1):
                    if (x - cx)**2 + (y - cy)**2 <= radius**2:
                        canvas.set_pixel(x, y, self.color)
        else:
            # Circle outline - Midpoint circle algorithm
            x = 0
            y = radius
            d = 1 - radius
            
            self._draw_circle_points(cx, cy, x, y, canvas)
            
            while x < y:
                if d < 0:
                    d += 2*x + 3
                else:
                    d += 2*(x - y) + 5
                    y -= 1
                x += 1
                
                self._draw_circle_points(cx, cy, x, y, canvas)
    
    def _draw_circle_points(self, cx, cy, x, y, canvas):
        """Draw 8 symmetric points of circle"""
        points = [
            (cx + x, cy + y), (cx - x, cy + y),
            (cx + x, cy - y), (cx - x, cy - y),
            (cx + y, cy + x), (cx - y, cy + x),
            (cx + y, cy - x), (cx - y, cy - x),
        ]
        for px, py in points:
            canvas.set_pixel(px, py, self.color)
