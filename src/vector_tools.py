"""
Vector Tools - Tools that create and manipulate vector objects
"""
from abc import ABC, abstractmethod
from .vector_objects import *
from .object_manager import ObjectManager


class VectorTool(ABC):
    """Base class for vector tools"""
    
    def __init__(self, color=(0, 0, 0, 255)):
        self.color = color
        self.preview_object = None
    
    @abstractmethod
    def on_press(self, x, y, object_manager: ObjectManager):
        """Called when mouse button is pressed"""
        pass
    
    @abstractmethod
    def on_drag(self, x, y, object_manager: ObjectManager):
        """Called when mouse is dragged"""
        pass
    
    @abstractmethod
    def on_release(self, x, y, object_manager: ObjectManager):
        """Called when mouse button is released"""
        pass
    
    def set_color(self, color):
        """Set tool color"""
        self.color = color
    
    def get_cursor(self):
        """Get cursor style for this tool"""
        return "crosshair"
    
    def get_preview_object(self):
        """Get preview object for rendering"""
        return self.preview_object


class VectorPencilTool(VectorTool):
    """Creates VectorPixel or VectorPath objects"""
    
    def __init__(self, color=(0, 0, 0, 255)):
        super().__init__(color)
        self.current_path = None
    
    def on_press(self, x, y, object_manager):
        # Start new path
        self.current_path = VectorPath([(x, y)], self.color)
        self.preview_object = self.current_path
    
    def on_drag(self, x, y, object_manager):
        if self.current_path:
            # Add point to path
            if (x, y) != self.current_path.points[-1]:
                self.current_path.points.append((x, y))
    
    def on_release(self, x, y, object_manager):
        if self.current_path:
            if len(self.current_path.points) == 1:
                # Single pixel
                px, py = self.current_path.points[0]
                object_manager.add_object(VectorPixel(px, py, self.color))
            else:
                # Add path
                object_manager.add_object(self.current_path)
            
            self.current_path = None
            self.preview_object = None


class VectorBrushTool(VectorTool):
    """Creates a single VectorPath for each brush stroke (High Performance)"""
    
    def __init__(self, color=(0, 0, 0, 255), size=3):
        super().__init__(color)
        self.size = size
        self.current_stroke = None
    
    def set_size(self, size):
        self.size = max(1, min(100, size))
    
    def on_press(self, x, y, object_manager):
        # Start new path with thickness
        self.current_stroke = VectorPath([(x, y)], self.color, thickness=self.size)
        self.preview_object = self.current_stroke
    
    def on_drag(self, x, y, object_manager):
        if self.current_stroke:
            # Add point to current stroke
            if (x, y) != self.current_stroke.points[-1]:
                self.current_stroke.points.append((x, y))
    
    def on_release(self, x, y, object_manager):
        if self.current_stroke:
            # Add the entire stroke as one object
            object_manager.add_object(self.current_stroke)
            self.current_stroke = None
            self.preview_object = None


class VectorEraserTool(VectorTool):
    """Removes objects under cursor"""
    
    def __init__(self, size=3):
        super().__init__((0, 0, 0, 0))
        self.size = size
    
    def set_size(self, size):
        self.size = max(1, min(10, size))
    
    def on_press(self, x, y, object_manager):
        self._erase(x, y, object_manager)
    
    def on_drag(self, x, y, object_manager):
        self._erase(x, y, object_manager)
    
    def on_release(self, x, y, object_manager):
        pass
    
    def _erase(self, cx, cy, object_manager):
        radius = self.size // 2
        to_remove = []
        
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if dx*dx + dy*dy <= radius*radius:
                    px, py = cx + dx, cy + dy
                    obj = object_manager.get_object_at(px, py)
                    if obj and obj not in to_remove:
                        to_remove.append(obj)
        
        for obj in to_remove:
            object_manager.remove_object(obj)


class VectorLineTool(VectorTool):
    """Creates VectorLine objects"""
    
    def __init__(self, color=(0, 0, 0, 255)):
        super().__init__(color)
        self.start_pos = None
    
    def on_press(self, x, y, object_manager):
        self.start_pos = (x, y)
        self.preview_object = VectorLine(x, y, x, y, self.color)
    
    def on_drag(self, x, y, object_manager):
        if self.start_pos:
            x0, y0 = self.start_pos
            self.preview_object = VectorLine(x0, y0, x, y, self.color)
    
    def on_release(self, x, y, object_manager):
        if self.start_pos:
            x0, y0 = self.start_pos
            if (x0, y0) != (x, y):
                object_manager.add_object(VectorLine(x0, y0, x, y, self.color))
            else:
                # Single pixel
                object_manager.add_object(VectorPixel(x, y, self.color))
            
            self.start_pos = None
            self.preview_object = None


class VectorRectangleTool(VectorTool):
    """Creates VectorRectangle objects"""
    
    def __init__(self, color=(0, 0, 0, 255), filled=False):
        super().__init__(color)
        self.filled = filled
        self.start_pos = None
    
    def on_press(self, x, y, object_manager):
        self.start_pos = (x, y)
        self.preview_object = VectorRectangle(x, y, x, y, self.color, self.filled)
    
    def on_drag(self, x, y, object_manager):
        if self.start_pos:
            x0, y0 = self.start_pos
            self.preview_object = VectorRectangle(x0, y0, x, y, self.color, self.filled)
    
    def on_release(self, x, y, object_manager):
        if self.start_pos:
            x0, y0 = self.start_pos
            if (x0, y0) != (x, y):
                rect = VectorRectangle(x0, y0, x, y, self.color, self.filled)
                
                # If filled, group the pixels for easier manipulation
                if self.filled:
                    from .vector_objects import VectorGroup
                    # Create as a single rect object (not pixel group)
                    object_manager.add_object(rect)
                else:
                    object_manager.add_object(rect)
            else:
                # Single pixel
                object_manager.add_object(VectorPixel(x, y, self.color))
            
            self.start_pos = None
            self.preview_object = None


class VectorCircleTool(VectorTool):
    """Creates VectorCircle objects"""
    
    def __init__(self, color=(0, 0, 0, 255), filled=False):
        super().__init__(color)
        self.filled = filled
        self.start_pos = None
    
    def on_press(self, x, y, object_manager):
        self.start_pos = (x, y)
        self.preview_object = VectorCircle(x, y, 0, self.color, self.filled)
    
    def on_drag(self, x, y, object_manager):
        if self.start_pos:
            cx, cy = self.start_pos
            radius = int(max(abs(x - cx), abs(y - cy)))
            self.preview_object = VectorCircle(cx, cy, radius, self.color, self.filled)
    
    def on_release(self, x, y, object_manager):
        if self.start_pos:
            cx, cy = self.start_pos
            radius = int(max(abs(x - cx), abs(y - cy)))
            if radius > 0:
                object_manager.add_object(VectorCircle(cx, cy, radius, self.color, self.filled))
            else:
                # Single pixel
                object_manager.add_object(VectorPixel(cx, cy, self.color))
            
            self.start_pos = None
            self.preview_object = None


class VectorEyedropperTool(VectorTool):
    """Picks color from rendered pixels"""
    
    def __init__(self, color_callback=None):
        super().__init__()
        self.color_callback = color_callback
    
    def on_press(self, x, y, object_manager):
        # This needs access to rendered pixels, handled by app
        pass
    
    def on_drag(self, x, y, object_manager):
        pass
    
    def on_release(self, x, y, object_manager):
        pass
    
    def pick_color(self, color):
        if self.color_callback:
            self.color_callback(color)
    
    def get_cursor(self):
        return "target"


class VectorSelectTool(VectorTool):
    """Selects and moves vector objects with marquee selection"""
    
    def __init__(self):
        super().__init__()
        self.mode = None  # 'move' or 'marquee'
        self.drag_start = None
        self.selected_obj = None
        self.marquee_rect = None  # (x1, y1, x2, y2) for preview
    
    def on_press(self, x, y, object_manager):
        # Try to select object at position
        obj = object_manager.get_object_at(x, y)
        
        if obj:
            # Clicking on an object - prepare to move
            if obj not in object_manager.selected_objects:
                # Deselect others and select this
                object_manager.deselect_all()
                object_manager.select_object(obj)
            
            self.selected_obj = obj
            self.mode = 'move'
            self.drag_start = (x, y)
        else:
            # Clicking on empty space - start marquee selection
            object_manager.deselect_all()
            self.selected_obj = None
            self.mode = 'marquee'
            self.drag_start = (x, y)
            self.marquee_rect = (x, y, x, y)
    
    def on_drag(self, x, y, object_manager):
        if self.mode == 'move' and self.drag_start and self.selected_obj:
            # Move selected objects
            dx = x - self.drag_start[0]
            dy = y - self.drag_start[1]
            
            if dx != 0 or dy != 0:
                object_manager.translate_selected(dx, dy)
                self.drag_start = (x, y)
        
        elif self.mode == 'marquee' and self.drag_start:
            # Update marquee rectangle
            x1, y1 = self.drag_start
            self.marquee_rect = (
                min(x1, x),
                min(y1, y),
                max(x1, x),
                max(y1, y)
            )
    
    def on_release(self, x, y, object_manager):
        if self.mode == 'marquee' and self.marquee_rect:
            # Select all objects within marquee
            x1, y1, x2, y2 = self.marquee_rect
            
            for obj in object_manager:
                # Get object bounds
                bounds = obj.get_bounds()
                obj_x1, obj_y1, obj_x2, obj_y2 = bounds
                
                # Check if object is within or intersects marquee
                if (obj_x1 <= x2 and obj_x2 >= x1 and
                    obj_y1 <= y2 and obj_y2 >= y1):
                    object_manager.select_object(obj)
        
        self.mode = None
        self.drag_start = None
        self.marquee_rect = None
    
    def get_preview_object(self):
        """Return marquee rectangle for preview"""
        if self.mode == 'marquee' and self.marquee_rect:
            from .vector_objects import VectorRectangle
            x1, y1, x2, y2 = self.marquee_rect
            # Return a semi-transparent blue rectangle
            return VectorRectangle(x1, y1, x2, y2, (100, 150, 255, 100), filled=False)
        return None
    
    def get_cursor(self):
        return "hand2"


class VectorFillTool(VectorTool):
    """Flood fill - creates filled rectangle covering area"""
    
    def __init__(self, color=(0, 0, 0, 255)):
        super().__init__(color)
    
    def on_press(self, x, y, object_manager):
        # For now, just add a pixel
        # TODO: Implement smart flood fill
        object_manager.add_object(VectorPixel(x, y, self.color))
    
    def on_drag(self, x, y, object_manager):
        pass
    
    def on_release(self, x, y, object_manager):
        pass


# Alias for compatibility
class VectorMouseTool(VectorSelectTool):
    """Mouse tool - alias for Select tool"""
    pass
