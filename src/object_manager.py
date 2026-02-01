"""
Object Manager - Manages all vector objects
"""
from typing import List, Optional
import copy
from .vector_objects import VectorObject, create_object_from_dict


class ObjectManager:
    """Manages all vector objects in the scene"""
    
    def __init__(self):
        self.objects: List[VectorObject] = []
        self.selected_objects: List[VectorObject] = []
    
    def add_object(self, obj: VectorObject):
        """Add a vector object"""
        self.objects.append(obj)
    
    def remove_object(self, obj: VectorObject):
        """Remove a vector object"""
        if obj in self.objects:
            self.objects.remove(obj)
        if obj in self.selected_objects:
            self.selected_objects.remove(obj)
    
    def clear(self):
        """Clear all objects"""
        self.objects.clear()
        self.selected_objects.clear()
    
    def get_object_at(self, x, y) -> Optional[VectorObject]:
        """Get top object at given position"""
        # Check from top to bottom
        for obj in reversed(self.objects):
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
        for obj in self.selected_objects:
            obj.selected = False
        self.selected_objects.clear()
    
    def delete_selected(self):
        """Delete all selected objects"""
        for obj in self.selected_objects:
            if obj in self.objects:
                self.objects.remove(obj)
        self.selected_objects.clear()
    
    def translate_selected(self, dx, dy):
        """Move all selected objects"""
        for obj in self.selected_objects:
            obj.translate(dx, dy)
    
    def group_selected(self):
        """Group selected objects"""
        if len(self.selected_objects) < 2:
            return None
        
        from .vector_objects import VectorGroup
        
        # Create group
        group = VectorGroup(self.selected_objects.copy(), f"Group {len(self.objects)}")
        
        # Remove individual objects
        for obj in self.selected_objects:
            if obj in self.objects:
                self.objects.remove(obj)
        
        # Add group
        self.objects.append(group)
        
        # Select group
        self.selected_objects.clear()
        self.selected_objects.append(group)
        group.selected = True
        
        return group
    
    def ungroup_selected(self):
        """Ungroup selected groups"""
        from .vector_objects import VectorGroup
        
        new_objects = []
        
        for obj in self.selected_objects:
            if isinstance(obj, VectorGroup):
                # Remove group
                if obj in self.objects:
                    self.objects.remove(obj)
                
                # Add ungrouped objects
                ungrouped = obj.ungroup()
                self.objects.extend(ungrouped)
                new_objects.extend(ungrouped)
        
        # Select ungrouped objects
        self.selected_objects.clear()
        for obj in new_objects:
            obj.selected = True
            self.selected_objects.append(obj)
        
        return len(new_objects)
    
    def change_selected_color(self, new_color):
        """Change color of selected objects and groups"""
        count = 0
        for obj in self.selected_objects:
            # Check if it's a group (VectorGroup doesn't typically use its own color)
            from .vector_objects import VectorGroup
            if isinstance(obj, VectorGroup):
                # Change all objects inside the group
                for sub_obj in obj.objects:
                    if hasattr(sub_obj, 'color'):
                        sub_obj.color = new_color
                        count += 1
            # Also change the object's own color if it has one
            elif hasattr(obj, 'color'):
                obj.color = new_color
                count += 1
        
        return count
    
    def rasterize(self, width, height):
        """
        Rasterize all objects to pixel data
        Returns 2D array of (r, g, b, a) tuples
        """
        # Initialize with transparent pixels
        pixels = [[(255, 255, 255, 0) for _ in range(width)] for _ in range(height)]
        
        # Rasterize each object
        for obj in self.objects:
            obj_pixels = obj.rasterize(width, height)
            for x, y, color in obj_pixels:
                if 0 <= x < width and 0 <= y < height:
                    # Alpha blending
                    r, g, b, a = color
                    if a == 255:
                        pixels[y][x] = (r, g, b, 255)
                    elif a > 0:
                        # Blend with existing pixel
                        old_r, old_g, old_b, old_a = pixels[y][x]
                        alpha = a / 255.0
                        new_r = int(r * alpha + old_r * (1 - alpha))
                        new_g = int(g * alpha + old_g * (1 - alpha))
                        new_b = int(b * alpha + old_b * (1 - alpha))
                        new_a = min(255, a + old_a)
                        pixels[y][x] = (new_r, new_g, new_b, new_a)
        
        return pixels
    
    def copy_objects(self) -> List[VectorObject]:
        """Deep copy all objects"""
        return copy.deepcopy(self.objects)
    
    def restore_objects(self, objects: List[VectorObject]):
        """Restore objects from copy"""
        self.objects = copy.deepcopy(objects)
        self.selected_objects.clear()
    
    def to_dict(self) -> dict:
        """Serialize to dictionary"""
        return {
            'objects': [obj.to_dict() for obj in self.objects]
        }
    
    def from_dict(self, data: dict):
        """Deserialize from dictionary"""
        self.clear()
        for obj_data in data.get('objects', []):
            obj = create_object_from_dict(obj_data)
            if obj:
                self.add_object(obj)
    
    def __len__(self):
        return len(self.objects)
    
    def __iter__(self):
        return iter(self.objects)
