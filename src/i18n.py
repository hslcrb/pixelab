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
                'bring_forward': '앞으로 가져오기',
                'send_backward': '뒤로 보내기',
                'bring_to_front': '맨 앞으로 가져오기',
                'send_to_back': '맨 뒤로 보내기',
                'layers': '레이어',
                'activity_logs': '활동 로그',
                'new_version_title': '새 업데이트 발견!',
                'new_version_msg': '새버전 {v}을 사용할 수 있습니다.',
                'update_now': '지금 업데이트',
                'later': '나중에',
                'size_limit_error': '크기는 1에서 8192 사이여야 합니다.',
                'invalid_input_error': '유효하지 않은 입력입니다.',
                'canvas_resized': '캔버스 크기가 {w}x{h}로 변경되었습니다.',
                'ask_clear_canvas': '모든 객체가 삭제됩니다. 계속하시겠습니까?',
                'ask_clear_title': '캔버스 초기화',
                'open_plb_title': 'PLB 파일 열기',
                'save_plb_title': 'PLB 파일 저장',
                'export_png_title': 'PNG로 내보내기',
                'export_svg_title': 'SVG로 내보내기',
                'rename_layer': '레이어 이름 변경',
                'enter_new_name': '새 이름을 입력하세요:',
                'last_layer_warning': '마지막 레이어는 삭제할 수 없습니다.',
                'layer': '레이어',
                'initializing': '초기화 중...',
                'project_initialized': '프로젝트 초기화됨',
                'added_layer': '레이어 추가됨: {name}',
                'removed_layer': '레이어 삭제됨: {name}',
                'added_obj': '{type} 추가됨',
                'deleted_objs': '{count}개 객체 삭제됨',
                'grouped_objs': '{count}개 객체 그룹화됨',
                'ungrouped_objs': '{count}개 객체 그룹 해제됨',
                'changed_color_objs': '{count}개 객체 색상 변경됨',
                'moved_objs_forward': '객체를 앞으로 보냄',
                'moved_objs_backward': '객체를 뒤로 보냄',
                'moved_objs_front': '객체를 맨 앞으로 보냄',
                'moved_objs_back': '객체를 맨 뒤로 보냄',
                'vector_pixel_hybrid': '벡터-픽셀 하이브리드 에디터',
                'created_by': '제작: rheehose',
                'help': '도움말',
                'about': '정보',
                'shortcuts': '단축키',
                'toggle_language_shortcut': '언어 전환',
                'horizontal_pan': '좌우 스크롤',
                'warning': '경고',
                'error': '오류',
                'updating': '업데이트 중...',
                'downloading': '다운로드 중: {p}%',
                'applying_update': '업데이트 적용 중...',
                'update_complete_restart': '업데이트 완료! 프로그램을 재시작합니다.',
                'update_failed': '업데이트 실패: {e}',
                'restarting': '재시작 중...',
                'ask_permission_update': '설치 폴더에 쓰기 권한이 없습니다. 계속하시겠습니까?\n(아니오를 누르면 브라우저 창이 열립니다)',
                'source_update_error': '소스 코드 버전은 자동 업데이트가 불가능합니다. git pull 명령어를 사용하거나 최신 바이너리를 별도로 다운로드해 주세요.',
                
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
                'bring_forward': 'Bring Forward',
                'send_backward': 'Send Backward',
                'bring_to_front': 'Bring to Front',
                'send_to_back': 'Send to Back',
                'layers': 'Layers',
                'activity_logs': 'Activity Logs',
                'new_version_title': 'New Update Available!',
                'new_version_msg': 'Version {v} is now available.',
                'update_now': 'Update Now',
                'later': 'Later',
                'size_limit_error': 'Size must be between 1 and 8192.',
                'invalid_input_error': 'Invalid input.',
                'canvas_resized': 'Canvas resized to {w}x{h}.',
                'ask_clear_canvas': 'All objects will be deleted. Continue?',
                'ask_clear_title': 'Clear Canvas',
                'open_plb_title': 'Open PLB File',
                'save_plb_title': 'Save PLB File',
                'export_png_title': 'Export PNG',
                'export_svg_title': 'Export SVG',
                'rename_layer': 'Rename Layer',
                'enter_new_name': 'Enter new name:',
                'last_layer_warning': 'Cannot remove last layer.',
                'layer': 'Layer',
                'initializing': 'Initializing...',
                'project_initialized': 'Project initialized',
                'added_layer': 'Added layer: {name}',
                'removed_layer': 'Removed layer: {name}',
                'added_obj': 'Added {type}',
                'deleted_objs': 'Deleted {count} objects',
                'grouped_objs': 'Grouped {count} objects',
                'ungrouped_objs': 'Ungrouped {count} objects',
                'changed_color_objs': 'Changed color of {count} objects',
                'moved_objs_forward': 'Moved objects forward',
                'moved_objs_backward': 'Moved objects backward',
                'moved_objs_front': 'Moved objects to front',
                'moved_objs_back': 'Moved objects to back',
                'vector_pixel_hybrid': 'Vector-Pixel Hybrid Editor',
                'created_by': 'Created by rheehose',
                'help': 'Help',
                'about': 'About',
                'shortcuts': 'Shortcuts',
                'toggle_language_shortcut': 'Toggle Language',
                'horizontal_pan': 'Horizontal Pan',
                'warning': 'Warning',
                'error': 'Error',
                'updating': 'Updating...',
                'downloading': 'Downloading: {p}%',
                'applying_update': 'Applying Update...',
                'update_complete_restart': 'Update Complete! Restarting...',
                'update_failed': 'Update Failed: {e}',
                'restarting': 'Restarting...',
                'ask_permission_update': 'No write permission in the installation folder. Proceed anyway?\n(Selecting No will open the browser)',
                'source_update_error': 'Source code version cannot be auto-updated. Please use git pull or download the binary separately.',
                
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
