"""
Internationalization (i18n) - Korean/English language support
"""


class I18n:
    """Simple internationalization system"""
    
    def __init__(self, lang='ko'):
        self.lang = lang
        self.translations = {
            'ko': {
                # Menu
                'file': '파일',
                'edit': '편집',
                'view': '보기',
                'object': '객체',
                'layers': '레이어',
                'help': '도움말',
                'about': '정보',
                'shortcuts': '단축키',
                
                # File menu
                'new': '새로 만들기',
                'open': '열기',
                'save': '저장',
                'save_as': '다른 이름으로 저장',
                'import_image': '이미지 가져오기',
                'export': '내보내기',
                'export_png': 'PNG로 내보내기',
                'export_svg': 'SVG로 내보내기',
                'exit': '종료',
                
                # Edit menu
                'undo': '실행 취소',
                'redo': '다시 실행',
                'group': '그룹 만들기',
                'ungroup': '그룹 해제',
                'clear_canvas': '캔버스 지우기',
                
                # View menu
                'toggle_grid': '격자 토글',
                'zoom_in': '확대',
                'zoom_out': '축소',
                'reset_zoom': '확대/축소 초기화',
                
                # Tools
                'mouse': '마우스',
                'select': '선택',
                'pencil': '연필',
                'brush': '브러시',
                'eraser': '지우개',
                'fill': '채우기',
                'eyedropper': '스포이드',
                'line': '선',
                'rectangle': '사각형',
                'circle': '원',
                
                # Dialog
                'save_changes': '변경 사항 저장',
                'save_before_close': '종료하기 전에 변경 사항을 저장하시겠습니까?',
                'yes': '예',
                'no': '아니오',
                'cancel': '취소',
                
                # Messages
                'ready': '준비',
                'tool': '도구',
                'grid_shown': '격자 표시됨',
                'grid_hidden': '격자 숨김',
                'canvas_cleared': '캔버스가 지워졌습니다',
                'grouped': '그룹화됨',
                'ungrouped': '그룹 해제됨',
                'imported': '가져오기 완료',
                
                # Status
                'objects': '객체',
                'selected': '선택됨',
                'position': '위치',
                'delete': '삭제',
                'change_color': '색상 변경',
                
                # Labels
                'tools_label': '도구',
                'zoom_label': '줌',
                'options_label': '옵션',
                'colors_label': '색상',
                'palette_label': '팔레트',
                'current_color': '현재:',
                'choose_color': '색상 선택...',
                'add_to_palette': '팔레트에 추가',
                'size_label': '크기:',
                'filled_label': '채우기',
                
                # Canvas Size
                'canvas_size': '캔버스 크기',
                'width': '너비',
                'height': '높이',
                'apply': '적용',
                'pixel_scale': '픽셀 스케일',
                'help_text': 'PixeLab 도움말',
                'panning_help': '방향키: 상하좌우 이동 | Ctrl +/-: 확대/축소',
                'tools_help': 'V: 선택 | P: 연필 | B: 브러시 | E: 지우개 | L: 선 | R: 사각형 | C: 원',
            },
            'en': {
                # Menu
                'file': 'File',
                'edit': 'Edit',
                'view': 'View',
                'object': 'Object',
                'layers': 'Layers',
                'help': 'Help',
                'about': 'About',
                'shortcuts': 'Shortcuts',
                
                # File menu
                'new': 'New',
                'open': 'Open',
                'save': 'Save',
                'save_as': 'Save As',
                'import_image': 'Import Image',
                'export': 'Export',
                'export_png': 'Export as PNG',
                'export_svg': 'Export as SVG',
                'exit': 'Exit',
                
                # Edit menu
                'undo': 'Undo',
                'redo': 'Redo',
                'group': 'Group',
                'ungroup': 'Ungroup',
                'clear_canvas': 'Clear Canvas',
                
                # View menu
                'toggle_grid': 'Toggle Grid',
                'zoom_in': 'Zoom In',
                'zoom_out': 'Zoom Out',
                'reset_zoom': 'Reset Zoom',
                
                # Tools
                'mouse': 'Mouse',
                'select': 'Select',
                'pencil': 'Pencil',
                'brush': 'Brush',
                'eraser': 'Eraser',
                'fill': 'Fill',
                'eyedropper': 'Eyedropper',
                'line': 'Line',
                'rectangle': 'Rectangle',
                'circle': 'Circle',
                
                # Dialog
                'save_changes': 'Save Changes',
                'save_before_close': 'Do you want to save changes before closing?',
                'yes': 'Yes',
                'no': 'No',
                'cancel': 'Cancel',
                
                # Messages
                'ready': 'Ready',
                'tool': 'Tool',
                'grid_shown': 'Grid shown',
                'grid_hidden': 'Grid hidden',
                'canvas_cleared': 'Canvas cleared',
                'grouped': 'Grouped',
                'ungrouped': 'Ungrouped',
                'imported': 'Imported',
                
                # Status
                'objects': 'objects',
                'selected': 'selected',
                'position': 'Position',
                'delete': 'Delete',
                'change_color': 'Change Color',
                
                # Labels
                'tools_label': 'Tools',
                'zoom_label': 'Zoom',
                'options_label': 'Options',
                'colors_label': 'Colors',
                'palette_label': 'Palette',
                'current_color': 'Current:',
                'choose_color': 'Choose Color...',
                'add_to_palette': 'Add to Palette',
                'size_label': 'Size:',
                'filled_label': 'Filled',
                
                # Canvas Size
                'canvas_size': 'Canvas Size',
                'width': 'Width',
                'height': 'Height',
                'apply': 'Apply',
                'pixel_scale': 'Pixel Scale',
                'help_text': 'PixeLab Help',
                'panning_help': 'Arrow Keys: Pan | Ctrl +/-: Zoom',
                'tools_help': 'V: Select | P: Pencil | B: Brush | E: Eraser | L: Line | R: Rect | C: Circle',
            }
        }
    
    def t(self, key, fallback=None):
        """Translate key to current language"""
        return self.translations.get(self.lang, {}).get(key, fallback or key)
    
    def set_language(self, lang):
        """Set current language"""
        if lang in self.translations:
            self.lang = lang
            return True
        return False
    
    def get_language(self):
        """Get current language"""
        return self.lang
    
    def toggle_language(self):
        """Toggle between Korean and English"""
        self.lang = 'en' if self.lang == 'ko' else 'ko'
        return self.lang


# Global instance
_i18n = I18n()


def t(key, fallback=None):
    """Shorthand for translation"""
    return _i18n.t(key, fallback)


def set_language(lang):
    """Set language"""
    return _i18n.set_language(lang)


def toggle_language():
    """Toggle language"""
    return _i18n.toggle_language()


def get_language():
    """Get current language"""
    return _i18n.get_language()
