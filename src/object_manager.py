"""
Object Manager - Manages all vector objects
"""
from typing import List, Optional
import copy
from .vector_objects import VectorObject, create_object_from_dict


class Layer:
    """Represents a single layer containing vector objects"""
    def __init__(self, name="Layer 1"):
        self.name = name
        self.objects: List[VectorObject] = []
        self.visible = True
        self.locked = False

    def to_dict(self):
        return {
            'name': self.name,
            'visible': self.visible,
            'locked': self.locked,
            'objects': [obj.to_dict() for obj in self.objects]
        }

    @staticmethod
    def from_dict(data):
        layer = Layer(data.get('name', 'Layer'))
        layer.visible = data.get('visible', True)
        layer.locked = data.get('locked', False)
        for obj_data in data.get('objects', []):
            obj = create_object_from_dict(obj_data)
            if obj:
                layer.objects.append(obj)
        return layer


class ObjectManager:
    """Manages multiple layers of vector objects"""
    
    def __init__(self):
        self.layers: List[Layer] = [Layer("Layer 1")]
        self.current_layer_index = 0
        self.selected_objects: List[VectorObject] = []
        self.palette_colors = [] # Store palette in manager for saving
        self.logs = [] # Activity logs
        from src.i18n import t
        self.add_log(t('project_initialized'))
    
    def add_log(self, message):
        """Add a timestamped log entry"""
        from datetime import datetime
        timestamp = datetime.now().isoformat()
        self.logs.append({"time": timestamp, "message": message})
        # Keep only last 100 logs to avoid file bloat
        if len(self.logs) > 100:
            self.logs.pop(0)

    @property
    def current_layer(self) -> Layer:
        return self.layers[self.current_layer_index]

    @property
    def all_objects(self) -> List[VectorObject]:
        """Returns all objects from all layers combined"""
        objs = []
        for layer in self.layers:
            objs.extend(layer.objects)
        return objs

    def add_layer(self, name=None):
        if not name:
            name = f"Layer {len(self.layers) + 1}"
        new_layer = Layer(name)
        self.layers.append(new_layer)
        self.current_layer_index = len(self.layers) - 1
        from src.i18n import t
        self.add_log(t('added_layer').format(name=name))
        return new_layer

    def remove_layer(self, index):
        if len(self.layers) > 1:
            name = self.layers[index].name
            # Deselect objects in this layer
            for obj in self.layers[index].objects:
                if obj in self.selected_objects:
                    self.selected_objects.remove(obj)
            
            del self.layers[index]
            self.current_layer_index = min(self.current_layer_index, len(self.layers) - 1)
            from src.i18n import t
            self.add_log(t('removed_layer').format(name=name))
            return True
        return False

    def find_layer_of_object(self, obj: VectorObject) -> Optional[Layer]:
        """Find which layer an object belongs to"""
        for layer in self.layers:
            if obj in layer.objects:
                return layer
        return None

    def add_object(self, obj: VectorObject):
        """Add a vector object to current layer"""
        if not self.current_layer.locked:
            self.current_layer.objects.append(obj)
            from src.i18n import t
            self.add_log(t('added_obj').format(type=type(obj).__name__))
    
    def remove_object(self, obj: VectorObject):
        """Remove a vector object from whichever layer it is in"""
        for layer in self.layers:
            if not layer.locked and obj in layer.objects:
                layer.objects.remove(obj)
                break
        if obj in self.selected_objects:
            self.selected_objects.remove(obj)
    
    def clear(self):
        """Clear all layers and objects"""
        self.layers = [Layer("Layer 1")]
        self.current_layer_index = 0
        self.selected_objects.clear()
        from src.i18n import t
        self.add_log(t('canvas_cleared'))
    
    def get_object_at(self, x, y) -> Optional[VectorObject]:
        """Get top object at given position across all visible layers"""
        # Check from top layer to bottom layer, and top object to bottom object within layer
        for layer in reversed(self.layers):
            if layer.visible and not layer.locked:
                for obj in reversed(layer.objects):
                    if obj.contains_point(x, y):
                        return obj
        return None
    
    def select_object(self, obj: VectorObject):
        """Select an object"""
        if obj and obj not in self.selected_objects:
            obj.selected = True
            self.selected_objects.append(obj)
    
    def deselect_object(self, obj: VectorObject):
        """Deselect an object"""
        if obj in self.selected_objects:
            obj.selected = False
            self.selected_objects.remove(obj)
    
    def deselect_all(self):
        """Deselect all objects"""
        for layer in self.layers:
            for obj in layer.objects:
                obj.selected = False
        self.selected_objects.clear()
    
    def delete_selected(self):
        """Delete all selected objects from their respective layers"""
        deleted_count = len(self.selected_objects)
        for obj in self.selected_objects:
            for layer in self.layers:
                if not layer.locked and obj in layer.objects:
                    layer.objects.remove(obj)
                    break
        self.selected_objects.clear()
        if deleted_count > 0:
            from src.i18n import t
            self.add_log(t('deleted_objs').format(count=deleted_count))
    
    def translate_selected(self, dx, dy):
        """Move all selected objects"""
        for obj in self.selected_objects:
            # Only move if its layer is not locked
            is_locked = False
            for layer in self.layers:
                if obj in layer.objects and layer.locked:
                    is_locked = True
                    break
            if not is_locked:
                obj.translate(dx, dy)
    
    def group_selected(self):
        """Group selected objects as a single group in the current layer"""
        if len(self.selected_objects) < 2:
            return None
        
        from .vector_objects import VectorGroup
        
        # Create group
        group = VectorGroup(self.selected_objects.copy(), f"Group {len(self.all_objects)}")
        count = len(self.selected_objects)
        
        # Remove individual objects from their original layers
        for obj in self.selected_objects:
            for layer in self.layers:
                if obj in layer.objects:
                    layer.objects.remove(obj)
                    break
        
        # Add group to CURRENT layer
        self.current_layer.objects.append(group)
        
        # Select group
        self.selected_objects.clear()
        self.select_object(group)
        
        from src.i18n import t
        self.add_log(t('grouped_objs').format(count=count))
        return group
    
    def ungroup_selected(self):
        """Ungroup selected groups into the layer they belong to"""
        from .vector_objects import VectorGroup
        
        new_objects = []
        groups_ungrouped = 0
        
        for obj in self.selected_objects.copy():
            if isinstance(obj, VectorGroup):
                # Find which layer it's in
                target_layer = None
                for layer in self.layers:
                    if obj in layer.objects:
                        target_layer = layer
                        break
                
                if target_layer and not target_layer.locked:
                    target_layer.objects.remove(obj)
                    ungrouped = obj.ungroup()
                    target_layer.objects.extend(ungrouped)
                    new_objects.extend(ungrouped)
                    self.selected_objects.remove(obj)
                    groups_ungrouped += 1
        
        # Select ungrouped objects
        for obj in new_objects:
            self.select_object(obj)
        
        if groups_ungrouped > 0:
            from src.i18n import t
            self.add_log(t('ungrouped_objs').format(count=groups_ungrouped))
        
        return len(new_objects)
    
    def change_selected_color(self, new_color):
        """Change color of selected objects and groups"""
        count = 0
        for obj in self.selected_objects:
            from .vector_objects import VectorGroup
            if isinstance(obj, VectorGroup):
                for sub_obj in obj.objects:
                    if hasattr(sub_obj, 'color'):
                        sub_obj.color = new_color
                        count += 1
            elif hasattr(obj, 'color'):
                obj.color = new_color
                count += 1
        
        if count > 0:
            from src.i18n import t
            self.add_log(t('changed_color_objs').format(count=count))
        return count
    
    def move_selected_up(self):
        """Move selected objects one step forward in their layers"""
        modified = False
        for layer in self.layers:
            if layer.locked: continue
            
            # Find indices of selected objects in this layer
            indices = [i for i, obj in enumerate(layer.objects) if obj in self.selected_objects]
            # Process from top to bottom to avoid index shifting issues
            for i in reversed(indices):
                if i < len(layer.objects) - 1:
                    layer.objects[i], layer.objects[i+1] = layer.objects[i+1], layer.objects[i]
                    modified = True
        
        if modified:
            from src.i18n import t
            self.add_log(t('moved_objs_forward'))
        return modified

    def move_selected_down(self):
        """Move selected objects one step backward in their layers"""
        modified = False
        for layer in self.layers:
            if layer.locked: continue
            
            indices = [i for i, obj in enumerate(layer.objects) if obj in self.selected_objects]
            # Process from bottom to top
            for i in indices:
                if i > 0:
                    layer.objects[i], layer.objects[i-1] = layer.objects[i-1], layer.objects[i]
                    modified = True
        
        if modified:
            from src.i18n import t
            self.add_log(t('moved_objs_backward'))
        return modified

    def move_selected_to_front(self):
        """Move selected objects to the very front of their layers"""
        modified = False
        for layer in self.layers:
            if layer.locked: continue
            
            selected_in_layer = [obj for obj in layer.objects if obj in self.selected_objects]
            if not selected_in_layer: continue
            
            # Remove and re-append at the end
            for obj in selected_in_layer:
                layer.objects.remove(obj)
            layer.objects.extend(selected_in_layer)
            modified = True
            
        if modified:
            from src.i18n import t
            self.add_log(t('moved_objs_front'))
        return modified

    def move_selected_to_back(self):
        """Move selected objects to the very back of their layers"""
        modified = False
        for layer in self.layers:
            if layer.locked: continue
            
            selected_in_layer = [obj for obj in layer.objects if obj in self.selected_objects]
            if not selected_in_layer: continue
            
            # Remove and re-insert at the beginning
            for obj in reversed(selected_in_layer):
                layer.objects.remove(obj)
                layer.objects.insert(0, obj)
            modified = True
            
        if modified:
            from src.i18n import t
            self.add_log(t('moved_objs_back'))
        return modified

    def rasterize(self, width, height) -> 'Image.Image':
        """
        Rasterize all visible layers to a PIL Image
        """
        from PIL import Image, ImageDraw
        
        # Create base image with transparency
        img = Image.new('RGBA', (width, height), (255, 255, 255, 0))
        
        for layer in self.layers:
            if not layer.visible:
                continue
            
            for obj in layer.objects:
                # Get pixels from object
                obj_pixels = obj.rasterize(width, height)
                
                # Draw pixels to image
                # This is faster than manual blending in Python loop
                for x, y, color in obj_pixels:
                    if 0 <= x < width and 0 <= y < height:
                        r, g, b, a = color
                        # Blend with current pixel if transparency < 255
                        if a == 255:
                            img.putpixel((x, y), (r, g, b, 255))
                        elif a > 0:
                            # Simple alpha compositing
                            bg_r, bg_g, bg_b, bg_a = img.getpixel((x, y))
                            alpha = a / 255.0
                            nr = int(r * alpha + bg_r * (1 - alpha))
                            ng = int(g * alpha + bg_g * (1 - alpha))
                            nb = int(b * alpha + bg_b * (1 - alpha))
                            na = min(255, a + bg_a)
                            img.putpixel((x, y), (nr, ng, nb, na))
        
        return img

    def to_dict(self) -> dict:
        """Serialize to dictionary including layers and palette"""
        return {
            'layers': [layer.to_dict() for layer in self.layers],
            'current_layer_index': self.current_layer_index,
            'palette': self.palette_colors,
            'logs': self.logs
        }
    
    def from_dict(self, data: dict):
        """Deserialize from dictionary"""
        self.selected_objects.clear()
        
        if 'layers' in data:
            self.layers = [Layer.from_dict(l_data) for l_data in data['layers']]
            self.current_layer_index = data.get('current_layer_index', 0)
        else:
            # Legacy format support
            legacy_layer = Layer("Background")
            for obj_data in data.get('objects', []):
                obj = create_object_from_dict(obj_data)
                if obj:
                    legacy_layer.objects.append(obj)
            self.layers = [legacy_layer]
            self.current_layer_index = 0
            
        self.palette_colors = data.get('palette', [])
        self.logs = data.get('logs', [{"time": "2026-01-01T00:00:00", "message": "Legacy file loaded"}])
    
    def __len__(self):
        return sum(len(l.objects) for l in self.layers)
    
    def __iter__(self):
        # Flattened iterator
        for layer in self.layers:
            for obj in layer.objects:
                yield obj
